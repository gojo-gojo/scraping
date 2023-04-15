import json
from os.path import exists
from pprint import pprint
import base64
import requests

class PostArticle:
    def __init__(self):
        self.jsonFileName = './save.json'
        self.articles = []

        # read json file
        self._read_json()
        pass

    def _read_json(self):
        if exists(self.jsonFileName):
            with open(self.jsonFileName) as user_file:
                self.articles = json.load(user_file)
        else:
            print('no articles')
            exit()

    def _delete_posted(self, date):
        print('delete posted')
        for line in self.articles:
            if line['date'] == date:
                line['posted'] = True
                self._save_json()
                break

    def _save_json(self):
        with open(self.jsonFileName, "w") as outfile:
            json_object = json.dumps(self.articles, indent=4)
            outfile.write(json_object)

    def post(self, title, body, date):
        credentials = 'gojo@gojo.run' + ':' + 'BhQKPLkb7CPojZ4jginWEIBP'
        token = base64.b64encode(credentials.encode())
        headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

        post = {
            'title': title,
            'status': 'publish',  # publish',
            'content': body
        }

        res = requests.post(
            "http://localhost:8080/?rest_route=/wp/v2/posts", headers=headers, json=post)
        if res.ok:
            print("投稿の追加 成功 code:" + str(res.status_code))
            self._delete_posted(date)
            return json.loads(res.text)
        else:
            print(
                f"投稿の追加 失敗 code:{res.status_code} reason:{res.reason} msg:{res.text}")
            return {}

    def _chose_article(self):
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
art = pa._chose_article()

# post. and set it posted flag.
pa.post(art[0], art[1], art[2])

