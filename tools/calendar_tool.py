from tools.subtasks.email_subtasks import send_calendar_invite, get_events_for_days
from langchain.tools import tool
from datetime import datetime

@tool
def send_calendar_invite_tool(
    emails: list[str],
    title: str,
    start_time: datetime,
    end_time: datetime,
    email_address: str,
    timezone: str = "America/Sao_Paulo"
):
    """
    Sends a calendar invite to a list of emails.

    Args:
        emails: The list of emails to send the calendar invite to.
        title: The title of the calendar invite.
        start_time: The start time of the calendar invite.
        end_time: The end time of the calendar invite.
        email_address: The email address of the sender.
        timezone: The timezone of the calendar invite.

    Returns:
        The response from the calendar invite.
    """
    start_time = start_time.isoformat()
    end_time = end_time.isoformat()
    return send_calendar_invite(emails, title, start_time, end_time, email_address, timezone)

@tool
def get_events_for_days_tool(dates: list[datetime]):
    """
    Retrieves events for a list of days. If you want to check for multiple days, call this with multiple inputs.

    Input in the format of [datetime, datetime]

    Args:
    dates: The days for which to retrieve events (datetime).

    Returns: availability for those days. Always prefer to return in BRT.
    """
    date_strs = [date.strftime("%d-%m-%Y") for date in dates]
    return get_events_for_days(date_strs)
