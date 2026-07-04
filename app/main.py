from fastapi import FastAPI
from datetime import datetime
import requests
from fastapi.exceptions import HTTPException

LISTA_TAREFAS = []
APP = FastAPI()

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

@APP.get("/")
def index():
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []
    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            return tarefa

    return {"mensagem": "Não existe nenhuma tarefa"}

@APP.post("/tarefas")
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
            raise ex

    tarefa_criada = nova_tarefa(id, titulo, descricao)
    LISTA_TAREFAS.append(tarefa_criada)
    return {"mensagem": "OK"}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            if titulo != "":
                tarefa['titulo'] = titulo
            if descricao != "":
                tarefa['descricao'] = descricao
            if concluido == True:
                tarefa['concluido'] = concluido

            if concluido == True:
                requests.post(f"http://notificacoes:8000/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}",
                timeout=10)

            return {"mensagem": "OK"}

    return {"mensagem": "TAREFA NÃO EXISTE"}

@APP.delete("/tarefas/{id}")
def deletar_tarefa(id: int):
    for tarefa in LISTA_TAREFAS:
        if tarefa['id'] == id:
            LISTA_TAREFAS.remove(tarefa)
            return {"mensagem": "OK"}

    return {"mensagem": "TAREFA NÃO EXISTE"}