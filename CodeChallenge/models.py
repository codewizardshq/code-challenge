import re
from hmac import compare_digest as str_cmp
from tempfile import NamedTemporaryFile
from typing import Tuple, List, Iterable, Optional

import argon2
import requests
from flask import request, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, orm, event
from werkzeug.datastructures import FileStorage

from CodeChallenge.mailgun import (
    mg_list_add,
    email_template,
    mg_send,
    FileAttachments,
    make_attachment,
    raise_undeliverable,
    UndeliverableEmail,
)

db = SQLAlchemy()


def init_db():
    db.create_all()


def drop_all():
    db.drop_all()


def ranking(answer_id: int) -> Tuple[int, int]:
    return db.session.execute(
        """
        select rainv.num_votes, rainv.rank
        from (
                 select @rownum := @rownum + 1 as 'rank',
                        prequery.answer_id,
                        prequery.num_votes
                 from (select @rownum := 0) sqlvars,
                      (select answer_id,
                              count(*) as num_votes
                       from vote
                       group by answer_id
                       order by count(*) desc) prequery
             ) as rainv
        where answer_id = :answer_id
    """,
        {"answer_id": answer_id},
    ).first()


class Transition(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    after_rank: int = db.Column(db.Integer, nullable=False, unique=True, index=True)
    media: str = db.Column(db.String(200), nullable=False)
    caption: str = db.Column(db.String(2000), nullable=False)

    def serialize(self) -> dict:
        return dict(id=self.id, media=self.media, caption=self.caption)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.Integer, nullable=False, index=True)
    asset = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    asset_ext = db.Column(db.String(10))
    hint1 = db.Column(db.String(5000))
    hint2 = db.Column(db.String(5000))
    match_type = db.Column(db.Integer, nullable=False, default=1)
    input_type = db.Column(db.Integer, nullable=False, default=1)

    MATCH_STRCMP = 1
    MATCH_REGEXP = 2

    INPUT_TEXT_FIELD = 1
    INPUT_TEXT_AREA = 2

    def __repr__(self):
        return "<Question %r>" % self.id

    def check_correct(self, answer: str) -> bool:
        if answer is None:
            return False

        if self.match_type == Question.MATCH_STRCMP:
            return str_cmp(answer.casefold().strip(), self.answer.casefold())
        elif self.match_type == Question.MATCH_REGEXP:
            return re.search(self.answer, answer) is not None
        return False

    def next_transition(self) -> Optional[Transition]:
        """Helper function to lookup any Transition that is scheduled to follow this Question."""
        r = Transition.query.filter_by(after_rank=self.rank).one_or_none()
        if r is not None:
            return r


class Answer(db.Model):
    """Tracks a user answering a question"""

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="cascade"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    text = db.Column(db.String(2000))
    correct = db.Column(db.Boolean)
    question = db.relationship("Question", lazy=True, uselist=False)
    user = db.relationship("Users", lazy=True, uselist=False)
    votes = db.relationship("Vote", cascade="all,delete", lazy=True, uselist=True)
    disqualified = db.Column(db.String(255))

    def confirmed_votes(self) -> int:
        confirmed = 0
        for vote in self.votes:
            if vote.confirmed:
                confirmed += 1

        return confirmed


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(
        db.Integer, db.ForeignKey("answer.id", ondelete="cascade"), nullable=False
    )
    answer = db.relationship("Answer", lazy=True, uselist=False)
    voter_email = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def existing_vote(email: str) -> bool:
        v = Vote.query.filter_by(voter_email=email).first()
        return v

    def ranking(self):
        return ranking(self.answer.id)


def lookup_username(try_username):
    return Users.query.filter_by(username=try_username).first()


def clean_username(try_username):
    return re.sub(r"[^ A-Z_0-9]", "_", try_username, flags=re.IGNORECASE).strip()


