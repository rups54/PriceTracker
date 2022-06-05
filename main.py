
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

url = 'https://www.amazon.co.uk/s?k=bin'

class Session(object):
    def __init__(self):
        self.url = url
        self.getdata(url)
        self.dealslist = []

    def getdata(self, url):
        try:
            r = s.get(self.url)
            r.html.render(sleep=1)
            soup = BeautifulSoup(r.html.html, 'html.parser')
        except:
            print('Something went wrong with loading the page' + e)
        self.getdeals(soup)

    def checkpage(self, soup):
        npf = soup.find('div', {'class': 'a-section a-text-center s-pagination-container'})
        if npf is None:
            print ('this is the only page')
            return
        else:
            print('there is more than one page')
            print('checking for the next page button')
            nextbut = soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
            if nextbut is not None:
                print('whoop next button is avail')
                self.findnexturl(nextbut, True)
            elif nextbut is None:
                print('next button isnt available')
            else:
                print('not sure how i got here')

    def findnexturl(self, nextbut, goto=False):
        urlpart = nextbut['href']
        print(urlpart)
        self.url = 'https://www.amazon.co.uk' + urlpart
        print(url)
        if goto:
            self.getdata(url)

    def getdeals(self, soup):
        print('getting deals')
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
            'title': title,
            'short_title': short_title,
            'saleprice': saleprice,
            'oldprice': oldprice,
            'reviews': reviews,
            'stars': stars
                    }
        self.dealslist.append(saleitem)
        print(dealslist)
        return


bot = Session()

# t = getdata(url)
# data = getdeals(t)
# df = pd.DataFrame(data)
# df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
# df = df.sort_values(by=['percentoff'], ascending=False)
# print(df.to_string())
#
# q = nextpage(t)


