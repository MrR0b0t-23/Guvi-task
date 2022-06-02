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
       
    
    
    
    
    
