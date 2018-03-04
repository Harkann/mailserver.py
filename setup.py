#! /usr/bin/env python3
import psycopg2
import delete_server #on supprime toute install précédente.

#on se connecte en tant que postgres pour etre root sur la bdd
conn = psycopg2.connect("dbname=postgres user=postgres")
cur = conn.cursor()

print("connected to postgres as postgres")
#on crée l'user mailuser et la base mailserver
cur.execute("BEGIN; \
            CREATE USER mailuser; \
            REVOKE CREATE ON SCHEMA public FROM PUBLIC; \
            REVOKE USAGE ON SCHEMA public FROM PUBLIC; \
            GRANT CREATE ON SCHEMA public TO postgres; \
            GRANT USAGE ON SCHEMA public TO postgres; \
            COMMIT;")

print("mailuser created")

cur.execute("CREATE DATABASE mailserver WITH OWNER mailuser;")

print("database mailserver created")
#on ferme la connection, on a plus besoin de postgres maintenant
cur.close()
conn.close()
print("connection to postgres closed")
#on se connecte maintenant en tant que mailuser sur mailserver
conn = psycopg2.connect("dbname=mailserver user=mailuser")
cur = conn.cursor()
print("connected to mailserver as mailuser")
cur.execute("BEGIN; \
            CREATE SEQUENCE seq_mail_domain_id START 1; \
            CREATE SEQUENCE seq_mail_user_id START 1; \
            CREATE SEQUENCE seq_mail_alias_id START 1; \
            COMMIT;")
print("sequences created")
cur.execute("BEGIN; \
            CREATE TABLE virtual_domains (\
            domain_id INT2 NOT NULL DEFAULT nextval('seq_mail_domain_id'), \
            domain_name varchar(50) NOT NULL, \
            PRIMARY KEY (domain_id)); \
            COMMIT;")
print("table virtual_domains created")
cur.execute("BEGIN; \
            CREATE TABLE virtual_users (\
            user_id INT2 NOT NULL DEFAULT nextval('seq_mail_user_id'), \
            domain_id INT2 NOT NULL, \
            password varchar(106) NOT NULL, \
            email varchar(100) NOT NULL, \
            PRIMARY KEY (user_id), \
            FOREIGN KEY (domain_id) REFERENCES virtual_domains(domain_id) ON DELETE CASCADE); \
            COMMIT;")
print("table virtual_users created")
cur.execute("BEGIN; \
            CREATE TABLE virtual_aliases ( \
            alias_id INT2 NOT NULL DEFAULT nextval('seq_mail_alias_id'), \
            domain_id INT2 NOT NULL, \
            source varchar(100) NOT NULL, \
            destination varchar(100) NOT NULL, \
            PRIMARY KEY (alias_id), \
            FOREIGN KEY (domain_id) REFERENCES virtual_domains(domain_id) ON DELETE CASCADE); \
            COMMIT;")
print("table virtual_aliases created")

