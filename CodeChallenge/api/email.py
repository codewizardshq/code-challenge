from flask import Blueprint, request

from CodeChallenge.mailgun import mg_send
from CodeChallenge.models import BulkImport

bp = Blueprint("emailApi", __name__, url_prefix="/api/v1/emails")


def reply_message(to: str, subject: str, message: str, in_reply_to: str):
    return mg_send([to], subject, message, {"In-Reply-To": in_reply_to})


def reply_error(to: str, message: str, in_reply_to: str):
    return reply_message(to, "Code Challenge Import Error", message, in_reply_to)


@bp.route("/process", methods=["POST"])
def timer_process():
    BulkImport.process_imports()
    return "", 200


@bp.route("/inbox", methods=["POST"])
def webhook_inbox():
    if request.form.get("X-Mailgun-SFlag") == "Yes":
        return "Message flagged as spam.", 200

    sender = request.form.get("Reply-To", request.form.get("From"))
    subject = "RE: " + request.form["Subject"]
    in_reply_to = request.form["Message-Id"]

    if len(request.files) == 0:
        reply_message(
            sender,
            subject,
            "There were no attachments to your message. Please try again.",
            in_reply_to,
        )
        return "Rejected: no suitable attachments found.", 200

    added = BulkImport.from_request_files(sender, subject, in_reply_to)

    if len(added) == 0:
        reply_message(
            sender,
            subject,
            "None of the attachments on your message appear to be Excel spreadsheets. Please ensure the "
            "correct .xlsx spreadsheet is attached for CodeWizardsHQ Code Challenge bulk student creation.",
            in_reply_to,
        )
        return "Rejected: none of the attachments are Excel spreadsheets."

    reply_message(
        sender,
        subject,
        "You will receive another message after user creation has completed with the created student "
        f" account information attached. Import Confirmation #: {', '.join([str(i) for i in added])}",
        in_reply_to,
    )

    return "Accepted.", 200
