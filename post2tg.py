# -*- encoding: utf-8 -*-

import requests


def post(chat_id, text):
    post_url = 'https://api.telegram.org/bot983128077:AAHYi5ouhw_pMnQe9ZwcANSK********4Mn4/sendMessag' \
               'e?chat_id={0}&text={1}'.format(chat_id, text)
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
    requests.get(post_url, headers=headers)
