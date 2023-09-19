# coding=utf-8
import unittest
from util.requestUtil import requestUtil

host = "https://api.xdclass.net"


class loginTestCase(unittest.TestCase):
    def testuserlogin(self):
        request = requestUtil()
        url = host+"/pub/api/v1/web/web_login"
        data = {"phone":"13113777555","pwd":"1234567890"}
        response = request.request(url,'post',param=data)
        self.assertEqual(response['code'], 0, 'okokok')

if __name__ == '__main__':
    unittest.main()
