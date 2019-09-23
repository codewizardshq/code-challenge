from flask import Flask, render_template, session, redirect, url_for, escape, request, Markup
import sqlite3
import datetime
import hashlib, os, binascii, re
from os import path
from helpers import Pilgrim,Level,hash_password,verify_password

#---setting up App

app = Flask(__name__)
app.secret_key = 'any random stringgg'

#---setting up Database (sqlite)

ROOT = path.dirname(path.realpath(__file__))
conn = sqlite3.connect(path.join(ROOT,"Hackathon.db"))
c = conn.cursor()

#c.execute("DROP TABLE Guests") #empty table
#conn.commit
#c.execute("CREATE TABLE IF NOT EXISTS Guests( Guest_id INTEGER PRIMARY KEY AUTOINCREMENT, First_name TEXT NOT NULL, Last_name TEXT NOT NULL, Email_address TEXT NOT NULL, Level INTEGER DEFAULT 0 NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL);")
#c.execute("CREATE TABLE IF NOT EXISTS Levels( Level_id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Badge_color TEXT NOT NULL, Img TEXT, Text TEXT NOT NULL, Answer TEXT NOT NULL, Release_date TEXT NOT NULL);")
#c.execute("CREATE TABLE IF NOT EXISTS Discord( Link TEXT NOT NULL);")
#c.execute("INSERT INTO Discord (Link) VALUES ('LINK NOT SET',);")
#c.execute("CREATE TABLE IF NOT EXISTS EndBossAnswers(Guest_id_f INTEGER, Guest_name TEXT, Email_Address TEXT, Date_and_Time TIMESTAMP, Answer TEXT, FOREIGN KEY(Guest_id_f) REFERENCES Guests(Guest_id))")
#c.execute("DELETE FROM EndBossAnswers WHERE Guest_name = 'Tinus'")
#conn.commit


#---globalvars

global pilgrim, gamelevel

#---routes

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        lvl = session['level']
        output = username
        output= username

        if username == "admin":
            return render_template("admin.html", output = "Hello Admin !", level = "99")
    else:
        output = "Guest"
        return redirect("/register")

    c.execute("SELECT * FROM Guests WHERE Username = '%s'" % username)
    conn.commit()
    rows = c.fetchall()

    global pilgrim

    for row in rows:
        pilgrim = Pilgrim(row[0], row[1], row[2], row[3], row[4], row[5]) #creating instance of class Pilgrim

    return render_template('home.html', guest = output , level = lvl )

@app.route('/register', methods=["POST","GET"] )
def register():
    if request.method == 'POST':
 
        First_name = request.form.get("firstname")
        Last_name = request.form.get("lastname")
        Email_address = request.form.get("email")
        Username = request.form.get("username")
        Password = request.form.get("password")
        Password = hash_password(Password)  #hashing the password

        if Username_exists(Username):
            return render_template("message.html", message = "Username already exists", desto="/register" , pic = "empty.png")

        c.execute("INSERT INTO Guests (First_name, Last_name, Email_address, Username, Password) values (?, ?, ?, ?, ?)",(First_name, Last_name, Email_address, Username, Password))
        conn.commit

        session['username'] = Username
        session['level'] = "0"

        return redirect("/")

    return render_template('register.html', output = "Guest")

@app.route('/login', methods=["POST","GET"] )
def login():

    output = "Guest"

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        c.execute("SELECT Username FROM Guests")
        conn.commit()
        rows = c.fetchall()
        usernames = []
        for row in rows:
            usernames.append(row[0])
        if Username not in usernames:
            return render_template("message.html", message = "No such user", desto="/login", pic = "empty.png")

        c.execute("SELECT Password, Level FROM Guests WHERE Username = '%s'" % Username)
        conn.commit()
        rows = c.fetchall()

        stored_password = ""
        for row in rows:
            stored_password = row[0]
            level = row[1]

        provided_password = Password

        if verify_password(stored_password, provided_password):
            print("Logged in succesfully !")
            session['username'] = Username
            session['level'] = level

            return redirect("/")
        else :
            return render_template("message.html", message = "Passwords don't match", desto="/login", pic = "empty.png")



    return render_template('login.html')
 
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('level', None)
    return redirect("/login")

