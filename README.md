# API de agendamentos Django com DRF e Docker

## ✨ Visão Geral
Esta API de agendamentos foi desenvolvida utilizando Django e Django Rest Framework (DRF), com suporte a PostgreSQL e Docker para ambiente de desenvolvimento.

---

## 📝 Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework:** Django + Django Rest Framework (DRF)
- **Autenticação:** SimpleJWT
- **Banco de Dados:** PostgreSQL
- **Gerenciamento de Containers:** Docker + Docker Compose
- **Documentação:** [Postman](https://documenter.getpostman.com/view/28722501/2sAYdinpKr)

---

## 🛠️ Como Executar o Projeto
### 1. Clonar o Repositório
```sh
git clone https://github.com/thiago-costa-barros/DesafioBackEnd_SistemaAgendamentoDjango.git
cd seu-repositorio
```

### 2. Configurar as Variáveis de Ambiente
Copie o arquivo `.env-example` disponível em `dotenv_files` e ajuste conforme necessário:

```sh
cp dotenv_files/.env-example .env
```

🔹 **Modelo do `.env`**
```ini
SECRET_KEY="CHANGE-ME"

# SuperUser django
DJANGO_SUPERUSER_USERNAME='username'
DJANGO_SUPERUSER_PASSWORD='password'

# 0 False, 1 True
DEBUG="1"

# Comma Separated values
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_ENGINE="django.db.backends.postgresql"
POSTGRES_DB="CHANGE-ME"
POSTGRES_USER="CHANGE-ME"
POSTGRES_PASSWORD="CHANGE-ME"
POSTGRES_HOST="psql" # Igual ao nome do service no docker
POSTGRES_PORT="5432"
```

### 3. Construir e Subir os Containers Docker
```sh
docker-compose up --build
```

### 4. Criar um Superusuário do Django
```sh
docker-compose exec djangoapp python manage.py createsuperuser
```
➡️ **Utilize o mesmo username e password configurados no `.env`**

### 5. (Opcional) Executar o Seed DB
```sh
python djangoapp/seed_db.py
```
Isso carregará dados iniciais no banco.
***É obrigatório que já tenha sido criado um SuperUsuário e passado seu Username e Senha no .env***

---

## Documentação da API
Esta API tem documentação no Postman.

🔹 **Acesse a documentação no navegador:**
- **Postman:** [Postman](https://www.postman.com/payload-geoscientist-29045431/desafiobackend-sistemaagendamentodjango/documentation/bdfsm9f/api-documentation-appointment-system-with-django)

---
## ✅ Testes com APITestCase

### 1. Teste de criação de usuário
Este teste verifica a criação de um usuário comum e de um super usuário
```sh
docker-compose run djangoapp python manage.py test users
```
### 2. Teste de criação de profissionais de saúde 
Este teste verifica a criação de um profissional de saúde e uma profissão a partir de um usuário IsStaff 
```sh
docker-compose run djangoapp python manage.py test professionals
```
---

## 🔧 Funcionalidades
### 1. **Gerenciamento de Profissionais de Saúde**
- Endpoints para cadastrar, editar e deletar profissionais de saúde
- Informações obrigatórias: Nome completo, Profissão, Endereço, Contato
- Nome Social é opcional
- Validação de CPF (utilize o [4Devs - Gerador de Pessoas](https://www.4devs.com.br/gerador_de_pessoas))
- Validação do CEP através da API [ViaCEP](https://viacep.com.br/)

### 2. **Gerenciamento de Profissiões/Especialidades**
- Endpoints para cadastrar, editar e deletar profissões
- Registro e edição só pode ser feito por usuários IsStaff (UserIsStaff=1)

### 3. **Gerenciamento de Consultas**
- Endpoints para cadastrar, editar e deletar consultas
- Validações de autenticação
- Regras de horários
- Permitir a pesquisa de consultas cadastradas utilizando o ID da pessoa profissional vinculada

### 4. **Autenticação e Autorização**
- Sistema de autenticação de usuários com SimpleJWT.
- Permissões baseadas em grupos (IsStaff, SuperUser).

### 5. **Integração com API's externas**
- Validação de Endereço pela API [ViaCEP](https://viacep.com.br/)

---

## 🛣️ Licença
Este projeto está sob a MIT License.


---

## 🌟 Contribuição
Fique à vontade para abrir issues e pull requests!


---


Desenvolvido por:
<a href="https://www.linkedin.com/in/thiago-costa-barros/" style="display: flex; align-items: center; text-decoration: none;">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="24" height="24" style="margin-right: 5px;">
    <strong>Thiago Costa</strong>
</a>





