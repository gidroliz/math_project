# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pymysql
from main import main
from dotenv import dotenv_values

secrets = dotenv_values(".env")


connection = pymysql.connections.Connection(
    host=secrets["MYSQL_HOST"],
    port=int(secrets["MYSQL_PORT"]),
    user=secrets["MYSQL_USER"],
    password=secrets["MYSQL_PASSWORD"],
    database=secrets["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
)


def verify_token(token):
    if token == secrets["HARD_TOKEN"]:
        return None, True
    else:
        with connection.cursor() as cursor:
            sql = f"""SELECT id FROM math_user WHERE token='{token}' LIMIT 1;"""
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result["id"], True
            else:
                return None, False


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = "<font size=+3>Hello world!</font><p>"
        self.wfile.write(bytes(message, "utf8"))

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
    print("starting server...")
    server_address = ("", 5656)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print("running server...")
    httpd.serve_forever()


run()
