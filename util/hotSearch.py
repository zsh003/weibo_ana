import requests

# 发送 GET 请求获取微博热搜榜 JSON 数据
response = requests.get('https://weibo.com/ajax/statuses/hot_band')
data = response.json()

# 解析 JSON 数据，提取热搜榜列表
hot_list = []
for item in data['data']['band_list']:
    title = item.get('word', '')
    hotness = item.get('label_name', '')
    category = item.get('category', '')
    print(f'{title},{hotness},{category}')