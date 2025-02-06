from tools.subtasks.attio_subtasks import create_attio_task
from langchain.tools import tool
from datetime import datetime

@tool
def create_new_attio_task_tool(
    content: str,
    deadline_at: datetime,
    target_object: str,
    target_record_id: str,
    assignee_actor_type: str,
    assignee_actor_id: str,
):
    """
    Creates a new task in Attio.
    If information is missing, ask the user for it, except for ids. Those you need to find in the sql database.

    Args:
        content: The content of the task.
        deadline_at: The deadline of the task.
        target_object: The object of the task. Can be people or companies.
        target_record_id: The record id of the task. To be found in the sql database people or companies table. Be careful there may be variations in the names
        assignee_actor_type: The type of the assignee. Always use workspace-member.
        assignee_actor_id: The id of the assignee. To be found in the sql database members table.

    Returns:
        The response from the task creation.
    """
    deadline_at = deadline_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return create_attio_task(content, deadline_at, target_object, target_record_id, assignee_actor_type, assignee_actor_id)

if __name__ == "__main__":
    print(create_attio_task("Create a task for John Doe", "2025-01-01", "people", "123", "workspace-member", "456", "789"))
