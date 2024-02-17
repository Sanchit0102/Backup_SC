import datetime

import motor.motor_asyncio


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users


    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            as_file=False,
            watermark_text='',
            sample_duration=30,
            as_round=False,
            watermark_color=0,
            screenshot_mode=0,
            font_size=1,
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )


    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)


    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False


    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count


    async def is_as_file(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('as_file', False)


    async def is_as_round(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('as_round', False)


    async def update_as_file(self, id, as_file):
        await self.col.update_one({'id': id}, {'$set': {'as_file': as_file}})


    async def update_as_round(self, id, as_round):
        await self.col.update_one({'id': id}, {'$set': {'as_round': as_round}})


    async def update_watermark_text(self, id, watermark_text=''):
        await self.col.update_one({'id': id}, {'$set': {'watermark_text': watermark_text}})


    async def update_sample_duration(self, id, sample_duration):
        await self.col.update_one({'id': id}, {'$set': {'sample_duration': sample_duration}})


    async def update_watermark_color(self, id, watermark_color):
        await self.col.update_one({'id': id}, {'$set': {'watermark_color': watermark_color}})


    async def update_screenshot_mode(self, id, screenshot_mode):
        await self.col.update_one({'id': id}, {'$set': {'screenshot_mode': screenshot_mode}})


    async def update_font_size(self, id, font_size):
        await self.col.update_one({'id': id}, {'$set': {'font_size': font_size}})


    async def update_watermark_position(self, id, pos):
        await self.col.update_one({'id': id}, {'$set': {'watermark_position': pos}})


    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})


    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})


    async def get_watermark_text(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('watermark_text', '')


    async def get_sample_duration(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('sample_duration', 30)


    async def get_watermark_color(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('watermark_color', 0)


    async def get_watermark_position(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('watermark_position', 6)


    async def get_screenshot_mode(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('screenshot_mode', 0)


    async def get_font_size(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('font_size', 1)


    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        return user.get('ban_status', default)


    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users


    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users


    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})