import cv2
import json
import pandas as pd

from utils.utils import cv_show, request_ocr
from utils.utils import find_qr_location, parse_qr
from utils.utils import identify_outer_borders
from utils.utils import transform_Coordinate
from utils.utils import post_processing

from structured_process.taxi_receipt import taxi_receipt 
from structured_process.business_license import business_license
from structured_process.household_register import household_register

from flask import Flask,request

app=Flask(__name__)

# 只接受get方法访问
@app.route("/test_1.0",methods=["GET"])
def check():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    img_path = get_data.get('img_path')
    category = get_data.get('category')
    # 
    areacode_unit_address = json.load(open(r'./data_correction/data/areacode_unit_address.json', "r", encoding="utf-8"))
    df_district = pd.read_csv('./data_correction/data/district.csv')

    # 对参数进行操作
    return_dict['result'] = tt(img_path,category, taxi_receipt, business_license, household_register, df_district, areacode_unit_address)
 
    return json.dumps(return_dict, ensure_ascii=False)
 
# 功能函数
def tt(img_path, category, taxi_receipt, business_license, household_register, df_district, areacode_unit_address):
    if category == '0' or category == 'taxi_receipt':
        img = cv2.imread(img_path)
        result = request_ocr(img, detail=False)
        taxi_receipt = taxi_receipt(img, " ".join(result))
        return taxi_receipt.res

    if category == '1' or category == 'business_license':
        img = cv2.imread(img_path)
        list_qr = find_qr_location(img)
        print("找到{}个疑似是二维码的location".format(len(list_qr)))
        url = parse_qr(img, list_qr)
        print(url)
        business_license = business_license(img, url)   
        business_license.res['url'] = url     
        return business_license.res

    if category == '2' or category == 'household_register':
        # areacode_unit_address = json.load(open(r'./data_correction/data/areacode_unit_address.json', "r", encoding="utf-8"))
        # df_district  = pd.read_csv('./data_correction/data/district.csv')

        img = cv2.imread(img_path)
        img_transform = identify_outer_borders(img)  # 寻找边框，投射变换
        output1 = request_ocr(img_transform[:310, 150:450], detail=True)  # 定位姓名、出生地、籍贯区域
        output1 = transform_Coordinate(output1)  # 转坐标
        for x in output1:
            x1, y1, x2, y2 = x['text_box_position']
            x1, y1, x2, y2 = x1 + 150, y1, x2 + 150, y2
            x['text_box_position'] = x1, y1, x2, y2
        output2 = request_ocr(img_transform[:210, 580:800], detail=True)  # 定位户主或与户主关系、性别、民族、出生日期区域
        output2 = transform_Coordinate(output2)
        for x in output2:
            x1, y1, x2, y2 = x['text_box_position']
            x1, y1, x2, y2 = x1 + 580, y1, x2 + 580, y2
            x['text_box_position'] = x1, y1, x2, y2
        output = output1 + output2
        household_register = household_register(img, img_transform, output)
        household_register.re = post_processing(household_register.re, df_district, areacode_unit_address)
        return household_register.re
 
if __name__ == "__main__":
    app.run(debug=True)
