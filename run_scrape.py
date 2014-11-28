from SECEdgar import SECCrawler
import time, sys, numpy as np

class runScrape:
    
    def scrape(self, fp = 'sample.txt'):
        crawler = SECCrawler()
        
        st = time.time()
        file_path = fp
        
        with open (file_path, 'r') as f:
            firms = []
            for line in f:
                arr = [item.strip() for item in line.split(',')]
                ticker = arr.pop(0)
                cik = arr.pop(0)
                ftypes = arr
                firm = [ticker, cik, ftypes]
                firms.append(firm)
                
        for firm in firms:
            ticker = firm[0]
            cik = firm[1]
            for ft in firm[2]:
                start_count = ['0', '100', '200']
                for s in start_count:
                    crawler.scrape_filings(ticker.upper(), ft.upper(), cik, s)
        
        print "\nRuntime: %s seconds" % repr(np.round(time.time()-st))
