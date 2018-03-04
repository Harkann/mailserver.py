#! /usr/bin/env python3
import psycopg2
import argparse

parser = argparse.ArgumentParser(description="Manage the domains of mail addresses")
parser.add_argument("--list", help="display the list of virtual domains and their ids", action="store_true")
parser.add_argument("--add", nargs="+", help="add a domain to be managed by the mailserver")
parser.add_argument("--delete", nargs="+", help="delete a domain from the mail server")
parser.add_argument("--delete-all", help="delete all the domains from the mail server", action="store_true")
args = parser.parse_args()

def start_conn_cur(dbname, user):
    conn = psycopg2.connect("dbname={} user={}".format(dbname, user))
    cur = conn.cursor()
    return conn, cur

def close_conn_cur(conn, cur):
    conn.close()
    cur.close()


def format_domains(domains):
    values = ""
    for dom in domains:
        values += "('{}')".format(dom)
        if dom != domains[-1]:
            values += ","
    return values

def add_domains(domains):
    conn, cur = start_conn_cur("mailserver", "mailuser")
    cur.execute("SELECT * FROM virtual_domains;")
    rows = cur.fetchall()
    for row in rows:
        if row[1] in domains:
            print("Domain {} already managed by the name server".format(row[1]))
            domains.remove(row[1])    
    if len(domains) != 0:
        cur.execute("BEGIN; \
                    INSERT INTO virtual_domains (domain_name) \
                    VALUES {}; \
                    COMMIT;".format(format_domains(domains)))
    close_conn_cur(conn, cur)

def list_domains():
    conn = psycopg2.connect("dbname=mailserver user=mailuser")
    cur = conn.cursor()
    cur.execute("SELECT * FROM virtual_domains;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def delete(domains):
    conn, cur = start_conn_cur("mailserver", "mailuser")
    for dom in domains:
        cur.execute("BEGIN; \
                    DELETE FROM virtual_domains \
                    WHERE domain_name ILIKE '{}'; \
                    COMMIT;".format(dom))
    close_conn_cur(conn, cur)

def delete_all():
    conn = psycopg2.connect("dbname=mailserver user=mailuser")
    cur = conn.cursor()
    cur.execute("BEGIN; \
                DELETE FROM virtual_domains; \
                COMMIT;")
    cur.close()
    conn.close()

if args.list:
    list_domains()
elif args.add:
    add_domains(args.add)
elif args.delete:
    delete(args.delete)
elif args.delete_all:
    delete_all()
