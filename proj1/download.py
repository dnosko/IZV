import os, requests, urllib, zipfile
from bs4 import BeautifulSoup

class DataDownloader:

    cookies = {}
    headers = {}
    regions = {'PHA':0,'STC':1,'JHC':2,'PLK':3,'KVK':19,'ULK':4,'LBK':18,
               'HKK':5,'PAK':17,'OLK':14,'MSK':7,'JHM':6,'ZLK':15,'VYS':16}

    def __init__(self,url="https://ehw.fit.vutbr.cz/izv/",folder="data",cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename
        self.create_folder(self.folder)
        self.set_connection()


    def create_folder(self,folder):
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass


    def download_data(self):

        s = requests.Session() 
        data = s.get(self.url, headers=self.headers, cookies=self.cookies).text
        soup = BeautifulSoup(data, features="lxml")
        
        for link in soup.find_all('a', href=lambda href: href.endswith('zip')):
            data = s.get(self.url+link['href'])
            open(link['href'],'wb').write(data.content)
            print("DEBUG DOWNLOAD")
 

    def set_connection(self):
        """ sets cookies and header for url request """

        self.cookies = {
            '_ranaCid': '1768967324.1556314328',
            '_ga': 'GA1.2.1173834230.1556314329',
            '_gcl_au': '1.1.30048206.1598966168',
        }

        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-US,en;q=0.9',
        }



    def parse_region_data(self,region):

        if not os.listdir(self.folder):
            self.download_data()
        
        region_f = '0'+ str(self.regions[region])+'.csv'

        for file in os.listdir(self.folder):
            with zipfile.ZipFile(os.path.join(self.folder,file)) as zf:
                with zf.open(region_f,'r') as f:
                    print(f)


    def get_list(self, regions = None):
        pass


if __name__ == "__main__":
    data = DataDownloader()
    data.parse_region_data('PHA')
    




    