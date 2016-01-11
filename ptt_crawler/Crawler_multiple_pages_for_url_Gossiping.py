import requests
import urllib2 
from bs4 import BeautifulSoup
import re
import time
import os

#os.chdir("C:/Users/Kile/Desktop")

ptt_url_list_file = open("ptt_url_list_file.txt", "w")
for page in range(1825, 3591):
    
    #payload = {"from":"/bbs/HatePolitics/index"+str(page)+".html", "yes":"yes"}
    #rs = requests.session()
    #res = rs.post("https://www.ptt.cc/ask/over18", verify = False, data = payload)
    header = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request("https://www.ptt.cc/bbs/HatePolitics/index"+str(page)+".html",None, header)
    res = urllib2.urlopen(req)
    
    bsobj = BeautifulSoup(res.read())
    article_content = bsobj.findAll("a", {"href":re.compile("^(/bbs/HatePolitics/M)")})
    url_list = ["https://www.ptt.cc"+x.attrs["href"] for x in article_content]
    ptt_url_list_file.write('\n'.join(url_list)+'\n')
    res.close()
    # pause for second to get all the data, avoid getting too fast to obtain all the data
    time.sleep(4)

ptt_url_list_file.close()
