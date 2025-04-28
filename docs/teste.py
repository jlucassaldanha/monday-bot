from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    try:
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [b'Hello World!']
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [b'Internal Server Error: ' + str(e).encode('utf-8')]


httpd = make_server('', 8000, simple_app)
print("Serving on port 8000...")
httpd.handle_request()