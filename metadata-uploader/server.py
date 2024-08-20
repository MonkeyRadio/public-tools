from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import time
import metadataUploader
import argsparser
import requests

class WebServerHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/metadata':
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            post_data_str = post_data_bytes.decode("UTF-8")
            list_of_post_data = post_data_str.split('&')
            post_data_dict = {}
            for item in list_of_post_data:
                variable, value = item.split('=')
                post_data_dict[variable] = unquote(value)
            try:
              print('Metadata file has changed, sending metadata...')
              time.sleep(1)
              metadataUploader.send_metadata(args, post_data_dict)
            except (Exception, requests.HTTPError) as e:
              print(f'Error: {e}')


def main():
    try:
        port = args.port
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    args = argsparser.parser.parse_args()
    main()