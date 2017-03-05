import asyncio
import logging

from autobahn.asyncio.websocket import (
    WebSocketServerFactory,
    WebSocketServerProtocol,
)

LOGGER = logging.getLogger(__name__)


class DesktopManagerServerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = set()

    @property
    def count(self):
        return len(self.clients)

    def register(self, client):
        LOGGER.info('Add new client %s', client.peer)
        self.clients.add(client)
        LOGGER.debug('Connected client count: %s', self.count)

    def unregister(self, client):
        if client in self.clients:
            LOGGER.info('Remove client %s', client.peer)
            self.clients.remove(client)
        LOGGER.debug('Connected client count: %s', self.count)


class DesktopManagerServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        if self.http_headers.get('user') == 'om26er@gmail.com':
            self.factory.register(self)
        else:
            self.sendClose(code=4030, reason='no device.')

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)

    def connection_lost(self, exc):
        self.factory.unregister(self)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    factory = DesktopManagerServerFactory()
    factory.protocol = DesktopManagerServerProtocol
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
