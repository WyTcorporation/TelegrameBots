from datetime import datetime, timedelta, date, time


class Request:
    def __init__(self, connectionDb):
        self.connectionDb = connectionDb

    async def dbAddUser(self, telegramId, firstname, lastname, phone, telegramNickname):
        query = f"INSERT INTO users (telegram_id, firstname, lastname, phone, telegram_nickname) VALUES" \
                f" ({telegramId}, '{firstname}','{lastname}','{phone}','{telegramNickname}')" \
                f" ON CONFLICT (telegram_id) DO UPDATE SET telegram_nickname='{telegramNickname}', firstname='{firstname}'," \
                f" lastname='{lastname}'"

        await self.connectionDb.execute(query)

    async def dbGetAreas(self):
        query = f"SELECT id,title FROM areas WHERE show=true"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        return results

    async def dbGetCity(self, areas_id, city):
        query = f"SELECT id,title FROM cities WHERE show=true and areas_id='{areas_id}' and title ILIKE '%{city}%'"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        return results
