import json
import psycopg
from BookingBot.core.Settings import settings

def addRegions(regTitle):
    with psycopg.connect(f'host={settings.db.host} user={settings.db.user}'
                         f' password={settings.db.password} dbname={settings.db.db}'
                         f' port=5432 connect_timeout=10') as conn:
        title = regTitle.replace("'", "\\'").capitalize()
        query = f"INSERT INTO areas (title) VALUES ('{title}') ON CONFLICT (title) DO UPDATE SET title='{title}' RETURNING id"
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchone()[0]
            conn.commit()
            return results


def addCities(areas_id, title, category, koatuu_code, community):
    with psycopg.connect(f'host={settings.db.host} user={settings.db.user}'
                         f' password={settings.db.password} dbname={settings.db.db}'
                         f' port=5432 connect_timeout=10') as conn:
        title = title.replace("'", "`").capitalize()
        community = community.replace("'", "`").capitalize()
        category = category.replace("'", "`").capitalize()
        query = f"INSERT INTO cities (areas_id,title,category,koatuu_code,community) VALUES ('{areas_id}','{title}','{category}','{koatuu_code}','{community}')"
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()


def openFiles():
    f = open('../../CitiesAndVillages.json', 'r', encoding='utf-8')
    data = json.load(f)
    for item in data:
        region = item['region']
        areaId = addRegions(region)
        title = item['object_name']
        category = item['object_category']
        koatuu_code = item['object_code']
        community = item['community']
        addCities(areaId, title, category, koatuu_code, community)
        print(item)

    f.close()

    # tree = ET.parse('../../ua-cities.xml')
    # root = tree.getroot()
    # for child in root:
    #     areaId = addRegions(child.attrib['name'])
    #     # print(child.tag, child.attrib)
    #     for item in child:
    #         print(item.tag, item.attrib)
    #         name = item.attrib['name']
    #         lat = item.attrib['lat']
    #         lon = item.attrib['lon']
    #         addCities(areas_id,title,category,koatuu_code,community)

# openFiles()
# print(addRegions('test'))