@app.route('/showguests', methods=["POST","GET"])
def showguests():

    if 'username' not in session:
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    
    output = "Welcome admin !"

    if request.method == 'POST':
        action = request.form.get("action")[:3]
        if action == "Del":
            record = request.form.get("action")
            record = int(record.split()[2]) # split "Delete 2"
            bericht = "Deleted record "+ str(record)
            c.execute("DELETE FROM Guests WHERE Guest_id = %s " % record)
            conn.commit()
            c.execute("SELECT * FROM Guests")
            conn.commit()

    c.execute("SELECT * FROM Guests")
    conn.commit()
    rows=c.fetchall()

    return render_template('showguests.html', rows=rows , output = output)

@app.route('/showranking', methods=["POST","GET"])
def showranking():

    if 'username' not in session:
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    
    output = "Welcome admin !"

    if request.method == 'POST':
        action = request.form.get("action")[:3]
        if action == "Del":
            record = request.form.get("action")
            record = int(record.split()[2]) # split "Delete 2"
            bericht = "Deleted record "+ str(record)
            c.execute("DELETE FROM Guests WHERE Guest_id = %s " % record)
            conn.commit()
            c.execute("SELECT * FROM Guests")
            conn.commit()

    c.execute("SELECT * FROM Guests ORDER BY Level DESC")
    conn.commit()
    rows=c.fetchall()

    return render_template('showranking.html', rows=rows , output = output)

@app.route('/showanswers', methods=["POST","GET"])
def showanswers():

    if 'username' not in session:
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    
    output = "Welcome admin !"

    if request.method == 'POST':
        action = request.form.get("action")[:3]
        if action == "Del":
            record = request.form.get("action")
            record = int(record.split()[2]) # split "Delete 2"
            bericht = "Deleted record "+ str(record)
            c.execute("DELETE FROM EndBossAnswers WHERE Guest_id_f = %s " % record)
            conn.commit()
            c.execute("SELECT * FROM EndBossAnswers")
            conn.commit()

    c.execute("SELECT * FROM EndBossAnswers ORDER BY Date_and_Time")
    conn.commit()
    rows=c.fetchall()

    return render_template('showanswers.html', rows=rows , output = output)


@app.route('/showlevels', methods = ["POST","GET"])

def showlevels():


    if 'username' not in session:
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login", pic = "empty.png")
    
    output = "Welcome admin !"

    if request.method == 'POST':
        action = request.form.get("action")[:3]
        if action == "Del":
            record = request.form.get("action")
            record = int(record.split()[2]) # split "Delete 2"
            bericht = "Deleted record "+ str(record)
            c.execute("DELETE FROM Levels WHERE Level_id = %s " % record)
            conn.commit()
            c.execute("SELECT * FROM Levels")
            conn.commit()
        elif action == "Edi":
            record = request.form.get("action")
            record = int(record.split()[2]) # split "Delete 2"
            session['level'] = record
            return redirect("/editlevel")

    c.execute("SELECT * FROM Levels ORDER BY Level_id")
    conn.commit()
    rows=c.fetchall()

    return render_template('showlevels.html', rows=rows , output = output)


@app.route('/level', methods = ["POST","GET"] )
def level():
    if 'username' not in session:
        return render_template("message.html", message = "Please login first", desto="/login" , pic = "empty.png")
    else :
        lvl = str(session['level'])
        user = session['username']
        if lvl == "22":
            print("### 1 ###")
            return redirect("/endgame")

        c.execute("SELECT * FROM Levels WHERE Level_id = %s" % lvl)
        conn.commit()
        rows = c.fetchall()

        for row in rows:
            gamelevel = Level(lvl,row[1],row[2],row[3],row[4],row[5],row[6])

        story = Markup(gamelevel.text)

        c.execute("SELECT * FROM Discord")
        conn.commit()
        rows = c.fetchall()

        for row in rows:
            link = row[0]



    now = datetime.datetime.now()
    today = Calcdate(now)
    release = int(gamelevel.date)



    if release > today:
        message = "This level will unlock on " + gamelevel.date
        return render_template("message.html", message = message, guest = user , level = lvl,desto = "/level" , pic = "empty.png")
    

    if request.method == 'POST':
        answer = request.form.get("answer")
        correct_answer = gamelevel.answer
        if answer == correct_answer:
            temp = int(lvl)
            temp +=1
            lvl = str(temp)
            session['level'] = lvl
            result = c.execute("UPDATE Guests SET Level ==:pv0 WHERE Username ==:pv1", {"pv0":temp, "pv1":user})
            conn.commit
            return render_template("message.html", message = "Well done young pilgrim ! Your answer is correct. You move up to the next level", guest = user , level = lvl, desto="/level"  , pic = "drag_fly.gif")
        else:
            return render_template("message.html", message = "Unfortunately that is not the right answer. But don't give up ! You WILL get there !", guest = user , level = lvl, desto="/level" , pic = "drag_loose.gif")

    story = Markup(gamelevel.text)

    return render_template('game.html', 
        title = gamelevel.name, 
        image = gamelevel.image, 
        guest = user, 
        level = lvl, 
        story = story,
        link = link)


