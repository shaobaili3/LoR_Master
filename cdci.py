# Update Riot set json files
from decoder.api_wrapper import card
import opencc

card.downloadAllSet()
card.downloadRawSet()

with open('Resource/zh_tw.json', 'r', encoding='utf-8') as fp:
    content = fp.read()
    newContent = opencc.OpenCC('t2s').convert(content)
    with open('Resource/zh_cn.json', 'w', encoding='utf-8') as output:
        output.write(newContent)