import time
from selenium import webdriver
from bs4 import BeautifulSoup
import uuid

driver = webdriver.Chrome()

CLASSES = {
    "author": "._2tbHP6ZydRpjI44J3syuqC",
    "post_date": "._3jOxDPIQ0KaOWpzvSQo-1s",
    "number_of_comments": ".FHCV02u6Cp2zYL0fhQPsO",
    "number_of_votes": "._1rZYMD_4xY3gRcSS3p8ODO",
    "post_url": "_1UoeAeSRhOKSNdY_h3iS1O",
    "post_category": "_3ryJoIoycVkA88fy40qNJc",
    "user_karma": "#profile--id-card--highlight-tooltip--karma",
    "user_comment_karma": ".comment-karma",
    "post_karma": ".karma",
    "user_cake_day": "#profile--id-card--highlight-tooltip--cakeday",
}

def get_post_field (post, field):
    node = post.select(field)
    if node:
        return node[0].getText()

def get_post_url (post):
    urls = post.select(f'a.{CLASSES["post_url"]}')
    if len(urls):
        return f"https://www.reddit.com{urls[0].get('href').split('/')[-2]}"
    else:
        return '' 

def get_post_category(post):
    links = post.select(f'a.{CLASSES["post_category"]}')
    if len(links):
        return post.select(f'a.{CLASSES["post_category"]}')[0].get('href').split('/')[-2]
    else:
        return ''

def fill_post_data (post):
    post_data = {}
    post_data["id"] = uuid.uuid1().hex

    post_data["post_date"] = get_post_field(post, CLASSES["post_date"])
    post_data["post_url"] = get_post_url(post)
    post_data["number_of_comments"] = get_post_field(post, CLASSES["number_of_comments"])
    post_data["number_of_votes"] = get_post_field(post, CLASSES["number_of_votes"])
    post_data["post_category"] = get_post_category(post)
    post_data["author"] = get_post_field(post, CLASSES["author"])
    return post_data



def main ():
    driver.get('https://www.reddit.com/top/?t=month')
    time.sleep(5)
    requiredHtml = driver.page_source
    soup = BeautifulSoup(requiredHtml, 'html5lib')
    posts = soup.find_all("div", class_="Post")
    for post in posts:
        # post URL;username;user karma;user cake day;post karma;comment karma;post date;number of comments;number of votes;post category
        post_data = fill_post_data(post)
    driver.quit()

main()