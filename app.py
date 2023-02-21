from flask import Flask,flash,redirect,render_template,url_for,request,jsonify
from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
import smtplib
app=Flask(__name__)
app.secret_key='#dgssgjhi'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='ammu'
app.config['MYSQL_DB']='projectwork'
mysql=MySQL(app)
@app.route('/')
def home():
    return render_template('Hostel website.html')
@app.route('/mess')
def mess():
    return render_template('mess.html')
@app.route('/about')
def about():
     return render_template('about.html')
@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=="POST":
        print(request.form)
        firstname=request.form['First_Name']
        print(request.form)
        lastname=request.form['Last_Name']
        print(request.form)
        email=request.form['Email']
        print(request.form)
        password=request.form['Password']
        print(request.form)
        cursor=mysql.connection.cursor()
        cursor.execute('insert into register(FristName,LastName,EmailId,password) values(%s,%s,%s,%s)',[firstname,lastname,email,password])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin'))
    return render_template('Register.html')
@app.route('/login')
def login():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT username,password from admin')
    books=cursor.fetchall()
    cursor.close()
    return render_template('Admin-login.html')
@app.route('/validate',methods=['POST'])
def validate():
    username=request.form['username']
    password=request.form['password']
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT username,password from admin')
    data=cursor.fetchall()[0]
    userid=data[0]
    password=data[1]
    cursor.close()
    if username==username and password==password:
        return redirect(url_for('adminpage'))
    else:
        return redirect(url_for('adminpage'))
@app.route('/adminpage')
def adminpage():
    return render_template('admin-homepage.html')

@app.route('/admin')
def admin():
    return render_template('Admin-homepage.html')
@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    if request.method=='POST':
        print(request.form)
        id1=request.form['id1']
        print(request.form)
        fullname=request.form['name']
        print(request.form)

        mobile=request.form['mobile']
        print(request.form)

        room=request.form['room']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into student(Id,name,mobile,Room) values(%s,%s,%s,%s)',[id1,fullname,mobile,room])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin'))
    return render_template('Add-student.html')
@app.route('/addvisitor',methods=['GET','POST'])
def addvisitor():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from visitors')
    data=cursor.fetchall()
    cursor.close()
    if request.method=='POST':       
        print(request.form)
        fullname=request.form['visitorname']
        print(request.form)
        mobile=request.form['mobilenumber']
        print(request.form)        
        id1=request.form['StudentId']
        cursor=mysql.connection.cursor()
        cursor.execute('insert ignore into visitors(visitorname,mobile,Id) values(%s,%s,%s)',[fullname,mobile,id1])
        mysql.connection.commit()
        cursor.execute('SELECT * from visitors')
        data=cursor.fetchall()
        cursor.close()
        return render_template('AddVisitor.html',data=data)
    return render_template('AddVisitor.html',data=data)
