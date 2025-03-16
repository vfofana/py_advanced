import duckdb


def stocker_dans_bdd(sql, fichier, bdd, nom_table):
    print("Chargement dans la BDD")
    connection = duckdb.connect(bdd)
    try:
        connection.sql(sql)
        connection.sql(f'INSERT INTO {nom_table} '
                       f'SELECT * FROM read_json_auto("{fichier}")')
    except Exception as e: #Doit se placer en dernier, il faut except toutes les heures qui peuvent arriver
        print(e)
        raise

    finally:
        connection.close()