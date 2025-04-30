import logging
from pathlib import Path
import requests


class ZapContabil:
    def __init__(self, bearer_token) -> None:
        self.bearer_token = bearer_token
        self.url_base = "https://api-advys.zapcontabil.chat/api/"
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
        }


    def enviar_mensagem(self, telefone, mensagem, cria_atendimento="nocreate"):
        url = self.url_base + f"send/{telefone}"
        dados_json = {
            "body": f"{mensagem}",
            "ticketStrategy": f"{cria_atendimento}",
        }
        try:
            resposta = requests.post(url, headers=self.headers, json=dados_json)
            if resposta.status_code == 200:
                logging.info(f"Mensagem enviada com sucesso para {telefone}")
        except requests.RequestException as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            

    def enviar_arquivo(self, telefone, caminho_arquivo:Path, legenda="Boleto Advys"):
        url = self.url_base + f"send/document/{telefone}"
        dados_json = {
            "caption": legenda,
        }
        with open(caminho_arquivo, "rb") as arquivo:
            arquivos = {
                "media": (caminho_arquivo.name, arquivo),
            }    
            try:   
                resposta = requests.post(url, headers=self.headers, data=dados_json, files = arquivos)
                id_atendimento = resposta.json().get("message", {}).get("ticketId")
                if id_atendimento:
                    self.encerra_atendimento(id_atendimento)
                    logging.info(f"ID atendimento ZapContabil: {id_atendimento}")
                    logging.info(f"Arquivo {caminho_arquivo.name} enviado com sucesso para {telefone}")
            except requests.RequestException as e:
                logging.error(f"Erro ao enviar arquivo: {e}")
                if hasattr(e.response, 'status_code'):
                    logging.error(f"Status code: {e.response.status_code}")


    def encerra_atendimento(self, id_atendimento):
        url = self.url_base + f"tickets/{id_atendimento}/resolve"
        dados_json = {"feedbackOption": "none"}
        try:
            requests.post(url, headers=self.headers, data=dados_json)
        except requests.RequestException as e:
            logging.error(f"Erro ao encerrar atendimento")
            

