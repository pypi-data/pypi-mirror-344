from dotenv import load_dotenv
import requests
import os

load_dotenv()
api_key = os.getenv("API_KEY_ZAP_CONTABIL")

def base_requisicao(
    metodo: str = "GET", endpoint=None, data=None, json=None, files=None
):
    api_url_base = "https://api-advys.zapcontabil.chat/api/"
    api_url = f"{api_url_base}{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    if metodo.upper() == "GET":
        reposta = requests.get(api_url, headers=headers, data=data, files=files)
    elif metodo.upper() == "POST":
        reposta = requests.post(
            api_url, headers=headers, data=data, json=json, files=files
        )
    else:
        print("Metodo inválido")
        return
    return reposta

