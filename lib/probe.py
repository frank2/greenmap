#!/usr/bin/env python

from gevent import Greenlet, socket
from martinellis import Address, V4Address, V6Address

__all__ = ['Probe']

class Probe(Greenlet):
    PORT = None
    ADDRESS = None
    TIMEOUT = 5.0
    
    STATE_CLOSED = 0
    STATE_OPEN = 1
    STATE_FILTERED = 2
    
    def __init__(self, **kwargs):
        Greenlet.__init__(self)
        
        self.port = kwargs.setdefault('port', self.PORT)
        self.address = kwargs.setdefault('address', self.ADDRESS)
        self.timeout = kwargs.setdefault('timeout', self.TIMEOUT)

        if self.port is None:
            raise ValueError('no port given')

        if not isinstance(self.port, int):
            raise TypeError('port is not an int')

        if isinstance(self.address, str):
            try:
                self.address = Address.blind_assertion(self.address)
            except:
                self.address = Address.blind_assertion(socket.gethostbyname(self.address))

        if not isinstance(self.address, Address):
            raise ValueError('address must be an IP address or domain')

        if isinstance(self.timeout, int):
            self.timeout = float(self.timeout)

        if not isinstance(self.timeout, float):
            raise ValueError('timeout must be a float value')
        
        self.state = None

    @property
    def finished(self):
        return not self.state is None

    @property
    def closed(self):
        return self.state == self.STATE_CLOSED

    @property
    def open(self):
        return self.state == self.STATE_OPEN

    @property
    def filtered(self):
        return self.state == self.STATE_FILTERED

    def _run(self):
        if isinstance(self.address, V4Address):
            af = socket.AF_INET
        elif isinstance(self.address, V6Address):
            af = socket.AF_INET6
        else:
            raise ValueError('not an address object')

        sock = socket.socket(af, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            sock.connect((str(self.address), self.port))
            self.state = self.STATE_OPEN
        except ConnectionRefusedError:
            self.state = self.STATE_CLOSED
        except socket.timeout:
            self.state = self.STATE_FILTERED
        except OSError as e:
            if e.errno == 113: # No route to host
                self.state = self.STATE_FILTERED
            else:
                raise e
        finally:        
            sock.close()
