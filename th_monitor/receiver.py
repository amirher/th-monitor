"""
Thornleigh Farm Monitor
Receiver Module
author: hugh@blinkybeach.com
"""
from http.server import BaseHTTPRequestHandler
from th_monitor.delivery import Delivery


class Receiver(BaseHTTPRequestHandler):
    """
    Handle requests received by the monitoring server
    """
    def _respond(self, status_code: int):
        assert isinstance(status_code, int)
        self.send_response(status_code)
        self._set_headers(status_code)
        return

    def _set_headers(self, status_code: int):
        assert isinstance(status_code, int)
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_GET(self):
        self._respond(405)
        return

    def do_PUT(self):
        self._respond(405)
        return

    def do_DELETE(self):
        self._respond(405)
        return

    def do_PATCH(self):
        self._respond(405)
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        delivery = Delivery(data, self.server.database)
        self._respond(delivery.status_code)
        return
