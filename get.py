import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json

"""
⬛使い方
python test3.py 2>/dev/null > out.json

⬛残件
・out.jsonの読み込み
・重複処理
・WPへのapi投稿部分
"""

class Scraping:
    def rtf(self):
        url = "http://buy.livedoor.biz/index.rdf"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        tes = soup.find_all('item')

        out = []
        for te in tes:
            tmp = {}
            lines = str(te).split('\n')
            for line in lines:
                if re.match(r'^<link', line):
                    line = line.replace('<link/>', '')
                    tmp['article_url'] = line
            tmp['body'] = te.find('content:encoded').get_text()
            tmp['img'], tmp['href'] = self._crop_first(tmp['body'])
            tmp['date'] = te.find('dc:date').get_text()
            tmp['title'] = te.find('title').get_text()
            out.append(tmp)
        self.out = out

    def _crop_first(self, bsObj):
        links = BeautifulSoup(str(bsObj), features="html.parser").find_all('a')
        return [
            links[0].find_all('img')[0]['src'],
            links[0]['href']
        ]


# インスタンス生成
sc = Scraping()

# rtfから記事をlistで生成
sc.rtf()

# sc.outをjsonに変換
json_object = json.dumps(sc.out, indent=4)

# 記事一覧のsc.outを代入。
with open("./save.json", "w") as outfile:
    outfile.write(json_object)
