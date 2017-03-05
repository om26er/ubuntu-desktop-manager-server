import asyncio
import logging
import os

from autobahn.asyncio.websocket import (
    WebSocketServerFactory,
    WebSocketServerProtocol,
)
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ubuntu_desktop_manager_server.settings')
django.setup()

from ubuntu_desktop_manager_app.models import Device, User

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
        user_email = self.http_headers.get('user_identifier', None)
        device_id = self.http_headers.get('device_id', None)
        if not user_email or not device_id:
            self.sendClose(code=4030, reason='Invalid header.')
            return
        try:
            user = User.objects.get(email=user_email)
            devices = Device.objects.filter(user=user, device_id=device_id)
            if devices:
                self.factory.register(self)
            else:
                self.sendClose(code=4040, reason='Device not found.')
        except User.DoesNotExist:
            self.sendClose(code=4040, reason='User does not exist.')

    def onMessage(self, payload, isBinary):
        print(self.http_request_data)
        print(payload)

    def connection_lost(self, exc):
        self.factory.unregister(self)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    factory = DesktopManagerServerFactory()
    factory.protocol = DesktopManagerServerProtocol
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
