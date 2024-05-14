from datetime import datetime, timedelta, date, time


class Request:
    def __init__(self, connectionDb):
        self.connectionDb = connectionDb

    async def dbAddUser(self, telegramId, firstname, lastname, phone, telegramNickname):
        query = f"INSERT INTO users (telegram_id, firstname, lastname, phone, telegram_nickname) VALUES" \
                f" ({telegramId}, '{firstname}','{lastname}','{phone}','{telegramNickname}')" \
                f" ON DUPLICATE KEY UPDATE telegram_nickname='{telegramNickname}', firstname='{firstname}'," \
                f" lastname='{lastname}'"

        self.connectionDb.execute(query)

