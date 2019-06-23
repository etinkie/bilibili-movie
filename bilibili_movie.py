‘’’
代码原文地址：https://www.teamssix.com/year/190619-202702.html
代码演示视频地址：https://www.bilibili.com/video/av56117996/
更多信息欢迎关注我的微信公众号：teamssix
‘’’

#导入需要的库
import re
import json
import execjs
import requests
import pandas as pd
from IPython.display import display
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}

#将数据传入字典中
def results():
    result = {}
    result['电影名'] = B_loads2['title']
    
    inurl = 'https://bangumi.bilibili.com/ext/web_api/season_count?season_id={}&season_type=2&ts=1560879181926'.format(season_id)
    B_inreq = requests.get(inurl,headers = headers)
    B_inloads = json.loads(B_inreq.text)['result']
    result['播放数量'] = B_inloads['views']
    result['弹幕数量'] = B_inloads['danmakus']
    result['硬币数量'] = B_inloads['coins']
    result['追剧人数'] = B_inloads['favorites']
    
    B_score = B_loads2['order']['score']
    result['B站评分'] =  B_score
    
    
    D_url = 'https://movie.douban.com/subject_search?search_text={}'.format(name)
    D_req = requests.get(D_url,headers)
    D_endata = re.search('window.__DATA__ = "([^"]+)"', D_req.text).group(1)  # 加密的数据
    # 导入js
    with open(r'C:\Users\Dora\Desktop\Spider-Crack-JS\douban\main.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    data = ctx.call('decrypt', D_endata)
    D_score = data['payload']['items'][0]['rating']['value']
    result['豆瓣评分'] = D_score
    
    result['B站豆瓣评分差'] = round(float(B_score.split('分')[0]) - D_score,2)
    
    return result
    
def pdd():
    df = pd.DataFrame(pools,columns = ['电影名','播放数量','弹幕数量','硬币数量','追剧人数','B站评分','豆瓣评分','B站豆瓣评分差'])
    for i in ['播放数量','弹幕数量','硬币数量','追剧人数','B站评分','豆瓣评分','B站豆瓣评分差']:
        print('\n',30*'-',i,'最高的电影',30*'-')
        display(df.sort_values(by=[i],ascending=False).head(3))

if __name__=='__main__':
    pools = []
    num = 1
    for i in range(1,51):#i表示页数，每页有20个视频
        #对主页发出请求
        B_url = 'https://bangumi.bilibili.com/media/web_api/search/result?area=-1&style_id=-1&year=-1&season_status=-1&order=2&st=2&sort=0&page={}&season_type=2&pagesize=20'.format(i)
        B_req = requests.get(B_url,headers = headers)
        #获取视频信息
        B_loads = json.loads(B_req.text)['result']['data']
        for l in range(len(B_loads)):
            try:
                B_loads2 = B_loads[l]
                season_id =  B_loads2['season_id']
                name =  B_loads2['title']
                print('{} 正在获取 {}'.format(num,name))
                num = num + 1
                pools.append(results())
            except:
                pass
            continue
    pdd()
    
 #保存文件
#df.to_csv('bilibili_movie.csv',index=False,encoding='utf-8-sig')
