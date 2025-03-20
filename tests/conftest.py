import pytest
import logging
from src.configuration import EconomieGouvConfiguration


@pytest.fixture
def fichier_non_existant():
    return "nom_fichier"

@pytest.fixture
def economie_gouv_fixture():
    return [EconomieGouvConfiguration(
        type_api="economie_gouv",
        dataset="dataset",
        fichier_cible="fichier_cible",
        fichier_sql="fixtures/sql/test_sql",
        nom_table="nom_table",
        sql_creation="SELECT",
        select=["id"]
    )]

@pytest.fixture
def logger_fixture():
    return logging.getLogger("fixture")