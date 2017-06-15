import sys
import requests
from bs4 import BeautifulSoup

url = 'https://eroshare.com/u/Eneswar'

def get_soup(url):
    r = requests.get(url, timeout=10)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
        r.raise_for_status()

    return soup

def get_albums_links(soup):
    album_links = []
    # none_album = soup.find(id='non-album-container')
    albums = soup.find_all('a',class_='item pull-left cycle')
    if albums:
        active_page = soup.find('li', class_='active')
        active_pageNum = active_page.text


        album_links.append('--- --- page {}: --- ---\n'\
            .format(active_pageNum))
        for _ in albums:
            album_links.append('https://eroshare.com'+ _.attrs['href']+'/')
    return album_links

def get_next_page(soup):
    next_page = None
    pagination = soup.find(class_='pagination')
    if pagination:
        next_page = pagination.find('a', attrs={'rel':'next'})

    if next_page:
        next_page = 'https://eroshare.com'+ next_page['href']

    return next_page

def main(url):
    # next_page = None
    all_album_links = []
    soup = get_soup(url)
    user_profile = soup.find(class_='user-profile')
    user = user_profile.find('a')['href'].strip('/u/')
    album_links = get_albums_links(soup)

    if album_links:
        next_page = get_next_page(soup)
        all_album_links.extend(album_links)
        while next_page:
            soup = get_soup(next_page)
            next_page = get_next_page(soup)
            album_links = get_albums_links(soup)
            all_album_links.extend(album_links)

        with open('{}_album_links.txt'.format(user), 'w')as f:
            for links in all_album_links:
        	   f.write(links+'\n')
    else:
        print 'Cannot find any links in {} page'.format(user)

if __name__ == '__main__':
    url = sys.argv[1:][0]
    main(url)



