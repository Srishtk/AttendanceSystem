from flask import Flask, request, render_template, redirect, url_for, Response
import subprocess
from models import Users, Attendance, db
from datetime import datetime
from camera import capture
import threading
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)
AUTHENTICATION_KEY = "qwerty12"
flag = False




@app.route('/', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Mark Attendance':
            return redirect(url_for('recognise_face'))
        if action == 'Admin':
            return redirect('/authenticate')
    return render_template('welcome.html')


@app.route('/face_recognition')
def recognise_face():
    status = subprocess.run(['python', 'app.py'], capture_output=True, text=True)
    if status.returncode == 0:
        printed_output = status.stdout.strip()
        lines = printed_output.split("\n")
        print(status)
        for line in lines:
            if line.isdigit():
                user_id = int(line)
                print(user_id)
                result = Users.query.filter_by(userId=user_id).first()
                time = datetime.now()
                username = result.userName
                result.last_attendance_time = time
                db.session.commit()
                record = Attendance(
                    userId=user_id,
                    userName=username,
                    AttendanceTime=time
                )
                db.session.add(record)
                db.session.commit()
                return render_template('face_recog_success.html', result=result,
                                       time=time.strftime('%Y-%m-%d %H:%M:%S'))
        return render_template('face_recog_fail.html', msg="Face did not match")
    return render_template('face_recog_fail.html', msg="Script run failed")


@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    if request.method == 'POST':
        provided_key = request.form.get("auth_key")
        if provided_key == AUTHENTICATION_KEY:
            flag = True
            attendance_list = Attendance.query.all()
            return render_template('admin.html', at_list=attendance_list)
        else:
            return redirect('/')
    return render_template('authenticate.html')


@app.route('/admin_redirect', methods=['POST'])
def admin_redirect():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Add a User':
            return render_template('adduser.html')
        # if action=='Train':
        #     subprocess.run(['python', 'encoding.py'])
        #     return redirect('/')
        if action == 'Home':
            flag = False
            return redirect('/')





@app.route('/adduser',methods=['POST'])
def adduser():
    if request.method=='POST':
        username=request.form.get('username')
        userid=request.form.get('userid')
        dept=request.form.get('department')
        result=Users.query.filter_by(userId=userid).first()
        if result is None:
            record=Users(userId=userid,userName=username,userDept=dept)
            db.session.add(record)
            db.session.commit()
            status = capture(userid)
            if status:
                return render_template('user_add_success.html')
            else:
                return render_template('face_recog_fail.html', msg="Camera failed to click images")
        else:
            return render_template('face_recog_fail.html', msg="User with the same ID exists already.")

if __name__ == "__main__":
    app.run(debug=True)
