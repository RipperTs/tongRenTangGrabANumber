import json
from datetime import datetime

import requests
import time
import uuid

import schedule

JS_SERVICE_URL = 'http://127.0.0.1:13451'

OPENID = 'olIH15BXwyP3YdaKo1RiJEm3Yvbk'
USERID = '420538'


def parameter_encryption(request_data):
    """
    请求参数加密算法
    :return:
    """
    url = JS_SERVICE_URL + '/encrypt'
    response = requests.post(url, json={
        'data': request_data
    }, timeout=10)

    try:
        result_json = json.loads(response.text)
    except Exception as e:
        print('请求参数加密失败：', response.text)
        result_json = {}

    return result_json.get('encrypted', '')


def get_signature(request_data):
    """
    获取签名
    :return:
    """
    url = JS_SERVICE_URL + '/signature'
    uuid_str = str(uuid.uuid4())
    response = requests.post(url, json={
        'data': request_data,
        'uuid': uuid_str
    }, timeout=10)

    try:
        result_json = json.loads(response.text)
    except Exception as e:
        print('获取签名失败：', response.text)
        result_json = {}

    return result_json.get('signature', ''), uuid_str


def build_base_request(url, method, data):
    """
    构建基础请求
    :return:
    """
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0MjA1MzgiLCJleHAiOjE3NjI2MDU3Mjd9.rKt8Alb-SeZcjrdZTiwN6NZanHMkHGwFPiMY9IcyUKM'
    userId = USERID
    signature, uuid_str = get_signature(data)
    requestData = parameter_encryption(data)

    response = requests.request(method, url, json={
        "requestData": requestData,
    }, headers={
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://servicewechat.com/wxfdf596bc524fc2ea/21/page-frame.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080813) XWEB/1227',
        'appId': 'wxfdf596bc524fc2ea',
        'appKind': '1',
        'appMark': '1',
        'appType': '5',
        'appVersion': '1.0',
        'hospitalId': '80034',
        'nonce': uuid_str,
        'signature': signature,
        'timestamp': str(int(time.time() * 1000)),
        'token': token,
        'userId': userId,
        'xweb_xhr': '1'
    }, timeout=30)

    if response.status_code != 200:
        print('请求失败：', response.text)
        return None

    return response.json()


def regTargets():
    """
    获取预约挂号列表
    :return:
    """
    url = 'https://zyyapp.tongrentangcare.com:10052/patient/v1/appoint/regTargets'
    request_data = {
        "hisDeptId": "0139",
        "targetType": 1,
        "patientId": "",
        "pageSize": "9999",
        "pageNo": "1",
        "appId": "wxfdf596bc524fc2ea",
        "openId": OPENID,
        "hospId": 80034,
        "hospitalId": 80034
    }

    return build_base_request(url, 'POST', request_data)


def getDoctorDetails(drId):
    """
    获取医生详情
    :param drId:
    :return:
    """
    url = "https://zyyapp.tongrentangcare.com:10052/patient/v1/appoint/regTargets"
    request_data = {"drId": drId, "targetType": 1, "isNeedDoctorDate": 1, "pageNo": 1, "pageSize": 9999,
                    "mbFlag": "undefined", "appId": "wxfdf596bc524fc2ea", "openId": OPENID,
                    "hospId": 80034, "hospitalId": 80034}
    return build_base_request(url, 'POST', request_data)


def regPoints(drId, startDate, endDate, deptId='277'):
    """
    获取指定医生指定时间的预约挂号时间点
    :param drId:
    :param startDate:
    :param endDate:
    :return:
    """
    url = 'https://zyyapp.tongrentangcare.com:10052/patient/v1/appoint/regPoints'
    request_data = {"deptId": deptId, "targetId": drId, "targetType": "1", "startDate": startDate,
                    "endDate": endDate, "pageNo": "1", "pageSize": "999", "mbFlag": "undefined",
                    "appId": "wxfdf596bc524fc2ea", "openId": OPENID, "hospId": 80034,
                    "hospitalId": 80034}

    return build_base_request(url, 'POST', request_data)


