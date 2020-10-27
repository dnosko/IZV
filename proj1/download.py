import os, requests, urllib, zipfile, csv
from bs4 import BeautifulSoup

class DataDownloader:

    cookies = {}
    headers = {}
    regions = {'PHA':0,'STC':1,'JHC':2,'PLK':3,'KVK':19,'ULK':4,'LBK':18,
               'HKK':5,'PAK':17,'OLK':14,'MSK':7,'JHM':6,'ZLK':15,'VYS':16}
    """ = ['Region','ID','Čas','Lokalita','Druh nehody','Druh zrážky','Druh prekážky',
               'Charakter','Zavinenie','Alkohol','Príčina','Následky','Celková škoda',
               'Druh povrchu vozovky','Stav povrchu vozovky','Stav komunikácie',
               'Poveternostné podmienky','Viditelnosť','Rozhledove pomery','Delenie komunikacie',
               'Situovanie nehody na komunikacii','Riadenie premavky','Prednost v jazde',
               'Miesta a objekty','Smerove pomery',]
    pedestrians = ['Kategoria chodca','Stav chodca','Chovanie chodca','Situacia']"""
    #urobit nech to sparsuje zo suboru
    columns = ['p1','p36','p37','p2a','weekday(p2a)','p2b','p6','p7','p8','p9',	'p10',
              'p11','p12','p13a','p13b','p13c','p14','p15',	'p16','p17','p18','p19',
              'p20','p21','p22','p23','p24','p27','p28','p34','p35','p39','p44',
              'p45a','p47','p48a','p49','p50a','p50b','p51','p52','p53','p55a',
              'p57','p58','a','b','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s','t','p5a']

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

        for zfile in os.listdir(self.folder):
            self.process_file(zfile,region_f)
            break


    def process_file(self,zfile,file_name):

        with zipfile.ZipFile(os.path.join(self.folder,zfile)) as zf:
            #TODO odstranit prazdne subory 7-13  ??
            with zf.open(file_name,'r') as csv_f:
                self.parse_file(csv_f)
    

    def parse_file(self,file):

            for line in file:
                line = line.decode("utf-8",'backslashreplace')
                splitted = line.split(";")
                splitted[-1] = splitted[-1].split("\r\n")[0]
                print(splitted)
                        
                break

    def get_list(self, regions = None):
        pass


if __name__ == "__main__":
    data = DataDownloader()
    data.parse_region_data('PHA')
    




    