import argparse
import os

import requests

with open("private_token.txt", 'r') as text_file:
    tok = text_file.readline()

COUNT_GROUPS = 20


def get_user_photoes(user_id: int) -> dict:
    photos = requests.get("https://api.vk.com/method/photos.getAll?",
                          params={
                              'access_token': tok,
                              'user_id': user_id,
                              'v': 5.131,
                              'owner_id': user_id
                          }).json()['response']
    return photos


def parse_user_photoes(photoes_dict: dict):
    photos_urls = []
    items = photoes_dict['items']
    user_id = items[0]['owner_id']
    for item in items:
        photos_urls.append(item['sizes'][0]['url'])

    save_photoes_by_user_name(photos_urls, user_id)


def get_user_name_by_id(user_id: int) -> str:
    user = requests.get("https://api.vk.com/method/users.get?",
                        params={
                            'access_token': tok,
                            'user_id': user_id,
                            'v': 5.131,
                            "user_ids": user_id
                        }).json()['response']
    return user[0]['first_name'] + ' ' + user[0]['last_name']


def get_int_id_by_string_id(user_str_id: str) -> int:
    return requests.get(
        "https://api.vk.com/method/users.get?",
        params={
            'access_token': tok,
            'user_id': user_str_id,
            'v': 5.131,
            'user_ids': user_str_id
        }
    ).json()['response'][0]['id']


def get_groups(user_id: int, count_groups: int):
    groups = requests.get("https://api.vk.com/method/groups.get?",
                          params={
                              'access_token': tok,
                              'user_id': user_id,
                              'v': 5.131,
                              "extended": 1,
                              "count": count_groups
                          }).json()['response']
    return groups


def get_friends(user_id: int):
    friends = requests.get("https://api.vk.com/method/friends.get?",
                           params={
                               'access_token': tok,
                               'user_id': user_id,
                               'v': 5.131,
                               "order": "hints",
                               "fields": ["nickname",
                                          "online"]
                           }).json()['response']

    return friends


def get_photo_albums(user_id: int):
    all_albums = requests.get("https://api.vk.com/method/photos.getAlbums?",
                              params={
                                  'access_token': tok,
                                  'user_id': user_id,
                                  'v': 5.131,
                                  "owner_id": str(user_id)
                              }).json()['response']
    return all_albums


def parse_friends(friends: dict):
    print("Общее количество друзей: " + str(friends['count']))
    items = friends['items']
    for item in items:
        line = "Online" if item['online'] == 1 else "Offline"
        print(item['first_name'] + " " +
              item['last_name'] + " " +
              line)


def parse_groups(groups: dict):
    print("Группы, в которых состоит человек:")
    items = groups['items']
    for group in items:
        print(group['name'])


def parse_photo_albums(albums: dict):
    print("Альбомы пользователя(название и описания)")
    count_albums = albums['count']
    print(f'У пользователя на данный момент {count_albums} альбомов:')
    for album in albums['items']:
        print('Название альбома ' + album['title'])
        print('Описание альбома ' + album['description'])
        print('___________________________________________')


def save_photoes_by_user_name(photoes_urls: list, user_id: int):
    directory = f"Photos_{get_user_name_by_id(user_id)}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    count = 0
    for url in photoes_urls:
        count += 1
        img_data = requests.get(url).content
        file_name = f'picture{count}'
        with open(f'{directory}/{file_name}.jpg', 'wb') as handler:
            handler.write(img_data)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', type=str, help='Type of request [f,g,a,p]'
                                               'f - friends,'
                                               'g - groups,'
                                               'a - albums,'
                                               'p - photos')
    parser.add_argument('nickname', type=str, help='User ID')
    args = parser.parse_args()
    if args.type == 'f':
        parse_friends(get_friends(get_int_id_by_string_id(args.nickname)))
    if args.type == 'g':
        parse_groups(get_groups(get_int_id_by_string_id(args.nickname), COUNT_GROUPS))
    if args.type == 'a':
        parse_photo_albums(get_photo_albums(get_int_id_by_string_id(args.nickname)))
    if args.type == 'p':
        parse_user_photoes(get_user_photoes(get_int_id_by_string_id(args.nickname)))


if __name__ == '__main__':
    parse_arguments()
