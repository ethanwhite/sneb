import os
import glob
import hashlib
import sys
import urllib
from zipfile import ZipFile

def install_bbs():
    """Install the BBS data using the EcoData Retriever"""
    if not os.path.isfile('./data/bbs.sqlite'):
        os.system("retriever install sqlite BBS --file ./data/bbs.sqlite --table_name {table}")
        print("Downloaded BBS data and installed it into bbs.sqlite")
    else:
        print("BBS data was already downloaded & installed")
        print("To download again delete ./data/bbs.sqlite")

def install_bioclim():
    """Download the 2.5 minute Bioclim data"""
    if not os.path.isfile('./data/bioclim_data_2pt5m.zip'):
        urllib.urlretrieve("http://biogeo.ucdavis.edu/data/climate/worldclim/1_4/grid/cur/bio_2-5m_bil.zip", "./data/bioclim_data_2pt5m.zip")
        with ZipFile('./data/bioclim_data_2pt5m.zip') as bioclimzip:
            bioclimzip.extractall(path='./data/')
            print("Downloaded Bioclim data")
    else:
        print("Bioclim data had was already downloaded")
        print("To download again delete ./data/bioclim_data_2pt5m.zip")

def write_data_hashes():
    """Store sha1 hashes for all data files for provenance"""
    data_files = glob.glob('./data/*')
    with open('data_hashes.txt', 'w') as output_file:
        for data_file in data_files:
            hash = hashlib.sha1(open(data_file, 'r').read()).hexdigest()
            output_file.writelines("%s,%s\n" % (data_file, hash))
    
def main():
    args = sys.argv[1:]
    if ('bbs' in args) or ('all' in args):
        install_bbs()
    if ('bioclim' in args) or ('all' in args):
        install_bioclim()
    write_data_hashes()

if __name__ == '__main__':
    main()
