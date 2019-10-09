from my_spider import Response
import pymongo
import json

lst = []
for num in range(0, 3000):
    print(f'av{num * 20000}')
    # url_user = 'https://api.bilibili.com/x/player.so?id=cid:433&aid=4000&buvid=B8B21500-8896-456A-837F-E8DE812514F040760infoc'
    url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(num * 20000)
    Res = Response(url)
    res = Res.requests_req().text
    res = json.loads(res)   # 字典
    # print(res)
    if res['message'] == '0':
        video_info = {}
        data = res['data']      # 字典
        video_info['av'] = str(data['aid'])                                         # av号
        video_info['title'] = data['title'].replace('\r', '').replace('\n', '').replace(',', '，')     # 标题
        # code   ...                                                                # 一级分区、上传时间
        RE = Response('https://www.bilibili.com/video/av' + str(num * 1000))
        re = RE.bs4_analytic()
        em = re.select('div.video-data > span')
        # print(em)
        if em != []:
            video_info['time'] = em[1].text
        else:
            print('Error. No video information.')
            continue
        r = re.find_all(target='_blank')
        if r != []:
            video_info['region0'] = r[0].text
        else:
            print('Error. No video information.')
            continue
        video_info['region'] = data['tname']                                        # 二级分区
        video_info_temp = data['stat']
        # print(data['stat'])
        video_info['views'] = str(video_info_temp['view'])                          # 播放量
        video_info['danmaku'] = str(video_info_temp['danmaku'])                     # 弹幕
        video_info['replys'] = str(video_info_temp['reply'])                        # 评论
        video_info['favorites'] = str(video_info_temp['favorite'])                  # 收藏
        video_info['coins'] = str(video_info_temp['coin'])                          # 投币
        video_info['shares'] = str(video_info_temp['share'])                        # 分享
        video_info['likes'] = str(video_info_temp['like'])                          # 点赞
        print(video_info)
        lst.append(video_info)
    else:
        print('Error. No video information.')
        continue
print(lst)
res = Response('https://www.bilibili.com/')
res.file_save_csv('video_info', lst)
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.bilibili
collection = db.video_info
result = collection.insert(lst)
