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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://loddhlwitwrztt:652dc3990b3768f16c582bb1de793be02842758f6360f433a397521748cfa78a@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/d3j0ipm3kckdu8"
db = SQLAlchemy(app)

class UserData(db.Model):
    __tablename__ = 'UserData'
    UserId = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(80), nullable=False)
    Lastname = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    MobileNumber = db.Column(db.Integer, nullable=False)
    PasswordHash = db.Column(db.String(80), nullable=False)

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
    Email = db.Column(db.String(80), nullable=False)
    DateTime = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())

    def __init__ (self, UserId, Email):
        self.UserId = UserId
        self.Email = Email

class ProfileData(db.Model):
    __tablename__ = 'ProfileData'
    ProfileId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, nullable=False)
    Firstname = db.Column(db.String(80), nullable=False)
    Lastname = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    MobileNumber = db.Column(db.Integer, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Degree = db.Column(db.String(80), nullable=False)
    Department = db.Column(db.String(80), nullable=False)
    PassoutYear = db.Column(db.Integer, nullable=False)
    RegisterNumber = db.Column(db.String(80), nullable=False)
    CollegeName = db.Column(db.String(80), nullable=False)
    CGPA = db.Column(db.Float, nullable=False)
    SelfIntro = db.Column(db.String(1000), nullable=False)
    SSLC_School = db.Column(db.String(80), nullable=False)
    SSLC_Precentage = db.Column(db.Float, nullable=False)
    SSLC_Year = db.Column(db.Integer, nullable=False)
    HSC_School = db.Column(db.String(80), nullable=False)
    HSC_Precentage = db.Column(db.Float, nullable=False)
    HSC_Year = db.Column(db.Integer, nullable=False)
    Website = db.Column(db.String(80), nullable=False)
    Github = db.Column(db.String(80), nullable=False)

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
                                PasswordHash = bcrypt.generate_password_hash(_pwd))
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
    if request.method == 'POST':
        _fname = request.form['inputfname']
        _lname = request.form['inputlname']
        _email = request.form['inputemail']
        _cnumber = request.form['inputcnumber']
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
        _newProfile = ProfileData(Firstname = _fname, Lastname = _lname, Email = _email,
                                MobileNumber = _cnumber, Age = _age, Degree = _degree, 
                                Department = _dept, PassoutYear = _poyear, RegisterNumber = _rnumber,
                                CollegeName = _clg, CGPA = _cgpa, SelfIntro = _intro, 
                                SSLC_School = _sslcSchool, SSLC_Precentage = _sslcPrecent, 
                                SSLC_Year = _ssclYear, HSC_School = _hscSchool, HSC_Precentage = _hscPrecent,
                                HSC_Year = _hscYear, Website = _website, Github = _github)
        db.session.add(_newProfile)
        db.session.commit()  
        return redirect(url_for('signup'))  
    _userId = int(request.cookies.get('userId'))
    _user = UserData.query.filter_by(UserId = _userId).first() 
    _data = {'FirstName': _user.Firstname, 'LastName': _user.Lastname,
             'MobileNumber': _user.MobileNumber, 'Email': _user.Email}
    return render_template('ProfilePage.html', data = _data)

if __name__ == "__main__":
    app.run()
       
    
    
    
    
    
