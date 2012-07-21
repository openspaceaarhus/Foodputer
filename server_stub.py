#! /usr/bin/env python
# This file is part of FoodPuter.

#     Foobar is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

#this could be used to mock connections to hal...


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import json

idtoken = "TokenTOKEN"

def gen_idresponse(rfid):
    global idtoken
    print rfid
            #the magic
    if rfid == "r2":
        return None

    resp = { 'user' : "Linda nielsen", 'token' : idtoken}
    return json.dumps(resp)



class HalMock(BaseHTTPRequestHandler):
    def do_GET(self):
        rfid = self.path[1:] #remove first /
        
        resp = gen_idresponse(rfid)
            #the magic
        if not resp:
            self.send_error(404,'User not Found: %s' % rfid)
        else:
            self.send_response(200)
            self.send_header('Content-type',	'text/json')
            self.end_headers()
            self.wfile.write(resp)


    def do_POST(self):
        print "got a POST request"

        length = int(self.headers.getheader('content-length'))        
        indata = self.rfile.read(length)
        data = json.loads(indata)
        print data
        # You now have a dictionary of the post data

        self.send_response(200)
        self.send_header('Content-type',	'text/json')
        self.end_headers()
            
        self.wfile.write(json.dumps({'orderstatus': "Accept"}));
        return

def main():
    try:
        server = HTTPServer(('localhost', 8080), HalMock)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()


