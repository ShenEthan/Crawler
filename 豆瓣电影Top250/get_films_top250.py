from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import pandas as pd


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬取网页
    datalist = getData(baseurl)
    # 2、解析数据
    savepath = "豆瓣电影Top250.xls"
    # 3、保存数据
    saveData(savepath,datalist)

# 正则定义要的元素
# 影片链接
findLink = re.compile(r'<a href="(.*?)">')
# 影片图片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #re.S忽略换行符
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

# 1、爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)  # 获取网页html

        datalist += parseData(html)

    return datalist

# 2、解析数据
def parseData(html):
    datalist = []
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all("div",class_="item"):
        data = []
        item = str(item)

        link = re.findall(findLink,item)[0]
        data.append(link)
        
        imgSrc = re.findall(findImgSrc,item)[0]
        data.append(imgSrc)
        
        titles = re.findall(findTitle,item)
        if len(titles)==2:
            ctitle = titles[0]
            data.append(ctitle)
            otitle = titles[1].replace("/","")
            data.append(otitle)
        else:
            data.append(titles[0])
            data.append("")
        
        rating = re.findall(findRating,item)[0]
        data.append(rating)
        
        judgeNum = re.findall(findJudge,item)[0]
        data.append(judgeNum)
        
        inq = re.findall(findInq,item)
        if len(inq) != 0:
            inq = inq[0].replace("。","")
            data.append(inq)
        else:
            data.append("")
            
        bd = re.findall(findBd,item)[0]
        bd = re.sub("<br(\s+)?/>(\s+)?","",bd)
        bd = re.sub("/","",bd)
        data.append(bd.strip()) #去掉前后空格

        datalist.append(data)
    return datalist

# 得到指定URL网页的数据
def askURL(url):
    head = { # 模拟浏览器头部信息
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html

# 3、保存数据
def saveData(savepath,datalist):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("豆瓣电影Top250")
    col = ['电影详情链接','影片图片链接','影片中文名','影片外文名','评分','评价数','概况','相关信息']
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print('第%d条' % (i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)
    print("save success")


if __name__ == '__main__':
    main()
