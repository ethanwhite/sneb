import os
import urllib
import sys
from zipfile import ZipFile

args = sys.argv[1:]

if ('bbs' in args) or ('all' in args):
    os.system("retriever install sqlite BBS --file ./data/bbs.sqlite --table_name {table}")
    print("Downloaded BBS data and installed it in bbs.sqlite")

if ('bioclim' in args) or ('all' in args):
    if not os.path.isfile('./data/bioclim_data_2pt5m.zip'):
        urllib.urlretrieve("http://biogeo.ucdavis.edu/data/climate/worldclim/1_4/grid/cur/bio_2-5m_bil.zip", "./data/bioclim_data_2pt5m.zip")
        with ZipFile('./data/bioclim_data_2pt5m.zip') as bioclimzip:
            bioclimzip.extractall(path='./data/')
        print("Downloaded Bioclim data")
    else:
        print("Bioclim data had was already downloaded")
        print("To download again delete ./data/bioclim_data_2pt5m.zip")
