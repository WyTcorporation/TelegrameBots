from datetime import datetime, timedelta, date, time


class Request:
    def __init__(self, connectionDb):
        self.connectionDb = connectionDb

    async def addUser(self, telegramId, firstname, lastname, phone, telegramNickname):
        query = f"INSERT INTO users (telegram_id, firstname, lastname, phone, telegram_nickname) VALUES" \
                f" ({telegramId}, '{firstname}','{lastname}','{phone}','{telegramNickname}')" \
                f" ON CONFLICT (telegram_id) DO UPDATE SET telegram_nickname='{telegramNickname}', firstname='{firstname}'," \
                f" lastname='{lastname}'"

        await self.connectionDb.execute(query)

    async def dbGetDate(self):
        dateNow = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
        query = f"SELECT DISTINCT b_date FROM booking WHERE b_status='free' " \
                f"AND b_datetime >'{dateNow}' ORDER BY b_date ASC LIMIT 3"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        datesList = [str(result[0].strftime('%d.%m.%Y')) for result in results]
        return datesList

    async def dbGetTime(self, dateNeeded):
        dateNow = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
        query = f"SELECT DISTINCT b_time FROM booking WHERE b_status='free' " \
                f"AND b_date = '{dateNeeded}' " \
                f"AND b_datetime >'{dateNow}' ORDER BY b_time ASC"
        rows = await self.connectionDb.execute(query)
        results = await rows.fetchall()
        timesList = [str(result[0].strftime('%H:%M:%S')) for result in results]
        return timesList

    async def dbChangeStatus(self, status, d, t):
        query = f"UPDATE booking SET b_status='{status}' WHERE b_date='{d}' AND b_time='{t}'"
        await self.connectionDb.execute(query)
