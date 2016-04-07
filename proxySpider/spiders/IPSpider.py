#coding=utf8
__author__ = 'DixonShen'

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import Request
import codecs
from datetime import *
import re

class IPSPider(BaseSpider):
    name = 'proxy_parse'
    allowed_domains = ''
    start_urls = []
    count = 1
    for page in range(1,6):
        url1 = 'http://www.xicidaili.com/nt/' + str(page)
        url2 = 'http://www.xicidaili.com/nn/' + str(page)
        url3 = 'http://www.xicidaili.com/wn/' + str(page)
        url4 = 'http://www.xicidaili.com/wt/' + str(page)
        start_urls.append(url1)
        start_urls.append(url2)
        start_urls.append(url3)
        start_urls.append(url4)

    def parse(self,response):
        fname = str(self.count) + '.txt'
        with codecs.open(fname,'w') as fd:
            fd.write(response.body)
        fd.close()
        self.count = self.count + 1
        sel = Selector(response)
        tr = sel.xpath('//tr')
        print type(tr)
        i = 0
        for ttr in tr:
            td = ttr.xpath('.//td')
            if td:
                print i+1
                i = i+1
                # llist =
                ip = td[2].xpath('.//text()').extract()[0]
                port = td[3].xpath('.//text()').extract()[0]
                dt = td[9].xpath('.//text()').extract()[0]
                location =' '.join(td[4].xpath('.//descendant::text()').extract())
                sp = td[7].xpath('.//div[@class="bar"]/@title').extract()[0]
                sp = re.findall('\d+.\d+',sp).pop()
                ltime = td[8].xpath('.//div[@class="bar"]/@title').extract()[0]
                ltime = re.findall('\d+.\d+',ltime).pop()
                # if
                m = dt.split('-')
                year = '20' + m[0]
                month = m[1]
                day = m[2].split(' ')[0]
                ttime = m[2].split(' ')[1]
                hour = ttime.split(':')[0]
                min = ttime.split(':')[1]
                date1 = datetime(int(year),int(month),int(day),int(hour),int(min))
                date2= datetime.now()
                duration = timedelta(2)
                # print sp,ltime
                if ((date2-date1)<duration and float(sp)<=5 and float(ltime)<=2):
                    print ip,':',port,\
                           location.strip(),\
                           td[5].xpath('.//text()').extract()[0],\
                           td[6].xpath('.//text()').extract()[0],\
                           sp,ltime,dt
                    with codecs.open('ValidIP.txt','a') as filehandler:
                        filehandler.write(ip+':'+port+'\n')
                    filehandler.close()
