import cv2
import boto3
import numpy as np
import random
import string

class ImgReader:
    def __init__(self):
        self.topic_numbers = 7

    def read_img(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        return img

    def check_pixel_size(self, img):
        h, w, c = img.shape
        if h > 4200 and w > 3200:  # 1400万画素以上
            img_size_type = 'size_1400'
        elif h > 3600 and w > 2700:  # 1000万画素以上
            img_size_type = 'size_1000'
        else:
            img_size_type = 'incompatible'
        height_rate = round((h / w), 2)
        return img_size_type, height_rate

    def inclination_correction(self, img, img_size_type, height_rate):
        isError = False
        dst = ''
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.GaussianBlur(image_gray, (47, 47), 0)

        params1, params2, minDist, minRadius, maxRadius = self.makeHoughCirclesParams(img_size_type)
        for param1, param2, md, minr, maxr in zip(params1, params2, minDist, minRadius, maxRadius):
            circles = cv2.HoughCircles(image_gray,cv2.HOUGH_GRADIENT,1,md,param1=param1,param2=param2,minRadius=minr,maxRadius=maxr)
            if circles is not None and len(circles[0]) == 4:
                break

        if isinstance(circles,type(None)) or len(circles[0]) != 4:
            isError = True
        else:
            # 検出した４つの円の座標を取得
            circle_list = self.makeCirclePositionList(circles)

            # 4つの円の右上,右下,左上,左下それぞれの座標を取得 (※ x:1000,y:1000を基準値にして振り分け)
            corners_circle_position_list = self.getCornersCirclePosition(circle_list)

            # 上記4点の座標を使って射影変換による傾き補正を行う
            height_value = round(3000 * height_rate)
            pts1 = np.float32(corners_circle_position_list)
            pts2 = np.float32([[3000,height_value],[3000,0],[0,0],[0,height_value]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(img,M,(3000,height_value))  # 補正した画像をw:3000,h:4000のサイズの画像として変数dstに保存
        return isError, dst

    def check_reading_questionnaire_topics(self, dst):  # 傾き補正した画像からアンケート項目を検出
        points = self.detectTopicPoint(dst, self.topic_numbers)
        # 検出されたアンケート項目の座標をチェックし誤検出していないかチェック(座標が左端から 200以内にあるかチェック && 検出されたポイント同士がy座標基準で+-100以内で被っていないかチェック)
        isError = self.checkFalsePositive(points)

        if len(points) != self.topic_numbers or isError:  # 検出した項目数が想定のアンケート項目数と一致するか
            reading_result = 'fail'
        else:
            reading_result = 'success'

        return reading_result, points

    def download_file(self, bucket_name, file_path):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        save_file_path = "/tmp/"+ self.randomname() + ".jpg"
        bucket.download_file(file_path, save_file_path)
        return save_file_path

    def randomname(self):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
        return ''.join(randlst)

    def makeHoughCirclesParams(self, img_size_type):
        params1 = [30, 30, 30, 10, 10]
        params2 = [40, 30, 20, 10, 10]
        if img_size_type == 'size_1400':
            minDist = [2400, 2300, 2200, 2100, 2000]
            minRadius = [15, 14, 13, 12, 11]
            maxRadius = [100, 95, 90, 85, 80]
        else:
            minDist = [2200, 2100, 2000, 1900, 1800]
            minRadius = [10, 9, 8, 7, 6]
            maxRadius = [80, 75, 70, 65, 60]

        return params1, params2, minDist, minRadius, maxRadius

    def makeCirclePositionList(self, circles):
        c_1 = [circles[0][0][0],circles[0][0][1]]  # [x座標,y座標]
        c_2 = [circles[0][1][0],circles[0][1][1]]
        c_3 = [circles[0][2][0],circles[0][2][1]]
        c_4 = [circles[0][3][0],circles[0][3][1]]
        circle_position_list = [c_1,c_2,c_3,c_4]
        return circle_position_list

    def getCornersCirclePosition(self, circle_list):
        for i in range(0,4):
            if circle_list[i][0] > 1000 and circle_list[i][1] > 1000:  # 右上: x >1000 and y>1000
                upper_right_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] > 1000 and circle_list[i][1] < 1000:  # 右下: x >1000 and y<1000
                under_right_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] < 1000 and circle_list[i][1] > 1000:  # 左上: x <1000 and y>1000
                upper_left_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] < 1000 and circle_list[i][1] < 1000:  # 左下: x <1000 and y<1000
                under_left_circle = [circle_list[i][0],circle_list[i][1]]
        cornersCirclePositionList = [
            upper_right_circle,
            under_right_circle,
            under_left_circle,
            upper_left_circle
        ]
        return cornersCirclePositionList

    def detectTopicPoint(self, dst, questionnaire_topic_numbers):
        Cascade = cv2.CascadeClassifier('cascade.xml')  # 検出器
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        points = Cascade.detectMultiScale(gray, 1.1, 5)
        if len(points) > questionnaire_topic_numbers:
            for q in range(6,15):
                points = Cascade.detectMultiScale(gray, 1.1, q)
                if len(points) == questionnaire_topic_numbers:
                    break
        if len(points) < questionnaire_topic_numbers:
            for q in range(0,4):
                q = 4-q
                points = Cascade.detectMultiScale(gray, 1.1, q)
                if len(points) == questionnaire_topic_numbers:
                    break
        return points

    def checkFalsePositive(self, points):
        isError = False
        p_lists = []
        for p in points:
            p_lists.append(int(p[0]))
        for p in points:
            if int(p[0]) > 200:
                isError = True
                break
            for pl in p_lists:
                if pl < int(p[1]) + 100 and pl > int(p[1]) - 100:
                    isError = True
                    break
        return isError
