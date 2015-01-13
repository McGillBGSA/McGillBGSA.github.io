from bs4 import BeautifulSoup
import urllib

url = "http://mcgillbgsa.weebly.com/helpful-links.html"
page = urllib.urlopen(url).read()
soup = BeautifulSoup(page)

original = ''
with open('helpful_links.md', 'r') as f:
    original = f.read()

links = []

for link in soup.find_all('a'):
    text, href = (link.get_text(), link.get('href'))
    text = text.replace(u'\u2019', u"'")
    try:
        text = str(text)
        href = str(href)
        try:
            if text in original:
                md_link = '[%s](%s)' % (text, href)
                links.append(md_link)
                print '.'
        except:
            print 'error: ', text, href
            pass
    except: 
        print 'error: ascii encoding', text, href
        pass


with open('links.md', 'w') as f:
    f.write('\n'.join(links))