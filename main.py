import json
from datetime import datetime

import requests
import time
import uuid

import schedule
import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

JS_SERVICE_URL = os.environ.get("JS_SERVICE_URL", default="http://127.0.0.1:13451")

OPENID = os.environ.get("QH_OPENID", default="")
USERID = os.environ.get("QH_USERID", default="")
USER_TOKEN = os.environ.get("QH_USER_TOKEN", default="")


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
        'token': USER_TOKEN,
        'userId': userId,
        'xweb_xhr': '1'
    }, timeout=30)

    if response.status_code != 200:
        print('请求失败：', response.text)
        return None

    return response.json()


def regTargets(hisDeptId='0139'):
    """
    获取预约挂号列表
    :return:
    """
    url = 'https://zyyapp.tongrentangcare.com:10052/patient/v1/appoint/regTargets'
    request_data = {
        "hisDeptId": hisDeptId,
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


def try_booking(drId, startDate, endDate, maxattempts=50):
    """
    开始尝试预约挂号
    :param drId:
    :param startDate:
    :param endDate:
    :param maxattempts:
    :return:
    """
    attempt = 0

    while attempt < maxattempts:
        try:
            attempt += 1
            print(f"Attempt {attempt} of {maxattempts}")

            drId = drId  # 医生ID
            startDate = startDate  # 挂号开始时间
            endDate = endDate  # 挂号结束时间点

            # Query available appointment times
            reg_points_data = regPoints(drId, startDate, endDate)

            reg_points = list(reg_points_data['data']["regPoints"].values())

            if len(reg_points) == 0:
                print('没有可预约的时间点')
                continue

            reg_points = reg_points[0]

            curr_reg_point = None
            for reg_point in reg_points:
                if int(reg_point['rmngNum']) > 0:
                    curr_reg_point = reg_point
                    break

            if curr_reg_point is None:
                print('没有可预约的时间点')
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


def job(drId, startDate, endDate, maxattempts=50):
    """
    执行任务
    :param drId:
    :param startDate:
    :param endDate:
    :return:
    """
    current_time = datetime.now()
    print(f"Starting booking job at {current_time}")
    try_booking(drId, startDate, endDate, maxattempts)


def get_args():
    if getattr(sys, 'frozen', False):
        # 打包后的处理
        args = []
        try:
            # 获取实际传入的参数
            args = sys.argv[1:]
        except Exception:
            args = []
    else:
        # 开发环境下的参数
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='小程序抢号助手')
    parser.add_argument('-type', type=int, help='启动方式: 1定时任务, 2立即运行一次, 3查看当前支持的医生列表', default=2)
    parser.add_argument('-time', type=str, help='定时抢票时间点, 如14:59:58', default='14:59:58')
    parser.add_argument('-drid', type=int, help='医生ID, 如:248', default=248)
    parser.add_argument('-startdate', type=int, help='挂号开始日期, 20241109', default='20241109')
    parser.add_argument('-enddate', type=int, help='挂号结束日期, 20241231', default='20241231')
    parser.add_argument("-maxattempts", type=int, help="最大尝试次数", default=50)

    if '-h' in args or '--help' in args:
        parser.print_help()
        print("\n如果不清楚医生ID, 使用 -type 3 查看当前支持的医生列表")
        print("\n注意事项：")
        print("- 为了保证抢号成功, 请将患者列表中仅保留一位患者信息, 或者需要预约的患者信息在第一位")
        print("- 时间格式必须是24小时制，例如：08:00:00、15:30:00")
        print("- 日期格式必须是8位数字，例如：20241109")
        print("- 定时任务模式下程序会持续运行，每天在指定时间执行")
        print("- 立即运行模式下程序执行一次后就会退出")
        sys.exit(0)

    return parser.parse_args(args)


def printRegTargets():
    """
    打印预约挂号列表
    :return:
    """
    reg_targets = regTargets()
    if reg_targets.get('status') != 0:
        print('获取数据失败')
        return

    print(f"医生名称 -------- 医生ID")
    for item in reg_targets.get('data',{}).get('regTargets',[]):
        print(f"{item.get('name')} -------- {item.get('targetId')}")

if __name__ == '__main__':
    args = get_args()

    print(f"当前用户: {USERID} / {OPENID}")

    if args.type == 3:
        printRegTargets()
        sys.exit(0)

    if args.type == 2:
        job(args.drid, args.startdate, args.enddate, args.maxattempts)
        sys.exit(0)

    schedule.every().day.at(args.time).do(job, args.drid, args.startdate, args.enddate, args.maxattempts)

    print(f"Scheduler started. Waiting for {args.time}...")

    while True:
        schedule.run_pending()
        time.sleep(0.1)  # 使用0.1秒间隔来提高精度
