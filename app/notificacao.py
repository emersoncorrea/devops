from fastapi import FastAPI
from datetime import datetime

APP_NOTIFICACAO = FastAPI()

#NOTIFICACOES = []

#@APP_NOTIFICACAO.get("/notificar")
#def listar_notificacoes():
#    return NOTIFICACOES

@APP_NOTIFICACAO.get("/notificar")
def listar_notificacoes():
    return NOTIFICACOES

@APP_NOTIFICACAO.post("/notificar")
def notificar(titulo: str, data_finalizacao: datetime):

    print(f"Tarefa '{titulo}' finalizada em '{data_finalizacao}'")
    return {"mensagem":"OK"}