from misc.globals import settings
from typing import Optional

signsObjects = {
    #apiName - sign name in url for request, alias - sign represenation for message.
    "козерог": {
        "apiName": "capricorn",
        "alias": "козерога"
    },
    
    "водолей": {
        "apiName": "aquarius",
        "alias": "водолея"
    },
    
    "рыбы": {
        "apiName": "pisces",
        "alias": "рыб"
    },
    
    "овен": {
        "apiName": "aries",
        "alias": "овна"
    },
    
    "телец": {
        "apiName": "taurus",
        "alias": "тельца"
    },
    
    "близнецы": {
        "apiName": "gemini",
        "alias": "близнецов"
    },
    
    "рак": {
        "apiName": "cancer",
        "alias": "рака"
    },
    
    "лев": {
        "apiName": "leo",
        "alias": "льва"
    },
    
    "весы": {
        "apiName": "libra",
        "alias": "весов"
    },
    
    "дева": {
        "apiName": "virgo",
        "alias": "девы"
    },
    
    "скорпион": {
        "apiName": "scorpio",
        "alias": "скорпиона"
    },
    
    "стрелец": {
        "apiName": "sagittarius",
        "alias": "стрельца"
    }   
}

   
class HoroManager:
    
    @staticmethod
    def getHoro(sign: str) -> Optional[dict]:
        """
        Returns dict horo object (apiName and alias).
        
        :param sign: russian sign name.
        Returns: dict if sign was finded, else None.
        """
        
        return signsObjects.get(sign, None)
    
    @staticmethod
    def getMemberHoro(memberId: str) -> Optional[str]:
        """
        Finds member sign.
        
        :param memberId: id of member whose sign need to find
        Returns: sign key if member has sign, else None.
        """
        signDictionary: dict = settings.getSetting("signs")
        
        sign = signDictionary.get(memberId, None)
        
        return sign

    
    @staticmethod
    def setMemberHoro(memberId: str, horo: str) -> bool:
        """
        sets horo for member and saves it to settings.json
        
        :param memberId: member who saves horo
        :param horo: member's sign
        Returns: True if operation was successfull, else False
        """
        
        #wrong sign
        if not signsObjects.get(horo.lower(), False): return False
        #print("valid sign")
        #return result of settings update
        return settings.addValueToDictionarySetting("signs", memberId, horo)