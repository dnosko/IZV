import os

class DataDownloader:


    def __init__(self,url="https://ehw.fit.vutbr.cz/izv/",folder="data",cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename
        self.create_folder(self.folder)


    def create_folder(self,folder):
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass


    def download_data(self):
        pass


    def parse_region_data(self,region):
        pass


    def get_list(self, regions = None):
        pass


if __name__ == "__main__":
    data = DataDownloader()
    





    