import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd


# DESCOMENTE PARA DEBUGAR E VER SE CONECTA AO DB
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")
# print(f"Conectando ao banco {db_name} no host {db_host} como usuário {db_user}.")



load_dotenv()

try:
    db = mysql.connector.connect(
        user = os.getenv("DB_USER"),
        passwd = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
    )
    print("Conexão bem-sucedida!")
    
except: print(f"Ocorreu um erro ao conectar ao Banco de Dados")

    
    

# Carregar o arquivo JSON
# df = pd.read_json("dados.json")

# Visualizar os primeiros registros
# print(df.head())