import requests
import os

auth_token = os.getenv("ATTIO_API_KEY")

def create_attio_task(
    content: str,
    deadline_at: str,
    target_object: str,
    target_record_id: str,
    assignee_actor_type: str,
    assignee_actor_id: str,
) -> dict:
    """
    Cria uma nova tarefa no Attio.
    
    Args:
        content: Conteúdo da tarefa
        deadline_at: Data limite no formato ISO (ex: "2023-01-01T15:00:00.000000000Z")
        target_object: Tipo do objeto alvo (ex: "people")
        target_record_id: ID do registro alvo
        assignee_actor_type: Tipo do responsável (ex: "workspace-member")
        assignee_actor_id: ID do responsável
        auth_token: Token de autenticação da API
    
    Returns:
        dict: Resposta da API em formato JSON
    """
    url = "https://api.attio.com/v2/tasks"
    
    payload = {
        "data": {
            "format": "plaintext",
            "is_completed": False,
            "content": content,
            "deadline_at": deadline_at,
            "linked_records": [
                {
                    "target_object": target_object,
                    "target_record_id": target_record_id
                }
            ],
            "assignees": [
                {
                    "referenced_actor_type": assignee_actor_type,
                    "referenced_actor_id": assignee_actor_id
                }
            ]
        }
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {auth_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()