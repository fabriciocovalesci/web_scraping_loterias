#!/usr/bin/env python3

import re
import os
import asyncio
import requests
import json


BASE_URL = "https://www.sorteonline.com.br/"

# BASE_URL + loteria + "/resultados/" + concurso
# from .database import DataBase


class Client:
    def __init__(self, endpoint, loteria) -> None:
        self.endpoint = endpoint
        self.loteria = loteria        
        
    def get_loteria(self, concurso):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
        resp = requests.get(f"{BASE_URL}{self.loteria}/{self.endpoint}/{concurso}", headers=headers)
        if resp.status_code == 200:
            return resp.text
        else:
            return "ERRO " + resp.status_code