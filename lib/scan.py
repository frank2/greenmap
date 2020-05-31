#!/usr/bin/env python

import random

from gevent import Greenlet, socket
from gevent.pool import Pool
from martinellis import Address

from greenmap.probe import Probe

__all__ = ['Scan']

class Scan(Greenlet):
    ADDRESS = None
    PORTS = None
    TIMEOUT = Probe.TIMEOUT
    RANDOMIZE = True
    CONCURRENCE = 20
    
    def __init__(self, **kwargs):
        Greenlet.__init__(self)
        
        self.address = kwargs.setdefault('address', self.ADDRESS)
        self.ports = kwargs.setdefault('ports', self.PORTS)
        self.concurrence = kwargs.setdefault('concurrence', self.CONCURRENCE)
        self.timeout = kwargs.setdefault('timeout', self.TIMEOUT)
        self.randomize = kwargs.setdefault('randomize', self.RANDOMIZE)
        
        if isinstance(self.address, str):
            try:
                self.address = Address.blind_assertion(self.address)
            except:
                self.address = Address.blind_assertion(socket.gethostbyname(self.address))

        if not isinstance(self.address, Address):
            raise ValueError('address must be an IP address')

        if not isinstance(self.ports, (list, tuple)):
            raise ValueError('ports must be a list of ports')

        if isinstance(self.timeout, int):
            self.timeout = float(self.timeout)

        if not isinstance(self.timeout, float):
            raise ValueError('timeout must be a float value')

        if not isinstance(self.concurrence, int):
            raise ValueError('concurrence must be an integer')

        if not isinstance(self.randomize, bool):
            raise ValueError('randomize must be a boolean value')

        self.results = None

    @property
    def finished(self):
        return not self.results is None

    @property
    def open_ports(self):
        if not self.finished:
            return list()

        return list(filter(lambda x: x.open, self.results))

    @property
    def closed_ports(self):
        if not self.finished:
            return list()

        return list(filter(lambda x: x.closed, self.results))

    @property
    def filtered_ports(self):
        if not self.finished:
            return list()

        return list(filter(lambda x: x.filtered, self.results))

    def _run(self):
        pool = Pool(self.concurrence)
        probes = list()
        self.results = None
        
        for p in self.ports:
            probe = Probe(address=self.address, port=p, timeout=self.timeout)
            probes.append(probe)

        if self.randomize:
            random.shuffle(probes)

        for p in probes:
            pool.start(p)

        pool.join()

        if self.randomize:
            probes.sort(key=lambda x: x.port)

        self.results = probes
