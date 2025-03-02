import requests
import re

def GetZipcode(zipcode: str):
    regex_zipcode = re.sub(r'[^0-9]', '', zipcode)  # Remove caracteres não numéricos
    # print(f"CEP formatado: {regex_zipcode}")
    
    try:
        url = f"https://viacep.com.br/ws/{regex_zipcode}/json/"
        response = requests.get(url)
        response.raise_for_status()  # Levanta uma exceção se a resposta for um erro HTTP
    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False, 
            "status_code": 400, 
            "message": f"Erro ao consultar CEP: {regex_zipcode}", 
            "error": "Verifique o CEP informado"
            }
    except requests.exceptions.RequestException as err:
        return {
            "success": False, 
            "status_code": 400, 
            "message": f"Erro ao consultar CEP: {regex_zipcode}", 
            "error": str(err)
            }

    # Verifica se a resposta contém um JSON válido
    if response.status_code == 200:
        try:
            data = response.json()
            if 'erro' in data:
                return {
                    "success": False, 
                    "status_code": 404, 
                    "message": f"CEP não encontrado: {regex_zipcode}", 
                    "error": "CEP não encontrado"
                    }
            return {
                "success": True, 
                "status_code": 200, 
                "data": data
                }
        except ValueError:
            return {
                "success": False, 
                "status_code": 400, 
                "message": "Resposta inválida da API", 
                "error": "Não foi possível decodificar a resposta"
                }
    else:
        return {
            "success": False, 
            "status_code": 400, 
            "message": "Erro desconhecido", 
            "error": "Resposta inválida"
            }
