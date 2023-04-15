import json
from os.path import exists
from pprint import pprint
import base64
import requests


class PostArticle:
    def __init__(self):
        # set saved article file path.
        self.jsonFileName = './save.json'

        # read username and password.
        self._userInfo()

        # read identity file
        self._read_json()

    def _userInfo(self):
        """
        get own username and passwd
        self.user
        self.passwd
        """
        with open('user.json') as user_file:
            tmp = json.load(user_file)
            self.user = tmp['user']
            self.passwd = tmp['passwd']
            self.postsiteurl = tmp['postsiteurl']

    def _read_json(self):
        """
        read save.json to list
        """
        if exists(self.jsonFileName):
            with open(self.jsonFileName) as user_file:
                self.articles = json.load(user_file)
        else:
            print('no articles')
            exit()

    def _delete_posted(self, date):
        """
        投稿済みの記事にposted=trueをつける。
        """
        print('delete posted')
        for line in self.articles:
            if line['date'] == date:
                line['posted'] = True
                self._save_json()
                break

    def _save_json(self):
        """
        save.jsonを現在の状態で上書き保存する。
        """
        with open(self.jsonFileName, "w") as outfile:
            json_object = json.dumps(self.articles, indent=4)
            outfile.write(json_object)

    def post(self, title, body, date):
        """
        投稿する。
        """
        credentials = self.user + ':' + self.passwd
        token = base64.b64encode(credentials.encode())
        headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

        post = {
            'title': title,
            'status': 'publish',  # publish',
            'content': body
        }

        res = requests.post(
            self.postsiteurl + "?rest_route=/wp/v2/posts", headers=headers, json=post)
        if res.ok:
            print("投稿の追加 成功 code:" + str(res.status_code))
            self._delete_posted(date)
            return json.loads(res.text)
        else:
            print(
                f"投稿の追加 失敗 code:{res.status_code} reason:{res.reason} msg:{res.text}")
            kaeri = res.text
            print('------------')
            print(json.loads(kaeri))
            return {}

    def chose_article(self):
        """
        return: date
        find postable article. if not , return none
        """
        for line in self.articles:
            if 'posted' not in line or line['posted'] != True:
                return [line['title'], line['body'], line['date']]

        print('no article for post.')
        exit(99)


# create instance
pa = PostArticle()

# choose top artile that is not already posted.
art = pa.chose_article()

# post. and set it posted flag.
pa.post(art[0], art[1], art[2])
