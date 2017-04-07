import os, logging
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from master.server_handler import ServerHandler
from xmlrpc.client import Binary


HOST = "0.0.0.0"
PORT = os.getenv('PORT', 5555)
ENDPOINT = 'RPC2'

logging.basicConfig(level=logging.INFO)

class RequestHandler(SimpleXMLRPCRequestHandler):
    # rpc_paths = ('RPC2',)
    def log_message(self, format, *args):
        logging.debug(format)


def start():
    server = SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler,
        allow_none=True, use_builtin_types=True)
    server.register_instance(ServerHandler())
    logging.info("Server is listening on " + HOST + ":" + str(PORT) + "/" + ENDPOINT)
    server.serve_forever()