class ValidationError(Exception):
    """Thrown when a field fails validation."""

    pass


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(80), nullable=True)
    student_last_name = db.Column(db.String(80), nullable=True)

    parent_first_name = db.Column(db.String(80), nullable=True)
    parent_last_name = db.Column(db.String(80), nullable=True)

    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    parent_email = db.Column(db.String(120), unique=False, nullable=False, index=True)
    student_email = db.Column(db.String(120), unique=False, nullable=True)
    dob = db.Column(db.String(10), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    found_us = db.Column(db.String(2000))
    school_name = db.Column(db.String(200))
    cwhq_username = db.Column(db.String(100))
    is_teacher = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    teacher = db.relationship("Users", lazy=True, uselist=False)

    def __init__(self):
        self.errors = []  # type: List[str]

        # temporary place to store the user's plaintext password for bulk imports
        # this property will otherwise be an empty string
        self.plaintext = ""  # type: str
        self.original_row = []  # type: List[str]

    def __repr__(self):
        return f"<User({self.username!r})>"

    def __str__(self):
        return self.username

    def check_password(self, password):
        ph = argon2.PasswordHasher()
        try:
            return ph.verify(self.password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def casted_votes(self) -> int:
        q = db.session.query(func.count(Vote.id)).filter_by(user_id=self.id)

        n = q.scalar()
        return n

    def votes(self):
        v = Vote.query.filter_by(user_id=self.id).all()
        return v

    def display(self):
        if (
            self.student_first_name is not None
            and self.student_last_name is not None
            and len(self.student_last_name)
        ):
            return f"{self.student_first_name} " f"{self.student_last_name[0]}."

    def _mail_recipients(self) -> List[str]:
        if not self.student_email:
            return [self.parent_email]
        return [self.parent_email, self.student_email]

    def send_welcome_email(self):
        email_template(
            self._mail_recipients(),
            "Mission Confirmed! Welcome to the CodeWizardsHQ Code Challenge",
            "challenge_welcome.html",
            name=self.student_first_name or self.parent_first_name,
        )

    def send_confirmation_email(self, password=None):
        email_template(
            self._mail_recipients(),
            "Your Code Challenge Account",
            "challenge_account_confirm.html",
            username=self.username,
            name=self.student_first_name or self.parent_first_name,
            password=password,
        )

    def _mg_vars(self):
        return dict(
            codeChallengeUsername=self.username,
            studentEmail=self.student_email,
            studentFirstName=self.student_first_name,
            studentLastName=self.student_last_name,
            studentName=f"{self.student_first_name} {self.student_last_name}",
            parentFirstName=self.parent_first_name,
            parentLastName=self.parent_last_name,
            parentName=f"{self.parent_first_name} {self.parent_last_name}",
            userId=self.id,
            studentDOB=self.dob,
            type="",
        )

    def add_to_mailing_list(self, list_name: str):
        for i, addr in enumerate(self._mail_recipients()):
            mg_vars = self._mg_vars()

            if i == 0:
                mg_vars["type"] = "parent"
            else:
                mg_vars["type"] = "student"

            mg_list_add(addr, list_name, mg_vars)

    def generate_password(self):
        """Generate a random password. Set's the user's password to the generated_students value,
        then returns the password string in plaintext. Does NOT commit.

        Raises :class:`HTTPError`, if one occurred."""
        if current_app.config["TESTING"]:
            import secrets

            pw = secrets.token_urlsafe()
            self.set_password(pw)
            self.plaintext = pw
            return

        response = requests.get("https://www.dinopass.com/password/strong")
        response.raise_for_status()

        self.set_password(response.text)
        self.plaintext = response.text

    def _initial_username(self) -> str:
        if not self.student_first_name or not self.student_last_name:
            return self.parent_email

        try:
            last = self.student_last_name[0]
        except IndexError:
            last = ""

        try_username = (self.student_first_name + last).casefold()
        try_username = clean_username(try_username)

        return try_username

    def generate_username(self) -> None:
        """Generates an initial username, then increments a discriminator number
        on the initial username until an unused one is generated_students. Sets the generated_students username
        on the object but does not commit changes."""
        try_username = self._initial_username()
        discriminator = 2

        while lookup_username(try_username) is not None:
            try_username += str(discriminator)
            discriminator += 1

        self.username = try_username

    def set_password(self, plaintext):
        self.password = argon2.PasswordHasher().hash(plaintext)

    def set_username(self, username: str):
        if not username:
            raise ValidationError("username cannot be null or empty")

        if len(username) < 3:
            raise ValidationError("username is not long enough")

        self.username = username.strip()

    def set_parent_email(self, email: str):
        if not email or type(email) != str:
            raise ValidationError("parent email cannot be null or empty")

        email = email.strip()
        raise_undeliverable(email)

        self.parent_email = email

    def set_parent_first_name(self, name: str):
        assert type(name) == str
        self.parent_first_name = name.strip().title()

    def set_parent_last_name(self, name: str):
        assert type(name) == str
        self.parent_last_name = name.strip().title()

    def set_student_first_name(self, name: str):
        assert type(name) == str
        self.student_first_name = name.strip().title()

    def set_student_last_name(self, name: str):
        assert type(name) == str
        self.student_last_name = name.strip().title()

    def set_school_name(self, name: str):
        assert type(name) == str
        if not name:
            raise ValidationError("school name may not be None or empty")
        self.school_name = name

    def set_student_email(self, email: str):
        if not email or type(email) != str:
            raise ValidationError(
                "may not set a None or empty student email. use clear_student_email()"
            )
        email = email.strip()
        raise_undeliverable(email)
        self.student_email = email

    def clear_student_email(self):
        self.student_email = None

    def to_csv(self) -> Tuple[str, ...]:
        return (
            str(self.id),
            self.student_first_name,
            self.student_last_name,
            self.parent_first_name,
            self.parent_last_name,
            self.username,
            self.plaintext,
        )

    @classmethod
    def lookup_teacher(cls, email: str):
        return cls.query.filter_by(is_teacher=True, parent_email=email).first()


@event.listens_for(Users, "after_insert")
def teacher_send_email(mapper, connection, target: Users):
    if target.is_teacher:
        target.send_confirmation_email(password=target.plaintext)
        target.send_welcome_email()


def get_teacher(email: str, name: str) -> Users:
    """Lookup a teacher user by email, creating a new one if one does not exist."""
    teacher = Users.lookup_teacher(email)

    if teacher is None:
        teacher = Users()
        teacher.set_parent_email(email)
        teacher.is_teacher = True

        name = name.split(" ", 1)
        if len(name) == 2:
            teacher.student_first_name = name[0]
            teacher.student_last_name = name[1]
        else:
            teacher.student_first_name = name

        teacher.generate_username()
        teacher.generate_password()
        db.session.add(teacher)
        db.session.flush()

    return teacher


def attachment_is_excel(attachment: FileStorage) -> bool:
    """Determine if a FileStorage attachment is an Excel spreadsheet.
    Uses Content-Type and extension. Does not attempt to file contents.

    :param attachment: FileStorage object to check.
    :return: True if the object appears to be a Microsoft Excel file.
    """
    return (
        attachment.content_type
        in (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        )
        or attachment.filename.endswith(".xlsx")
        or attachment.filename.endswith(".xls")
    )


def list_to_csv(v: Iterable) -> bytes:
    import csv
    from io import StringIO

    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerows(v)

    return bytes(buf.getvalue(), "utf8")


def empty_row(row: list) -> bool:
    """Check if the first 3 columns of a row are 'nan'."""
    import math

    return any(
        map(lambda column: type(column) == float and math.isnan(column), row[:3])
    )


class BulkImport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=1)
    sender = db.Column(db.String(80), nullable=False)
    document = db.Column(db.LargeBinary(length=(2 ** 32) - 1))
    subject = db.Column(db.String(200), nullable=False)
    in_reply_to = db.Column(db.String(200), nullable=False)
    users = db.Column(db.Text)
    import_errors = db.Column(db.Text)

    STUDENT_FIRST_NAME = 0
    STUDENT_LAST_NAME = 1
    PARENT_FIRST_NAME = 2
    PARENT_LAST_NAME = 3
    PARENT_EMAIL = 4
    DOB = 5
    TEACHER_NAME = 6
    TEACHER_EMAIL = 7
    SCHOOL = 8

    def __init__(self):
        self.generated_students = []  # type: List[Users]
        self.generated_teachers = []  # type: List[Users]
        self.errors = []  # type: List[Tuple[int, str]]

    @orm.reconstructor
    def init_on_load(self):
        self.generated_students = []  # type: List[Users]
        self.generated_teachers = []  # type: List[Users]
        self.errors = []  # type: List[Tuple[int, str]]

    @classmethod
    def from_request_files(
        cls, sender: str, subject: str, in_reply_to: str
    ) -> List[int]:
        added = []  # type: List[int]
        for attachment in request.files.values():
            if attachment_is_excel(attachment):
                bulk_import = cls()

                bulk_import.sender = sender
                bulk_import.document = attachment.stream.read()
                bulk_import.status = 1
                bulk_import.in_reply_to = in_reply_to
                bulk_import.subject = subject

                db.session.add(bulk_import)
                db.session.flush()
                added.append(bulk_import.id)

        db.session.commit()

        return added

    @classmethod
    def process_imports(cls):
        for bulk_import in cls.query.filter_by(status=1):
            bulk_import.run_import()

    def read_excel(self) -> List[List[str]]:
        """Convert the Excel spreadsheet on this BulkImport to a list."""
        import pandas as pd

        fp = NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(self.document)
        fp.flush()
        fp.seek(0)

        df = pd.read_excel(fp.name)
        fp.close()

        return df.values.tolist()

    def generate_user_from_row(self, row_num: int, row: List[str]):
        """Create a Users object from a row. Generated user is stored on the generated_students property.

        :param row_num: Row number to show in error messages.
        :param row: User row from spreadsheet/CSV
        """

        try:
            teacher_email = row[self.TEACHER_EMAIL]
            teacher_name = row[self.TEACHER_NAME]
        except IndexError:
            self.import_error(row_num, "Missing Teacher Email or Teacher Name column.")
            return

        if (
            not teacher_name
            or not teacher_email
            or type(teacher_name) != str
            or type(teacher_email) != str
        ):
            self.import_error(row_num, "Missing Teacher Email or Teacher name values.")
            return

        teacher = get_teacher(teacher_email, teacher_name)

        try:
            check = Users.query.filter_by(
                student_first_name=row[self.STUDENT_FIRST_NAME].strip(),
                student_last_name=row[self.STUDENT_LAST_NAME].strip(),
                parent_email=row[self.PARENT_EMAIL],
            ).first()
        except (IndexError, AttributeError):
            self.import_error(
                row_num, "Missing Student First Name or Student Last Name values."
            )
            return

        if check:
            self.import_error(
                row_num, "A user with the same first and last name already exists."
            )
            return

        user = Users()
        self.generated_students.append(user)

        try:
            user.set_student_first_name(row[self.STUDENT_FIRST_NAME])
            user.set_student_last_name(row[self.STUDENT_LAST_NAME])
            user.set_parent_first_name(row[self.PARENT_FIRST_NAME])
            user.set_parent_last_name(row[self.PARENT_LAST_NAME])
            user.set_parent_email(row[self.PARENT_EMAIL])
            user.set_school_name(row[self.SCHOOL])
        except (IndexError, AssertionError):
            self.import_error(
                row_num,
                "One of the required columns was missing. Please make sure you sent the correct template.",
            )
            return
        except ValidationError as e:
            self.import_error(row_num, "Failed validation: " + str(e))
            return
        except UndeliverableEmail:
            self.import_error(row_num, "Cannot deliver to this email address.")
            return

        if type(row[self.DOB]) == str:
            user.dob = row[self.DOB]
        else:
            user.dob = str(row[self.DOB].date())

        user.teacher_id = teacher.id
        user.generate_username()
        user.generate_password()
        db.session.add(user)

        try:
            db.session.commit()
        except Exception as e:
            self.import_error(row_num, "did not pass database constraints: " + str(e))
            return

        try:
            user.send_confirmation_email(password=user.plaintext)
            user.send_welcome_email()
        except:
            self.import_error(
                row_num,
                "user was created, but an error occurred sending welcome and confirmation emails. "
                "please provide student with credentials",
            )

    def run_import(self):
        self.status = 2
        db.session.commit()

        self.generated_students = []

        for i, row in enumerate(self.read_excel()):
            if empty_row(row):
                continue

            self.generate_user_from_row(i + 1, row)

        db.session.commit()

        created = list(
            map(
                lambda u: u.to_csv(),
                filter(lambda u: not u.errors, self.generated_students),
            )
        )
        html = render_template("bulk_import_results.html", errors=len(self.errors))

        self.users = list_to_csv(created)

        attachments = [make_attachment("Users.csv", self.users)]
        if self.errors:
            errors = [("Row #", "Error Message")]
            errors.extend(self.errors)
            self.import_errors = list_to_csv(errors)

            attachments.append(make_attachment("ImportErrors.csv", self.import_errors))

        db.session.commit()

        self.reply(html, attachments=attachments)

    def import_error(self, row: int, message: str):
        self.errors.append((row, message))

    def reply(self, message, attachments: FileAttachments = None):
        """Reply to the sender with a message."""
        sender = current_app.config["BULK_IMPORT_SENDER"]

        mg_send(
            [self.sender],
            "RE: " + self.subject,
            message,
            {"In-Reply-To": self.in_reply_to, "Reply-To": sender},
            from_=sender,
            attachments=attachments,
        )
