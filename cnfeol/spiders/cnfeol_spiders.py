# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import scrapy.cmdline
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from scrapy.http import Request, FormRequest
import codecs
import urllib
import logging
from cnfeol.items import CnfeolItem

logger = logging.getLogger(__name__)

class CnfeolSpider(scrapy.Spider):
    name = "cnfeol"
    allowed_domains = ["cnfeol.com"]
    # start_urls = urls
    start_urls = [
        'http://www.cnfeol.com/'
    ]

    def parse(self, response):
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        driver.find_element_by_id('Signin_MemberName').clear()
        driver.find_element_by_id('Signin_MemberName').send_keys('zglny2016')
        driver.find_element_by_id('Signin_MemberPassword').clear()
        driver.find_element_by_id('Signin_MemberPassword').send_keys('lirr20165996')
        # 登陆
        driver.find_element_by_id('Signin_Submit').click()

        time.sleep(10)

        driver.find_element_by_xpath('//*[@id="Content_Jiage"]/div/a').click()
        current_handle = driver.current_window_handle

        # 获取到所有的窗口
        handles = driver.window_handles
        print handles

        for h in handles:
            if h != current_handle:
                # 切换到查询列表窗口
                print 'h = %s'%h
                driver.switch_to_window(h)

        # TODO 切换到查询列表页面
        flag = True
        pageIndex = 0
        items = []
        while(flag):
            pageIndex = pageIndex + 1
            print '------当前第%d页------'%pageIndex


            # 产品名称
            names = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[1]')
            # 规格
            types = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[2]')
            # 最低价格
            min_prices = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[3]')
            # 最高价格
            max_prices = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[4]')
            # 涨跌
            changes = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[5]')
            # 单位
            units = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[6]')
            # 备注
            remarks = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[7]')
            # 日期
            dates = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr/td[8]')

            trs = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[6]/table/tbody/tr')
            print 'trs.length = %d'%trs.__len__()
            for i in range(1,trs.__len__()):
                item = CnfeolItem()
                '''
                name = scrapy.Field()
                type = scrapy.Field()
                min_price = scrapy.Field()
                max_price = scrapy.Field()
                change = scrapy.Field()
                unit = scrapy.Field()
                remark = scrapy.Field()
                date = scrapy.Field()
                '''
                item['name'] = names[i].text
                item['type'] = types[i].text
                item['min_price'] = min_prices[i].text
                item['max_price'] = max_prices[i].text
                item['change'] = changes[i].text
                item['unit'] = units[i].text
                item['remark'] = remarks[i].text
                item['date'] = dates[i].text
                items.append(item)

            next_pages = driver.find_elements_by_xpath('//*[@id="contentlistcontainer_zdj"]/div[7]/a')
            index=1
            for next_page in next_pages:
                flag = False
                if next_page.text == u'下一页':
                    flag = True
                    xpath = '//*[@id="contentlistcontainer_zdj"]/div[7]/a[%d]'%index
                    # print 'xpath='+xpath
                    driver.find_element_by_xpath(xpath).click()
                else:
                    index = index+1

            print 'flag = %s'%flag

        return items

if __name__ == '__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'cnfeol'])
