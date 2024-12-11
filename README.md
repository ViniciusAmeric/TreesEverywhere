# Trees Everywhere

## Descrição
O "Trees Everywhere" é uma aplicação web para o gerenciamento de árvores plantadas. A aplicação permite que os usuários registrem e visualizem árvores, além de integrar com um banco de dados para armazenar as informações de forma eficiente.

## Tecnologias Utilizadas
- **Python 3.x**
- **Django** (framework web)
- **MySQL** (banco de dados)
- **Django REST Framework** (para criação de APIs)
- **dotenv** (para gerenciamento de variáveis de ambiente)

## Pré-requisitos

Certifique-se de ter o Python 3.x e o MySQL (ou outro banco de dados compatível) instalados. Você também vai precisar de uma chave secreta para o Django e das credenciais do banco de dados configuradas.

## Instalação

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/trees-everywhere.git
    cd trees-everywhere
    ```

2. **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```

3. **Ative o ambiente virtual:**

    - **No Windows:**
      ```bash
      venv\Scripts\activate
      ```

    - **No macOS/Linux:**
      ```bash
      source venv/bin/activate
      ```

4. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Crie o banco de dados e execute as migrações:**
    Se você estiver usando MySQL, execute:
    ```bash
    mysql -u root -p
    CREATE DATABASE treeseverywhere;
    exit
    ```

    Em seguida, no terminal, execute as migrações do Django:
    ```bash
    python manage.py migrate
    ```

6. **Crie um superusuário (para acessar a área administrativa):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Configure as variáveis de ambiente**:
    Crie um arquivo `.env` no diretório raiz do projeto e adicione as seguintes variáveis (use as suas próprias credenciais):

    ```dotenv
    SECRET_KEY='sua-chave-secreta'
    DEBUG=True
    DB_NAME='treeseverywhere'
    DB_USER='seu-usuario'
    DB_PASSWORD='sua-senha'
    DB_HOST='localhost'
    DB_PORT='3306'
    ```

8. **Execute o servidor localmente:**
    ```bash
    python manage.py runserver
    ```

    A aplicação estará disponível em `http://127.0.0.1:8000/`.

## Funcionalidades

- Cadastro de árvores com informações sobre sua localização e espécies.
- Visualização de árvores registradas.
- Área administrativa para gerenciamento das árvores plantadas.

## Testes

Você pode rodar os testes do Django com o seguinte comando:

```bash
python manage.py test
