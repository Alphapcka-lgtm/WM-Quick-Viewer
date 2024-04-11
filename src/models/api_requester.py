from pywmapi.items import list_items
from pywmapi.items.models import ItemShort

from pywmapi.statistics import get_statistic
from pywmapi.statistics.models import Statistic

from pywmapi.orders import get_orders
from pywmapi.orders.models import OrderRow

from pywmapi.common.enums import Platform, Language

from urllib.parse import urlencode
import json

import requests

DEFAULT_PLATFORM = Platform.pc
REQUEST_TIMEOUT = float(180)
"""Time in seconds until the connection should timeout"""

def request_items(lang: Language) -> list[ItemShort]:
    return list_items(lang)

def request_item_statistics(url_name: str) -> Statistic:
    return get_statistic(url_name, DEFAULT_PLATFORM)

def request_item_orders(url_name: str) -> list[OrderRow]:
    return get_orders(url_name, DEFAULT_PLATFORM)

def request_prime_data() -> dict:
    # building request url
    origin = 'https://warframe.fandom.com'
    path = '/api.php'
    params = {
	    'action': "scribunto-console",
	    'format': "json",
	    'title': "Module:Void/data",
	    'content': "",
	    'question': 'local VoidData = require(\'Module:Void/data\').PrimeData local json = require(\'Module:JSON\') print(json.stringify(VoidData))',
	    'clear': '1'
    }
    query_string = urlencode(params)
    request_url = f"{origin}{path}?{query_string}"

    # request the actual data
    response = requests.get(request_url)
    if response.status_code > 299:
        raise requests.ConnectionError(f'Invalid Response code: {response.status_code}', response=response)
    relics_json = json.loads(response.json()['print'])
    return relics_json
