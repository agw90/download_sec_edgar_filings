# dump S&P 500 companies and CIK's into a text file
# output run_scrape to logfile: http://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python
    
from Tkinter import *
import tkFileDialog as TkF
from run_scrape import *
import webbrowser, os, time, logging

class myApp:
    ## WIDGETS ##
    def __init__(self, parent):
        self.myParent = parent
        self.file_path = 'sample.txt'
        
        self.Frame0 = Frame(parent)
        self.Frame0.pack()
                   
        self.label = Label(self.Frame0, text="_________SEC EDGAR Filings Scraper_________\n\n\nWorks for up to 300 filings per company.\n\nIf you need 10-Q's or 10-K's in order, just copy/paste them\n into the same folder because they are named by date.\n")
        self.label.pack()

        self.Frame1 = Frame(parent)
        self.Frame1.pack()

        self.openButton = Button(self.Frame1, command=self.followLink)
        self.openButton.configure(text="Open SEC homepage", background="grey", padx="3m", pady="3m")
        self.openButton.pack(side=LEFT)
        
        self.selectButton = Button(self.Frame1, command=self.selectFileClick)
        self.selectButton.configure(text="Select your file", background="grey", padx="3m", pady="3m")
        self.selectButton.pack(side=LEFT)
        
        self.runButton = Button(self.Frame1, command=self.runButtonClick)
        self.runButton.configure(text="Run program", background= "grey", padx="3m", pady="3m")
        self.runButton.pack(side=LEFT)
        
        self.closeButton = Button(self.Frame1, command=self.closeButtonClick)
        self.closeButton.configure(text="Close", background= "grey", padx="3m", pady="3m")
        self.closeButton.pack(side=LEFT)
        
    ## EVENT HANDLERS ##
    def selectFileClick(self):
        self.file_path = TkF.askopenfilename()
        # self.write(sys.stdout)
        
    def runButtonClick(self):
        S = runScrape()
        S.scrape() if self.file_path=='' else S.scrape(self.file_path)
                       
    def closeButtonClick(self):
        global root
        root.destroy()
        
    def followLink(self):
        webbrowser.open('http://www.sec.gov/edgar/searchedgar/companysearch.html')

print "##################################################\n"
print (time.strftime("%I:%M:%S")) + ": Starting..."
root = Tk()
myapp = myApp(root)
root.mainloop()
print "Done.\n"