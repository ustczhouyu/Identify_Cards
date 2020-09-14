import pyzbar.pyzbar as pyzbar
import requests
import json
import cv2
import base64
import numpy as np
from data_correction.fix_birthday import fix_birthday
from data_correction.fix_birthplace import fix_birthplace
from data_correction.fix_idnum import fix_idnum


def cv_show(name,img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def request_ocr(img, detail=False):
    def cv2_to_base64(image):
        data = cv2.imencode(r'.jpg', image)[1]
        return base64.b64encode(data.tostring()).decode('utf8')

    headers = {"Content-type": "application/json"}
    url = "http://192.168.63.8:18889/predict/chinese_ocr_db_crnn_mobile"
    img_base64 = cv2_to_base64(img)

    data = {'images': [img_base64]}
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = r.json()["results"]
    result_detail = result[0]['data']
    if detail:
        return result_detail
    else:
        result = []
        for x in result_detail:
            result.append(x['text'])
        return result

def find_qr_location(img):
    # 灰度处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv_show('gray', gray)

    # 二值处理
    binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # cv_show('binary', binary)

    # 膨胀处理
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    gradX = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, rectKernel)
    # cv_show('gradX', gradX)

    _, cnts, hierarchy = cv2.findContours(
        gradX.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    edges = cv2.drawContours(img.copy(), cnts, -1, (0, 255, 0), 1)
    # cv_show('edges', edges)

    w0, h0 = img.shape[1], img.shape[0]
    # 遍历轮廓，找出二维码的区域
    list_qr = []
    for (i, c) in enumerate(cnts):
        # 计算矩形
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if 0.7 < ar < 1.3 and 10 < w < 0.2*w0 and 10 < h < 0.15*h0 and ((x < 0.4*w0 and y > 0.5*h0) or (x > 0.6*w0 and y < 0.5*h0)):
            list_qr.append((x, y, w, h))

    return list_qr

def parse_qr(img, list_qr):
    list_urls = []
    for (i, (gX, gY, gW, gH)) in enumerate(list_qr):
        # initialize the list of group digits
        # 根据坐标提取每一个组
        # 放置越界
        try:
            img_qr = img[gY - 20 :gY + gH + 20, gX - 20 :gX + gW +20]
            img_qr = cv2.resize(img_qr, (0, 0), fx=1.5, fy=1.5)  # 放大区域
        except:
            continue    

        barcodes = pyzbar.decode(img_qr)    

        for barcode in barcodes:
            list_urls.append(barcode.data.decode("utf-8"))
    if len(list_urls) == 1:
        url = list_urls[0]
        print(url)
        return url
    elif len(list_urls) == 0:
        print('not found qr!!!!')
        return None

def order_points(pts):
    # 一共4个坐标点
    rect = np.zeros((4, 2), dtype = "float32")

    # 按顺序找到对应坐标0123分别是 左上，右上，右下，左下
    # 计算左上，右下
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 计算右上和左下
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(img, pts):
    # 获取输入坐标点
    rect = order_points(pts)  
    (tl, tr, br, bl) = rect

    # 计算输入的w和h值
#     widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#     widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#     maxWidth = max(int(widthA), int(widthB))

#     heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#     heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#     maxHeight = max(int(heightA), int(heightB))

    # 变换后对应坐标位置
    dst = np.array([
        [0, 0],
        [800, 0],
        [800, 500],
        [0, 500]], dtype = "float32")

    # 计算变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (800, 500))

    # 返回变换后结果
    return warped

def identify_outer_borders(img):
    # 灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv_show('gray', gray)

    # 二值
    binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    # cv_show('binary', binary)

    rows, cols = binary.shape
    scale = 44
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols//scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    #cv2.imshow("Eroded Image",eroded)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    # cv_show("表格横线展示：", dilatedcol)

    # 识别竖线
    scale = 44
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
    eroded = cv2.erode(binary,kernel,iterations = 1)
    dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)
    # cv_show("表格竖线展示：", dilatedrow)

    # 标识交点
    bitwiseAnd = cv2.bitwise_and(dilatedcol,dilatedrow)
    # cv_show("表格交点展示：",bitwiseAnd)

    # 标识表格
    merge = cv2.add(dilatedcol,dilatedrow)
    # cv_show("表格整体展示：",merge)

    # #两张图片进行减法运算，去掉表格框线
    # merge2 = cv2.subtract(binary,merge)
    # cv_show("图片去掉表格框线展示：",merge2)

    # 寻找轮廓
    _, cnts, hierarchy =  cv2.findContours(merge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    edges =  cv2.drawContours(img.copy(), cnts, -1, (0,255,0), 1)
    # cv_show('edges', edges)

    # 定位外轮廓
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    for c in cnts:
        # 计算轮廓近似
        peri = cv2.arcLength(c, True)
        # C表示输入的点集
        # epsilon表示从原始轮廓到近似轮廓的最大距离，它是一个准确度参数
        # True表示封闭的
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # 4个点的时候就拿出来
        if len(approx) == 4:
            if sum(approx[0].flatten()) < 20:
                continue
            screenCnt = approx
            break

    edge = cv2.drawContours(img.copy(), [screenCnt], -1, (0, 0, 255), 2)
    # cv_show('edge', edge)

    warped = four_point_transform(img, screenCnt.squeeze())  # 关键一步
    # cv_show('test', warped)

    return warped

def transform_Coordinate(list):
    for x in list:
        x1,y1 = x['text_box_position'][0]  # 左上
        x2,y2 = x['text_box_position'][1]  # 右上
        x3,y3 = x['text_box_position'][2]  # 右下
        x4,y4 = x['text_box_position'][3]  # 左下
        x['text_box_position'] = (x1, y1, x3, y3)

    return list

def post_processing(re, df_district, areacode_unit_address):

    if '出生日期' in re.keys() and '身份证号' in re.keys():
        re['出生日期'] = fix_birthday(re['出生日期'], re['身份证号'])
    if '出生日期' in re.keys() and '身份证号' in re.keys() and '籍贯' in re.keys():
        re['身份证号'] = fix_idnum(re['身份证号'], re['出生日期'], re['籍贯'])
    if '身份证号' in re.keys() and '籍贯' in re.keys():
        re['籍贯'] = fix_birthplace(re['籍贯'], re['身份证号'], df_district, areacode_unit_address)
    if '身份证号' in re.keys() and '出生地' in re.keys():
        re['出生地'] = fix_birthplace(re['出生地'], re['身份证号'], df_district, areacode_unit_address)

    return re