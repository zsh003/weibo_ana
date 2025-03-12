import requests
from bs4 import BeautifulSoup
import json
import pymysql


conn = pymysql.connect(host='localhost', port=3306, user='mysql', passwd='123456', db='weibo_ana',
                           charset='utf8mb4')
cur = conn.cursor()

session=requests.Session()
headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9"
         }

# headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
#          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
#          }


# 存储爬取关键字帖子信息
def save_search(wid,uid,screen_name,reposts_count,comments_count,attitudes_count,status_city,status_province,text,created_at,keyword):
    sql = 'INSERT into search(wid,uid,screen_name,reposts_count,comments_count,attitudes_count,status_city,status_province,text,created_at,keyword) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'\
          %(repr(wid),repr(uid),repr(screen_name),repr(reposts_count),repr(comments_count),repr(attitudes_count),repr(status_city),repr(status_province),repr(text),repr(created_at),repr(keyword))
    cur.execute(sql)
    conn.commit()

# 存储评论信息
def save_comment(wid,uid,screen_name,comment,source,like_count,created_at,keyword):
    sql = 'INSERT into comment(wid,uid,screen_name,comment,source,like_count,created_at,keyword) VALUES ( "{}","{}","{}","{}","{}","{}","{}","{}")'.format(wid,uid,screen_name,comment,source,like_count,created_at,keyword)
    cur.execute(sql)
    conn.commit()

# 爬取微博关键字帖子
def search_search(page,keyword):
    uri='https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D'+keyword+'&page_type=searchall&page='+str(page)  # 薛之谦演唱会
    print(uri)
    with requests.get(uri) as url:
        data = url.text.encode('UTF-8', 'ignore').decode('UTF-8')
        with open("file.json", "w", encoding='utf-8') as f:
            f.write(data)
    file = open(r'./util/file.json', 'r', encoding='utf-8')
    # file = open(r'.\util\file.json', 'r', encoding='utf-8')     备注
    json_data = json.load(file)
    cards = json_data['data']['cards']
    for card in cards:
        try:
            created_at = card['card_group'][0]['mblog']['created_at']
            text = card['card_group'][0]['mblog']['text'].encode('UTF-8', 'ignore').decode('UTF-8')
            text=text.replace("\'","\'\'")
            wid = card['card_group'][0]['mblog']['id']
            with open('wid_list.txt', 'a', encoding='utf-8') as f:
                f.write(wid + '\n') # 将每个wid写入文档中
            userid = card['card_group'][0]['mblog']['user']['id']
            screen_name = card['card_group'][0]['mblog']['user']['screen_name']
            reposts_count = card['card_group'][0]['mblog']['reposts_count']
            comments_count = card['card_group'][0]['mblog']['comments_count']
            attitudes_count = card['card_group'][0]['mblog']['attitudes_count']
            status_city = card['card_group'][0]['mblog']['status_city']
            status_province = card['card_group'][0]['mblog']['status_province']
            print('帖子TEXT：')
            print(text)
            save_search(wid,userid,screen_name,reposts_count,comments_count,attitudes_count,status_city,status_province,text,created_at,keyword)
        except:
            pass

# 爬取评论
def search_comment(wid,max_id,keyword):
    url='https://m.weibo.cn/comments/hotflow?id='+str(wid)+'&mid='+str(wid)+'&max_id='+str(max_id)+'&max_id_type=0'
    print(url)
    keyword=keyword
    wid=wid
    req = session.get(url, headers=headers)
    html = req.text.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml').text
    print(soup)
    json_data = json.loads(eval(json.dumps(soup)))
    if 'data' not in json_data:
        print(f'Wid {wid} 没有评论。')
        return
    max_id=json_data['data']['max_id']
    print(f'max_id:{max_id}')
    datas=json_data['data']['data']
    for data in datas:
        created_at=data['created_at']
        like_count=data['like_count']
        source=data['source']
        text=data['text'].encode('UTF-8', 'ignore').decode('UTF-8')
        text=text.replace('</span>','')
        if '转发微博' in text:
            text=''
        uid=data['user']['id']
        screen_name=data['user']['screen_name'].encode('UTF-8', 'ignore').decode('UTF-8')
        print(f'text:{text}')
        save_comment(wid,uid,screen_name,text,source,like_count,created_at,keyword)
    print(max_id)


if __name__=='__main__':
    keyword=input("请输入你想要爬取的数据:")
    with open('wid_list.txt', 'w', encoding='utf-8') as f:
        f.write('')
    for i in range(30,40):
        print(i)
        search_search(i,keyword)
        # 爬取评论
    with open('wid_list.txt', 'r') as f:
        wid_list = [line.strip() for line in f.readlines()]
        for wid in wid_list:
            print(f'评论wid:{wid}')
            max_id=0
            while True:
                print("开始爬取评论！")
                search_comment(wid,max_id,keyword)
                if max_id==0 or max_id=='':
                    print("爬取本页结束")
                    break
