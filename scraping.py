#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from datetime import date, datetime, timedelta
from .api import Client


class LotofacilBot(Client):
    
    def __init__(self):
        super().__init__()
        
        self.domain = "https://www.uol.com.br/"
        self.base_url_politica = self.domain + "politica/"
        

    async def _request_site_async(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    html = await response.text()
                    return html
        except Exception as err:
            print(f"ERROR - UOL: function [_request_site_async()] : {err}")
            
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
    

    async def _filter_urls(self, date):
        """Description
    
        Args:
            soup (Object): Instance type BeautifulSoup
            date (Object): Date for filter

        Returns:
            list: List of string with valid url
        """
        try:
            task = asyncio.create_task(coro=self._request_site_async(self.base_url_politica))
            html_page = await task
            
            soup = self._object_soup(html_page)
            list_url = []
            divs = soup.find('div', { "class": "flex-wrap" }) 
            for div in divs:
                if div.find('a') != -1 and div.find('a') != None:
                    date_consult = div.find('time', { 'class' : 'thumb-date' }).get_text()[0:10]
                    date_formated = datetime.strptime(date_consult, "%d/%m/%Y").date()
                    if date_formated == date:
                        list_url.append({ "date": datetime.strftime(date_formated, "%d/%m/%Y") , "url": div.find('a').get('href')})
            return list_url
        except Exception as err:
            print(f"ERROR - UOL: function [_filter_urls()] : {err}")
    
        
    async def _scraping_site(self, url, date):
        try:
            data_site = {
                "title": "",
                "date": date,
                "domain": self.domain,
                "status": "",
                "url": url,
                "author": "",
                "text": []
            }

            task = asyncio.create_task(coro=self._request_site_async(url))
            content = await task
            
            soup = self._object_soup(content)
            title = soup.find('i', {"class": "custom-title"}).text
            if title:
                data_site['title'] = self._clean_data(title)
            else:
                data_site['title'] = ""
                
            author = soup.find('p', { "class": "p-author" }).text            
            if self._is_date(author[:10]) == False:
                data_site['author'] = author
            else:
                data_site['author'] = "Colunista do UOL"
                        
            div = soup.find('div', {"class": "text"})
            children = div.findChildren("p" , recursive=False)
            
            text_elements = []
            for child in children:
                if len(child.get_text()) != 0:
                    text_elements.append(self._clean_data(child.get_text()))
                    
            text_elements = ''.join(map(str,text_elements))

            data_site['text'] = text_elements
            return data_site
        except Exception as err:
            print(f"ERROR - UOL: function [_scraping_site()] : {err}")
        
        
    async def get_text(self):
        try:
            result = []
            last_day = datetime.today() - timedelta(days=1)
            list_urls = await self._filter_urls(last_day.date())
            for url in list_urls:
                content = await self._scraping_site(url['url'], url['date'])
                if content:
                    result.append(content)
                    print(f"Add new title: {content['title']} | url {content['url']}")
            return result
        except Exception as err:
            print(f"ERROR - UOL: function [get_text()] : {err}")