import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from lxml import html
import json
import re

class FireBase_DataBase:
    def __init__(self, api_key) -> None:

        self.api_key = api_key
        pass


    def request_prdutos_post(self, date):

        if type(date) == str:
            date = json.loads(date)
        
        requisicao = requests.post(f'{self.api_key}/Produtos/.json', data=json.dumps(date))

        return requisicao, requisicao.text

