import json
from os.path import exists
from pprint import pprint

class PostArticle:
    def __init__(self):
        self.jsonFileName = './save.json'
        self.articles = []

        # read json file
        self._read_json()


    def _read_json(self):
        if exists(self.jsonFileName):
            with open(self.jsonFileName) as user_file:
                self.articles = json.load(user_file)
        else:
            print('no articles')
            exit()

    def post(self):
        """
        メイン。どうやってpostするかー。
        """
        pass


# create instance
pa = PostArticle()

# print test
pprint(pa.articles)
