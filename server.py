
import cgi,cgitb
import sys
import json
from product import add_product,search_product,update_product,delete_product
from authmodule import sign_up,login,authenticate
import sqlite3
try:
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler
    from urlparse import urlparse
except Exception as e:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse

class ServerRequestHandler(BaseHTTPRequestHandler):
    conn = sqlite3.connect('wingify.db')
    def do_GET(self):
        try:
            is_authenticate =False
            query_components = None
            url = urlparse(self.path)
            path = url.path
            query = url.query
            if query:
                query_components = dict(qc.split("=") for qc in query.split("&"))
                if 'token' in query_components:
                    is_authenticate = authenticate(self.conn,query_components['token'])
                    del query_components['token']

            if path == "/user":
                print 'user'
            elif path =="/product":
                if is_authenticate:
                    data = search_product(self.conn,query_components)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({'data': data}))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write({"unauthorized": "You are not authorized to make request"})
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': "requested url does not exists"}))
            return
        except Exception as e:
            return {"error":str(e)}

    def do_POST(self):
        try:
            is_authenticate = False
            query_components = None
            url = urlparse(self.path)
            path = url.path
            query = url.query
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print "--->",post_data
            if query:
                query_components = dict(qc.split("=") for qc in query.split("&"))
                if 'token' in query_components:
                    is_authenticate = authenticate(self.conn,query_components['token'])
                    del query_components['token']
            if path == "/user/signup":
                if post_data:
                    data = json.loads(post_data)
                    if 'username' in data and 'password' in data:
                        response = sign_up(self.conn,data)
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(json.dumps(response))
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(json.dumps({"error":"please provide required fields"}))
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': "Please provide valid json"}))

            elif path == "/product/add":
                if is_authenticate:
                    if post_data:
                        data = json.loads(post_data)
                        if 'product_name' in data and 'price' in data:
                            response = add_product(self.conn,data)
                            self.send_response(201)
                            self.end_headers()
                            self.wfile.write(json.dumps({'data': response}))
                        else:
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(json.dumps({'error': "Please provide mandatory fileds"}))
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': "Please provide valid json"}))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write({"unauthorized": "You are not authorized to make request"})

            elif path == "/login":
                data = json.loads(post_data)
                if 'username' in data and 'password' in data:
                    response = login(self.conn,data)
                    if 'error' in response:
                        self.send_response(406)
                    else:
                        self.send_response(202)
                    self.end_headers()
                    self.wfile.write(json.dumps({'data': response}))
                else:
                    self.send_response(406)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': "please provide username and password"}))

            # elif path == "/logout":
            #     self.send_response(200)
            #     self.end_headers()
            #     # self.wfile.write(json.dumps({'data': data}))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': "requested url does not exists"}))
            return
        except Exception as e:
            return {"error":str(e)}

    def do_PUT(self):
        try:
            is_authenticate = False
            query_components = None
            url = urlparse(self.path)
            path = url.path
            query = url.query
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            if query:
                query_components = dict(qc.split("=") for qc in query.split("&"))
                if 'token' in query_components:
                    is_authenticate = authenticate(self.conn,query_components['token'])
                    del query_components['token']

            # if path == "/user/update":
            #     self.send_response(200)
            #     self.end_headers()
            #     self.wfile.write(json.dumps({'data': data}))
            if path == "/product/update":
                if is_authenticate:
                    response = update_product(self.conn,data)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({'data': response}))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write({"unauthorized": "You are not authorized to make request"})
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': "requested url does not exists"}))
            return
        except Exception as e:
            return {"error":str(e)}


    def do_DELETE(self):
        try:
            is_authenticate = False
            query_components = None
            url = urlparse(self.path)
            path = url.path
            query = url.query
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            if query:
                query_components = dict(qc.split("=") for qc in query.split("&"))
                if 'token' in query_components:
                    is_authenticate = authenticate(self.conn,query_components['token'])
                    del query_components['token']
                print ("query",query_components)
            # if path == "/user/delete":
            #     self.send_response(200)
            #     self.end_headers()
            #     self.wfile.write(json.dumps({'data': data}))
            if path == "/product/delete":
                if is_authenticate:
                    response = delete_product(self.conn,data)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({'data': response}))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write({"unauthorized": "You are not authorized to make request"})
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': "requested url does not exists"}))
            return
        except Exception as e:
            return {"error":str(e)}


def run(server_class=HTTPServer,
        handler_class=ServerRequestHandler):
        server_address = ('0.0.0.0', 8000)
        httpd = server_class(server_address, handler_class)
    # httpd.serve_forever()
        while True:
            print ("running at 0.0.0.0:8000")
            httpd.handle_request()


if __name__ == '__main__':
    run()
