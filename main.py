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


if __name__ == "__main__":


    # 发票-出租车票据
    # img = cv2.imread(r"C:\Users\ZHOU-JC\Desktop\829.png")
    # result = request_ocr(img, detail=False)
    # taxi_receipt = taxi_receipt(img, " ".join(result))
    # print(result)
    # print(taxi_receipt.res)

    # 证件-营业执照
    img = cv2.imread(r"C:\Users\ZHOU-JC\Desktop\3771_3652782ab85ce3fa4575e2bdce504fea.jpg")
    list_qr = find_qr_location(img)
    print("找到{}个疑似是二维码的location".format(len(list_qr)))
    url = parse_qr(img, list_qr)
    business_license = business_license(img, url)
    print(business_license.res)

    # 证件-户口本
    # areacode_unit_address = json.load(open(r'./data_correction/data/areacode_unit_address.json', "r", encoding="utf-8"))
    # df_district  = pd.read_csv('./data_correction/data/district.csv')

    # img = cv2.imread(r'C:\Users\ZHOU-JC\Desktop\4.jpg')
    # img_transform = identify_outer_borders(img)  # 寻找边框，投射变换
    # output1 = request_ocr(img_transform[:310, 150:450], detail=True)  # 定位姓名、出生地、籍贯区域
    # output1 = transform_Coordinate(output1)  # 转坐标
    # for x in output1:
    #     x1, y1, x2, y2 = x['text_box_position']
    #     x1, y1, x2, y2 = x1 + 150, y1, x2 + 150, y2
    #     x['text_box_position'] = x1, y1, x2, y2
    # output2 = request_ocr(img_transform[:210, 580:800], detail=True)  # 定位户主或与户主关系、性别、民族、出生日期区域
    # output2 = transform_Coordinate(output2)
    # for x in output2:
    #     x1, y1, x2, y2 = x['text_box_position']
    #     x1, y1, x2, y2 = x1 + 580, y1, x2 + 580, y2
    #     x['text_box_position'] = x1, y1, x2, y2
    # output = output1 + output2
    # household_register = household_register(img, img_transform, output)
    # print(household_register.re)
    # household_register.re = post_processing(household_register.re, df_district, areacode_unit_address)
    # print(household_register.re)
    # a = 1