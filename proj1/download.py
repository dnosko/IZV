import os, requests, urllib, zipfile, csv,timeit
import numpy as np
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

    col_dic = ('p1','p36','p37','p2a','weekday(p2a)','p2b','p6','p7','p8','p9',	'p10',
              'p11','p12','p13a','p13b','p13c','p14','p15',	'p16','p17','p18','p19',
              'p20','p21','p22','p23','p24','p27','p28','p34','p35','p39','p44',
              'p45a','p47','p48a','p49','p50a','p50b','p51','p52','p53','p55a',
              'p57','p58','a','b','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s','t','p5a')
    


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
        

        self.columns.insert(0,region)

        region_f = '0'+ str(self.regions[region])+'.csv'
        data = self.process_folder(region_f)

        print(data)

    def process_folder(self,file_name):

        data = []
        for zfile in os.listdir(self.folder): 
            with zipfile.ZipFile(os.path.join(self.folder,zfile)) as zf:
                #TODO odstranit prazdne subory 7-13  ??
                with zf.open(file_name,'r') as csv_f:
                    for line in csv_f:
                        clean_line = self.parse_line(line)
                        data.append(clean_line)
                        break    

        #data = self.check_duplicates(data)
        print(len(data))

        return (self.columns,data)


    def check_duplicates(self, data):

        seen = set()
        data = [x for x in data if x[0] not in seen and not seen.add(x[0])]

        return data


    def parse_line(self,line):
        """ Processing of the given line """

        line = line.decode("utf-8",'backslashreplace')
        splitted = line.split(";")
        splitted[-1] = splitted[-1].split("\r\n")[0]

        # Create a dictionary from list
        zipbObj = zip(self.col_dic, splitted)
        line_dic = dict(zipbObj)
        print('#DEBUG#')
        print(line_dic)
        
        return self.cleanup(line_dic)


    def cleanup(self, line):
        """ Cleans up data values at given line """

        line = self.replace_quotes(line)

        line['p2b'] = self.clean_time(line['p2b'])
        line['p47'] = self.clean_XX(line['p47'])
        
        return line


    def replace_quotes(self,line):
        """ Replaces double quotes from all values with them """
        
        for k,v in line.items():
            line[k] = v.replace("\"",'')
        
        return line
        

    def clean_time(self,col):
        """ Cleans column with time, when hour is unknown set value to empty,
            if only minutes are unknown set them to XX. 
            Sets to HH:MM format """

        hour = col[:2]
        min = col[2:]

        if hour == 25:
            col = ''
        if min == 60:
            min = 'XX'

        return hour + ':' + min


    def clean_XX(self,col):
        """ Replaces XX with """
        
        if col == "XX":
            col = col.replace("XX","")
        
        return col


    def get_list(self, regions = None):
        pass


if __name__ == "__main__":
    data = DataDownloader()
    data.parse_region_data('PHA')




    