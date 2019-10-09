import pandas as pd
import pygal

def data(df):
# 饼图
    p = pygal.Pie()
    x_data = df.index.values
    for i, per in enumerate(df['views']):
        p.add(x_data[i], per)
    p.title = 'Bilibili视频信息'
    p.render_to_file(f'饼图.svg')

df = pd.read_csv('video_info.csv', encoding='utf-8')
df_sum = df.drop(['title', 'av', 'region'], axis=1).groupby('region0').sum().sort_values('views', ascending=False)
# print(df_sum)
data(df_sum)


