from bs4 import BeautifulSoup
import requests as re
import numpy as np

class get_data():

    def __init__(self,nse_code):
        self.nse_code = nse_code
        url = f"https://www.screener.in/company/{self.nse_code}/consolidated/"

        response = re.get(url=url)
        self.soup = BeautifulSoup(response.content,"html.parser")

        if self.soup.find_all('span',class_='number')[0].text == '':
            url = f"https://www.screener.in/company/{nse_code}/"
            response = re.get(url=url)
            self.soup = BeautifulSoup(response.content, "html.parser")

    def find_mar_cap(self):
        a = self.soup.find_all('span',class_='number')[0].text
        return int(a.replace(',',"")) 

    def find_current_PE(self):
        b = self.soup.find_all('span',class_='number')[4].text
        return float(b)       
    
    def find_sales_growth(self):
        year_10 = int(self.soup.find_all('table',class_='ranges-table')[0].find_all('td')[1].text.removesuffix('%'))
        year_5 = int(self.soup.find_all('table',class_='ranges-table')[0].find_all('td')[3].text.removesuffix('%'))
        year_3 = int(self.soup.find_all('table',class_='ranges-table')[0].find_all('td')[5].text.removesuffix('%'))
        TTM = int(self.soup.find_all('table',class_='ranges-table')[0].find_all('td')[7].text.removesuffix('%'))
       
        return [year_10,year_5,year_3,TTM]
    
    def find_profit_growth(self):
        year_10 = int(self.soup.find_all('table',class_='ranges-table')[1].find_all('td')[1].text.removesuffix('%'))
        year_5 = int(self.soup.find_all('table',class_='ranges-table')[1].find_all('td')[3].text.removesuffix('%'))
        year_3 = int(self.soup.find_all('table',class_='ranges-table')[1].find_all('td')[5].text.removesuffix('%'))
        TTM = int(self.soup.find_all('table',class_='ranges-table')[1].find_all('td')[7].text.removesuffix('%'))
        
        return [year_10,year_5,year_3,TTM]
    
    def find_median_roce(self):
        l = []
        for i in self.soup.find_all('div',class_='responsive-holder fill-card-width')[4].find_all('td')[-6:-1]:
            a = int((i.text).removesuffix('%'))
            l.append(a)
        return str(np.median(l))+"%"
    
    def find_netProfit_2023(self):
        c = self.soup.find("section",{"id":"profit-loss"}).find_all('tr',class_='strong')[2].find_all('td')[-2].text
        return int(c.replace(',',""))
    
    def FY23PE(self):
        Mar = self.find_mar_cap()
        profit = self.find_netProfit_2023()
        return round(Mar/profit,1)









