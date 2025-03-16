from utils.stocker_fichier import stocker_fichier
from utils.lecteur_configuration import lire_configuration
from bdd.db import stocker_dans_bdd
from utils.custom_logging import setup_advanced_logging

fichier_base_de_donnees = "../data/bdd_cours_python_avance"

# Creation des logger
logger_main = setup_advanced_logging("main_pipeline", "../logs/main.log")
logger_lecteur_config = setup_advanced_logging("lecteur_config", "../logs/main.log")

if __name__ == "__main__":
    logger_main.info("lecture configuration")
    configuration = lire_configuration(logger_lecteur_config)

    logger_main.info("Telechargement et stockage")
    for config in configuration:
        logger_main.debug(f"Telechargement de {config.type_api}, dataset {config.dataset}")

        resultat = config.telecharger()
        logger_main.debug(f"Recu {len(resultat)} lignes")

        logger_main.debug(f"Stockage dans le fichier {config.fichier_cible}")
        stocker_fichier(resultat, config.fichier_cible)

        logger_main.debug("Stockage dans la BDD")
        stocker_dans_bdd(config.sql_creation, config.fichier_cible, fichier_base_de_donnees,config.nom_table)
