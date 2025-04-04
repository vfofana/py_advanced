from pydantic.dataclasses import dataclass
from time import sleep
import requests
from requests import HTTPError
from typing import List

def requests_get(url:str, max_retries:int=3) -> requests.Response: # pragma: no cover
    error_count = 0
    http_error_count = 0

    r = None
    while True:
        try:
            r = requests.get(url)
            r.raise_for_status()
            break
        except requests.exceptions.ConnectionError:
            error_count += 1
            if error_count > max_retries:
                raise
            else:
                sleep(10)
                continue
        except HTTPError:
            http_error_count += 1
            if http_error_count > max_retries:
                raise
            else:
                sleep(10)
                continue
    return r

@dataclass
class EconomieGouvConfiguration:
    type_api:str
    dataset:str
    fichier_cible:str
    fichier_sql:str
    nom_table:str
    sql_creation :str
    select:list

    @property
    def url(self) -> str:
        if self.select:
            select_param = "%2C".join(self.select)
            return f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/{self.dataset}/records?select={select_param}&limit={{step}}&offset={{offset}}"
        else:
            return f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/{self.dataset}/records?limit={{step}}&offset={{offset}}"


    def telecharger(self) -> list[dict]: # pragma: no cover
        step = 100
        offset = 0
        toutes_les_data = []
        print("Télécharger les données economie gouv")
        while True:
            r = requests_get(self.url.format(step=step, offset=offset), )
            data = r.json()
            toutes_les_data += data['results']
            total_count = data['total_count']
            offset += step
            if total_count - offset <= 0:
                break
            if offset + step > 10000:
                break
        return toutes_les_data

@dataclass
class DataGouvConfiguration:
    type_api: str
    dataset: str
    fichier_cible: str
    fichier_sql: str
    nom_table: str
    sql_creation: str


    @property
    def url(self) -> str:
        return f"https://tabular-api.data.gouv.fr/api/resources/{self.dataset}/data/?Date__exact='2024-10-31'"

    def telecharger(self) -> list[dict]: # pragma: no cover
        toutes_les_data = []
        url = self.url
        print("Télécharger les données data gouv")
        while url:
            r = requests_get(url, )
            data = r.json()
            toutes_les_data += data['data']
            url = data['links'].get("next")
        return toutes_les_data