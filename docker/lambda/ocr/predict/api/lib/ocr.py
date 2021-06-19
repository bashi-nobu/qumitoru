import numpy as np
import tensorflow as tf
import cv2
import os
import s3_lib as s3Lib
import reader

BUCKET_NAME = os.environ.get('BUCKET_NAME')
imgReader = reader.ImgReader()

# 10点尺度の認識処理をするtensorflowファイルのパス指定
DEFAULT_INPUT_GRAPHDEF_ten = 'scale1_predict_model.pb'
DEFAULT_INPUT_GRAPHDEF_ten_none_check = 'scale1_none_check_predict_model.pb'

# 5点尺度の認識処理をするtensorflowファイルのパス指定
DEFAULT_INPUT_GRAPHDEF_five = 'scale2_predict_model.pb'
DEFAULT_INPUT_GRAPHDEF_five_none_check = 'scale2_none_check_predict_model.pb'

class ocrQuestionare:

    def ten_scale_ocr(self, file_path):
        imgReader.resize_img_write_func(file_path,400,30)
        sess = tf.Session()
        with tf.gfile.GFile(DEFAULT_INPUT_GRAPHDEF_ten_none_check,'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def,name = '')

        prediction = self.predictScoreUsingCnn(sess,file_path)
        none_check = np.argmax(prediction)

        if none_check == 0:
            ocr_result = -1
        else:
            sess = tf.Session()
            with tf.gfile.GFile(DEFAULT_INPUT_GRAPHDEF_ten,'rb') as f:
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def,name = '')
            prediction = self.predictScoreUsingCnn(sess,file_path)
            ocr_result = int(np.argmax(prediction))
            os.remove(file_path)
        sess.close()
        return ocr_result

    def five_scale_ocr(self, file_path):
        imgReader.resize_img_write_func(file_path,400,30)
        sess = tf.Session()
        with tf.gfile.GFile(DEFAULT_INPUT_GRAPHDEF_five_none_check,'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def,name = '')
        prediction = self.predictScoreUsingCnn(sess,file_path)
        none_check = np.argmax(prediction)

        if none_check == 0:
            ocr_result = -1
        else:
            sess = tf.Session()
            with tf.gfile.GFile(DEFAULT_INPUT_GRAPHDEF_five,'rb') as f:
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def,name = '')

            prediction = self.predictScoreUsingCnn(sess,file_path)
            ocr_result = int(np.argmax(prediction)+1)
        os.remove(file_path)
        sess.close()
        return ocr_result


    def predictScoreUsingCnn(self, sess, img):
        image = cv2.imread(img,0)
        image = np.reshape(image, (30, 400,1))
        image_list = [image]
        image = np.asarray(image_list)
        X = image.astype('float32')
        X = X / 255.0
        prediction = sess.run('strided_slice:0',{'conv2d_1_input:0':X})
        tf.compat.v1.reset_default_graph()
        return prediction


    def questionareOcr(self, scale_patarn, file_path, s3):
        img = s3Lib.download_file(BUCKET_NAME, file_path)
        if scale_patarn == 10:
            ocr_result = self.ten_scale_ocr(img)
        else:
            ocr_result = self.five_scale_ocr(img)
        return ocr_result
