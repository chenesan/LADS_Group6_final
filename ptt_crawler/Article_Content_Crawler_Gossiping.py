#-*- coding: utf-8 -*-
import logging
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import math
import time
import urllib2 
from urllib2 import HTTPError, URLError

#logging.basicConfig(filename='content.log')

#os.chdir("C:/Users/Kile/Desktop")

### test

article_list = []
article_count = 0

fr = open(sys.argv[1])
url_list =[x.strip() for x in fr]

url_fail_list = []

ptt_HatePolitics_article = open("ptt_HatePolitics_article.txt", "w")    
for idx, url in enumerate(url_list):
    try:
        #payload = {"from":page, "yes":"yes"}
        #rs = requests.session()
        #res = rs.post("https://www.ptt.cc/ask/over18", verify = False, data = payload)
        header = {'User-agent' : 'Mozilla/5.0'}
        req = urllib2.Request(url, None, header)
        res = urllib2.urlopen(req)

        print('get {count} html, url: {url}'.format(count=idx+1, url=url))
        bsobj = BeautifulSoup(res.read())

        if bsobj.findAll("div", {"class":"article-metaline"})  == []:
            continue
        elif "公告".decode('utf8') in bsobj.findAll("div", {"class":"article-metaline"})[1].find("span",{"class":"article-meta-value"}).get_text():
            continue
        else:
            article_count +=1
            # title 
            article_title = bsobj.findAll("div", {"class":"article-metaline"})[1].find("span",{"class":"article-meta-value"}).get_text()
            if "]" in article_title:
                article_title = article_title.split("]")[1][1:]
            # time
            article_time = bsobj.findAll("div", {"class":"article-metaline"})[2].find("span",{"class":"article-meta-value"}).get_text().split(" ")
            if len(article_time) == 6:
                article_time = article_time[5]+"-"+article_time[1]+"-"+article_time[3]
            else:
                article_time = article_time[4]+"-"+article_time[1]+"-"+article_time[2]              
            # content
            article_content = bsobj.findAll("div", {"class":"article-metaline"})[2].next_siblings
            span_word = ""
            article_word = ""
            for t in article_content:
                if t.name == None:
                    if "From" in t:
                        continue
                    else:                    
                        article_word += t
                elif t.name == "span":
                    if u"發信站" in t.get_text() or u"編輯" in t.get_text():
                        continue
                    else:
                        span_word += t.get_text()
            # comment
            article_comment = bsobj.findAll("div", {"class":"push"})
            
            article_str = ""
            article_str += article_title+"&&&"+article_time+"&&&"+ article_word+" "+span_word+"&&&"
            for i in article_comment:
                article_str += i.findAll("span")[0].get_text().strip()+i.findAll("span")[2].get_text().strip()+"@@@"
            article_str = article_str.replace("\n","")
            article_str += "\n"                   
            article_list.append(article_str)
            print(article_count)
            ptt_HatePolitics_article.write(article_str.encode('utf8'))
            time.sleep(4)
            res.close()
    except HTTPError as e:
        print('get error {error}'.format(error=e)) 
    except IndexError:
        continue
    except URLError as e:
        print('get error {error}'.format(error=e)) 
        url_fail_list.append(url)
        print('get {url} fail!'.format(url=url))

#ptt_HatePolitics_article.writelines(article_list)
fw = open('ptt_url_fail.txt','w').write('\n'.join(ptt_url_fail_list))
ptt_HatePolitics_article.close()
