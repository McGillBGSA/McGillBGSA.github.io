'''
Quick script to fetch previous BGSA blog posts on Blogger to populate new Jekyll blog.
'''
import feedparser
from time import strftime
import string, re
import html2text

RSS_FEED = 'http://mcgillbgsa.blogspot.com/feeds/posts/default'
POST_ROOT = '_posts/'

def get_post_filename(title, date, ext='.md'): 
    # remove punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    title = regex.sub('', title)

    slug = '-'.join(title.lower().split())
    date_str = strftime("%Y-%m-%d-", date)

    post_name = ''.join([date_str, slug, ext])
    return post_name

def get_post_body(html):
    # not great, but will do for now
    body = html2text.html2text(html).encode('utf-8')
    body = body.replace('\n', '\n\n')
    return body

def get_post_date(date):
    date_str = strftime("%Y-%m-%d %H:%M:%S", date)
    return date_str


def get_post_categories(tags):
    '''
    No easy way to do this. Will skip for now.
    '''
    return [t['term'] for t in tags]

def write_post(entry, root=POST_ROOT):
    post = '''---
layout: post
title: "{title}"
date: {date}
categories: {categories}
archive: "{original}"
---

{content}
    '''.format(**entry)
    fn = root+entry['filename']
    with open(fn, 'w') as f:
        f.write(post)


def get_info(feed=RSS_FEED):
    '''
    Returns useful blog post information 
    '''
    d = feedparser.parse(feed)
    entries = []
    for e in d['entries']:
        date = e['updated_parsed']
        title = e['title']
        html_content = e['summary']
        info = {
            'title': title,
            'content': get_post_body(html_content),
            'filename': get_post_filename(title, date),
            'date': get_post_date(date),
            'categories': 'archive',
            'original': e['link']
        }
        entries.append(info)

    for e in entries:
        write_post(e)


if __name__ == '__main__':
    get_info()
