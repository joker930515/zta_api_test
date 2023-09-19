# -*- coding: utf-8 -*-
import requests
from requests.packages import urllib3

urllib3.disable_warnings()


class requestUtil:

    def __init__(self):
        pass

    def request(self, url, method, header=None, param=None, content_Type=None):
        try:
            if method == 'get':
                result = requests.get(url=url, headers=header, params=param, verify=False).json()
                return result
            elif method == 'post':
                if content_Type == "application/json":
                    result = requests.post(url=url, headers=header, json=param, verify=False).json()
                else:
                    result = requests.post(url=url, headers=header, data=param, verify=False).json()
                return result
            else:
                print("不支持其他method")


        except Exception as e:
            print("http请求报错{0}".format(e))


if __name__ == '__main__':
    '''url = "https://api.xdclass.net/pub/api/v1/web/video_detail"
    datas = {"video_id": 53}
    method = 'get'
    r = requestUtil()
    result = r.request(url,method, None,datas)
    print(result)'''

    url = "https://api.xdclass.net/pub/api/v1/web/web_login"
    params = {"phone": "13113777555", "pwd": "1234567890"}
    method = 'post'
    r = requestUtil()
    result = r.request(url, method, param=params)
    print(result)
