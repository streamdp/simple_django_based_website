def application(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    body = [(arg+'\n').encode('ascii') for arg in environ['QUERY_STRING'].split('&')]
    start_response(status, headers )
    return body
