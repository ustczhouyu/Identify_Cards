import re


def fix_idnum(idnum, birthday, birthplace):
    '''
    描述：修正识别的身份证号
    
    输入：
    idnum：识别到的身份证号
    birthday：修正后的出生日期
    bithplace：识别到的出生地

    输出：
    idnum：修正后的身份证号
    '''
    d = {'北京市' : '11',
         '天津市' : '12',
         '河北省' : '13',
         '山西省' : '14',
         '内蒙古自治区' : '15',
         '辽宁省' : '21',
         '吉林省' : '22',
         '黑龙江省' : '23',
         '上海市' : '31',
         '江苏省' : '32',
         '浙江省' : '33',
         '安徽省' : '34',
         '福建省' : '35',
         '江西省' : '36',
         '山东省' : '37',
         '河南省' : '41',
         '湖北省' : '42',
         '湖南省' : '43',
         '广东省' : '44',
         '广西壮族自治区' : '45',
         '海南省' : '46',
         '重庆市' : '50',
         '四川省' : '51',
         '贵州省' : '52',
         '云南省' : '53',
         '西藏自治区' : '54',
         '陕西省' : '61',
         '甘肃省' : '62',
         '青海省' : '63 ',
         '宁夏回族自治区' : '64',
         '新疆维吾尔自治区' : '65'}

    idnum = ''.join(re.findall('[\dX]', idnum))

    year = birthday.split('年')[0]
    areacode = idnum.split(year)[0]

    birthplace ="".join(re.findall('[\u4e00-\u9fa5]',birthplace))
    matchObj = re.match('(\w+省)?(\w+市)?(\w+[区县])?', birthplace)
    province = matchObj[1] 
    city = matchObj[2]
    district = matchObj[3]
    
    # 如果行政区号只有5位，大部分情况是第一位由于压线，导致无法识别，根据省份进行修正
    if len(areacode) >= 4 and len(areacode) < 6:
        if len(areacode) == 5:
            if province in d:
                idnum = d[province] + idnum[1:]
        elif len(areacode) == 4:
            if province in d:
                idnum = d[province] + idnum[:]
    # 身份证号第一位有可能压线，导致识别成1，如身份证号是44142220130528001X，识别成14142220130528001X，检测这种情况
    if len(idnum) == 18 and province and idnum[0] in ['1', '7', '8', '9']:
        idnum = d[province] + idnum[2:]
                
    return idnum

if __name__ == '__main__':
    idnum = fix_idnum('441422201611160059', '2016年11月16日', '广东省广州市白云区')
    print(idnum)
    