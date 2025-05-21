# clients/school_client.py

import requests

BASE_URL = "http://localhost:8000"  

def turma_existe(turma_id):
    try:
        response = requests.get(f"{BASE_URL}/turmas/{turma_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API de gerenciamento escolar: {e}")
        return False

def aluno_existe(aluno_id):
    try:
        response = requests.get(f"{BASE_URL}/alunos/{aluno_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API de gerenciamento escolar: {e}")
        return False
