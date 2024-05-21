# -*- coding: utf-8 -*-

"""
TSDM-coin-farmer
适配云函数, 单个文件完成天使动漫多人签到
requests方式
cookies.json的例子见 https://github.com/Trojblue/TSDM-coin-farmer/blob/main/doc/cookies.json.example
"""

import json
import requests
import random
import time
import os
import urllib.parse
import logging


# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ======== CONSTANT ========
sign_url = 'https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign'
work_url = 'https://www.tsdm39.com/plugin.php?id=np_cliworkdz:work'
login_url = 'https://www.tsdm39.com/member.php?mod=logging&action=login'

tsdm_domain = ".tsdm39.com"
s1_domain = "bbs.saraba1st.com"



# ========= COOKIE ========

def get_cookies_all():
    """从文件读取所有cookies
    { username: [cookie_list] }
    """
    cookies_json_file = os.path.join(os.path.realpath(os.path.split(__file__)[0]), 'cookies.json')
    try:
        with open(cookies_json_file, 'r', encoding='utf-8') as json_file:
            logging.info(f'找到 "{cookies_json_file}"')
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        logging.error("cookies.json 不存在")
        return {}


def get_cookies_by_domain(domain:str):
    """从所有cookie里分离出指定域名的cookie
    domain: cookie_list domain, (".tsdm39.com")
    """
    cookies_all = get_cookies_all() #     { username: [cookie_list] }
    domain_cookies = {}

    for username in cookies_all.keys():
        curr_user_cookies = cookies_all[username]
        curr_user_cookies_domained = []

        # 同一个用户名下可能有多个网站的cookie
        for cookie in curr_user_cookies:
            if cookie['domain'] == domain:
                curr_user_cookies_domained.append(cookie)

        if curr_user_cookies_domained != []:
            domain_cookies[username] = curr_user_cookies_domained

    return domain_cookies


# ======= SIGN ======

sign_page_with_param = \
    'https://www.tsdm39.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'


def sign_single_post_v2(cookie):
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])

    logging.info(cookie_serialized)

    # 必须要这个content-type, 否则没法接收
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Cookie': cookie_serialized,
        'Connection': 'Keep-Alive',
        'Referer': 'https://www.tsdm39.com/home.php?mod=space&do=pm',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    s = requests.session()
    sign_response = s.get(sign_url, headers=headers).text

    form_start = sign_response.find("formhash=") + 9  # 此处9个字符
    formhash = sign_response[form_start:form_start + 8]  # formhash 8位

    sign_data = "formhash=" + formhash + "&qdxq=wl&qdmode=3&todaysay=&fastreply=1"  # formhash, 签到心情, 签到模式(不发言)

    sign_response = s.post(sign_page_with_param, data=sign_data, headers=headers)

    if "恭喜你签到成功!获得随机奖励" in sign_response.text:
        logging.info("签到成功")
        return True
    elif "您今日已经签到" in sign_response.text:
        logging.warning("该账户已经签到过")
    elif "已经过了签到时间段" in sign_response.text or "签到时间还没有到" in sign_response.text:
        logging.error("签到失败: 目前不在签到时间段")
    elif "未定义操作" in sign_response.text:
        logging.error(f"签到失败, 可能是formhash获取错误\n\n{sign_response.text}")
    else:
        logging.error(f"未知原因签到失败\n\n{sign_response.text}")

    return False


def sign_multi_post():
    cookies = get_cookies_by_domain(tsdm_domain)

    for user in cookies.keys():
        logging.info(f"正在签到: {user}")
        try:
            sign_single_post_v2(cookies[user])
        except Exception as e:
            logging.error(f"post签到出错: {e}")

        time.sleep(random.uniform(0.5, 1))

    logging.info("POST方式: 全部签到完成")
    return

def main_handler(event, context):
    sign_multi_post()

if __name__ == '__main__':
    sign_multi_post()