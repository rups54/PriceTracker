
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse

# #Comment out these 3 lines and change the searchterm variable, if you do not wish to use argparse version
# my_parser = argparse.ArgumentParser(description='Return BF Amazon Deals')
# my_parser.add_argument('searchterm', metavar='searchterm', type=str, help='The item to be searched for. Use + for spaces')
# args = my_parser.parse_args()
#
# searchterm = args.searchterm
#
# pd.set_option('display.max_columns', None)
s = HTMLSession()
dealslist = []
#
#
url = 'https://www.amazon.co.uk/s?k=bin&i=black-friday'
#
def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getdeals(soup):
     products = soup.find_all('div', {'data-component-type': 's-search-result'})
     print(len(products))
     for item in products:
      title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
      short_title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:30]
      try:
       saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('£','').replace(',','').strip())
       oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('£','').replace(',','').strip())
      except:
       oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('£','').replace(',','').strip())
      try:
       reviews = item.find('span', {'class': 'a-size-base s-underline-text'}).text.strip()
      except:
       reviews = 0
      try:
       stars = item.find('a', {'class': 'a-popover-trigger a-declarative'}).text.strip()
      except:
       stars = 'No ratings'

      saleitem = {
      # 'title': title,
      'short_title': short_title,
      'saleprice': saleprice,
      'oldprice': oldprice,
      'reviews': reviews,
      'stars': stars
      }
      dealslist.append(saleitem)

     print(dealslist)

     return dealslist

def nextpage(soup):
    print('hello im here')
    pages = soup.find('div', {'class': 'a-section a-text-center s-pagination-container'})

    while not pages.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled '}):
        print('next page available')
        url = 'https://www.amazon.co.uk'+ str(pages.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        print(url)
        getdata(url)
        pages = soup.find('div', {'class': 'a-section a-text-center s-pagination-container'})
        print('looping')

    return

t = getdata(url)
data = getdeals(t)
df = pd.DataFrame(data)
df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
df = df.sort_values(by=['percentoff'], ascending=False)
print(df.to_string())

q = nextpage(t)

# df.to_csv(searchterm + '-bfdeals.csv', index=False)
# print('Fin.')
# print('hello')

#     for item in products:
#         title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
#         short_title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()[:25]
#         link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']
#         try:
#             saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('£','').replace(',','').strip())
#             oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('£','').replace(',','').strip())
#         except:
#             oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('£','').replace(',','').strip())
#         try:
#             reviews = float(item.find('span', {'class': 'a-size-base'}).text.strip())
#         except:
#             reviews = 0
#
#         saleitem = {
#             'title': title,
#             'short_title': short_title,
#             'link': link,
#             'saleprice': saleprice,
#             'oldprice': oldprice,
#             'reviews': reviews
#             }
#         dealslist.append(saleitem)
#     return

