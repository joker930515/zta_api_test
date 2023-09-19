import datetime
import json
import time

from util.db_conn import MysqlDB
from util.requestUtil import requestUtil
from util.send_mail import SendMail


class apiClassTestCase:
    def loadAllCaseByApp(self, app):
        print("loadAllCaseByApp")
        my_db = MysqlDB()
        sql = "select * from `case` where app='{0}'".format(app)
        result = my_db.query(sql, state="all")
        return result

    def findCaseById(self, case_id):
        print("findCaseById")
        my_db = MysqlDB()
        sql = "select * from `case` where id='{0}'".format(case_id)
        result = my_db.query(sql, state="one")
        return result

    def findConfigByAppAndKey(self, app, key):
        print("findConfigByAppAndKey")
        my_db = MysqlDB()
        sql = "select * from `config` where app='{0}' and dict_key='{1}'".format(app, key)
        result = my_db.query(sql)
        return result

    def updateResultByCaseId(self, response, is_pass, msg, case_id):
        print("updateResultByCaseId")
        my_db = MysqlDB()
        currnt_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if is_pass:
            sql = "update `case` set  response='{0}',pass='{1}',msg='{2}',update_time='{3}' where id='{4}'".format("",
                                                                                                                   is_pass,
                                                                                                                   msg,
                                                                                                                   currnt_time,
                                                                                                                   case_id)
        else:
            sql = "update `case` set  response=\"{0}\",pass='{1}',msg='{2}',update_time='{3}' where id='{4}'".format(
                str(response), is_pass, msg, currnt_time, case_id)
        print(sql)
        result = my_db.execute(sql)
        return result

    def runAllCase(self, app):
        print("runAllCase")
        api_host_obj = self.findConfigByAppAndKey(app, "host")
        result = self.loadAllCaseByApp(app)
        for case in result:
            print(case)
            if case['run'] == 'yes':
                try:
                    response = self.runOneCase(case, api_host_obj)
                    assert_msg = self.assertResponse(case, response)
                    rows = self.updateResultByCaseId(response, assert_msg['is_pass'], assert_msg['msg'], case['id'])
                    print(rows)

                except Exception as e:
                    print("id:{0},标题:{1},报错:{2}".format(case['id'], case['title'], e))
        self.sendTestReport(app)

    def runOneCase(self, case, api_host_obj):
        print("runOneCase")
        headers = json.loads(case['headers'])
        body = json.loads(case['request_body'])
        method = case['method']
        print(method, api_host_obj, case)
        req_url = api_host_obj['dict_value'] + case['url']
        print(req_url)

        if case['pre_case_id'] > -1:
            print("前置条件处理")
            pre_case_id = case['pre_case_id']
            pre_case = self.findCaseById(pre_case_id)
            pre_response = self.runOneCase(pre_case, api_host_obj)
            pre_assert_msg = self.assertResponse(pre_case, pre_response)
            print(pre_assert_msg)
            if not pre_assert_msg['is_pass']:
                pre_response['msg'] = "前置条件不通过" + pre_response['msg']
                return pre_response
            pre_fields = json.loads(case['pre_fields'])
            for pre_field in pre_fields:
                print(pre_field)
                if pre_field['scope'] == 'header':
                    for header in headers:
                        field_name = pre_field['field']
                        if header == field_name:
                            field_value = pre_response['data'][field_name]
                            headers[field_name] = field_value
                elif pre_field['scope'] == 'body':
                    print("tihuan body")

        req = requestUtil()
        response = req.request(req_url, method, header=headers, param=body)
        print(response)
        return response

    def assertResponse(self, case, response):
        print("assertResponse")
        assert_type = case['assert_type']
        except_result = case['except_result']
        is_pass = False
        if assert_type == "code":
            response_code = response['code']
            if int(except_result) == response_code:
                is_pass = True
                print("code test case pass")
            else:
                is_pass = False
                print("code test case no pass")
        elif assert_type == "data_json_array":
            data_json_array = response['data']
            if data_json_array is not None and isinstance(data_json_array, list) and len(data_json_array) > int(
                    except_result):
                is_pass = True
                print("data_json_array test case pass")
            else:
                is_pass = False
                print("test case no pass")
        elif assert_type == "data_json":
            data = response['data']
            if data is not None and isinstance(data, dict) and len(data) > int(except_result):
                is_pass = True
                print("data_json test case pass")
            else:
                is_pass = False
                print("test case no pass")
        msg = "模块:{0},标题:{1},断言:{2},响应:msg{3}".format(case['module'], case['title'], assert_type, response['msg'])
        assert_msg = {"is_pass": is_pass, "msg": msg}
        return assert_msg

    def sendTestReport(self, app):
        print("sendTestReport")
        cases = self.loadAllCaseByApp(app)
        title = "测试报告"
        content = """
        <html><body>
            <h4>{0} 接口测试报告：</h4>
            <table border="1">
            <tr>
              <th>编号</th>
              <th>模块</th>
              <th>标题</th>
              <th>是否通过</th>
              <th>备注</th>
              <th>响应</th>
            </tr>
            {1}
            </table></body>
        </html>
        """
        template = ""
        for case in cases:
            template += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                case['id'], case['module'], case['title'], case['pass'], case['msg'], case['response'])
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content.format(current_time,template)
        mail_host = self.findConfigByAppAndKey(app,"mail_host")['dict_value']
        mail_receivers = self.findConfigByAppAndKey(app, "mail_receivers")['dict_value'].split(",")
        mail_auth_code = self.findConfigByAppAndKey(app, "mail_auth_code")['dict_value']
        mail_sender = self.findConfigByAppAndKey(app, "mail_sender")['dict_value']
        mail = SendMail(mail_host)
        mail.send(title,content,mail_sender,mail_auth_code,mail_receivers)



if __name__ == "__main__":
    print("main")
    test = apiClassTestCase()
    result = test.runAllCase("小滴课堂")

