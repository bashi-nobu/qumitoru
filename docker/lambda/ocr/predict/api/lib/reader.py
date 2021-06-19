import cv2
import boto3
import numpy as np
import os
import random
import string

BUCKET_NAME = os.environ.get('BUCKET_NAME')

class ImgReader:
    def __init__(self):
        self.topic_numbers = 7

    def read_img(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        return img

    def check_pixel_size(self, img):
        h, w, c = img.shape
        if h > 4200 and w > 3200:
            img_size_type = 'size_1400'
        elif h > 3600 and w > 2700:
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
            if len(circles[0]) == 4:
                break

        if isinstance(circles,type(None)) or len(circles[0]) != 4:
            isError = True
        else:
            circle_list = self.makeCirclePositionList(circles)
            corners_circle_position_list = self.getCornersCirclePosition(circle_list)

            height_value = round(3000 * height_rate)
            pts1 = np.float32(corners_circle_position_list)
            pts2 = np.float32([[3000,height_value],[3000,0],[0,0],[0,height_value]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(img,M,(3000,height_value))
        return isError, dst

    def checkReadingQuestionnaireTopics(self, dst):
        points = self.detectTopicPoint(dst, self.topic_numbers)
        isError = self.checkFalsePositive(points)

        if len(points) != self.topic_numbers or isError:
            reading_result = 'fail'
        else:
            reading_result = 'success'

        return reading_result, points

    def download_file(self, bucket_name, file_path):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.download_file(file_path, '/tmp/target.jpg')

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
        c_1 = [circles[0][0][0],circles[0][0][1]]
        c_2 = [circles[0][1][0],circles[0][1][1]]
        c_3 = [circles[0][2][0],circles[0][2][1]]
        c_4 = [circles[0][3][0],circles[0][3][1]]
        circle_position_list = [c_1,c_2,c_3,c_4]
        return circle_position_list

    def getCornersCirclePosition(self, circle_list):
        for i in range(0,4):
            if circle_list[i][0] > 1000 and circle_list[i][1] > 1000:
                upper_right_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] > 1000 and circle_list[i][1] < 1000:
                under_right_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] < 1000 and circle_list[i][1] > 1000:
                upper_left_circle = [circle_list[i][0],circle_list[i][1]]
            elif circle_list[i][0] < 1000 and circle_list[i][1] < 1000:
                under_left_circle = [circle_list[i][0],circle_list[i][1]]
        cornersCirclePositionList = [
            upper_right_circle,
            under_right_circle,
            under_left_circle,
            upper_left_circle
        ]
        return cornersCirclePositionList

    def detectTopicPoint(self, dst, questionnaire_topic_numbers):
        Cascade = cv2.CascadeClassifier('cascade.xml')
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

    def exportQuestionnaireTopicImg(self, dst, point, questionare_topic_numbers):
        scale_h={}
        scale_img_list = []
        h_min = self.checkMinTopicsHeight(point, questionare_topic_numbers)
        for i in range(0,len(point)):
            saved_file_path = '/tmp/'+self.randomname()+'.jpg'
            h = (h_min * 4) + 30
            imgs = dst[point[i][1]+point[i][3]:point[i][1]+h, point[i][0]:3000]
            imgs = cv2.resize(imgs,(2000, 140))
            cv2.imwrite(saved_file_path, imgs)
            none_noise_img = self.noiseRemoval(saved_file_path)
            image = cv2.bitwise_not(none_noise_img)
            cv2.imwrite(saved_file_path, image)
            scale_h[point[i][1]] = saved_file_path
        for k, v in sorted(scale_h.items()):
            scale_img_list.append(str(v))
        return scale_img_list

    def checkMinTopicsHeight(self, point, questionare_topic_numbers):
        h_list=[]
        for i in range(0, questionare_topic_numbers):
            h_list.append(int(point[i][3]))
        h_min = min(h_list)
        return h_min

    def noiseRemoval(self, save_path):
        im = cv2.imread(save_path)
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        imgray = cv2.GaussianBlur(imgray, (9,9), 0)
        th = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,19,2)
        invgray = cv2.bitwise_not(th)
        kernel = np.ones((4,4),np.uint8)
        none_noise_img = cv2.morphologyEx(invgray, cv2.MORPH_OPEN, kernel)
        return none_noise_img

    def randomname(self):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
        return ''.join(randlst)

    def resize_img_write_func(self, file_path, width_size, height_size):
        img = cv2.imread(file_path)
        imgs= cv2.resize(img,(width_size,height_size))
        cv2.imwrite(file_path, imgs)
        os.chmod(file_path, 0o777)
