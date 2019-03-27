# -*- coding: utf-8 -*-
import requests
from lxml import etree

def main(number):
    url = 'https://www.iu91.com/' + 'content/ListContent/contentid/' + number
    response = requests.get(url)
    resp = etree.HTML(response.text)

    title = resp.xpath('//*[@id="title"]/text()')[0]
    #print('标题：'+title)
    print(title)
    item = resp.xpath('//*[@id="content"]/div[3]/div')

    price = item[1].xpath('div[1]/div[1]/div[2]')
    price = str(price[0].xpath('normalize-space(string(.))'))
    print('价格：' + price)

    floor = item[1].xpath('div[1]/div[2]/span/text()')
    if floor:
        print('楼层：'+floor[0])
    else:
        print('楼层：no info')


    enter_time = item[1].xpath('normalize-space(div[2]/ul/li[4]/span[2]/text())')
    print('入住时间：'+enter_time)

    description = item[2].xpath('normalize-space(string(div))')
    print(description)

    address = item[3].xpath('normalize-space(string(div/div))')
    print(address)

if __name__ == '__main__':
    main('66121')
