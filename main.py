
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from tabulate import tabulate


# #Comment out these 3 lines and change the searchterm variable, if you do not wish to use argparse version
# my_parser = argparse.ArgumentParser(description='Return BF Amazon Deals')
# my_parser.add_argument('searchterm', metavar='searchterm', type=str, help='The item to be searched for. Use + for spaces')
# args = my_parser.parse_args()
#
# searchterm = args.searchterm
#
# pd.set_option('display.max_columns', None)
s = HTMLSession()
dealslist =[]

#url = 'https://www.amazon.co.uk/s?k=bin&i=black-friday'
url = 'https://www.amazon.co.uk/s?k=racing+simulator&crid=1WTSID86FSEHB&sprefix=racing+simulator%2Caps%2C128&ref=nb_sb_noss_2'

class Session(object):
    def __init__(self):
        self.url = url
        self.getdata(url)
        self.dealslist = []
        self.soup = ''

    def getdata(self, url):
        try:
            r = s.get(self.url)
            r.html.render(sleep=1)
            self.soup = BeautifulSoup(r.html.html, 'html.parser')
        except:
            print('Something went wrong with loading the page' + e)
        self.getdeals()

    def checkpage(self):
        npf = self.soup.find('div', {'class': 'a-section a-text-center s-pagination-container'})
        if npf is None:
            print ('this is the only page')
            return
        else:
            print('there is more than one page')
            print('checking for the next page button')
            nextbut = self.soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
            if nextbut is not None:
                print('whoop next button is avail')
                self.findnexturl(nextbut)
            elif nextbut is None:
                print('next button isnt available')
                print('going to sort out results')
                self.sortresults()
            else:
                print('not sure how i got here')

    def findnexturl(self, nextbut, goto=False):
        urlpart = nextbut['href']
        # print(urlpart)
        self.url = 'https://www.amazon.co.uk' + urlpart
        print(self.url)
        if goto:
            self.getdata(self.url)
        else:
            self.sortresults()

    def getdeals(self):
        print('getting deals')
        products = self.soup.find_all('div', {'data-component-type': 's-search-result'})
        print ('There are ' + str(len(products)) + 'on this page')
        nopricecount = 0
        pricecount = 0
        for item in products:
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
            short_title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:55]
            try:
                saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('£','').replace(',','').strip())
                pricecount +=1
            except:
                nopricecount += 1
                continue
            try:
                oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('£','').replace(',','').strip())
            except:
                oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('£','').replace(',','').strip())
            try:
                reviews = item.find('span', {'class': 'a-size-base s-underline-text'}).text.strip()
            except:
                continue
            try:
                stars = item.find('a', {'class': 'a-popover-trigger a-declarative'}).text.strip()
            except:
                continue
            saleitem = {
                #'title': title,
                'short_title': short_title,
                'saleprice': saleprice,
                'oldprice': oldprice,
                'reviews': reviews,
                'stars': stars
                        }
            dealslist.append(saleitem)
        print('Ive found, ' + str(pricecount) + ' ...there were also ' + str(nopricecount) + ' with no prices')
        print(len(dealslist))
        self.checkpage()
        return
    def sortresults(self):
        df = pd.DataFrame(dealslist)
        df = df.loc[df['stars'] != 'No rating']
        print(df.dtypes)
        df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
        df = df.sort_values(by=['percentoff'], ascending=False)
        print(tabulate(df, headers='keys'))



bot = Session()

# t = getdata(url)
# data = getdeals(t)
# df = pd.DataFrame(data)
# df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
# df = df.sort_values(by=['percentoff'], ascending=False)
# print(df.to_string())
#
# q = nextpage(t)


