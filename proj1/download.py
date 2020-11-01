import os, requests, urllib, zipfile, csv, pickle, gzip
import numpy as np
from bs4 import BeautifulSoup

class DataDownloader:

    cookies = {}
    headers = {}
    cache = {} 
    regions = {'PHA':'00','STC':'01','JHC':'02','PLK':'03','KVK':'19','ULK':'04','LBK':'18',
               'HKK':'05','PAK':'17','OLK':'14','MSK':'07','JHM':'06','ZLK':'15','VYS':'16'}
    """ = ['Region','ID','Čas','Lokalita','Druh nehody','Druh zrážky','Druh prekážky',
               'Charakter','Zavinenie','Alkohol','Príčina','Následky','Celková škoda',
               'Druh povrchu vozovky','Stav povrchu vozovky','Stav komunikácie',
               'Poveternostné podmienky','Viditelnosť','Rozhledove pomery','Delenie komunikacie',
               'Situovanie nehody na komunikacii','Riadenie premavky','Prednost v jazde',
               'Miesta a objekty','Smerove pomery',]
    pedestrians = ['Kategoria chodca','Stav chodca','Chovanie chodca','Situacia']"""

    columns = ('p1','p36','p37','p2a','weekday(p2a)','p2b','p6','p7','p8','p9',	'p10',
              'p11','p12','p13a','p13b','p13c','p14','p15',	'p16','p17','p18','p19',
              'p20','p21','p22','p23','p24','p27','p28','p34','p35','p39','p44',
              'p45a','p47','p48a','p49','p50a','p50b','p51','p52','p53','p55a',
              'p57','p58','a','b','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s','t','p5a')
    

    def __init__(self,url="https://ehw.fit.vutbr.cz/izv/",folder="data",cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = folder+'/'+cache_filename
        self.create_folder(self.folder)
        self.set_connection()


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
            if data not in os.listdir(self.folder):
                print("DEBUG DOWNLOAD")
                open(link['href'],'wb').write(data.content)
 
    #TODO
    def get_years(self,soup):
        """ Function returns list of years on website """
        years = []
        tr = soup.find_all('tr')[0::12] #every 12th row has year
        for i in tr:
            td = i.find_all('td')
            years.append(td[0].getText())
            
        return years
    
    #TODO
    def get_last_month(self,year,soup):
        """ returns last month zip """
        td = soup.find_all('td')
        for i in td:
            #if i.find(text=("Prosinec {}")):
            pass
        

    def parse_region_data(self,region):
        """ Function processes data for given region. Returns (list, np.array), where
            list contains names of columns and np.array data """

        if not os.listdir(self.folder):
            self.download_data()
        

        region_f = str(self.regions[region])+'.csv'
        data = self.process_folder(region_f)
        
        columns = list(self.columns)
        columns.insert(0,"region")
        region_arr = np.repeat(region,len(data[1]))
        data = np.insert(data,0,region_arr,0) #insert name of region

        return (columns,data) 


    def process_folder(self,file_name):

        data = {}

        for zfile in os.listdir(self.folder):
            #TODO zobrat iba posledny subor z kazdeho roku
            try:
                with zipfile.ZipFile(os.path.join(self.folder,zfile)) as zf:
                    with zf.open(file_name,'r') as csv_f:
                        for line in csv_f:
                            clean_line = list(self.parse_line(line))

                            #add to dictionary if it's not already there
                            if clean_line[0] not in data:
                                data.update({clean_line[0] : clean_line})
                            break #DEBUG

            except zipfile.BadZipFile:
                continue       
                            
        
        # make array out of dict
        arr = np.array(list([item for item in data.values()]))
        
        #create empty arr
        new  = self.reshape_arr(arr,len(self.columns),len(arr))
        
        
        return np.array(new)


    def reshape_arr(self,arr,x, y):
        """ reshapes numpy array to list of desired shape"""

        new = []
        for col in range(x):
            a = arr[:,col]
            new.append(list(a))
        
        return new


    def parse_line(self,line):
        """ Processing of the given line """

        line = line.decode("utf-8",'backslashreplace')
        splitted = line.split(";")
        splitted[-1] = splitted[-1].split("\r\n")[0]

        # Create a dictionary from list
        zipbObj = zip(self.columns, splitted)
        line_dic = dict(zipbObj)
        line_dic = self.cleanup(line_dic)

        return line_dic.values()


    def cleanup(self, line):
        """ Cleans up data values at given line """

        line = self.replace_quotes(line)

        #line = self.clean_date(line)
        line['p2b'] = self.clean_time(line['p2b'])
        line['p47'] = self.clean_XX(line['p47'])
        line = self.change_to_float(['d','e','f','g'],line)

        return line


    def replace_quotes(self,line):
        """ Replaces double quotes from all values with them """
        
        for k,v in line.items():
            line[k] = v.replace("\"",'')
        
        return line
        

    def clean_time(self,col):
        """ Cleans column with time, when hour is unknown set value to empty,
            if only minutes are unknown set them to -1. 
            Sets to HH:MM format """

        hour = col[:2]
        min = col[2:]

        if int(hour) == 25:
            return '-1'
        if int(min) == 60:
            min = '-1'

        return hour + min


    def clean_XX(self,col):
        """ Replaces XX with """
        
        if col == "XX":
            col = col.replace("XX","")
        
        return col
    
    
    def change_to_float(self,cols,line):
        """ Changes values in all cols [list] to float type. If value is text, change to None"""

        for i in cols:
            a = line[i]
            if a == '':
                continue
            try:
                line[i] = float(a.replace(",","."))
            except ValueError:
                line[i] = None #sometimes theres string in data ????

        return line
    
    
    def clean_date(self,line):
        """ Makes one int in YYYYMMDD format """
        line['p2a'] = int(line['p2a'].replace("-",''))
        
        return line


    def get_list(self, regions = None):
        """ If param regions = None, print all regions except PHK"""

        process_regs = []
        data_lst = []
        linked = np.zeros(shape=(2,2))

        if not regions: 
            process_regs = list(self.regions.keys())[1:] #all regions except prague
        else:
            process_regs = regions

        for reg in process_regs:
            if reg in self.cache:
                region_data =  self.cache[reg]
            elif os.path.exists(self.cache_filename.format(reg)):
                region_data = self.unpickle_file(reg)
                self.cache.update({reg : region_data})
            else:
                region_data = self.parse_region_data(reg)
                self.cache.update({reg : region_data}) # save to class attribute
                self.pickle_file(reg,region_data) #pickle file

            
            #concat arrays
            if np.count_nonzero(linked) == 0:
                linked = region_data[1].flatten()
                linked = np.reshape(linked,(65,-1))          
            else:
                linked = np.concatenate((linked,region_data[1]),axis=1)
            

            
        return (region_data[0],list(linked))

    
    def pickle_file(self,region, tuple_val):
        """ Pickles and gzips tuple_val into file named data_{region}.pkl.gz"""
        #TODO uklada do zlej zlozky!!!!!
        f = self.cache_filename.format(region)
        
        #with open(self.folder+'/data'+region+'.pkl','wb') as pickle_f:
        gfile = gzip.GzipFile(f, 'wb')
        gfile.write(pickle.dumps(tuple_val, 0))
        gfile.close()

            

    def unpickle_file(self,region):
        """ Function ungzips and unpickles file and returns  data from the pickle file"""

        f = self.cache_filename.format(region)
        gfile = gzip.GzipFile(f, 'rb')
        dataa =  gfile.read()
        data = pickle.loads(dataa)
        gfile.close()

        return data


if __name__ == "__main__":
    data = DataDownloader()
    #ret = data.get_list(['PHA','KVK','MSK']) #,'KVK','MSK'
    #print('Stĺpce:',ret[0])
    #print('Počet záznamov:',len(ret[1][0]))
    #print('Kraje:',set(ret[1][0]))



    