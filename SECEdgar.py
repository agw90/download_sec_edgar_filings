# @alexpetralia
# adapted from @rahulrrixe's code on GitHub: https://github.com/rahulrrixe

from bs4 import BeautifulSoup # HTML parser
import requests, os, re

class SECCrawler():
    def __init__(self):
        pass
        
    base = os.getcwd() + "/../SEC-Edgar-data/"
    c = 0

    def make_directory(self, ticker, filing_type):
        # Making the directory to save company filings
        filing_type = re.sub(r'/','-',filing_type)
        if not os.path.exists(self.base):
            os.makedirs(self.base)
        if not os.path.exists(self.base+ticker):
            os.makedirs(self.base+ticker)
        if not os.path.exists(self.base+ticker+"/"+filing_type):
            os.makedirs(self.base+ticker+"/"+filing_type)     
            
    def parse_filing_index(self, ticker, filing_type, link):
        self.c+=1
        tld = 'http://www.sec.gov'
        
        r = requests.get(tld + link)
        soup = BeautifulSoup(r.text) 
        table = soup.find('table', 'tableFile')
        linkList = table.find_all('a')
        
        if linkList[0].string == None: # if first link empty because old SEC filing, get .txt
            link = tld+str(linkList[len(linkList)-1].get('href'))
        else:
            link = tld+linkList[0].get('href')
            
        # pull exact filing (eg. if amended) from the Type column
        exact_fts = [ft for ft in table.find_all('td') if ">"+filing_type in repr(ft)]
        if not exact_fts: # if list is empty
            exact_ft = filing_type
        else: # if a list is returned
            if len(exact_fts[0].string.split()) > 1: # if wrongly pull first cell, which has spaces
                exact_ft = re.sub(r'/','-', exact_fts[1].string) # take the second cell
            else: 
                exact_ft = re.sub(r'/','-', exact_fts[0].string) # if only one, it is correct
                

        fd_field = soup.find_all('div', 'formGrouping')
        filing_date = fd_field[0].find('div', 'info').string
        fd = re.sub(r'-','',filing_date)
        filing_period = fd_field[1].find('div', 'info').string
        
        print "filing period: %s from %s" % (filing_period, link)
        
        self.save_filing(ticker, filing_type, exact_ft, filing_period, link)
        
    def save_filing(self, ticker, filing_type, exact_ft, filing_period, link):
        r = requests.get(link)
        filing_type = re.sub(r'/','-',filing_type)
        path = self.base+str(ticker)+"/"+str(filing_type)+"/"+str(filing_period)+"_"+str(exact_ft)+"_"+str(ticker)
        term = '.txt' if '.txt' in link else '.htm'
        with open(path+term,'w') as f:
            f.write(r.text.encode('ascii', 'ignore'))
        
    ###############################################################
            
    def scrape_filings(self, ticker, filing_type, cik, start):
        try:
            self.make_directory(ticker, filing_type)
        except: 
            print "Unable to create directory"
            
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type={1}%25&dateb=&owner=exclude&start={2}&count=100".format(cik, filing_type, start)
        print "\ndownloading", filing_type+"s for", ticker, "starting from entry", start, "at", base_url
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text) # Initializing to crawl again
        table = soup.find('table', 'tableFile2')
        linkList = table.find_all('a', id='documentsbutton')
        #fileTypeList = table.findall('tr', class='file_type')
		
        print "\tNumber of files to download: %s" % len(linkList)
        
        if len(linkList) > 0:
            print "\tStarting download...."
            
            # Get all the doc
            for link in linkList:
                l = link.get('href')
                self.parse_filing_index(ticker, filing_type, l)
        else: print "\tSkipping..."
                        
        print "\tSuccessfully downloaded %s files. Total files saved: %s." % (len(linkList), self.c)
