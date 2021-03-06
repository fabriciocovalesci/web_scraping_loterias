#!/usr/bin/env python3

import re
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup, Tag, NavigableString
import aiohttp
import asyncio
from datetime import date, datetime, timedelta
from lxml import etree
import json
from unidecode import unidecode
from datetime import datetime, date, timedelta

from api import Client

class LotofacilBot(Client):
    
    def __init__(self, url_api):
        self.url_api = url_api
        super().__init__("resultados", "lotofacil")
            
    def start(self, concurso):
        content = self.get_loteria(concurso)
        print(content)
    
    
    def _clean_data(self, data):
        text = data.replace("“", '').replace("”", '').replace("`", '').replace("´", '').replace("’", '').replace("‘", '').strip()
        return text
    
    
    def _object_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def _is_date(self, string):
        """
        Return whether the string can be interpreted as a date.
        
        :param string: str, string to check for date
        """
        try: 
            datetime.strptime(string, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    
    def scraping_page(self, concurso):
        html_page = self.get_loteria(concurso)
        soup = self._object_soup(html_page)
        dom = etree.HTML(str(soup))
        divs = soup.find('div', { "class": "card lot-lotofacil" }) 
        
        if divs:
            acumulou = False
            data_sorteio = ""
            data_proximo_concurso = ""
                
            wins = divs.find('a', { "class": "button-win" })
            concurso_atual = int(divs.find('span', { 'class' : "color header-resultados__nro-concurso" }).get_text())
            local_sorteio =  divs.find('span', { 'class' : "color header-resultados__local-sorteio" }).get_text()
            _data_sorteio = divs.find('div', { 'class' : "sub-title" }).get_text()
            estados_premiados = []
            
            # if wins.attrs["data-estados-premiados"] :
            #     estados_premiados = wins.attrs["data-estados-premiados"]
            
            
                
            if _data_sorteio and 'hoje' in _data_sorteio.lower().strip():
                today_date = date.today()
                data_sorteio = today_date.strftime("%d/%m/%Y") 
                            
            # if wins.attrs["data-acertadores"].isnumeric():
            #     acumulou = False
            # else:
            #     acumulou = True
                
            if dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[2]/span[2]/span')[0].text:
                acumulou = True
                        
            dezenas = []
            for item in divs.find_all('li', {"class": "bg"}):
                dezenas.append(item.text)
                            
            premiacoes = [
                {
                "acertos": "15 Pontos",
                "vencedores": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[2]/span[2]/span')[0].text,
                "premio": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[2]/span[3]')[0].text
                },
                {
                "acertos": "14 Pontos",
                "vencedores": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[3]/span[2]/span')[0].text,
                "premio": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[3]/span[3]')[0].text
                },
                {
                "acertos": "13 Pontos",
                "vencedores": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[4]/span[2]/span')[0].text,
                "premio": "25,00"
                },
                {
                "acertos": "12 Pontos",
                "vencedores": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[5]/span[2]/span')[0].text,
                "premio": "10,00"
                },
                {
                "acertos": "11 Pontos",
                "vencedores": dom.xpath('//*[@id="DivDeVisibilidade[0]"]/div/div[5]/div/div[6]/span[2]/span')[0].text,
                "premio": "5,00"
                }
            ]      
            
            if divs.find("div", { "class": "col estimative separador" }).find("div", { "class": "value color" }) and divs.find("div", { "class": "col estimative separador" }).find("div", { "class": "value color" }).text:
                valor_prx_consurso = divs.find("div", { "class": "col estimative separador" }).find("div", { "class": "value color" }).text
            else:
                valor_prx_consurso = ""
            if divs.find("div", { "class": "col estimative separador" }).find("span", { "class": "color foother-resultados__data-sorteio" }) and divs.find("div", { "class": "col estimative separador" }).find("span", { "class": "color foother-resultados__data-sorteio" }).get_text():
                data_prx_concurso = divs.find("div", { "class": "col estimative separador" }).find("span", { "class": "color foother-resultados__data-sorteio" }).get_text()
            else:
                data_prx_concurso = ""

            if data_prx_concurso and 'amanha' in unidecode(data_prx_concurso.lower().strip()):
                ini_time_for_now = datetime.now()
                future_date_after_1day = ini_time_for_now + timedelta(days=1)
                data_proximo_concurso = datetime.strftime(future_date_after_1day, "%d/%m/%Y")
            else:
                data_proximo_concurso = data_prx_concurso
        
            body_lotofacil = {
                "acumuladaProxConcurso": valor_prx_consurso.strip(),
                "acumulou": acumulou,
                "concurso": concurso_atual,
                "data": data_sorteio,
                "dataProxConcurso": data_proximo_concurso,
                "dezenas": dezenas,
                "estadosPremiados": estados_premiados,
                "local": "ESPAu00c7ODASORTE em Su00c3OPAULO,SP",
                "loteria": "lotofacil",
                "mesSorte": "",
                "nome": "LotoFacil",
                "premiacoes": premiacoes,
                "proxConcurso": int(concurso_atual)+1,
                "timeCoracao": ""
                }
        else:
            body_lotofacil = {}         
        
        return body_lotofacil
    
    def send_loteria(self, concurso_atual,  obj):
        if int(concurso_atual) < int(obj["concurso"]):
            headers = CaseInsensitiveDict()
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'text/plain'
            body_loteria = json.dumps(obj, ensure_ascii=True)
            # url = 'http://localhost:8000/api/v1/lotofacil/update/db'
            # req = requests.post(url, data=body_loteria, headers=headers)
            req = requests.post(f"http://{self.url_api}/api/v1/lotofacil/update/db", data=body_loteria, headers=headers)
            print(req.json())
        else:
            print("Concurso nao realizado")
            

    def check_consurso(self):
        resp = requests.get(f"http://{self.url_api}/api/v1/lotofacil/latest/one")
        if resp.status_code == 200:
            return resp.json()["response"][0]["concurso"]
        
