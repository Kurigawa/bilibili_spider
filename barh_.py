import pandas as pd
import pygal

def data(df,s):
# 条形图
    b = pygal.Bar()
    x_data = df.index.values
    # 获取索引值
    b.add('播放', df['views'])
    b.add('评论', df['replys'])
    b.add('弹幕', df['danmaku'])
    b.add('收藏', df['favorites'])
    b.add('投币', df['coins'])
    b.x_labels = x_data
    b.title = f'Bilibili视频信息({s})'
    b.x_title = '分区'
    b.render_to_file(f'条形图（{s}）.svg')

df = pd.read_csv('video_info.csv', encoding='utf-8')
df_mean = df.drop(['title', 'av', 'region'], axis=1).groupby('region0').mean().sort_values('views', ascending=False)
df_sum = df.drop(['title', 'av', 'region'], axis=1).groupby('region0').sum().sort_values('views', ascending=False)
df_mean = df_mean.astype(int)
# 去掉小数部分
data(df_mean, '均值')
data(df_sum, '总数')


