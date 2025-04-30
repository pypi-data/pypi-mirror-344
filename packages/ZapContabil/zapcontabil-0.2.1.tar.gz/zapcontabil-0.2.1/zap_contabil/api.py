import requests

API_KEY_ZAP_CONTABIL="d37ef120540c14b61773b56090235752e2faf3a8bbf90b1a93e9e9db8131bb37aef3f10750cc4bc474263d2968b162447ad97bf1a3c37cba140f891efd6ced5b0b8c96daea53da20966bf331943c6298ca20d7357e35bcb167e773e0cf67547532f5d6b3cb5edd2fdd99441de218ccac0ac71e2f9a804e377abcf2d16a"


def base_requisicao(
    metodo: str = "GET", endpoint=None, data=None, json=None, files=None
):
    api_url_base = "https://api-advys.zapcontabil.chat/api/"
    api_url = f"{api_url_base}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY_ZAP_CONTABIL}",
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

