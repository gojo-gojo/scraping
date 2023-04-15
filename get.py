import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json
from os.path import exists


"""
⬛使い方
python ./get.py
./save.jsonが生成される。
"""


class Scraping:

    def __init__(self):
        self.jsonFileName = './save.json'
        self._read_jsonfile()

    def _read_jsonfile(self):
        """
        self.jsonFileNameがある場合は、読み込みして、
        self.articlesに代入
        無いならself.articlesの初期化
        """
        file_exists = exists(self.jsonFileName)
        if exists(self.jsonFileName):
            with open(self.jsonFileName) as user_file:
                self.articles = json.load(user_file)
        else:
            self.articles = []

    def rtf(self):
        """
        メイン処理。
        """
        url = "http://buy.livedoor.biz/index.rdf"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'xml')

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

            # 重複なしにappendする
            self._nonDupAppend(tmp)

    def _nonDupAppend(self,singleObj):
        broken = False
        for line in self.articles:
            if line['date'] == singleObj['date']:
                broken = True
                break

        if not broken:
            self.articles.append(singleObj)
            print(singleObj['date'] + ' append')
        else:
            print(singleObj['date'] + ' exist')

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
json_object = json.dumps(sc.articles, indent=4)

# 記事一覧のsc.outを代入。
with open("./save.json", "w") as outfile:
    outfile.write(json_object)
