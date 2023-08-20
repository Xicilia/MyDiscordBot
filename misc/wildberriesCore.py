"""
Wildberries is a russian marketplace which has a pretty easy api to get products card from.

####################################################################################################################################################

Each product has it's own id, which is combination of vol id, part id, and product id in part.

vol id is a number between 100 and 1737 (pretty much last vol that i found)

vol is separated in parts, each vol has 100 (0 to 99) parts, so part id is random number between 0 and 99.

each part have 1000 individual products that have their own id inside this part. product id in part is a number between 0 and 999.

by concatenating this three id's we can get global product id.

for example: product with id 106253433 located in 1062 vol, then in 53 part of this vol, and have 433 id in this part.

####################################################################################################################################################

vols can be accessed through wb.ru page. However, we need to know in which basket our vol is located.

baskets is something like containers for vols. Baskets size is pretty random, so we cant write an universal algorithm that can get basket by vol id.

but it's not hard to trace baskets sizes by increasing vol id and watching from which basket wildberries gets info about this vol.

in function getBasketByVol i traced i think all of the baskets that currently (19.08.2023) working. 

####################################################################################################################################################

"""

import discord
import random

from dataclasses import dataclass
from typing import Optional

from misc.httpManager import HttpRequestManager

#FOR RANDOM PRODUCT GENERATION
#first vols have a lot of deleted products which still contains in baskets
_usingVolsStart = 900 
_usingVolsEnd = 1737


@dataclass 
class WildberriesProduct:
    
    name: str
    description: str
    category: str
    type: str
    imageLink: Optional[str]
    productLink: str
    
    
def serializeWildberriesProductToString(product: WildberriesProduct) -> str:
    """
    Serializes wildberries product to string.
    
    :param product: product which will be serialized.
    Returns: serialized product.
    """
    
    return (
        f"Название: {product.name}\n\n" +
        f"Категория: {product.category}\n\n" +
        f"Тип: {product.type}\n\n" +
        f"Описание: {product.description}\n\n" +
        f"Ссылка: {product.productLink}"
    )


def serializeWildberriesProductImageToEmbed(product: WildberriesProduct) -> Optional[discord.Embed]:
    """
    creates discord.Embed with image at wildberries product imageLink.
    
    :param product: wildberries product with imageLink not None.
    Returns: discord.Embed with image at imageLink, if product has no imageLink returns None.
    """
    
    if not product.imageLink: return None
    
    return discord.Embed().set_image(url=product.imageLink)
 
 
def getBasketByVol(vol: int) -> str:
    """
    Gets basket by vol id
    
    :param vol: vol id
    Returns: basket name.
    """
    if vol >= 100 and vol <= 143:
        return 'basket-01'
    elif vol >= 144 and vol <= 287:
        return 'basket-02'
    elif vol >= 288 and vol <= 431:
        return 'basket-03'
    elif vol >= 432 and vol <= 719:
        return 'basket-04'
    elif vol >= 720 and vol <= 1007:
        return 'basket-05'
    elif vol >= 1008 and vol <= 1061:
        return 'basket-06'
    elif vol >= 1062 and vol <= 1115:
        return 'basket-07'
    elif vol >= 1116 and vol <= 1169:
        return 'basket-08'
    elif vol >= 1170 and vol <= 1313:
        return 'basket-09'
    elif vol >= 1314 and vol <= 1601:
        return 'basket-10'
    elif vol >= 1602 and vol <= 1655:
        return 'basket-11'
    elif vol >= 1656 and vol <= 1737:
        return 'basket-12'
    
    return ''
  
    
def getWildberriesProduct(volId: int, partId: int, productPartId: int) -> Optional[WildberriesProduct]:
    
    """
    Gets wildberries product by given ids
    
    :param volId: vol id
    :param partId: part id inside vol
    :param productPartId: product id inside part
    Returns: WildberriesProduct if product with given id exist, else None.
    """
    
    basket = getBasketByVol(volId)
    
    answer: dict = HttpRequestManager.getRequest(f"https://{basket}.wb.ru/vol{volId}/part{volId}{partId}/{volId}{partId}{productPartId}/info/ru/card.json", True).jsonAnswer
    
    if not answer:
        return None
    
    #if product have images
    if answer['media'].get("photo_count", 0):
        
        imageUrl = f'https://{basket}.wb.ru/vol{volId}/part{volId}{partId}/{volId}{partId}{productPartId}/images/big/1.jpg'
        
    else: 
        
        imageUrl = None
    
    return WildberriesProduct(
        answer.get("imt_name", "У товара нет названия"),
        answer.get("description", "Пустое описание товара"), #description can be empty
        answer.get("subj_root_name", "Отсутствует"),
        answer.get("subj_name", "Отсутствует"),
        imageUrl,
        f'https://www.wildberries.ru/catalog/{volId}{partId}{productPartId}/detail.aspx'
    )
 
    
def getRandomWildberriesProduct() -> Optional[WildberriesProduct]:
    """
    Shortcut for getting random wildberries product.
    
    Returns: WildberriesProduct if product with generated id exist, else None.
    """
    
    return getWildberriesProduct(
        random.randint(_usingVolsStart, _usingVolsEnd),
        random.randint(0, 99),
        random.randint(0, 999)
    )
    