import requests


def getRegions():
    API_URL = 'https://decentralization.gov.ua/graphql?query={areas{title,id,square,population,local_community_count,percent_communities_from_area,sum_communities_square}}'
    r = requests.post(API_URL)
    result = r.json()
    for item in result['data']['areas']:
        regId = item["id"]
        regTitle = item["title"]
        print(f'{regId} - {regTitle} - {item}')


getRegions()
