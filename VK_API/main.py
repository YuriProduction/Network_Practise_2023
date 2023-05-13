import vk_api

with open("private_token.txt", 'r') as text_file:
    tok = text_file.readline()

session = vk_api.VkApi(token=tok)
vk = session.get_api()

MY_ID = 332315239
COUNT_GROUPS = 20


def get_groups(user_id: int, count_groups: int):
    groups_ids = session.method("groups.get",
                                {"user_id": user_id,
                                 "extended": 1,
                                 "count": count_groups})
    return groups_ids


def get_friends(user_id: int):
    friends_ids = session.method("friends.get",
                                 {"user_id": user_id,
                                  "order": "hints",
                                  "fields": ["nickname",
                                             "online"]})
    return friends_ids


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


parse_friends(get_friends(MY_ID))
parse_groups(get_groups(MY_ID, COUNT_GROUPS))
