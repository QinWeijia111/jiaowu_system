# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# 数据库连接
db = pymysql.connect(host="localhost", user="root", password="root", database="school")
cursor = db.cursor()  # 数据库的指针

# 后端服务启动asd
app = Flask(__name__)
CORS(app, resources=r'/*')


# 登录接口
@app.route('/login/login', methods=['POST'])
def login_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute(
            "select * from `user` u where username = \"" + username + "\" and password = \"" + password + "\";")
        data = cursor.fetchone()
        if (data != None):
            print("result:", data)
            jsondata = {"id": str(data[0]), "username": str(data[1])}
            return jsonify(jsondata)
        else:
            print("result: NULL")
            jsondata = {}
            return jsonify(jsondata)


# 列出全部学生信息的接口
@app.route('/student/stu_list', methods=['POST'])
def student_list():
    if request.method == "POST":
        cursor.execute("select * from student s ;")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for da in data:
                temp["sno"] = da[0]
                temp["sname"] = da[1]
                temp["ssex"] = da[2]
                temp["sage"] = da[3]
                temp["sdept"] = da[4]
                result.append(temp.copy())
            print("result:", "列出全部学生数量", len(data))
            return jsonify(result)
        else:
            print("列出全部学生出错")
            return jsonify([])


# 增加一个学生
@app.route('/student/stu_insert', methods=['POST'])
def student_insert():
    if request.method == "POST":
        sno = request.form.get("sno")
        sname = request.form.get("sname")
        ssex = request.form.get("ssex")
        sage = request.form.get("sage")
        sdept = request.form.get("sdept")
        try:
            sql = f"insert into student(sno, sname, Ssex, Sage, Sdept) " \
                  f"values (\"{sno}\", \"{sname}\",\"{ssex}\",\"{int(sage)}\",\"{sdept}\");"
            cursor.execute(sql)
            db.commit()
            print("add a student successfully!")
            return "1"
        except Exception as e:
            print("add a new user failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


# 更新/修改某个学生的信息
@app.route('/student/stu_update', methods=['POST'])
def student_update():
    if request.method == "POST":
        sno = request.form.get("sno")
        sname = request.form.get("sname")
        ssex = request.form.get("ssex")
        sage = request.form.get("sage")
        sdept = request.form.get("sdept")
        try:
            sql = f"update student set sno = \"{sno}\"," \
                  f" sname = \"{sname}\", ssex = \"{ssex}\", " \
                  f"sage = {sage}, sdept = \"{sdept}\" " \
                  f"where sno = \"{sno}\";"
            cursor.execute(sql)
            db.commit()
            print("update a student successfully!")
            return "1"
        except Exception as e:
            print("update a student failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


# 删除某个学生
@app.route("/student/stu_delete", methods=["POST"])
def student_delete():
    if request.method == "POST":
        sno = request.form.get("sno")
        try:
            sql = f"delete from student where sno = \"{sno}\";"
            cursor.execute(sql)
            db.commit()
            print("delete a student whose sno is", sno)
            return "1"
        except Exception as e:
            print("删除学生出错")
            db.rollback()
            return "-1"


# 列出全部课程信息的接口
@app.route('/course/course_list', methods=['POST'])
def course_list():
    if request.method == "POST":
        cursor.execute("select * from course ORDER BY CONVERT(`Cno`, SIGNED) ASC;")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for da in data:
                temp["cno"] = da[0]
                temp["cname"] = da[1]
                temp["cpno"] = da[2]
                temp["ccredit"] = da[3]
                result.append(temp.copy())
            print("result:", len(data))
            return jsonify(result)
        else:
            print("data : NULL")
            return jsonify([])


# 增加一门课程
@app.route('/course/course_insert', methods=['POST'])
def course_insert():
    if request.method == "POST":
        cno = request.form.get("cno")
        cname = request.form.get("cname")
        cpno = request.form.get("cpno")
        ccredit = request.form.get("ccredit")
        try:
            cpno_value = f'"{cpno}"' if cpno is not None and cpno != '' else 'NULL'
            sql = f"insert into course(cno, cname, cpno, ccredit) " \
                  f"values (\"{cno}\", \"{cname}\",{cpno_value},\"{ccredit}\");"
            cursor.execute(sql)
            db.commit()
            print("add a course successfully!")
            return "1"
        except Exception as e:
            print("add a new course failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


# 删除某个课程
@app.route("/course/course_delete", methods=["POST"])
def course_delete():
    if request.method == "POST":
        cno = request.form.get("cno")
        try:
            sql = f"delete from course where cno = \"{cno}\";"
            cursor.execute(sql)
            db.commit()
            print("delete a course whose cno is", cno)
            return "1"
        except Exception as e:
            print("delete false")
            db.rollback()
            return "-1"


# 更新/修改某个课程的信息
@app.route('/course/course_update', methods=['POST'])
def course_update():
    if request.method == "POST":
        cno = request.form.get("cno")
        cname = request.form.get("cname")
        cpno = request.form.get("cpno")
        ccredit = request.form.get("ccredit")
        try:
            sql = f"update course " \
                  f"set cno = \"{cno}\" , cname = \"{cname}\", cpno = \"{cpno}\"," \
                  f" ccredit = {ccredit} where cno = \"{cno}\";"
            cursor.execute(sql)
            db.commit()
            print("update a course successfully!")
            return "1"
        except Exception as e:
            print("update a course failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


# 列出全部选课信息的接口,包括为选课的同学
@app.route('/sc_system/list', methods=['POST'])
def sc_system_list():
    if request.method == "POST":
        sql = "select student.sno,sname,sdept,sc.cno,cname,grade " \
              "from student " \
              "left join " \
              "(sc join course on sc.cno = course.Cno) " \
              "on sc.Sno = student.sno;"
        cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)
        temp = {}
        result = []
        if (data != None):
            for da in data:
                temp["sno"] = da[0]
                temp["sname"] = da[1]
                temp["sdept"] = da[2]
                temp["cno"] = da[3]
                temp["cname"] = da[4]
                temp["grade"] = da[5]
                result.append(temp.copy())
            print("result:", "列出全部学生数量以及课程选课信息", len(data))
            return jsonify(result)
        else:
            print("列出全部学生以及课程选课信息出错")
            return jsonify([])


# 删除某个选课信息
@app.route("/sc_system/delete", methods=["POST"])
def sc_delete():
    if request.method == "POST":
        sno = request.form.get("sno")
        cno = request.form.get("cno")
        print(sno, cno)
        try:
            sql = f"delete from sc where cno = \"{cno}\" and sno = \"{sno}\";"
            cursor.execute(sql)
            db.commit()
            print("delete a sc whose cno is", cno)
            return "1"
        except Exception as e:
            print("delete false")
            db.rollback()
            return "-1"


# 插入选课信息
@app.route('/sc_system/insert', methods=['POST'])
def sc_insert():
    if request.method == "POST":
        sno = request.form.get("sno")
        cno = request.form.get("cno")
        grade = request.form.get("grade")
        try:
            grade_value = grade if grade is not None and grade != '' else 'NULL'
            sql = f"insert into sc(sno,cno,Grade) values ('{sno}','{cno}',{grade_value});"
            cursor.execute(sql)
            db.commit()
            print("add a sc successfully!")
            return "1"
        except Exception as e:
            print("add a new sc failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8899)
    db.close()
    print("Good bye!")
