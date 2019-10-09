import pandas as pd
import pygal

def data(df,s):
# 折线图
    l = pygal.Line()
    x_data = df.index.values
    # 获取索引值
    # l.add('播放', df['views'])
    l.add('评论', df['replys'])
    l.add('弹幕', df['danmaku'])
    l.add('收藏', df['favorites'])
    l.add('投币', df['coins'])
    l.x_labels = x_data
    l.title = f'Bilibili视频信息({s})'
    l.x_title = '分区'
    l.render_to_file(f'折线图1（{s}）.svg')

df = pd.read_csv('video_info.csv', encoding='utf-8')
for i in range(len(df[['time']])):
    df.loc[i, 'time'] = df.loc[i, 'time'].split('-')[0]
    # 将时间更改为年份做分组
df_mean = df.drop(['title', 'av', 'region'], axis=1).groupby('time').mean().sort_values('time', ascending=True)
df_sum = df.drop(['title', 'av', 'region'], axis=1).groupby('time').sum().sort_values('time', ascending=True)
df_mean = df_mean.astype(int)
# 去掉小数部分
data(df_mean, '均值')
data(df_sum, '总数')
