# coding=utf-8
import unittest
from util.requestUtil import requestUtil

host = "https://api.xdclass.net"


class indexTestCase(unittest.TestCase):
    def testIndexCategoryList(self):
        request = requestUtil()
        url = host + "/pub/api/v1/web/all_category"
        respose = request.request(url,'get',)
        self.assertEqual(respose['code'],0,"nononono")

    def testIndexVedioList(self):
        request = requestUtil()
        url =host+"/pub/api/v1/web/index_card"
        response = request.request(url,'get')
        self.assertEqual(response['code'],0,'okokok')
        video_list = response['data']
        for card in video_list:
            self.assertTrue(len(card['title'])>0,"sss"+str(card['title']))


if __name__ == '__main__':
    unittest.main()
