import requests
import random

BASE_URL = "http://127.0.0.1:8000"


def run_test():
    print("Iniciando Teste de estresse")
    try:
        bairros = requests.get(f"{BASE_URL}/bairros/").json()
        candidatos = requests.get(f"{BASE_URL}/candidatos/").json()

        if not isinstance(bairros, list) or len(bairros) == 0:
            print("Crie bairros no Swagger antes de executar o teste.")
            return

        b_ids = [b["id"] for b in bairros]
        c_ids = [c["id"] for c in candidatos]

        sucessos = 0
        for i in range(50):
            voto = {
                "nome_votante": f"Eleitor {i}",
                "pesquisador_nome": "Bot_Teste",
                "bairro_id": random.choice(b_ids),
                "casa": str(i),
                "candidato_voto_id": random.choice(c_ids),
                "texto_anotacao": f"Nota {i}" if i % 2 == 0 else None,
            }
            res = requests.post(f"{BASE_URL}/entrevistas/", json=voto)
            if res.status_code == 201:
                sucessos += 1

        print(f"Sucessos: {sucessos}/50")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    run_test()
