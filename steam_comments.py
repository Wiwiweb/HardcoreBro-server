import collections
import re
import time

from bs4 import BeautifulSoup
import pymysql
import requests

import config


STEAM_PAGE = 'http://steamcommunity.com/groups/vohcb'
EMOTICON_REGEX = r'<img class="emoticon" src="https?://.+\..{3}/economy/emoticon/(\w+)"/>'

SteamComment = collections.namedtuple('SteamComment', 'id author avatar text date')


def get_steam_comments():
    req = requests.get(STEAM_PAGE)
    soup = BeautifulSoup(req.text)
    all_comments = soup.find_all('div', class_='commentthread_comment')
    comment_list = []
    for comment in all_comments:
        comment_id = comment['id'].split('_')[1]
        author = comment.find('div', class_='commentthread_comment_author').a.string.strip()
        avatar = comment.find('div', class_='commentthread_comment_avatar').img['src']

        date = comment.find('span', class_='commentthread_comment_timestamp').string.strip()
        date = time.strptime(date, '%d %b @ %I:%M%p')

        text = comment.find('div', class_='commentthread_comment_text').renderContents()
        text = text.decode("utf-8").strip()
        text = re.sub(EMOTICON_REGEX, r':\1:', text)

        comment_list.append(SteamComment(comment_id, author, avatar, text, date))
    return comment_list


def update_database(steam_comments):
    conn = pymysql.connect(host=config.mysql_host, port=3306, user=config.mysql_user, passwd=config.mysql_pass,
                           db='hardcore_bro')

    cur = conn.cursor()

    cur.execute("SELECT * FROM steam_comments")

    print(cur.description)

    print()

    for row in cur:
        print(row)

    cur.close()
    conn.close()


if __name__ == '__main__':
    comments = get_steam_comments()
    for c in comments:
        print(c)
    # update_database(comments)
