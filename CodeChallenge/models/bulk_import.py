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
        """Create a User object from a row. Generated user is stored on the generated_students property.

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

        attachments = [make_attachment("User.csv", self.users)]
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
