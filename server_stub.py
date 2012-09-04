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
import hashlib
import cgi
import json
import Hal
import putil

idtoken = "TokenTOKEN"
PIN = "p1"


def gen_idresponse(rfid):
    global idtoken
    print rfid
            #the magic
    if rfid == "r2":
        return None

    resp = { 'user' : "Linda nielsen", 'token' : idtoken}
    return json.dumps(resp)


def validate_order(data):
    """Checks if the signature is correct

    the encoding part is in Hal.py
    """

    #verify its a valid token
    #assert(data['token'] == get_token(data['name']))
    #pin = get_token(data['name']) BUT THIS IS NOT STORED IN HAL...
    msg = "{}{}{}{}".format(data['name'], data['total'],idtoken, PIN)
    print "MSG: ", msg
    digest = hashlib.sha512(msg).hexdigest()
    print digest
    return data['signature'] == digest

def validate_accountbalance(data):
    amount = float(data['total'])
    putil.trace("Amount to see is {}".format(amount))
    return amount < 42;

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
        # You now have a dictionary of the post data
        putil.trace(data)

        ret = {} #return value

        if not validate_order(data):
            putil.trace("status: HAL.DENY")
            ret['status'] = "{}".format(Hal.DENY)
        elif not validate_accountbalance(data):
            putil.trace("nofounds")
            putil.trace("status: HAL.NOFOUNDS")
            ret['status'] = "{}".format(Hal.NOFUNDS)
        else:
            putil.trace("status: HAL.ACCEPT")
            ret['status'] = Hal.ACCEPT

        self.send_response(200)
        self.send_header('Content-type',	'text/json')
        self.end_headers()
        self.wfile.write(json.dumps(ret));
        self.wfile.close()


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


