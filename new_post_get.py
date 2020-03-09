'''
新たに投稿された記事のタイトルとURLを取得する

利用条件 ： 記事の一覧を表示するページがあること
      　　各記事の<a>タグに共通するselecterが設定されていること

新しいURLが存在した場合にのみ動作するため、記事の変更（タイトルや内容など）は取得しない
（記事のURLが変わるものは例外）
'''

import requests, bs4


def new_post_getter(url, selecter, txt):
    '''
    記事タイトル及びURLのbs4_elementを取得
    第1引数 : 投稿一覧のあるページのURL
    第２引数 : 各投稿の<a>タグに付与されているセレクター 頭に.をつけて
    第3引数 : 記録用txtのpath
    '''
    res = requests.get(url)
    posts = bs4.BeautifulSoup(res.text, 'html.parser').select(selecter)

    now_posts_url = []
    now_posts_url_title_set = []
    for post in posts:
        # URLを抽出
        index_first = int(str(post).find('href=')) + 6
        index_end = int(str(post).find('">'))
        url = (str(post)[index_first : index_end])
        # タイトルを抽出
        index_first = int(str(post).find('">')) + 2
        index_end = int(str(post).find('</a'))
        title = (str(post)[index_first : index_end].replace('\u3000', ' ')) # 空白置換

        now_posts_url.append(url)
        now_posts_url_title_set.append(f"{url}>>>{title}")

    old_post_text = open(txt)
    old_post = old_post_text.read().split(',') # テキストファイルからリスト型へ 
    # differences : 投稿済だが一覧画面に表示されていない投稿 + 新しい投稿
    differences = list(set(now_posts_url) - set(old_post))
    old_post_text.close()

    # 記録用txtを上書き all_postsは過去の投稿 + 新しい投稿
    all_posts = ",".join(old_post + differences)
    f = open(txt, mode='w')
    f.writelines(all_posts)
    f.close()

    new_post_info = []
    for new in now_posts_url_title_set:
        for incremental in differences:
            if incremental in new:
                new_post_info.append(new.split(">>>"))
    return new_post_info

import codecs

code = "100054"
bin = '0' * (8 - len(code)) + code
bin = codecs.decode(bin,'hex_codec').decode('utf-32BE').encode('utf-8').decode('utf-8')

def send_line_notify(posts, token):
    '''
    # new_post_getterの返り値を引数に
    '''
    notice_url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    for url, title in posts:
        if 'http' not in url:
            url = 'https://qiita.com/' + url
        message = f'投稿したよ--\n(o・∇・o)/{bin}\n{title}\n{url}'
        payload = {'message': message}
        r = requests.post(notice_url, headers=headers, params=payload,)

