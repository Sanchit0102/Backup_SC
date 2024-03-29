#(©) 𝚂𝙰𝙽𝙲𝙷𝙸𝚃 ♛⛧
from pyrogram import Client

from .config import Config
from .database import Database


class ScreenShotBot(Client):

    def __init__(self):
        super().__init__(
            name = screenshotbot,
            bot_token = Config.BOT_TOKEN,
            api_id = Config.API_ID,
            api_hash = Config.API_HASH,
            workers = 20,
            plugins = dict(
                root="sanchit"
            )
        )

        self.db = Database(Config.DATABASE_URL, Config.NAME)
        self.CURRENT_PROCESSES = {}
        self.CHAT_FLOOD = {}
        self.broadcast_ids = {}


    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"\n\nNew session started for {me.first_name}({me.username})")


    async def stop(self):
        await super().stop()
        print('Session stopped. Bye!!')
