## Pequeno projeto de etl em Python para transformar uma base de dados csv,

## popular um banco de dados Mongo DB e uma pagina WEB para exemplificar

## a utilização.

## Para a utilização do app é necessário ter instalado no computador o VS Code,

## o Python versão 3.12.3 ou superior e o banco de dados MongoDB, para verificar

## se ao executar o etl o mesmo efetuou a criação do banco de dados, a collection

## e populou o banco, pode ser utilizado o MongoDBCompass, NoSQLBooster ou Mongosh.

# Após clonar o repositório, usar o comando a seguir para criar o ambiente virtual.

# Windows

phyton -m venv venv

# Linux ou Mac

phyton3 -m venv venv

# Executar o ambiente virtual Phython

# Windows

venv\Scripts\activate

# Linux ou Mac

venv/bin/activate

# Criar na raiz do projeto o arquivo .env e inserir as credenciais do banco de dados

MONGO_URI=mongodb://localhost:27017/

## Instalar as dependências

pip install -r requirements.txt

## Executar o etl

# Windows

python etl/etl.py

# Linux ou Mac

python3 etl/etl.py

## Executar a pagina WEB

# Windows

python run.py

# Linux ou Mac

python3 run.py

## Para acessar a pagina copiar o endereço que será apresentado no terminal e colar no navegador

## ou apertar o botão "Ctrl" e clicar com o mouse sobre o endereço para abrir no navegador padrão
