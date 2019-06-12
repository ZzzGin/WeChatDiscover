import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from Analysis.DataMapper.Mapper06082019 import mapper as m
import jieba
from os import path
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, ImageColorGenerator

def WordcloudForChatRoom(historyData, cache):
    r = []
    for h in historyData:
        if h[m.Des]==0 and h[m.Type]==1:
            r += jieba.cut(h[m.Message])
        if h[m.Des]==1 and h[m.Type]==1:
            r += jieba.cut(h[m.Message].split("\n")[1])
    text = " ".join(r)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    font_path = 'D://WeChatDiscover/src/Analysis/wc_cn/fonts/SourceHanSerif/SourceHanSerifK-Light.otf'
    wc = WordCloud(font_path=font_path, background_color="white", max_words=2000,
               max_font_size=400, random_state=42, width=3000, height=2580, margin=2,)
    wc.generate(text)
    plt.figure()
    # recolor wordcloud and show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wc.to_file("C:/Users/zzzgi/Desktop/figure_1.jpg")
    return True
