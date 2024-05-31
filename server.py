# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pymysql
from main import main
from dotenv import dotenv_values
from modules.migrate import make_migration
from modules.service import generate_table
from modules.sql_querys import sql_verify_token, sql_check_tasks

secrets = dotenv_values(".env")


connection = pymysql.connections.Connection(
    host=secrets["MYSQL_HOST"],
    port=int(secrets["MYSQL_PORT"]),
    user=secrets["MYSQL_USER"],
    password=secrets["MYSQL_PASSWORD"],
    database=secrets["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
)

def check_tasks():
    with connection.cursor() as cursor:
        cursor.execute(sql_check_tasks)
        result = cursor.fetchone()
    if result['COUNT(*)']==0:
        generate_table(connection)

def verify_token(token):
    if token == secrets["HARD_TOKEN"]:
        return None, True
    else:
        with connection.cursor() as cursor:
            cursor.execute(sql_verify_token.format(token))
            result = cursor.fetchone()
            if result:
                return result["id"], True
            else:
                return None, False


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        try:
            user_id, verification = verify_token(self.headers["Authorization"])
            if verification:
                b = body.decode("cp1251")
                print("requests body: ", b)
                code, response = main(connection, json.loads(b), user_id)
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response), "utf-8"))
            else:
                self.send_response(403, "Bad token")
                self.end_headers()
        except Exception as e:
            self.send_response(403, "Auth error")
            print(e)
            self.end_headers()


def run():
    make_migration()
    check_tasks()
    print("starting server...")
    server_address = ("", 5656)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print("running server...")
    httpd.serve_forever()


run()
