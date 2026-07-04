from fastapi.testclient import TestClient
from app import APP

CLIENT = TestClient(APP)

def test_index():
    requisicao = CLIENT.get("/")

    assert requisicao.status_code == 200
    assert requisicao.json() == "Olá, DevOps!"

def test_criar_tarefa():
    requisicao = CLIENT.post(
        "/tarefas",
        params={"id": 1, "titulo": "Estudar", "descricao": "Estudar FastAPI"},
    )

    assert requisicao.status_code == 200
    assert requisicao.json() == {"mensagem": "OK"}


def test_criar_tarefa_ja_existente():
    CLIENT.post(
        "/tarefas",
        params={"id": 2, "titulo": "Estudar", "descricao": "Estudar FastAPI"},
    )

    requisicao = CLIENT.post(
        "/tarefas",
        params={"id": 2, "titulo": "Estudar", "descricao": "Estudar FastAPI"},
    )

    assert requisicao.status_code == 202
    assert requisicao.json()['detail'] == {"mensagem": "TAREFA JÁ EXISTE!"}



