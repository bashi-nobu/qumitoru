import pymysql
import os

def connectDB():
    host = os.environ.get('DB_HOST')
    user = os.environ.get('DB_USER')
    db_name = os.environ.get('DB_NAME')
    password = os.environ.get('DB_PASS')
    mysql_connection = pymysql.connect(host=host, port=3306, user=user, password=password, db=db_name, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return mysql_connection

def get_questionare_data(target_record_id):
    mysql_connection = connectDB()
    with mysql_connection.cursor() as cursor:
        sql = "SELECT * FROM `questionnaire_questionarescore` WHERE id = " + str(target_record_id)
        cursor.execute(sql)
        mysql_connection.commit()
    results=cursor.fetchall()
    mysql_connection.close()
    return results[0]

def saveOcrResult(scores, target_record_id):
    # 質問項目が10項目未満の場合はその差分は空値を挿入
    for i in range(0, 9-len(scores)):
        scores.append(-1)
    mysql_connection = connectDB()
    with mysql_connection.cursor() as cursor:
        sql = "UPDATE questionnaire_questionarescore SET q1=%s,q2=%s,q3=%s,q4=%s,q5=%s,q6=%s,q7=%s,q8=%s,q9=%s,is_finished=%s WHERE id=%s"
        cursor.execute(sql,(scores[0],scores[1],scores[2],scores[3],scores[4],scores[5],scores[6],scores[7],scores[8],True,target_record_id))
        mysql_connection.commit()
