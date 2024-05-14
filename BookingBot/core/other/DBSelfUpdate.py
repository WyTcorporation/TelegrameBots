from datetime import datetime, timedelta, date, time

import psycopg
from psycopg import Connection

from BookingBot.core.Settings import settings


async def DBEntry():
    with psycopg.connect(f'host={settings.db.host} user={settings.db.user}'
                         f' password={settings.db.password} dbname={settings.db.db}'
                         f' port=5432 connect_timeout=10') as conn:

        if await getCountRow(conn) < 1:
            query = await getQuery(3, str(datetime.today().date()))  # Заполняем базу данных на 3 дня от сегодня
        else:
            query = await getQuery(1, str(datetime.today().date()))  # если база пуста заполняем на текущий день

        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()


async def getCountRow(conn: Connection):
    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM booking')
        count = cursor.fetchone()
    return count[0]


async def getQuery(countDays, targetDay):
    query = 'INSERT INTO booking (b_date, b_time, b_status, b_datetime) VALUES '

    target = datetime.strptime(targetDay, '%Y-%m-%d').date() + timedelta(days=1)

    for x in range(countDays):
        date_target = target + timedelta(days=x)
        if date_target.weekday() < 5:
            for i in range(0, 10 * 60, 60):
                time_delta = f'{(datetime.combine(date.today(), time(10, 0)) + timedelta(minutes=i)).time().strftime("%H:%M")}'
                full_date_time = f'{date_target} {time_delta}'
                line = f"\r\n('{date_target}', '{time_delta}', 'free', '{full_date_time}'),"
                query += line
    query = f'{query.rstrip(query[-1])}'  # убераем последний елемент ,
    # print(query)
    return query

#getQuery(5, str(datetime.today().date()))
