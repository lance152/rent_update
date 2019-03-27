# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import os
import broadcast

base_url = 'https://www.iu91.com/'
base_path = os.path.abspath('.')
def read():
    with open("posted.txt","r") as f:
        result=f.read().splitlines()

    return result

def posted(a):
    with open('posted.txt','w') as f:
        for i in a:
            f.write(i)
            f.write('\n')

def get_list():
    url = base_url+'content/ListRS?mobile=4&page=1&viewtype=image&loadviplist=1&filter%5Btradetype%5D=rent&filter%5Bstatus%5D=1&filter%5Bprovince%5D=QC&filter%5Bcity%5D=MONTREAL&filter%5Barea%5D=LASALLE&filter%5Brent_method%5D=whole&filter%5Bhouse_type%5D=Condominium&filter%5Brooms_sleeping%5D=2&filter%5Btype%5D=zhuzhai&rightversion=1';
    response = requests.get(url);
    resp = etree.HTML(response.text)
    listing = resp.xpath('//div[@id="listings"]/div/@id')
    for i in range(len(listing)):
        listing[i] = re.sub('\D','',listing[i])
    return listing

def get_detail(number):
    path = base_path+'\\'+number
    mkdir(path)
    url = base_url+'content/ListContent/contentid/'+number
    response = requests.get(url)
    resp = etree.HTML(response.text)
    get_pic(resp,path)
    get_info(resp,path)

def get_info(resp,path):
    title = resp.xpath('//*[@id="title"]/text()')[0]

    item = resp.xpath('//*[@id="content"]/div[3]/div')

    price = item[1].xpath('div[1]/div[1]/div[2]')
    price = str(price[0].xpath('normalize-space(string(.))'))
    price = '价格：' + price

    floor = item[1].xpath('div[1]/div[2]/span/text()')
    if floor:
        floor = '楼层：'+floor[0]
    else:
        floor = '楼层：no info'

    enter_time = item[1].xpath('normalize-space(div[2]/ul/li[4]/span[2]/text())')
    enter_time = '入住时间：' + enter_time

    description = item[2].xpath('normalize-space(string(div))')
    description = '特色说明：'+description

    address = item[3].xpath('normalize-space(string(div/div))')
    address = '地址：'+address

    with open(path+'\\info.txt','w',encoding='utf-8') as f:
        f.writelines(title+'\n')
        f.writelines(price+'\n')
        f.writelines(floor+'\n')
        f.writelines(enter_time+'\n')
        f.writelines(description+'\n')
        f.writelines(address+'\n')

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def get_pic(resp,path):
    pics = resp.xpath('//*[@id="content"]/div[2]/script[1]/text()')[0]
    pics = str(pics)
    pics_url = re.findall(r'src: \'(.+?\.(JPG|jpeg|jpg))\'',pics)
    for i in pics_url:
        url = base_url+i[0]
        img = requests.get(url)
        with open(path+'\\'+str(pics_url.index(i))+'.jpg','wb') as f:
            f.write(img.content)

if __name__=='__main__':
    old_listing = read();
    new_listing = get_list();
    print(set(old_listing));
    print(set(new_listing));
    new_post = list(set(new_listing).difference(set(old_listing)))
    print(new_post)
    posted(new_listing)
    for i in new_post:
        print(i)
        get_detail(i)
        broadcast.send(i)
