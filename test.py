import json
import DataBase
from datetime import datetime, timedelta
import os
import shutil
import subprocess
import time
import logging
from dotenv import load_dotenv
import Firebase_DataBase

load_dotenv(override=True)

api_key = os.getenv("WEBSCRAPING_FIREBASE_KEY")

my_db = Firebase_DataBase.FireBase_DataBase(api_key)

# Leitura do arquivo e processamento de cada JSON
with open(rf'{os.getcwd()}\scrapy_kabum\scrapy_kabum\json\output.json', 'r', encoding="utf-8") as json_file:
    for linha in json_file:
                # Lê todas as linhas do arquivo
        lines = json_file.readlines()

        for line in lines:

            # Removendo a vírgula no final (se existir)
            line = line.strip(',\n')

            my_db.request_prdutos_post(line)