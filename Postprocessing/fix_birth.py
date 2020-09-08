import re

def fix_birthday(birthday, id_num):
    id_num = str(id_num)
    try:  # 保险一点的做法
        matchObj = re.match(r'(\d+)年(\d+)月(\d+)日', birthday)
        year = matchObj.group(1)
        month = matchObj.group(2)
        day = matchObj.group(3)
    except:  # 放宽的做法
        matchObj = re.findall('\d+', birthday)
        if len(matchObj) >= 3:
            year = matchObj[0]
            month = matchObj[1]
            day = matchObj[2]
        else:
            year = '0000'
            month = '00'
            day = '00'   

    if len(year) != 4:
        if len(id_num) == 18:
            year = id_num[6:10]
    if len(month) == 1:
        month = "0" + month
    elif len(month) == 0:
        if len(id_num) == 18:
            month = id_num[10:12]
        if year in id_num and len(year) == 4:
            month = id_num.split(year)[1][0:2]

    if len(day) == 1:
        day = "0" + day
    elif len(day) == 0:
        if len(id_num) == 18:
            day = id_num[12:14]
        if year in id_num and len(year) == 4:
            day = list(id_num.split(year)[1][2:4])
    y_m_d = year + month + day
    # 可靠性高，不用纠正
    if y_m_d in id_num and len(y_m_d) == 8:
        return y_m_d[:4] + '年' + y_m_d[4:6] + '月' + y_m_d[6:] + '日'
    else:
        start_loc = 6  # 定位身份证出生日期起始位置， 粗略定位，用年、日月
        if year in id_num and len(year) == 4:
            start_loc = len(id_num.split("".join(self.year))[0])
        elif month + day in id_num:
            start_loc = len(id_num) - len(id_num.split(month + day)[-1]) - 8
        valid_bir = judge_birth(y_m_d)  # 判断出生日期有没有问题
        if not valid_bir:  # 出生日期存在问题
            valid_bir = judge_birth(id_num[start_loc:start_loc+8])
            if valid_bir:  # 身份证信息没有问题，直接替换
                y_m_d = id_num[start_loc:start_loc + 8]
                return y_m_d[:4] + '年' + y_m_d[4:6] + '月' + y_m_d[6:] + '日'
            else:  # 身份证信息存在问题
                y_m_d, id_num = correct_birth(y_m_y, id_num[start_loc: start_loc+8])  # 互相纠错
                return y_m_d[:4] + '年' + y_m_d[4:6] + '月' + y_m_d[6:] + '日'

def judge_birth(date):
    
    if len(date) < 8:
        return False
    if len(date) > 8:
        return False
    for i in date:
        if i not in "0123456789":
            return False
    if (date[:2] != '19' and date[:2] != '20') or date[4] not in '01':
        return False
    if date[6] not in "0123":
        return False
    if date[6] == "3":
        if date[7] not in "01":
            valid_bir = False
    
    return True

def correct_birth(self, date1, date2):

    if len(date1) < 8:
        for i in range(8 - len(date1)):
            date1.append("0")
    if len(date2) < 8:
        for i in range(8 - len(date2)):
            date2.append("0")
    for index, i in enumerate(date1):
        if date1[index] not in "0123456789" and date2[index] in "0123456789":
            date1[index] = date2[index]
        elif date2[index] not in "0123456789" and date1[index] in "0123456789":
            date2[index] = date1[index]
        elif date2[index] not in "0123456789" and date1[index] not in "0123456789":
            date2[index] = date1[index] = "0"
    if (date1[:2] != '19' and date1[:2] != '20') and (
            date2[:2] != '19' and date2[:2] != '20'):
        date1[:2] = date2[:2] = list('19')
    elif date1[:2] != '19' and date1[:2] != '20':
        date1[:2] = date2[:2]
    else:
        date2[:2] = date1[:2]
    # 月
    if date1[4] not in "01" and date2[4] in "01":
        date1[4] = date2[4]
    elif date2[4] not in "01" and date1[4] in "01":
        date2[4] = date1[4]
    elif date2[4] not in "01" and date1[4] not in "01":
        date2[4] = date1[4] = "0"
    # 日
    if date1[6] not in "0123" and date2[6] in "0123":
        date1[6] = date2[6]
    elif date2[6] not in "0123" and date1[6] in "0123":
        date2[6] = date1[6]
    elif date2[6] not in "0123" and date1[6] not in "0123":
        date2[6] = date1[6] = "0"
    if date1[6] == "3":
        if date1[7] not in "01" and date2[7] in "01":
            date1[7] = date2[7]
        else:
            date1[7] = "0"
    if date2[6] == "3":
        if date2[7] not in "01" and date1[7] in "01":
            date2[7] = date1[7]
        else:
            date2[7] = "0"

    return date1, date2

if __name__ == '__main__':
    birthday = fix_birthday('990年12月14日', '11302199012143211')
    print(birthday)