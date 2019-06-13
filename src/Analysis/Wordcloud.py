import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from Analysis.DataMapper.Mapper06082019 import mapper as m
import jieba
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import math

def WordcloudForChatRoom(historyData, cache, logger):
    r = []
    d = path.dirname(__file__)
    fp = path.join(d + "/wc_cn/fonts/SourceHanSerif/SourceHanSerifK-Light.otf")
    outputPath = path.join(d + "/WordCloudPics/")
    for h in historyData:
        if h[m.Des]==0 and h[m.Type]==1:
            r += jieba.cut(h[m.Message])
        if h[m.Des]==1 and h[m.Type]==1:
            r += jieba.cut(h[m.Message].split("\n")[1])
    text = " ".join(r)
    textToWordCloud(text, fp, outputPath, cache["groupName"])
    return True

def WordcloudForEachMenbersInChatRoom(historyData, cache, logger):
    pass

def textToWordCloud(text, fp, outputPath, outputFileName, showFigure = False):
    mfs = int(1500/math.log10(len(text)))/100*100
    mfs = mfs if mfs <= 600 else 600
    mfs = mfs if mfs >= 200 else 200
    wc = WordCloud(font_path=fp, background_color="white", max_words=2000,
               max_font_size=mfs, random_state=42, width=3000, height=2580, margin=2,)
    wc.generate(text)
    if showFigure:
        plt.figure()
        # recolor wordcloud and show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()
    wc.to_file(outputPath + outputFileName + ".jpg")
    return True