@app.route('/remove/<id1>')
def remove(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('delete FROM visitors where number=%s',[id1])
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('addvisitor'))
@app.route('/modefi/<id1>',methods=['GET','POST'])
def modefi(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from visitors where number=%s',[id1])
    data=cursor.fetchone()
    print(data)
    if request.method=='POST':      
        fullname=request.form['name']
        id2=request.form['Room']
        mobile=request.form['mobileNumber']
        cursor.execute('update visitors set visitorname=%s,mobile=%s,id=%s where number=%s',[fullname,mobile,id2,id1])
        mysql.connection.commit()
        return redirect(url_for('addvisitor'))
    return render_template('update1.html',data=data)
@app.route('/studentrecord',methods=['GET','POST'])
def studentrecord():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student')
    data=cursor.fetchall()
    cursor.close()
    if request.method=='POST':
        StudentId=request.form['StudentId']
        name=request.form['name']
        room =request.form['Room']
        mobileNumber=request.form['mobileNumber']
        cursor=mysql.connection.cursor()
        cursor.execute('insert ignore into student(Id,Name,room,mobile) values(%s,%s,%s,%s)',[StudentId,name,room,mobileNumber])
        mysql.connection.commit()
        cursor.execute('SELECT * from student')
        data=cursor.fetchall()
        cursor.close()
        return render_template('Student Record.html',data=data)
    return render_template('Student Record.html',data=data)
@app.route('/delete/<id1>')
def delete(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('DELETE FROM student where Id=%s',[id1])
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('studentrecord'))
@app.route('/update/<id1>',methods=['GET','POST'])
def update(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student where id=%s',[id1])
    data=cursor.fetchone()
    if request.method=='POST':      
        name=request.form['name']
        print(name)
        room =request.form['Room']
        mobileNumber=request.form['mobileNumber']
        cursor.execute('update student set Name=%s,room=%s,mobile=%s where id=%s',[name,room,mobileNumber,id1])
        mysql.connection.commit()
        return redirect(url_for('studentrecord'))
    return render_template('update.html',data=data)
@app.route('/checkin',methods=['GET','POST'])
def checkin():
    details=None
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student')
    data=cursor.fetchall()
    data1=request.args.get('name') if request.args.get('name') else 'empty'
    print(data1)
    cursor.execute('SELECT * from student where id=%s',[data1])
    details=cursor.fetchone()
    cursor.execute('SELECT date,id,name,mobilenumber,checkin,checkout from records')
    std_records=cursor.fetchall()
    cursor.close()
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        Id2=request.form['empCode']
        today=date.today()
        day=today.day
        month=today.month
        year=today.year
        today_date=datetime.strptime(f'{year}-{month}-{day}','%Y-%m-%d')
        date_today=datetime.strftime(today_date,'%Y-%m-%d')
        fullname=request.form['studid']
        mobile=request.form['salary']
        cursor.execute('select count(*) from records where Id=%s and date=%s',[Id2,date_today])
        count=int(cursor.fetchone()[0])
        if Id2=="" or fullname=="" or mobile=="":
            flash('Select The student Id first')
        elif count>=1:
            flash('The student already gone outside')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into records(Id,name,mobilenumber,checkin,checkout,date) values(%s,%s,%s,%s,%s,%s)',[Id2,fullname,mobile,None,None,date_today])
            mysql.connection.commit()
            cursor.execute('SELECT date,id,name,mobilenumber,checkin,checkout from records')
            std_records=cursor.fetchall()
            cursor.close()
    return render_template('Check in-page.html',data1=data1,data=data,details=details,std_records=std_records)
@app.route('/checkoutupdate/<date>/<id1>')
def checkoutupdate(date,id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkout=current_timestamp() where date=%s and Id=%s',[date,id1])
    mysql.connection.commit()
    return redirect(url_for('checkin'))
@app.route('/checkinupdate/<date>/<id1>')
def checkinupdate(date,id1):
    cursor=mysql.connection.cursor()
    cursor.execute('update records set checkin=current_timestamp() where date=%s and Id=%s',[date,id1])
    mysql.connection.commit()
    return redirect(url_for('checkin'))
@app.route('/visitor',methods=['GET','POST'])
def visitor():
        details=None
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * from visitors')
        data=cursor.fetchall()
        data1=request.args.get('name') if request.args.get('name') else 'empty'
        print(data1)
        cursor.execute('SELECT * from visitors where mobile=%s',[data1])
        details=cursor.fetchone()
        cursor.execute('SELECT name,mobile,id,checkin,checkout,date from visitorrecords')
        visitor=cursor.fetchall()
        cursor.close()
        if request.method=='POST':
            cursor=mysql.connection.cursor()           
            mobile=request.form['mobile']
            print(request.form)
            today=date.today()
            print(request.form)
            day=today.day
            month=today.month
            print(request.form)
            year=today.year
            today_date=datetime.strptime(f'{year}-{month}-{day}','%Y-%m-%d')
            print(request.form)
            date_today=datetime.strftime(today_date,'%Y-%m-%d')
            print(request.form)
            Name=request.form['Name']
            print(request.form)
            Id2=request.form['empCode']
            print(request.form)
            cursor.execute('select count(*) from visitorrecords where mobile=%s and date=%s',[mobile,date_today])
            print(request.form)
            count=int(cursor.fetchone()[0])
            if mobile=="" or Name=="" or Id2=="":
               flash('Select The visitors mobile first')
            elif count>=1:
               flash('hello visitor')
            else:
                cursor=mysql.connection.cursor()
                cursor.execute('insert into visitorrecords(name,mobile,id,checkin,checkout,date) values(%s,%s,%s,%s,%s,%s)',[Name,mobile,Id2,None,None,date_today])
                mysql.connection.commit()
                cursor.execute('SELECT name,mobile,id,checkin,checkout,date from visitorrecords')
                visitor=cursor.fetchall()
                cursor.close()
        return render_template('visitor.html',data1=data1,data=data,details=details,visitor=visitor)      
@app.route('/incoming/<date>/<mobile>')
def incoming(date,mobile):
    cursor=mysql.connection.cursor()
    cursor.execute('incoming visitorrecords set checkin=current_timestamp() where date=%s and mobile=%s',[date,mobile])
    mysql.connection.commit()
    return redirect(url_for('visitor'))
@app.route('/outgoing/<date>/<mobile>')
def outgoing(date,mobile):
     cursor=mysql.connection.cursor()
     cursor.execute('outgoing visitorrecords set checkout=current_timestamp() where date=%s and mobile=%s',[date,mobile])
     mysql.connection.commit()
     return redirect(url_for('visitor'))
app.run(port='8000',debug=True)

            
