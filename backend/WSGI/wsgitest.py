import json
from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from WSGI.ORM.BL import BL


def application(environ, start_response):
    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])

    # As there can be more than one value for a variable then
    # a list is provided as a default value.
    page = d.get('p', [''])[0]  # Returns the first age value
    pageSize = d.get('ps', [''])[0]
    changeStart = d.get('changeStart', [''])[0]
    changeEnd = d.get('changeEnd', [''])[0]
    type = d.get('type', [''])[0]

    # Always escape user input to avoid script injection
    page = escape(page)
    pageSize = escape(pageSize)
    changeStart = escape(changeStart)
    changeEnd = escape(changeEnd)
    type = escape(type)

    if page is None or page == "":
        page = 1

    if pageSize is None or pageSize == "":
        pageSize = 10

    if changeStart is None or changeStart == "":
        changeStart = '1900-01-01'

    if changeEnd is None or changeEnd == "":
        changeEnd = '5000-01-01'

    if type is None or type == "":
        type = 0

    data = BL().getAllAssets(int(page), int(pageSize), changeStart, changeEnd)

    if (type == 1):
        dt = BL().getCanonicalTags().values()
        print(dt)
        for dd in data['data']:
            for d in dd.keys():
                if "openpipe_canonical_" in d:
                    for i in dd[d]:
                        if i in dt:
                            print(i)
                            dd[d] = [""]
                            break

    response_body = json.dumps(data, default=str)
    # response_body = data

    status = '200 OK'

    # Now content type is text/html
    response_headers = [
        ('Content-Type', 'text/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]


httpd = make_server('localhost', 8051, application)

# Now it is serve_forever() in instead of handle_request()
httpd.serve_forever()
