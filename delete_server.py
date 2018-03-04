#! /usr/bin/env python3
import psycopg2
#on se connecte en tant que postgres pour etre root sur la bdd
conn = psycopg2.connect("dbname=postgres user=postgres")
cur = conn.cursor()
#on supprime la base et l'user
conn.autocommit=True
if input("Voulez vous vraiment supprimer le serveur mail ? [y/N]",default="n") == y:
    try:
        cur.execute("DROP DATABASE mailserver;")
    except:
        pass
    try:
        cur.execute("BEGIN; \
                     DROP USER mailuser; \
                     COMMIT;")
    except:
        pass
#on ferme la connection, on a plus besoin de postgres maintenant
cur.close()
conn.close()
