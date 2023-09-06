from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer, nullable=False,unique=True)
    userName=db.Column(db.String(50),nullable=False)
    userDept=db.Column(db.String(50))
    last_attendance_time=db.Column(db.DateTime)

class Attendance(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userId=db.Column(db.Integer,db.ForeignKey(Users.userId))
    userName=db.Column(db.String(50),db.ForeignKey(Users.userName))
    AttendanceTime=db.Column(db.DateTime)

