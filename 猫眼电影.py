#coding:utf8
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}


#通过requests方法请求页面内容
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
  #          print(response.text)
            return response.text
        else:
            return None
    except RequestException:
        return None



#根据正则匹配请求页面返回的内容
def parse_one_page(content):
    guize=re.compile('<dd>.*?<i.*?board.*?>(.*?)</i>.*?data-src="(.*?)"\s.*?>.*?<p.*?title="(.*?)"\s.*?</p>.*?star">\s*(.*?)\s*?</p>.*?releasetime">(.*?)</p>.*?<p.*?score.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items= re.findall(guize,content)
    for item in items:
        yield({
            '排名':item[0],
            '图片链接':item[1],
            '电影名称':item[2],
            '主演':item[3][3:],
            '上映时间':item[4][5:],
            '评分':item[5]+item[6]

        })


#保存到文件 猫眼电影榜单.txt中
def save_file(item):
    with open('猫眼电影榜单.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
#UnicodeEncodeError: 'gbk' codec can't encode character '\xXX' in position XX
#在windows下面，新文件的默认编码是gbk,python解释器会用gbk编码去解析我们的网络数据流txt，然而txt此时已经是decode过的unicode编码，这样的话就会导致解析不了，出现上述问题。
# 解决的办法就是，改变目标文件的编码：with open('猫眼电影榜单.txt','a',encoding='utf-8') as f:


#main方法

def main(num):
    url = "http://maoyan.com/board/4?offset="+str(num)
    content = get_one_page(url)
    for item in parse_one_page(content):
        print(item)
        print('\n')
        save_file(item)




#get_one_page(url)



if __name__=='__main__':
    p=Pool(3)
    p.map(main,[i*10 for i in range(20)])







