#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

class EchoClient(LineReceiver):
    def connectionMade(self):
        # ordertoken, buy/sell, stock, price range
        # sends message to server
        self.sendLine(b"00000000000000:B44xAMAZGOOG@33")

    def lineReceived(self, line):
        # prints to client
        print("receive:", line)

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
