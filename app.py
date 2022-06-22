from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, make_response, request, url_for, session
from flask_bcrypt import Bcrypt
import datetime
import os
import json 

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['DEBUG'] = True
app.secret_key = '$2b$12$gAwc2M'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://cqvvsnpftqxvff:1f3e22cd57a34a1c43b3f3464afd8bf4586097ec7ab548deb3a39548fb72ba48@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/db3fgetdk9r5i0"
db = SQLAlchemy(app)

class UserData(db.Model):
    __tablename__ = 'UserData'
    UserId = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(255), nullable=False)
    Lastname = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    MobileNumber = db.Column(db.String(255), nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)

    def __init__ (self, Firstname, Lastname, Email, MobileNumber, PasswordHash):
        self.Firstname= Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.MobileNumber = MobileNumber
        self.PasswordHash = PasswordHash   

class LoginData(db.Model):
    __tablename__ = 'LoginData'
    LoginId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, nullable = False)
    Email = db.Column(db.String(255), nullable=False)
    DateTime = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())

    def __init__ (self, UserId, Email):
        self.UserId = UserId
        self.Email = Email

class ProfileData(db.Model):
    __tablename__ = 'ProfileData'
    ProfileId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, nullable=False)
    Firstname = db.Column(db.String(255), nullable=False)
    Lastname = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    MobileNumber = db.Column(db.String(255), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Degree = db.Column(db.String(255), nullable=False)
    Department = db.Column(db.String(255), nullable=False)
    PassoutYear = db.Column(db.Integer, nullable=False)
    RegisterNumber = db.Column(db.String(255), nullable=False)
    CollegeName = db.Column(db.String(255), nullable=False)
    CGPA = db.Column(db.Float, nullable=False)
    SelfIntro = db.Column(db.String(5000), nullable=False)
    SSLC_School = db.Column(db.String(255), nullable=False)
    SSLC_Precentage = db.Column(db.Float, nullable=False)
    SSLC_Year = db.Column(db.Integer, nullable=False)
    HSC_School = db.Column(db.String(255), nullable=False)
    HSC_Precentage = db.Column(db.Float, nullable=False)
    HSC_Year = db.Column(db.Integer, nullable=False)
    Website = db.Column(db.String(255), nullable=False)
    Github = db.Column(db.String(255), nullable=False)

    def __init__ (self, UserId, Firstname, Lastname, Email, MobileNumber, Age, 
                 Degree, Department, PassoutYear, RegisterNumber, CollegeName, CGPA,
                 SelfIntro, SSLC_School, SSLC_Precentage, SSLC_Year, HSC_School,
                 HSC_Precentage, HSC_Year, Website, Github):
        self.UserId = UserId
        self.Firstname= Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.MobileNumber = MobileNumber
        self.Age = Age
        self.Degree = Degree
        self.Department = Department
        self.PassoutYear = PassoutYear
        self.RegisterNumber = RegisterNumber
        self.CollegeName = CollegeName
        self.CGPA = CGPA
        self.SelfIntro = SelfIntro
        self.SSLC_School = SSLC_School
        self.SSLC_Precentage = SSLC_Precentage
        self.SSLC_Year = SSLC_Year
        self.HSC_School = HSC_School
        self.HSC_Precentage = HSC_Precentage
        self.HSC_Year = HSC_Year
        self.Website = Website
        self.Github = Github
        
@app.route('/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        _fname = request.form['fname']
        _lname = request.form['lname']
        _email = request.form['email']
        _mnumber = request.form['mnumber']
        _pwd = request.form['pwd']
        if _email and _pwd:
            _newUser = UserData(Firstname = _fname, Lastname = _lname, Email = _email,
                                MobileNumber = _mnumber, 
                                PasswordHash = bcrypt.generate_password_hash(_pwd).decode('utf8'))
            db.session.add(_newUser)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('SignupPage.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        _email = request.form['email']
        _pwd = request.form['pwd']
        _user = UserData.query.filter_by(Email = _email).first()
        if _user:
            resp = make_response(redirect(url_for('profile')))
            if bcrypt.check_password_hash(_user.PasswordHash, _pwd):
                resp.set_cookie('Authentication', 'True')
                resp.set_cookie('userId', str(_user.UserId))
                _newLogin = LoginData(UserId = _user.UserId, Email = _user.Email)
                db.session.add(_newLogin)
                db.session.commit()
                return resp
    return render_template('LoginPage.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    _Auth = request.cookies.get('Authentication')
    if _Auth == "True":
        _userId = int(request.cookies.get('userId'))
        _user = UserData.query.filter_by(UserId = _userId).first() 
        _data = {'FirstName': _user.Firstname, 'LastName': _user.Lastname,
                 'MobileNumber': _user.MobileNumber, 'Email': _user.Email}
        if request.method == 'POST':
            _fname = _user.Firstname
            _lname = _user.Lastname
            _email = _user.Email
            _cnumber = _user.MobileNumber
            _age = request.form['inputage']
            _degree = request.form['inputdegree']
            _dept = request.form['inputdept']
            _poyear = request.form['inputpoyear']
            _rnumber = request.form['inputrnumber']
            _clg = request.form['inputclg']
            _cgpa = request.form['inputcgpa']
            _intro = request.form['inputintro']
            _sslcSchool = request.form['inputsslcschool']
            _sslcPrecent = request.form['inputsslcprecent']
            _ssclYear = request.form['inputsslcyear']
            _hscSchool = request.form['inputhscschool']
            _hscPrecent = request.form['inputhscprecent']
            _hscYear = request.form['inputhscyear']
            _website = request.form['inputwebsite']
            _github = request.form['inputgithub']
            _newProfile = ProfileData(UserId =_userId, Firstname = _fname, Lastname = _lname, Email = _email,
                                    MobileNumber = _cnumber, Age = _age, Degree = _degree, 
                                    Department = _dept, PassoutYear = _poyear, RegisterNumber = _rnumber,
                                    CollegeName = _clg, CGPA = _cgpa, SelfIntro = _intro, 
                                    SSLC_School = _sslcSchool, SSLC_Precentage = _sslcPrecent, 
                                    SSLC_Year = _ssclYear, HSC_School = _hscSchool, HSC_Precentage = _hscPrecent,
                                    HSC_Year = _hscYear, Website = _website, Github = _github)
            db.session.add(_newProfile)
            db.session.commit()  
            return redirect(url_for('signup'))  
        return render_template('ProfilePage.html', data = _data)
    return render_template('LoginPage.html')

if __name__ == "__main__":
    app.run()
    
from flask import Flask, render_template
<<<<<<< HEAD
import flask
import mysql.connector
from multiprocessing import Process, Manager, Value
import pandas as pd
from datetime import date, timedelta, datetime
import pymongo
import time
import datetime
from ctypes import c_char_p

app = Flask(__name__)

def orderPlotQuery(orderPlotDict):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT FROM_UNIXTIME(date), SUM(amount) from `order` 
                WHERE FROM_UNIXTIME(date) > NOW() - interval 15 day AND `status` LIKE "paid"
                GROUP BY CAST(FROM_UNIXTIME(date) AS DATE) """
    cursorObject.execute(query)

    queryResult = cursorObject.fetchall()
    mydb.close()
    df = pd.DataFrame(queryResult, columns=['Date', 'TotalSales'])
    df['Date'] = df['Date'].dt.date
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date').reindex(pd.date_range(start=pd.to_datetime(date.today() - timedelta(days=15)),
                                                    end=pd.to_datetime(date.today()), freq='D'))
    df.index.name = "Date"
    df = df.reset_index().fillna(0)
    dates, sales = df['Date'].dt.date, df['TotalSales'].values
    orderPlotDict['dates'] = dates
    orderPlotDict['sales'] = sales
    return orderPlotDict


def orderCountQuery(orderCountValue):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT COUNT(sno) from `order` 
                WHERE FROM_UNIXTIME(date) > NOW() - interval 15 day AND `status` LIKE "paid" """
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    orderCountValue.value = queryResult[0][0]
=======

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("HomePage.html")

@app.route("/activity")
def activityPage():
    return render_template("ActivityPage.html")

@app.route("/course")
def coursePage():
    return render_template("CoursePage.html")

@app.route("/search")
def searchPage():
    return render_template("SearchPage.html")

@app.route("/user")
def userPage():
    return render_template("UserPage.html")
>>>>>>> a4fb573cdeb8dfd30f932973a1573313c725bd1c


def orderTotalSalesQuery(orderTotalSalesValue):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT SUM(amount) from `order` 
                WHERE FROM_UNIXTIME(date) > NOW() - interval 15 day AND `status` LIKE "paid" """
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    orderTotalSalesValue.value = queryResult[0][0]


def UserPlotQuery(userPlotDict):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT FROM_UNIXTIME(timestamp), COUNT(DISTINCT('hash')) FROM `course_point_live` WHERE 
                FROM_UNIXTIME(timestamp) > NOW() - interval 15 day GROUP BY CAST(FROM_UNIXTIME(timestamp) AS DATE) """
    cursorObject.execute(query)

    queryResult = cursorObject.fetchall()
    mydb.close()
    df = pd.DataFrame(queryResult, columns=['Date', 'Count'])
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date').reindex(pd.date_range(start=pd.to_datetime(date.today() - timedelta(days=15)),
                                                    end=pd.to_datetime(date.today()), freq='D'))
    df.index.name = "Date"
    df = df.reset_index().fillna(0)
    dates, count = df['Date'].dt.date, df['Count'].values
    userPlotDict['dates'] = dates
    userPlotDict['count'] = count
    return userPlotDict


def UserTotalCountQuery(userTotalCountValue):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT COUNT(DISTINCT('hash')) from `course_point_live` WHERE 
                FROM_UNIXTIME(timestamp) > NOW() - interval 15 day GROUP BY CAST(FROM_UNIXTIME(timestamp) AS DATE) """
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    #orderTotalCountValue = int(queryResult[0][0]) #queryResult returns NULL
    orderTotalCountValue = 0  # temp value
    return orderTotalCountValue


@app.route("/")
def homePage():
    manager = Manager()
    orderPlotDict = manager.dict()
    userPlotDict = manager.dict()
    orderCountValue = Value('f')
    orderTotalSalesValue = Value('f')
    userTotalCountValue = Value('f')

    orderPlotProcess = Process(target=orderPlotQuery, args=(orderPlotDict,))
    orderCountProcess = Process(
        target=orderCountQuery, args=(orderCountValue,))
    orderTotalSalesProcess = Process(
        target=orderTotalSalesQuery, args=(orderTotalSalesValue,))
    UserPlotProcess = Process(target=UserPlotQuery, args=(userPlotDict,))
    UserTotalCountProcess = Process(
        target=UserTotalCountQuery, args=(userTotalCountValue,))

    orderPlotProcess.start()
    orderCountProcess.start()
    orderTotalSalesProcess.start()
    UserPlotProcess.start()
    UserTotalCountProcess.start()

    orderPlotProcess.join()
    orderCountProcess.join()
    orderTotalSalesProcess.join()
    UserPlotProcess.join()
    UserTotalCountProcess.join()

    #UserAvgCount = int(orderTotalCountValue/15)
    UserAvgCount = 0  # temp value
    data = {
        "UserPlot": userPlotDict,
        "orderPlot": orderPlotDict,
        "orderCount": orderCountValue.value,
        "orderTotalSales": orderTotalSalesValue.value,
        "UserTotalCount": userTotalCountValue.value,
        "UserAvgCount": UserAvgCount
    }
    return render_template("HomePage.html", data=data)


@app.route("/activity")
def activityPage():
    return render_template("ActivityPage.html")

def CourseNameQuery(CourseNameDict):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT `course_name`, `key` FROM `courses` WHERE 1"""
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    CourseNameDict['detail'] = queryResult
    return CourseNameDict

def CourseDetailQuery(CourseDetailDict, _courseName):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT * FROM `courses` WHERE key LIKE "{}" """.format(_courseName)
    cursorObject.execute(query)
    mydb.close()
    CourseDetailDict["courseDetail"] = cursorObject.fetchall()
    return CourseDetailDict

def CourseUserQuery(CouseUserDict, _courseName):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT * FROM `courses` WHERE key LIKE "{}" """.format(_courseName)
    cursorObject.execute(query)
    CouseUserDict["userDetail"] = cursorObject.fetchall()
    mydb.close()
    return CouseUserDict

@app.route("/course", methods=["GET"])
def coursePage():
    manager = Manager()
    CourseNameDict = manager.dict()
    CourseDetailDict = manager.dict()
    CourseUserDict = manager.dict()

    _courseKey = flask.request.args.get('courseKey')

    CourseNameProcess = Process(target=CourseNameQuery, args=(CourseNameDict,))
    CourseDetailProcess = Process(target=CourseDetailQuery, args=(CourseDetailDict, _courseKey))
    CouseUserProcess = Process(target=CourseUserQuery, args=(CourseUserDict, _courseKey))

    CourseNameProcess.start()
    #CourseDetailProcess.start()
    #CouseUserProcess.start()

    CourseNameProcess.join()
    #CourseDetailProcess.join()
    #CouseUserProcess.join()

    data = {"Courses": CourseNameDict["detail"]}
    
    return render_template("CoursePage.html", data=data)


@app.route("/search")
def searchPage():
    return render_template("SearchPage.html")


def UserDetailQueryMongo(UserPersDetailDict, _email):
    client = pymongo.MongoClient(
        "mongodb://guvidbmongo:guviGEEK9Mongo7@localhost")
    mytable = client['userData']
    mycollection = mytable['userObject']
    UserPersDetailDict["user"] = mycollection.find_one({"email": {"$eq": _email}})
    return UserPersDetailDict


def UserCoursePointQuery(_email, _coursekey):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT `course`, `score`, FROM_UNIXTIME(timestamp) FROM `course_point` WHERE 
                `email` LIKE "{}" AND `course` LIKE "{}" """.format(_email, _coursekey)
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    UserCoursePointDict = {"score": 0, "date": None}
    for points in queryResult:
        UserCoursePointDict = {"score": points[1], "date": points[2]}

    return UserCoursePointDict


def UserCourseQuery(UserCourseList, TotalAmountSpendValue, TotalCourseCountValue, _email):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ashwin",
        password="guvi123",
        database="guvi"
    )
    cursorObject = mydb.cursor()
    query = """ SELECT order.PaymentID, courses.key, courses.course_name, courses.language, courses.level, order.mode, 
                order.net_amount_debit, FROM_UNIXTIME(order.date) FROM `courses` JOIN `order` ON courses.key = 
                order.product_info WHERE order.email LIKE "{}" AND order.status LIKE "paid" """.format(_email)
    cursorObject.execute(query)
    queryResult = cursorObject.fetchall()
    mydb.close()
    for courses in queryResult:
        course = {"PaymentID": courses[0], "CourseKey": courses[1], "CourseName": courses[2], 
                  "CoursePoint": UserCoursePointQuery(_email, courses[1]),"CourseLanguage": courses[3], "CourseLevel": courses[4],
                  "PaymentMode": courses[5], "AmountDebit": float(courses[6]), "Date": courses[7] }
        TotalAmountSpendValue.value += float(courses[6])
        TotalCourseCountValue.value += 1

        UserCourseList.append(course)

    return (UserCourseList, TotalAmountSpendValue, TotalCourseCountValue)

@app.route("/user", methods=["GET"])
def userPage():
    manager = Manager()
    UserPersDetailDict = manager.dict()
    UserCourseList = manager.list()
    TotalAmountSpendValue = Value('f')
    TotalCourseCountValue = Value('i')

    _email = flask.request.args.get('userEmail')

    UserDetailProcessMongo = Process(target=UserDetailQueryMongo, args=(UserPersDetailDict, _email,))
    UserCourseProcess = Process( target=UserCourseQuery, args=(UserCourseList, TotalAmountSpendValue, TotalCourseCountValue, _email))

    UserDetailProcessMongo.start()
    UserCourseProcess.start()

    UserDetailProcessMongo.join()
    UserCourseProcess.join()

    data = {"UserPersDetail": UserPersDetailDict, "UserCourseDict": UserCourseList, 
            "TotalAmountSpend": round(TotalAmountSpendValue.value), "TotalCourseCount": TotalCourseCountValue.value }
    return render_template("UserPage.html", data=data)

@app.template_filter('ctime')
def timectime(s):
    return datetime.datetime.strptime(time.ctime(s), "%a %b %d %H:%M:%S %Y")

@app.context_processor
def inject_enumerate():   
    return dict(enumerate=enumerate)
if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True, port=2323, host="0.0.0.0")

""" 
SELECT COUNT(DISTINCT('hash')) as 'count', FROM_UNIXTIME(date) as 'Date' FROM `order` WHERE 
FROM_UNIXTIME(date) > NOW() - interval 15 day GROUP BY CAST(FROM_UNIXTIME(date) AS DATE)

"""
=======
    app.run(debug = True)
>>>>>>> a4fb573cdeb8dfd30f932973a1573313c725bd1c

       
    
    
    
    
    
