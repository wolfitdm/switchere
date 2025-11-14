from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

import threading 

class thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID, port=8008): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
        self.server_class=HTTPServer
        self.handler_class=Server
        self.port=port
        
    # helper function to execute the threads
    def run(self): 
        print(str(self.thread_name) +" "+ str(self.thread_ID)); 
        server_address = ('', self.port)
        httpd = self.server_class(server_address, self.handler_class)
    
        print('Starting httpd on port %d...' % port)
        httpd.serve_forever()
        print(str(self.thread_name) +" "+ str(self.thread_ID));

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Content-Security-Policy", "default-src 'self'; connect-src 'self'")
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        data = ''
        with open('data.json', 'r') as file:
             data = json.load(file)
        self.wfile.write(json.dumps(data).encode())
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))

import argparse
from datetime import datetime
import difflib
from functools import partial
import logging
import os.path
import requests
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('email', type=str.lower, default="swtest@byom.de", help='please use byom.de enail addresses, default: swtest@byom.de')
parser.add_argument('--port', default=8008, type=int, help='port in order to save the auth code for the json server see http://localhost:port default: http://localhost:8008')
parser.add_argument('--contains', nargs='+', help='Triggers if a poll contains any of the provided values')
parser.add_argument('--interval', default=60, type=int, help='Polling interval in seconds')
parser.add_argument('--save', action='store_true', help='Save new text from polls when triggered')
print(len(sys.argv))
if len(sys.argv) == 1:
   sys.argv.append("swtest@byom.de")

# Add custom functions here to trigger on new content from a poll.
# Functions should accept two arguments `old, current` where
# `old` is the text from the previous poll and `current` is the text
# from the current poll. A true return value will cause a trigger.
checks = []

# Add custom functions here to react on a trigger from a poll.
# Functions should accept two arguments `old, current` where
# `old` is the text from the previous poll and `current` is the text
# from the current poll.
callbacks = []


headers_template = {
    'authority': 'api.byom.de',
    'method': 'GET',
    'path': '/mails/werrireloaded@byom.de?alt=json-in-script&callback=angular.callbacks._a',
    'scheme': 'https',
    'upgrade-insecure-requests': '1',    
    'Host': 'api.byom.de',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.byom.de/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

def get_new_text(old, new):
    diff = difflib.ndiff(old.splitlines(keepends=True), new.splitlines(keepends=True))
    return ''.join(line[2:] for line in diff if line.startswith('+ '))


def check_contains(old, new, *, strings):
    new = get_new_text(old, new)
    #print(new)
    return any(x in new for x in strings)


def save_new_text(old, new):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    f_name = f'{os.path.splitext(__file__)[0]}_{now}.txt'
    with open(f_name, 'w') as fh:
        fh.write(get_new_text(old, new))
    logging.info('saving new text to %s', f_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    import sys
    port=8008
    if args.port:
       port=int(args.port)
    else:
       port=8008
    
    thread1 = thread("GFG", 1000, port)
    thread1.start() 

    if args.contains:
       checks.insert(0, partial(check_contains, strings=args.contains))
       logging.info('Adding contains check: %s', args.contains)
    if args.save:
       callbacks.insert(0, save_new_text)

    old = ''
    while True:
        logging.info('checking mails')
        try:
            r = requests.post('https://www.byom.de/nachrichten/privatdetekteien',
                              data={'main-search': args.email})
        except:
            continue
        #print(r.text)
        new_headers={}
        new_cookies={}
        #print(r.cookies)
        for key, value in r.headers.items():
            new_headers[key] = value
        headers = headers_template.copy()
        for key, value in headers.items():
            new_headers[key] = value
        headers = new_headers
        for key, value in r.cookies.items():
            new_cookies[key] = value
        #print(new_cookies)
        if not "__cfduid" in new_cookies.keys():
           new_cookies["__cfduid"] = "xyz"
        headers.update(Cookie=f'__cfduid={new_cookies["__cfduid"]}')
        url="https://api.byom.de/mails/"+args.email+"?alt=json-in-script&callback=angular.callbacks._a"
        print(url)
        #print(headers)
        #print(new_cookies)
        r = requests.get(url, headers=headers, cookies=new_cookies)
        r.raise_for_status()
        import json
        try:
            rtext=r.text[21:-1]
            print(rtext)
            rjson=json.loads(rtext)
            rjsonr=rjson[0]
        except:
            continue
        import html        
        for key,value in rjsonr.items():
            okey=key
            ovalue=value
            tkey=key
            tvalue=value
            try:
                value=html.unescape(str(value))
            except:
                value=str(tvalue)
            value=str(value).replace('\\n','\n')
            value=str(value).replace('\\t','\t')
            try:
                key=html.unescape(str(key))
            except:
                key=str(tkey)
            key=str(key).replace('\\n','\n')
            key=str(key).replace('\\t','\t')
            rjsonr[key]=value
            rjsonr[okey]=value

        pattern = r"[\[<]([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})[\]>]"
        import re
        from_matches = re.findall(pattern, rjsonr["from"])
        to_matches = re.findall(pattern, rjsonr["to"])
        if len(from_matches) > 0:
           print(from_matches[-1])
           rjsonr["from"]=from_matches[-1]
        if len(to_matches) > 0:
           print(to_matches[-1])
           rjsonr["to"]=to_matches[-1]
        stra='>(\d{6})'
        auth_code_matches=re.findall(stra, rtext)
        auth_codes={"auth_code": 0}
        if len(auth_code_matches)  > 0:
           for auth_code in auth_code_matches:
               auth_code=auth_code[-6:60]
               print("auth_code")
               print(auth_code)
               auth_codes["auth_code"]=auth_code
               json_str = json.dumps(auth_codes, indent=4)
               with open("data.json", "w") as f:
                    f.write(json_str)
               #print(rjsonr["text"])
               import pyperclip
               pyperclip.copy(auth_code)
        #print(rjsonr)
        import html        
        rtext=html.unescape(r.text)
        rtext=rtext.replace('\\n','\n')
        rtext=rtext.replace('\\t','\t')
        import json
        #for line in rtext.splitlines():
        #    print(line)
        #        time.sleep(3)
        logging.debug('poll text length: %d', len(rtext))
        #print(rtext)
        if any(func(old, rtext) for func in checks):
            logging.info('new trigger')
            for func in callbacks:
                func(old, rtext)
        old = rtext
        time.sleep(args.interval)
         