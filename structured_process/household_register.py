class household_register:
    def __init__(self, img, img_transform, result):
        self.img = img
        self.img_transform = img_transform
        self.result = result
        self.re = {}
        self.field_location = {
            "姓名"  :    (150, 0, 450, 60),
            "出生地":    (150, 90, 450, 160),
            "籍贯":      (150, 140, 450, 210),
            "身份证号":  (150, 240, 450, 310),
            "与户主关系":(580, 0, 800, 60),
            "性别":      (580, 40, 800, 110),
            "民族":      (580, 90, 800, 160),
            "出生日期":   (580, 140, 800, 210)
            }

            # cv_show('temp', warped[:310, 150:450])  # 姓名
            # cv_show('temp', warped[90:160, 150:450])  # 出生地
            # cv_show('temp', warped[140:210, 150:450])  # 籍贯
            # cv_show('temp', warped[240:310, 150:450])  # 身份证号

            # cv_show('temp', warped[:210, 580:800])  # 与户主关系
            # cv_show('temp', warped[40:110, 580:800])  # 性别
            # cv_show('temp', warped[90:160, 580:800])  # 民族
            # cv_show('temp', warped[140:210, 580:800])  # 出生日期
        self.extract_structured_fields()
        
    def calc_area(self, rect1, rect2):
        xl1, yb1, xr1, yt1 = rect1
        xl2, yb2, xr2, yt2 = rect2
        xmin = max(xl1, xl2)
        ymin = max(yb1, yb2)
        xmax = min(xr1, xr2)
        ymax = min(yt1, yt2)
        width = xmax - xmin
        height = ymax - ymin
        if width <= 0 or height <= 0:
            return 0
        cross_square = width * height
        return cross_square

    def extract_structured_fields(self):
        d = {"姓名":0 , "出生地":0, "籍贯":0, "身份证号": 0, "与户主关系": 0, "性别":0, "民族":0, "出生日期":0}
        for x in self.result:
            area_x = x['text_box_position']
            record = 0
            for key, area_y in self.field_location.items():
                area_intersection = self.calc_area(area_x, area_y)
                if area_intersection > record and area_intersection != 0:
                    if area_intersection > d[key] and area_intersection > 20:
                        d[key] = area_intersection
                        self.re[key] = x['text']
                    record = area_intersection




            