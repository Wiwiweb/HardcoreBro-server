import calendar
import collections
import re
import time

from bs4 import BeautifulSoup
import datetime
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
        if '@' in date:
            date = time.strptime(date, '%d %b @ %I:%M%p')
        else:
            date = datetime.datetime.now()

        text = comment.find('div', class_='commentthread_comment_text').renderContents()
        text = text.decode("utf-8").strip()
        text = re.sub(EMOTICON_REGEX, r':\1:', text)

        comment_list.append(SteamComment(comment_id, author, avatar, text, date))
    return comment_list


def update_database(steam_comments):
    conn = pymysql.connect(host=config.mysql_host, port=3306, user=config.mysql_user, passwd=config.mysql_pass,
                           db='hardcore_bro')

    cur = conn.cursor()

    cur.execute("DELETE FROM steam_comments")
    for comment in steam_comments:
        print(comment)
        cur.execute("INSERT INTO steam_comments VALUES (%s,%s,%s,%s,%s)", comment)

    cur.close()
    conn.close()


if __name__ == '__main__':
    comments = get_steam_comments()
    update_database(comments)
