### Python网络爬虫 ###

# 一般网页爬取的代码框架
import requests
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常！"

if __name__ == "__main__":
    url = "http://www.baidu.com"
    print(getHTMLText(url))


# 连续爬取100次并记录时间
import requests
import time
starttime = time.clock()
url = "https://www.baidu.com"
for i in range(100):
    r = requests.get(url)
    if r.status_code != 200:
        print("ERROR. Can't get url for 100 times.")
        break
else:
    print("Get the url successfully.")
endtime = time.clock()
print("Total time is %.2fs" % (endtime-starttime))


# 京东商城的页面爬取
import requests
url = "https://item.jd.com/2967929.html"
try:
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r. apparent_encoding
    print(r.text[:1000])
except:
    print("产生异常！")


# 亚马逊商品页面爬取 - 更改user-agent以突破网站限制
import requests
url = "https://www.amazon.cn/dp/B0186FESGW"
kv = {'user-agent':'Mozilla/5.0'}
try:
    r = requests.get(url, headers=kv)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[:1000])
except:
    print("ERROR!")


# 百度搜索关键词提交
import requests
keyword = 'python'
try:
    kv = {'wd': keyword}
    r = requests.get("http://www.baidu.com/s", params=kv)
    print(r.request.url)
    r.raise_for_status()
    print(len(r.text))
except:
    print("ERROR.")


# 爬取网页图片
import requests
import os
url = "http://s.cn.bing.net/th?id=OJ.DVG1PrNbhS0Uvg&pid=MSNJVFeeds"
root = "D:/pic/"
path = root + "th.jpg"
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        r = requests.get(url, timeouot=10)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("保存成功")
    else:
        print("文件已存在")
except:
    print("爬取失败")


# 自动查询IP地址
import requests
url = "http://m.ip138.com/ip.asp?ip="
ip = "202.204.80.112"
try:
    r = requests.get(url+ip)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[-500:])
except:
    print("爬取失败")


# 爬取中国大学排名
import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivInfo(uhead, ubody, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('thead').children:
        if isinstance(tr, bs4.element.Tag):
            ths = tr('th')
            uhead.append([ths[0].string, ths[1].string, ths[2].string, ths[3].string])
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ubody.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])

def printUnivInfo(uhead, ubody, num):
    h = uhead[0]
    print("|{0:^11}|{1:{4}^10}|{2:{4}^8}|{3:{4}^8}|".format(h[0], h[1], h[2], h[3], chr(12288)))
    for i in range(num):
        u = ubody[i]
        print("|{0:^13}|{1:{4}^10}|{2:{4}^8}|{3:{4}^10.1f}|".format(u[0], u[1], u[2], float(u[3]), chr(12288)))

def main():
    url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html"
    html = getHTMLText(url)
    uhead, ubody = list(), list()
    fillUnivInfo(uhead, ubody, html)
    printUnivInfo(uhead, ubody, 20)

main()


# 爬取淘宝商品信息
import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText Error")
        return ""

def parseGoods(glist, html):
    try:
        name = re.findall(r'"raw_title":".*?"', html)  # 最小匹配
        price = re.findall(r'"view_price":".*?"', html)
        loc = re.findall(r'"item_loc":".*?"', html)
        for i in range(len(name)):
            glist.append([name[i].split('"')[-2], price[i].split('"')[-2], loc[i].split('"')[-2]])
    except:
        print("parseGoods Error")

def printGoods(glist):
    print("{0:<8}{2:<10}{3:{4}<8}{1:<35}".format("序号", "商品名称", "价格", "地区", chr(12288)))
    count = 0
    for g in glist:
        count = count + 1
        print("{0:<8}{2:<10}{3:{4}<8}{1:<35}".format(count, g[0], g[1], g[2], chr(12288)))

def main():
    goods = "书包"
    url = "https://s.taobao.com/search?q=" + goods
    depth = 2
    glist = list()
    for i in range(depth):
        try:
            html = getHTMLText(url + '&s=' + str(i*44))
            parseGoods(glist, html)
        except:
            continue
    printGoods(glist)

main()


# 爬取股票信息 基础版
import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText Error")
        return ""

def getStockList(codelist, stock_list):
    html = getHTMLText(stock_list)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for tag in a:
        try:
            stockcode = re.findall(r's[hz]\d{6}', tag.attrs["href"])[0]
            # [0]使得stockcode去掉list外壳只保留string类型
            if stockcode:
                codelist.append(stockcode)
        except:
            continue

def getStockInfo(codelist, stock_info, file_path):
    # info = list()
    for stockcode in codelist[:20]:
        url = stock_info + stockcode + ".html"
        html = getHTMLText(url)
        if html == "":
            continue
        try:
            soup = BeautifulSoup(html, 'html.parser')
            stocktag = soup.find('div', {"class":"stock-bets"})
            if stocktag:
                nametag = stocktag.find('a', "bets-name")
                pricetag = stocktag.find('strong', "_close")
                name = nametag.get_text(strip=True)  # text是下级标签
                price = pricetag.string              # string是同级标签
                with open(file_path, 'a') as f:
                    f.write(str(name) + '\t' + str(price) + '\n')
        except:
            traceback.print_exc()
            continue

def main():
    stock_list = "http://quote.eastmoney.com/stocklist.html"
    stock_info = "https://gupiao.baidu.com/stock/"
    file_path = "D:/stockinfo.txt"
    codelist = list()
    getStockList(codelist, stock_list)
    getStockInfo(codelist, stock_info, file_path)
    print("爬取完成！")

main()


# 爬取股票信息 改进版
import requests
from bs4 import BeautifulSoup
import re

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url, {'user-agent':'Chrome/10'})
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("getHTMLText Error")
        return ""

def getStockList(codelist, stock_list):
    html = getHTMLText(stock_list, "GB2312")
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for tag in a:
        try:
            stockcode = re.findall(r's[hz]\d{6}', tag.attrs["href"])[0]
            # [0]使得stockcode去掉list外壳只保留string类型
            if stockcode:
                codelist.append(stockcode)
        except:
            continue

def getStockInfo(codelist, stock_info, file_path):
    count = 0
    for stockcode in codelist[100:110]:
        url = stock_info + stockcode + ".html"
        html = getHTMLText(url)
        if html == "":
            continue
        try:
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stocktag = soup.find('div', attrs={"class":"stock-bets"})
            if stocktag:
                nametag = stocktag.find('a', "bets-name")  # find等同于find_all再取列表的[0]
                pricetag = stocktag.find('strong', "_close")
                name = nametag.get_text(strip=True)  # .get_text(strip=True)等同于.text.split()[0]都是取股票名称的字符串
                price = pricetag.string      # .text是下级标签  .string是同级标签
                infoDict.update({"股票名称": name})
                infoDict.update({"当前价格": price})

                keyList = stocktag.find_all('dt')
                valueList = stocktag.find_all('dd')
                for i in range(len(keyList)):
                    key = keyList[i].text
                    val = valueList[i].text
                    infoDict[key] = val

                with open(file_path, 'a') as f:
                    f.write(str(infoDict) + '\n')
                    count = count + 1
                    print("\r已爬取数量：{}".format(count), end="")
        except:
            print("\r已爬取数量：{}".format(count), end="")
            continue

def main():
    stock_list = "http://quote.eastmoney.com/stocklist.html"
    stock_info = "https://gupiao.baidu.com/stock/"
    file_path = "D:/stockinfo.txt"
    codelist = list()
    getStockList(codelist, stock_list)
    getStockInfo(codelist, stock_info, file_path)
    print("\n爬取完成！")

main()


