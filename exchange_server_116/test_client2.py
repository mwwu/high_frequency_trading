#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import time
from OuchServer.ouch_messages import OuchClientMessages, OuchServerMessages
from random import randrange


class Trader(LineReceiver):
    def connectionMade(self):
        self.transport.write(b"00000000000000:B44xAMAZGOOG@33")
        print("sent to server: 00000000000000:B44xAMAZGOOG@33")

    def lineReceived(self, line):
        print("received from server:", line)

    def dataReceived(self, data):
        print("data received from server:", data.decode())

class TraderFactory(ClientFactory):
    protocol = Trader

    def __init__(self):
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

def main(reactor):
    factory = TraderFactory()
    reactor.connectTCP('localhost', 8000, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)