def queryPatients():
    """
    预约挂号确认页面数据查询
    :return:
    """
    url = "https://zyyapp.tongrentangcare.com:10052/patient/v1/myself/queryPatients"
    request_data = {"dictTypes": ["MARK_TYPE", "PAPERS_TYPE"], "appId": "wxfdf596bc524fc2ea",
                    "openId": OPENID, "hospId": 80034, "hospitalId": 80034}
    return build_base_request(url, 'POST', request_data)


def regPoint(drId, patientId, pointId, pointName,
             pointDate, regLevelId, regLevelName,
             deptId, startTime, endTime,
             totalFee, noonId, noonName):
    """
    生成预约订单
    :param drId:  医生ID
    :param patientId:  患者ID, 在queryPatients接口中获取
    :param pointId: pointId
    :param pointName:
    :param pointDate:
    :param regLevelId:
    :param regLevelName:
    :param deptId:
    :return:
    """
    url = 'https://zyyapp.tongrentangcare.com:10052/patient/v1/appoint/regPoint'
    request_data = {"pointId": pointId, "pointName": pointName, "pointDate": pointDate, "regLevelId": regLevelId,
                    "regLevelName": regLevelName, "patientId": patientId, "deptId": deptId, "drId": drId,
                    "visitTime": startTime, "medInsType": "", "specialDeptType": "",
                    "beginTime": startTime, "endTime": endTime, "diagnoseFee": totalFee, "noonId": noonId,
                    "noonName": noonName, "regFee": "", "inspectFee": "", "hisDeptId": "", "referenceCode": "",
                    "mbFlag": "undefined", "appId": "wxfdf596bc524fc2ea", "openId": OPENID,
                    "hospId": 80034, "hospitalId": 80034}

    return build_base_request(url, 'POST', request_data)


def regHospPay(orderId, regId):
    """
    确认订单预约完成
    :return:
    """
    url = 'https://zyyapp.tongrentangcare.com:10052/patient/v1/pay/regHospPay'
    request_data = {"orderId": orderId, "regId": regId, "appId": "wxfdf596bc524fc2ea",
                    "openId": OPENID, "hospId": 80034, "hospitalId": 80034}

    return build_base_request(url, 'POST', request_data)


def try_booking():
    max_attempts = 50
    attempt = 0

    while attempt < max_attempts:
        try:
            attempt += 1
            print(f"Attempt {attempt} of {max_attempts}")

            drId = '248'
            startDate = '20241109'
            endDate = '20241231'

            # Query available appointment times
            reg_points_data = regPoints(drId, startDate, endDate)
            reg_points = list(reg_points_data['data']["regPoints"].values())[0]

            curr_reg_point = None
            for reg_point in reg_points:
                if int(reg_point['rmngNum']) > 0:
                    curr_reg_point = reg_point
                    break

            if curr_reg_point is None:
                print('没有可预约的时间点')
                time.sleep(1)  # Wait 1 second before next attempt
                continue

            patients = queryPatients()
            patient = patients['data']['getPatientsResp']['patients'][0]

            # Book appointment
            regPointResult = regPoint(drId=drId,
                                      patientId=patient['patientId'],
                                      pointId=curr_reg_point['pointId'],
                                      pointName=curr_reg_point['pointName'],
                                      pointDate=curr_reg_point['pointDate'],
                                      regLevelId=curr_reg_point['regLevelId'],
                                      regLevelName=curr_reg_point['regLevelName'],
                                      deptId=curr_reg_point['deptId'],
                                      startTime=curr_reg_point['startTime'],
                                      endTime=curr_reg_point['endTime'],
                                      totalFee=curr_reg_point['totalFee'],
                                      noonId=curr_reg_point['noonId'],
                                      noonName=curr_reg_point['noonName'])

            regHospPayResult = regHospPay(regPointResult['data']['orderId'],
                                          regPointResult['data']['regId'])

            if regHospPayResult['status'] == 0:
                print('预约成功')
                return True

            time.sleep(0.5)  # Wait 1 second before next attempt

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            time.sleep(0.5)  # Wait 1 second before next attempt
            continue

    print("已达到最大尝试次数。预约失败。")
    return False


def job():
    current_time = datetime.now()
    print(f"Starting booking job at {current_time}")
    try_booking()


if __name__ == '__main__':
    # Schedule the job to run at 15:00 (3 PM) every day
    schedule.every().day.at("15:00").do(job)

    print("Scheduler started. Waiting for ...")

    while True:
        schedule.run_pending()
        time.sleep(1)

