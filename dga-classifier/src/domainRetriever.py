import pandas as pd
import urllib
import tldextract
from zipfile2 import ZipFile
import io
import math
import pickle


class retrieveDomains():

    def __init__(self):
        self.alexa_address = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        self.cisco_address = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"
        self.net_address = "https://data.netlab.360.com/feeds/dga/dga.txt"
        self.bamb_address = "http://osint.bambenekconsulting.com/feeds/dga-feed.txt"

    def get_domains(self, address):
        """specify file location for alexa 1m"""
        url = urllib.request.urlopen(address)
        zipfile = ZipFile(io.BytesIO(url.read()))
        tld_domains = []
        for i in zipfile.read("top-1m.csv").split():
            tld = tldextract.extract(i.decode("utf-8").split(",")[1]).domain
            tld_domains.append(tld)
        return tld_domains

    def dedup_domains(self):
        cisco = self.get_domains(self.cisco_address)
        alexa = self.get_domains(self.alexa_address)
        combined = cisco + alexa
        return list(set(combined))

    def _find_between(self, string, start, end):
        return (string.split(start))[1].split(end)[0]

    def get_dga_bamb(self):
        url = urllib.request.urlopen(self.bamb_address)
        list_of_domains = []
        for line in url.readlines()[14:]:
            splits = line.decode("utf-8").split(",")
            family = self._find_between(splits[1], "by", "for").strip()
            domain = tldextract.extract(splits[0]).domain
            list_of_domains.append((domain, family))
        return list_of_domains

    def get_dga_netlab(self):
        url = urllib.request.urlopen(self.net_address)
        list_of_domains = []
        for line in url.readlines()[21:]:
            splits = line.decode("utf-8").split("\t")
            family = splits[0]
            domain = tldextract.extract(splits[1]).domain
            list_of_domains.append((domain, family))
        return list_of_domains

    def dedup_dga(self):
        net = self.get_dga_netlab()
        bamb = self.get_dga_bamb()
        combined = []

        for i in net:
            combined.append(i[0])
        for j in bamb:
            combined.append(j[0])

        return list(set(combined))

    def gen_train_test_data(self):
        """collect all data for train/test, add labels and save"""

        domains = self.dedup_domains()

        dga = self.dedup_dga()

        if len(domains) > len(dga):
            num_m = len(dga)
            num_b = math.floor((num_m/40) * 60)

        if len(domains) < len(dga): 
        	num_m = len(domains)
        	num_b = math.floor((num_m/40) * 60)

        print ("number of malicious domains used for training/testing: %d" %num_m)

        print ("number of benign domains used for training/tetsing: %d" %num_b)

        all_domains = domains[:(num_b+1)] + dga[:(num_m+1)]

        print ("enitre size of training/testing set: %d" %len(all_domains))

        labels = []

        labels += ["benign"] * num_b

        labels += ["malicious"] * num_m

        return zip(all_domains, labels)

    def save_data(self, zipped_list):
        DATA_FILE = 'data/traindata_01.pkl'
        pickle.dump(zipped_list, open(DATA_FILE, 'wb'))
        return
