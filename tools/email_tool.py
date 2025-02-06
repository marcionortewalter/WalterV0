from tools.subtasks.email_subtasks import create_email_draft, send_email_to_address
from langchain.tools import tool

@tool
def create_email_draft_tool(
    to_email: str,
    subject: str,
    message_text: str,
    cc_emails: list[str] = [],
    bcc_emails: list[str] = [],
):
    """
    Creates an email draft

    Args:
        to_email (str): The email address to send the email to
        subject (str): The subject of the email
        message_text (str): The body of the email
        cc_emails (list[str]): The email addresses to send the email to
        bcc_emails (list[str]): The email addresses to send the email to
    """
    return create_email_draft(to_email, subject, message_text, cc_emails, bcc_emails)

@tool
def send_email_to_address_tool(
    to_email: str,
    subject: str,
    message_text: str,
    cc_emails: list[str] = [],
    bcc_emails: list[str] = []
):
    """
    Sends an email to an address. Prioritize create_email_draft before this tool.
    Since this tool doesn't validate content to the user

    Args:
        to_email (str): The email address to send the email to
        subject (str): The subject of the email
        message_text (str): The body of the email
        cc_emails (list[str]): The email addresses to send the email to
        bcc_emails (list[str]): The email addresses to send the email to
    """
    return send_email_to_address(to_email, subject, message_text, cc_emails, bcc_emails)
