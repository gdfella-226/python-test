import telethon
from telethon import TelegramClient
from qrcode import QRCode
from loguru import logger


API_ID = 23953960
API_HASH = 'ce481c40f2788959f46b438a36433cde'
VIRTUAL_CLIENT = None

class VirtualClient:
    def __init__(self, api_id: int, api_hash: str) -> None:
        self.qr = QRCode()
        self.is_login = False
        self.client = None
        self.start_client(api_id, api_hash)

    def start_client(self, api_id: int, api_hash: str) -> telethon.TelegramClient:
        self.is_login = True
        self.client = TelegramClient('NewSession', api_id, api_hash, device_model="Acer Nitro",
                                     app_version='5.1.0', system_version='Windows 11')
        self.client.start()
        return self.client

    def gen_qr(self, token: str) -> None:
        self.qr.clear()
        self.qr.add_data(token)
        self.qr.print_ascii()

    def display_url_as_qr(self, url: str) -> None:
        print(url)
        self.gen_qr(url)

    async def connect(self) -> None:
        if not self.client.is_connected():
            await self.client.connect()
        self.client.connect()
        qr_login = await self.client.qr_login()
        # print(self.client.is_connected())
        r = False
        while not r:
            self.display_url_as_qr(qr_login.url)
            # Important! You need to wait for the login to complete!
            try:
                r = await qr_login.wait(10)
            except:
                await qr_login.recreate()

    def send_message(self, username: str, message: str) -> None:
        if not self.is_login:
            self.connect()
        self.client.loop.run_until_complete(self.client.send_message(username, message))

    def get_messages(self, chat_id: str) -> list:
        if not self.is_login:
            self.connect()
        res = []
        for message in self.client.iter_messages(chat_id):
            try:
                datetime = '.'.join([str(message.date.day), str(message.date.month), str(message.date.year)]) + ' ' + \
                    ':'.join([str(message.date.hour), str(message.date.minute)])
                is_self = (message.peer_id.user_id == message.from_id.user_id)
                res.append({
                    'username': message.peer_id.user_id,
                    'is_self': is_self,
                    'message_text': message.message,
                    'created_at': datetime
                })
            except AttributeError as err:
                logger.error(err)
                continue
        return res


def main():
    cl = VirtualClient(API_ID, API_HASH)
    # cl.send_message('your_invention@vpe_mf', 'XUY')
    msg = cl.get_messages('@vpe_mf')
    for i in msg:
        print(i)


if __name__ == '__main__':
    main()
else:
    VIRTUAL_CLIENT = VirtualClient(API_ID, API_HASH)

