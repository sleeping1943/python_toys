import shutil
import json
import sqlite3
import matplotlib.pyplot as plt
from wordcloud import WordCloud

word_count = dict()

def test_sqlite(fpath, pic_width, pic_height, pic_scale, color, record_count):
    conn = sqlite3.connect(fpath)
    c = conn.cursor()
    res_list = c.execute('''
    select url, title, visit_count,
    last_visit_time from urls where last_visit_time>0
    order by visit_count desc limit {}
        '''.format(record_count))
    # res_list = c.fecthall()
    index = 1
    for value in res_list:
        #print('line[{}]:{} type:{}'.format(index, value, type(value)))
        title = value[1]
        count = value[2]
        if title in word_count.keys():
            count = word_count[title] + count
        word_count[title] = count
        index = index + 1
    #print('word_counr:{}'.format(word_count))
    #print('select over!!!')
    word_cloud = WordCloud(width=pic_width, height=pic_height, font_path='simhei.ttf', background_color=color, scale=pic_scale)
    word_cloud = word_cloud.fit_words(word_count)
    plt.imshow(word_cloud)
    plt.show()


if __name__ == '__main__':
    with open('./conf.json', 'r') as f:
        conf = json.load(f)
        shutil.copy(conf['history_path'], conf['db_path'])
        test_sqlite(conf['db_path'], conf['width'],conf['height'],conf['scale'],conf['bg_color'], conf['record_count'])