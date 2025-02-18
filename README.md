# API de Gerenciamento de Consultas Médicas

## ✨ Visão Geral
Esta API Restful foi desenvolvida para gerenciar consultas médicas e profissionais de saúde, seguindo boas práticas de desenvolvimento, segurança e eficiência.

---

## 📝 Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework:** Django + Django Rest Framework (DRF)
- **Gerenciamento de dependências:** Poetry
- **Banco de Dados:** PostgreSQL
- **Testes:** APITestCase do Django Rest Framework
- **Docker:** *(Em desenvolvimento)*

---

## 🛠️ Como Executar o Projeto
### 1. Clonar o Repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

### 2. Instalar o Poetry (caso não tenha)
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Instalar as Dependências
```sh
poetry install
```

### 4. Criar e Configurar o Banco de Dados
- Certifique-se de ter um banco PostgreSQL rodando e configure as credenciais no arquivo `.env`.
- Aplique as migrações:
```sh
poetry run python manage.py migrate
```

### 5. Criar um Superusuário
```sh
poetry run python manage.py createsuperuser
```
Preencha com o **usuário** e **senha** configurados no `.env`.

### 6. Executar o Seed DB
Após criar o superusuário, execute:
```sh
python seed_db.py
```
Isso carregará os dados iniciais no banco.

### 7. Executar o Servidor
```sh
poetry run python manage.py runserver
```

A API estará disponível em: **http://127.0.0.1:8000/**

---

## 🔧 Funcionalidades
### 1. **Gerenciamento de Profissionais de Saúde**
- Criar, editar e deletar profissionais.
- Campos obrigatórios: Nome completo, Profissão, Endereço, Contato.
- Cadastro permite **Nome Social**.

### 2. **Gerenciamento de Consultas**
- Criar, editar e deletar consultas.
- Cada consulta inclui:
  - Data da consulta.
  - Profissional de saúde vinculado.

### 3. **Busca de Consultas**
- Permite pesquisar consultas cadastradas pelo **ID do profissional vinculado**.

### 4. **Segurança e Validação**
- Sanitiza inputs para evitar ataques (ex: SQL Injection).
- Valida os dados recebidos antes de armazenar.

---

## 🔮 Testes
Para rodar os testes unitários, execute:
```sh
poetry run python manage.py test
```

---

## 🛠️ Docker *(Em desenvolvimento)*
O suporte para Docker será adicionado em breve para facilitar a implantação.

---

## 📝 Modelo de `.env`
```
# SUPABASE 
SUPABASE_user=
SUPABASE_password=
SUPABASE_host=
SUPABASE_port=
SUPABASE_dbname=
DATABASE_URL=

DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
```

---

## 🌟 Contribuição
Fique à vontade para abrir issues e pull requests!

---

## 🛣️ Licença
Este projeto está sob a MIT License.

