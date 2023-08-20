import requests

from dataclasses import dataclass
from typing import Optional

@dataclass
class RequestAnswer:
    
    statusCode: int
    answer: Optional[str]
    jsonAnswer: Optional[dict]
  
    
class HttpRequestManager:
    
    #basic headers dictionary for requests 
    _basicHeaders = {
    "Host": "", #needs to be set
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "", #needs to be set
    "Connection": "keep-alive",
    "Referer": "", #needs to be set
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Content-Length': '0',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    
    @staticmethod
    def checkHeaders(headers: dict) -> bool:
        """
        checks that headers dictionary is full
        
        :param headers: checking headers
        Returns: True if headers dictionary is correct, else False
        """

        #if headers['Host'] 
    
    @staticmethod
    def getHeaders(host: str, origin: str, referer: str) -> dict:
        """
        Copies basic headers dictionary and sets host, origin and referer for post request.
        
        :param host: host headers parameter.
        :param origin: origin headers parameter.
        :param referer: referer headers parameter.
        Returns: headers dictionary.
        """
        
        newHeaders = HttpRequestManager._basicHeaders.copy()
        
        newHeaders['Host'] = host
        newHeaders['Origin'] = origin
        newHeaders['Referer'] = referer
        
        return newHeaders
    
    @staticmethod
    def getRequest(url: str, useUtf8: bool = False) -> RequestAnswer:
        """
        Performs get request to given url and returns RequestAnswer object.
        
        :param url: url for perform request.
        :param useUtf8: encode answer to utf-8.
        Returns: RequestAnswer object.
        """
        
        request = requests.get(url)
        
        if request.status_code != 200:
            return RequestAnswer(request.status_code, None, None)
        
        if useUtf8: request.encoding = "utf-8"
        
        try:
            
            jsonAnswer = request.json()
            
        except: 
            
            jsonAnswer = None
        
        return RequestAnswer(request.status_code, request.text, jsonAnswer)
    
    @staticmethod
    def postRequest(url: str, headers: dict) -> dict:
        """
        Performs post request for url and returns json answer.
        
        :param url: url to perform request.
        :param headers: headers for request
        Returns: json answer.
        """
        return requests.post(url, headers=headers).json()