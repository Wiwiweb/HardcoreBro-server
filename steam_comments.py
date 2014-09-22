from bs4 import BeautifulSoup
import pymysql
import requests

import config

STEAM_PAGE = "http://steamcommunity.com/groups/vohcb"


def get_steam_comments():
    req = requests.get(STEAM_PAGE)
    print(req.text)


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
    update_database(comments)