@app.route('/createlevels', methods=["POST","GET"] )
def create_levels():
    
    if 'username' not in session:
        return render_template("message.html", message = "Please login first", desto="/login", pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login" , pic = "empty.png")
    
    if request.method == 'POST':
        id = request.form.get("number")
        name = request.form.get("name")
        color = request.form.get("color")
        image = request.form.get("image")
        text = request.form.get("text")
        answer = request.form.get("answer")
        date = request.form.get("date")

        gamelevel = Level(id,name,color,image,text,answer,date)

        c.execute("INSERT INTO Levels (Level_id, Name, Badge_color, Img, Text, Answer, Release_date) VALUES (?,?,?,?,?,?,?)", 
            (id,name,color,image,text,answer,date))
        conn.commit
        return render_template("message.html", message = "Level is created", desto="/createlevels", guest = "Admin" , level = "99" , pic = "empty.png")
    
    return render_template('levelcreator.html')

@app.route('/editlevel', methods=["POST","GET"] )
def editlevel():
    
    lvl = session['level']

    if 'username' not in session:
        return render_template("message.html", message = "Please login first", desto="/login" , pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login" , pic = "empty.png")
    
    if request.method == 'POST':

        id = request.form.get("number")
        name = request.form.get("name")
        color = request.form.get("color")
        image = request.form.get("image")
        text = request.form.get("text")
        answer = request.form.get("answer")
        date = request.form.get("date")

        gamelevel = Level(id,name,color,image,text,answer,date)

        c.execute("DELETE FROM Levels WHERE Level_id = %s" % id)
        conn.commit
        c.execute("INSERT INTO Levels (Level_id, Name, Badge_color, Img, Text, Answer, Release_date) VALUES (?,?,?,?,?,?,?)", 
            (id,name,color,image,text,answer,date))
        conn.commit
        return render_template("message.html", message = "Level is saved", desto="/showlevels", guest = "Admin" , level = "99" , pic = "empty.png")
    
    c.execute("SELECT * FROM Levels WHERE Level_id = %s" % lvl)
    conn.commit()
    rows = c.fetchall()
    for row in rows:
        gamelevel = Level(lvl,row[1],row[2],row[3],row[4],row[5],row[6])

    return render_template('leveleditor.html', 
        number = gamelevel.id , 
        name = gamelevel.name, 
        color = gamelevel.color, 
        image =  gamelevel.image, 
        text = gamelevel.text, 
        answer = gamelevel.answer, 
        date = gamelevel.date)

@app.route('/editDiscord' , methods=["POST", "GET"])
def editDiscord():
    if 'username' not in session:
        return render_template("message.html", message = "Please login first", desto="/login" , pic = "empty.png")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login" , pic = "empty.png")
    
    if request.method == 'POST':

        link = str(request.form.get("link"))
        c.execute("DELETE FROM Discord")
        conn.commit
        c.execute("INSERT INTO Discord (Link) VALUES (?)", 
            (link,))
        conn.commit
        return render_template("message.html", message = "Discordlink is saved", desto="/", guest = "Admin" , level = "99" , pic = "empty.png")
    
    c.execute("SELECT * FROM Discord")
    conn.commit()
    rows = c.fetchall()
    saved_link = "#"
    for row in rows:
        saved_link = row[0]

    return render_template('discordEditor.html', 
        saved_link = saved_link)

#Functions without routes

def Username_exists(Username):
    c.execute("SELECT Username FROM Guests")
    conn.commit()
    rows=c.fetchall()
    usernames = []
    for row in rows:
        usernames.append(row[0])
    if Username not in usernames:
        return False
    else:
        return True

def Calcdate(now):
    year = str(now.year)
    month = str(now.month)
    if len(month) < 2:
        month = "0" + month
    day = str(now.day)
    if len(day) < 2:
        day = "0" + day  

    total = year + month + day  
    
    return int(total)

@app.route('/endgame', methods=["POST","GET"])
def Endgame():
    lvl = str(session['level'])
    user = session['username']
    if 'username' not in session:
        return render_template("message.html", message = "Please login first", desto="/login" , pic = "empty.png")
    elif lvl!="22":
        return render_template("message.html", message = "Finish the first 21 levels, please !", desto="/" , pic = "empty.png")
    else:
        if request.method == 'POST':
            answer = request.form.get("code")
            id = "999999"
            if answer:
                #result = c.execute("SELECT Guest_id FROM Guests WHERE Username = 'user'")
                result = c.execute("SELECT Guest_id,Email_address FROM Guests WHERE Username = ?", (user,))
                conn.commit
                rows = c.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        id = str(row[0])
                        email = str(row[1])
                else:
                    return render_template("message.html", message = "Strange, but this user is not in our Database", desto="/" , pic = "empty.png")
                result = c.execute("SELECT Guest_id_f FROM EndBossAnswers WHERE Guest_name = ?",(user,))
                conn.commit
                rows = c.fetchall()
                if len(rows) > 0:
                    c.execute("UPDATE EndBossAnswers SET Answer ==:pv0 WHERE Guest_id_f ==:pv1", {"pv0":answer, "pv1":id})
                    return render_template("message.html", message = "Your answer is updated", desto="/" , pic = "empty.png")
                else:
                    now = datetime.datetime.now()
                    today = Calcdate(now)
                    c.execute("INSERT INTO EndBossAnswers (Guest_id_f, Guest_name,Email_address, Date_and_Time, Answer) VALUES (?,?,?,?,?)",(id, user, email, today, answer) )
                    return render_template("message.html", message = "Your answer is stored in our Database. You will hear from us shortly !", desto="/" , pic = "empty.png")
                
            else:
                return render_template("message.html", message = "Your answer was empty ??", guest = user , level = lvl, desto="/endgame" , pic = "drag_loose.gif")
    result = c.execute("SELECT Answer FROM EndBossAnswers WHERE Guest_name = ?",(user,))
    conn.commit
    rows = c.fetchall()
    if len(rows) >0:
        for row in rows:
            placeholder = row[0]
    else:
        placeholder = "Put your code here"

    name = str(session['username'])
    story = Markup('''
            <h2>Congratulations, my young Pilgim ! You have made it to the final round.</h2>
            <br/>
            <img src="static/Dragon_final.png" width = "400"/>
            <br/><br/>
            <h3>It is time that you battle ME, the dragon !<br/>
            By this time you should have figured out what my strength is...<br/>
            My strength is the knowledge of coding ! The power to CREATE !</h3>
            <br/>
            <h3>It is now time for you to create !</h3>
            <br/>
            <h3>Here is your assignment : </h3>
            <br/>
            <h3 class="assignment">Find out for me what the "Fibonacci sequence" is.<br/>
            Then... write a python application that adds up all Fibonacci numbers under 1000.<br/>
            Now.. I don't want the answer. I know the answer !<br/>
            I want you to post your code here and submit it.<br/>
            I will be looking at the way you coded it, how much time your app takes to do the math 
            and how much memory it uses.</h3>
            <br/>
            <h3>Now go ahead and create that code !</h3><br/>
            <h3>You will find a website to create your code here. </br>
            <h3>When done, paste your code in the box under this line and click 'Submit'</h3></br>
            <img src="static/Arrow_down.png" width = "200"/>

    ''')
    return render_template("endgame.html", guest = name, story = story, placeholder = placeholder)