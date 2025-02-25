import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dotenv_files/.env"))
load_dotenv(dotenv_path)

def SeedDb():
    BASE_URL = "http://localhost:8000/api"  
    
    # Credenciais do admin
    ADMIN_DATA = {
        "username": os.getenv("DJANGO_SUPERUSER_USERNAME"), # Username do superuser criado
        "password": os.getenv("DJANGO_SUPERUSER_PASSWORD")  # Password do superuser criado
    }
    
    PROFESSIONS = [
        {
          "name": "Outros", "description": "Outras especialidades."
        },
        {
          "name": "Médico Clínico Geral", "description": "Responsável por avaliar e diagnosticar pacientes, encaminhando para especialistas quando necessário."
        },
        {
          "name": "Médico Cardiologista", "description": "Especialista no diagnóstico e tratamento de doenças do coração e sistema circulatório."
        },
        {
          "name": "Médico Pediatra", "description": "Cuida da saúde de bebês, crianças e adolescentes, tratando e prevenindo doenças."
        },
        {
          "name": "Médico Ginecologista", "description": "Especialista na saúde da mulher, tratando questões relacionadas ao sistema reprodutivo feminino."
        },
        {
          "name": "Médico Ortopedista", "description": "Foca no diagnóstico e tratamento de problemas nos ossos, músculos e articulações."
        },
        {
          "name": "Médico Neurologista", "description": "Especializado em doenças do sistema nervoso, incluindo cérebro e medula espinhal."
        },
        {
          "name": "Médico Dermatologista", "description": "Cuida da saúde da pele, cabelos e unhas, tratando condições dermatológicas."
        },
        {
          "name": "Médico Psiquiatra", "description": "Especialista no diagnóstico e tratamento de transtornos mentais e emocionais."
        },
        {
          "name": "Médico Endocrinologista", "description": "Cuida do sistema endócrino, tratando distúrbios hormonais como diabetes e tireoide."
        },
        {
          "name": "Médico Oftalmologista", "description": "Diagnostica e trata problemas relacionados à visão e aos olhos."
        },
        {
          "name": "Médico Otorrinolaringologista", "description": "Trata problemas no ouvido, nariz e garganta."
        },
        {
          "name": "Médico Urologista", "description": "Cuida do trato urinário e do sistema reprodutivo masculino."
        },
        {
          "name": "Médico Nutrólogo", "description": "Foca no impacto da alimentação e nutrição na saúde dos pacientes."
        },
        {
          "name": "Fisioterapeuta", "description": "Ajuda na recuperação e prevenção de problemas musculoesqueléticos e de mobilidade."
        },
        {
          "name": "Nutricionista", "description": "Elabora planos alimentares para promover a saúde e tratar condições específicas."
        },
        {
          "name": "Psicólogo", "description": "Atua na saúde mental, ajudando pacientes com transtornos emocionais e comportamentais."
        },
        {
          "name": "Enfermeiro", "description": "Presta assistência a pacientes, administra medicamentos e coordena cuidados."
        },
        {
          "name": "Técnico de Enfermagem", "description": "Auxilia enfermeiros no cuidado direto com os pacientes."
        },
        {
          "name": "Terapeuta Ocupacional", "description": "Ajuda pacientes a desenvolverem habilidades para a vida diária e o trabalho."
        },
        {
          "name": "Fonoaudiólogo", "description": "Atua no diagnóstico e tratamento de problemas de fala, audição e deglutição."
        },
        {
          "name": "Assistente Social", "description": "Oferece suporte a pacientes e famílias em questões sociais e psicológicas."
        },
        {
          "name": "Farmacêutico", "description": "Responsável pela dispensação e orientação sobre o uso correto de medicamentos."
        }
    ]
    
    try:
        print("\n🔹 Obtendo token de autenticação...")
        print(f"🔹 Usuário: {ADMIN_DATA['username']}")
        login_response = requests.post(f"{BASE_URL}/token/", json={
            "username": ADMIN_DATA["username"],
            "password": ADMIN_DATA["password"]
        })
        if login_response.status_code == 200:
            token = login_response.json().get("access")
            print(f"✅ Token obtido: {token}")
        else:
            print(f"⚠️ Falha ao autenticar: {login_response.text}")
            return
        HEADERS = {"Authorization": f"Bearer {token}"}

        # Criando profissões
        print("\n🔹 Criando profissões...")
        profession_ids = []
        for profession in PROFESSIONS:
            response = requests.post(f"{BASE_URL}/profession/", json=profession, headers=HEADERS)
            if response.status_code == 201:
                profession_id = response.json().get("payload", {}).get("id")
                profession_ids.append(profession_id)
                print(f"✅ Profissão '{profession['name']}' criada! ID: {profession_id}")
            else:
                print(f"⚠️ Erro ao criar '{profession['name']}': {response.text}")

        # Criar profissionais de saúde
        print("\n🔹 Criando profissionais de saúde...")
        if profession_ids:
            health_professionals = [
                    {
  	                  "full_name":"Jonas Albuquerque",
  	                  "social_name":"",
  	                  "email":"teste@email.com",
  	                  "profession":profession_ids[15],
  	                  "zipcode":"60.110-301",
  	                  "phone":"85988776655",
  	                  "taxnumber":"943.799.610-52"
                    },
                    {
  	                  "full_name":"Luiz Henrique",
  	                  "social_name":"",
  	                  "email":"teste@email.com",
  	                  "profession":profession_ids[16],
  	                  "zipcode":"60.110-301",
  	                  "phone":"85988776655",
  	                  "taxnumber":"132.088.330-32"
                    },
                    {
  	                  "full_name":"Mariana Sampaio",
  	                  "social_name":"",
  	                  "email":"teste@email.com",
  	                  "profession":profession_ids[17],
  	                  "zipcode":"60.110-301",
  	                  "phone":"85988776655",
  	                  "taxnumber":"945.629.610-58"
                    },
                    {
  	                  "full_name":"Trajano de Almeida",
  	                  "social_name":"",
  	                  "email":"teste@email.com",
  	                  "profession":profession_ids[18],
  	                  "zipcode":"60.110-301",
  	                  "phone":"85988776655",
  	                  "taxnumber":"279.681.220-07"
                    },
                    {
  	                  "full_name":"Lucia Mendes",
  	                  "social_name":"",
  	                  "email":"teste@email.com",
  	                  "profession":profession_ids[0],
  	                  "zipcode":"60.110-301",
  	                  "phone":"85988776655",
  	                  "taxnumber":"374.601.430-14"
                    }
            ]
            for hp in health_professionals:
                response = requests.post(f"{BASE_URL}/healthprofessional/", json=hp, headers=HEADERS)
                if response.status_code == 201:
                    print(f"✅ Profissional '{hp['full_name']}' criado!")
                else:
                    print(f"⚠️ Erro ao criar '{hp['full_name']}': {response.text}")
        else:
            print("⚠️ Nenhuma profissão foi criada. Não foi possível adicionar profissionais.")
        print("\n🎉 Seed finalizado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro durante o seed: {e}")

SeedDb()