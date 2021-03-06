import sys 
import os
sys.path.append(os.path.abspath('./src')) 
from Analysis.DataMapper.Mapper06082019 import mapper as m
from Analysis.CacheNeeds import needs

import jieba
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import math

@needs("groupName", "outputFolder")
def WordcloudForChatRoom(historyData, cache, logger):
    logger.info("[Info] Text history for " + cache["groupName"] + " processing...")
    d = path.dirname(__file__)
    fp = path.join(d + "/wc_cn/fonts/SourceHanSerif/SourceHanSerifK-Light.otf")
    outputPath = cache["outputFolder"]
    r = []
    for h in historyData:
        if h[m.Des]==0 and h[m.Type]==1:
            r += jieba.cut(h[m.Message])
        if h[m.Des]==1 and h[m.Type]==1:
            r += jieba.cut(h[m.Message].split("\n")[1])
    text = " ".join(r)
    textToWordCloud(text, fp, outputPath, cache["groupName"], logger)
    return True

@needs("groupName", "outputFolder", "textMessagesSplitedByIdInGroupChat")
def WordcloudForEachMembersInChatRoom(historyData, cache, logger):
    logger.info("[Info] Each members text history for " + cache["groupName"] + " processing...")
    d = path.dirname(__file__)
    fp = path.join(d + "/wc_cn/fonts/SourceHanSerif/SourceHanSerifK-Light.otf")
    outputPath = cache["outputFolder"]
    for case in cache["textMessagesSplitedByIdInGroupChat"]:
        r = []
        weChatName = cache["textMessagesSplitedByIdInGroupChat"][case][0]
        if len(weChatName)==0:
            weChatName = "me"
        logger.info("[Info] Text history for " + weChatName + " processing...")
        messages = cache["textMessagesSplitedByIdInGroupChat"][case][1]
        for m in messages:
            r += jieba.cut(m)
        text = " ".join(r)
        textToWordCloud(text, fp, outputPath, cache["groupName"]+"-"+weChatName, logger)
    return True


def textToWordCloud(text, fp, outputPath, outputFileName, logger, showFigure = False):
    logger.info("[Info] WordCloud " + outputFileName + ".jpg "+"generating...")
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
    wc.to_file(outputPath + "\\" + outputFileName + ".jpg")
    logger.info('[Info] WordCloud figure saved to : "%s".' % (outputPath + "\\" + outputFileName + ".jpg"))
    return True
