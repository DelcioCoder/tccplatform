# Plataforma de Orientação Acadêmica

Esta API é parte de uma plataforma que conecta estudantes e orientadores para facilitar a orientação de TCCs. A aplicação foi desenvolvida com **Django** e **Django REST Framework** e utiliza **JWT** para autenticação e **PostgreSQL** como banco de dados. O frontend será desenvolvido em **Next.js 15** com **Tailwind CSS**.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Fluxo de Usuário](#fluxo-de-usuário)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Endpoints da API](#endpoints-da-api)
  - [Cadastro e Confirmação de Usuário](#cadastro-e-confirmação-de-usuário)
  - [Autenticação JWT](#autenticação-jwt)
  - [Gerenciamento de Perfis](#gerenciamento-de-perfis)
  - [Busca e Filtro](#busca-e-filtro)
  - [Sistema de Conexão](#sistema-de-conexão)
  - [Comunicação (Mensagens Diretas)](#comunicação-mensagens-diretas)
- [Instalação e Execução](#instalação-e-execução)
- [Testes e Considerações Finais](#testes-e-considerações-finais)

## Funcionalidades

1. **Cadastro de Usuários**  
   - Registro de estudantes e orientadores com informações básicas.
   - Criação do usuário com `is_active=False` e envio de email de confirmação.
   - Opção de cadastro pago com integração de métodos de pagamento locais (em desenvolvimento).

2. **Confirmação de Email**  
   - Envio de email com link de ativação que contém um token e UID codificado.
   - Endpoint para ativar a conta do usuário após a validação do token.

3. **Autenticação JWT**  
   - Implementação de login e refresh token utilizando `djangorestframework-simplejwt`.

4. **Gerenciamento de Perfis**  
   - Criação e edição de perfis de usuário com informações específicas para estudantes e orientadores.
   - Endpoint para recuperar e atualizar o perfil do usuário.

5. **Busca e Filtro**  
   - **Busca de Orientadores:** Estudantes podem pesquisar orientadores por área de especialização, com retorno de dados resumidos (nome, especialização, biografia).
   - **Busca de Estudantes:** Orientadores podem pesquisar estudantes por curso, ano de conclusão e tema de interesse.

6. **Sistema de Conexão**  
   - **Envio de Solicitação de Orientação:** Estudantes enviam solicitações de conexão a orientadores com mensagem personalizada.
   - **Resposta do Orientador:** Orientadores podem aceitar ou rejeitar solicitações, respondendo com uma mensagem.

7. **Comunicação (Mensagens Diretas)**  
   - Sistema de chat para troca de mensagens entre estudantes e orientadores.
   - Permite a listagem e criação de mensagens, garantindo comunicação privada e segura.

## Fluxo de Usuário

1. **Cadastro e Ativação:**  
   - O usuário se cadastra fornecendo os dados necessários.
   - Um email de confirmação é enviado. O usuário ativa sua conta clicando no link recebido.

2. **Login e Acesso ao Perfil:**  
   - Usuário realiza login utilizando JWT.
   - A partir daí, pode acessar e atualizar seu perfil.

3. **Busca e Conexão:**  
   - Estudantes acessam a página "Conectar" e visualizam a lista de orientadores através do endpoint `/api/profiles/advisors/`.
   - Ao selecionar um orientador, o estudante envia uma solicitação de orientação pelo endpoint `/api/connections/create/`.
   - Orientadores podem visualizar e responder às solicitações recebidas.

4. **Comunicação:**  
   - Após a conexão, estudantes e orientadores podem trocar mensagens diretas por meio do endpoint `/api/messaging/`.

## Tecnologias Utilizadas

- **Backend:** Django, Django REST Framework, PostgreSQL, JWT (SimpleJWT)
- **Frontend (em desenvolvimento):** Next.js 15, Tailwind CSS
- **Outros:** Django Filters para busca e filtragem de dados.

## Estrutura do Projeto

myproject/ ├── myproject/ # Configurações gerais (settings, urls, wsgi) ├── users/ # Cadastro e autenticação de usuários ├── profiles/ # Gerenciamento dos perfis dos usuários ├── connections/ # Solicitações de orientação e conexão ├── messaging/ # Sistema de mensagens diretas (chat) └── requirements.txt # Dependências do projeto


## Endpoints da API

### Cadastro e Confirmação de Usuário

- **Registro de Usuários (Estudantes e Orientadores):**
  - **Endpoint:** `POST /api/users/register/`
  - **Payload Exemplo:**
    ```json
    {
      "username": "usuario123",
      "email": "usuario@example.com",
      "password": "senhaSegura123",
      "user_type": "student"
    }
    ```
  - O usuário é criado com `is_active: false` e um email de confirmação é enviado.

- **Ativação de Conta:**
  - **Endpoint:** `GET /api/users/activate/<uidb64>/<token>/`
  - Ao acessar o link, o token é verificado e a conta é ativada.

### Autenticação JWT

- **Obtenção de Token:**
  - **Endpoint:** `POST /api/users/login/`
  - **Payload:**
    ```json
    {
      "username": "usuario123",
      "password": "senhaSegura123"
    }
    ```
  - **Resposta:**
    ```json
    {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
    ```

- **Refresh Token:**
  - **Endpoint:** `POST /api/users/token/refresh/`
  - Envia o refresh token para obter um novo access token.

### Gerenciamento de Perfis

- **Recuperação e Atualização de Perfil:**
  - **Endpoint:** `GET/PUT /api/profiles/`
  - Permite que o usuário recupere e atualize seu perfil com informações adicionais.

### Busca e Filtro

- **Busca de Orientadores:**
  - **Endpoint:** `GET /api/profiles/advisors/`
  - **Exemplo de Resposta:**
    ```json
    [
      {
        "username": "Harold",
        "specialization": "Engenharia Informática",
        "biography": "PYTHON | NEXT | JAVA | SQL"
      }
    ]
    ```
- **Busca de Estudantes:**
  - **Endpoint:** `GET /api/profiles/students/`
  - Permite aos orientadores filtrar estudantes por curso, ano de conclusão e tema de interesse.

### Sistema de Conexão

- **Envio de Solicitação de Orientação (Estudantes):**
  - **Endpoint:** `POST /api/connections/create/`
  - **Payload Exemplo:**
    ```json
    {
      "advisor": 1,
      "message": "Olá, estou interessado em sua experiência para meu TCC sobre IA."
    }
    ```
- **Listagem de Solicitações Recebidas (Orientadores):**
  - **Endpoint:** `GET /api/connections/advisor/requests/`
- **Resposta à Solicitação (Orientadores):**
  - **Endpoint:** `PATCH /api/connections/response/<id>/`
  - **Payload Exemplo:**
    ```json
    {
      "status": "accepted",
      "response_message": "Aceito, podemos discutir detalhes."
    }
    ```

### Comunicação (Mensagens Diretas)

- **Listagem e Criação de Mensagens:**
  - **Endpoint:** `GET/POST /api/messaging/`
  - **Filtragem:** Utilize parâmetro de query `recipient` para obter mensagens entre dois usuários.
  - **Exemplo de Criação (POST):**
    ```json
    {
      "recipient": 3,
      "content": "Olá, podemos marcar uma reunião?"
    }
    ```

## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/DelcioCoder/tccplatform.git
   cd nome-do-projeto
   
2. **Crie e active o ambiente virtual:**
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

