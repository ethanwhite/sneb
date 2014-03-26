import os
import hashlib
import pandas
import sqlite3
import sys
import urllib
from zipfile import ZipFile

def get_bbs_env():
    """Run an R script the combines the BBS and environmental data"""
    os.system("Rscript get_env_data.r")
    
def get_bbs_locations():
    """Extract BBS route location data and write to file"""
    con = sqlite3.connect("./data/bbs.sqlite")
    query = "SELECT statenum * 1000 + route AS siteID, lati AS lat, loni AS long FROM routes;"
    bbs_locations = pandas.io.sql.read_frame(query, con)
    bbs_locations.to_csv("./data/bbs_locations.csv", index=False)

def get_data_file_paths():
    """Get the paths for all data files in the project"""
    data_file_paths = []
    for dirs, _, filenames in os.walk('data'):
        for filename in filenames:
            data_file_paths.append(os.path.join(dirs, filename))
    return data_file_paths

def install_bbs():
    """Install the BBS data using the EcoData Retriever"""
    if not os.path.isfile('./data/bbs.sqlite'):
        os.system("retriever install sqlite BBS --file ./data/bbs.sqlite --table_name {table}")
        print("Downloaded BBS data and installed it into bbs.sqlite")
    else:
        print("BBS data was already downloaded & installed")
        print("To download again delete ./data/bbs.sqlite")

def install_bioclim():
    """Download the 2.5 minute Bioclim data

    Data is stored in a wc2-5 subdirectory to allow the dismo library in R
    to automatically discover the data

    """
    bioclim_file_path = './data/wc2-5/bio_2-5m_bil.zip'
    if not os.path.isfile(bioclim_file_path):
        if not os.path.isdir('./data/wc2-5'):
            os.mkdir('./data/wc2-5')
        print("Downloading Bioclim data. This may take a few minutes...")
        bioclim_url = "http://biogeo.ucdavis.edu/data/climate/worldclim/1_4/grid/cur/bio_2-5m_bil.zip"
        urllib.urlretrieve(bioclim_url, bioclim_file_path)
        with ZipFile(bioclim_file_path) as bioclimzip:
            bioclimzip.extractall(path='./data/wc2-5/')
            print("Downloaded Bioclim data")
    else:
        print("Bioclim data had was already downloaded")
        print("To download again delete " + bioclim_file_path)

def write_data_hashes():
    """Store sha1 hashes for all data files for provenance"""
    data_files = get_data_file_paths()
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
    get_bbs_locations()
    get_bbs_env()
    write_data_hashes()

if __name__ == '__main__':
    main()
