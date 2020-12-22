import collections
from urllib import parse
import json
from flask import Flask, request, render_template, url_for, session,redirect,jsonify
import sqlite3
#from emailverifier import Client
#from emailverifier import exceptions
import re
#from flask_mail import Mail , Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import data_base_calls as dbc
from flask_socketio import SocketIO, send, emit



app = Flask(__name__)
#############################################################################################################
app.config['SECRET_KEY'] = 'niceWork@EKKO2'
app.config['DEBUG']=True
app.config['TESTING']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']="623264tag@gmail.com"
app.config['MAIL_PASSWORD']="bsse02163094@outlook.com"
app.config['MAIL_DEFAULT_SENDER']="623264tag@gmail.com"
app.config['MAIL_USE_TLS'] = True
app.config['JSON_AS_ASCII'] = False
######################################################################################################################


mail = Mail(app)
s = URLSafeTimedSerializer('niceWork@EKKO2')

def characterCheaker(string):
    regex = re.compile('[1234567890@_!#$%^&*()<>?/\|}{~: ]')
    if (regex.search(string) == None):
        return True
    else:
        return False


def email_verifier(email):
    client = Client('at_JRHtlBjqHgBwZVgvgQGJFFprt6OEh')
    try:
        data = client.get(email)
        return data
    # If you get here, it means service returned HTTP error code
    except exceptions.HttpException:
        pass

    # If you get here, it means you cannot connect to the service
    except exceptions.GeneralException:
        pass

    # If you get here, it means you forgot to specify the API key
    except exceptions.UndefinedVariableException:
        pass

    # If you get here, it means you specified invalid argument
    # (options should be a dictionary)
    except exceptions.InvalidArgumentException:
        pass

    except:
        pass
    # Something else happened related.Maybe you hit CTRL - C
    # while the program was running, the kernel is killing your process, or
    # something else all together.

def email_sender(email):
    try:
        token = s.dumps(email, salt='email-confirm')
        msg = Message("Confirm Email", sender="623264tag@gmail.com", recipients=[output.email_address])
        link = url_for('con', token=token, _external=True)
        msg.body = 'Confirm Yor email You link is {}'.format(link)
        mail.send(msg)
    except Exception as err:
        return str(err)
    return """<h1>email is {}. the token is {}""".format(email, token)



@app.route('/')
def index():
    return render_template("sign-up.html")


@app.route('/sign-up.html',methods = ['POST', 'GET'])
def sign_up():
    return render_template("sign-up.html")

@app.route('/reg',methods=['POST'])
def reg():
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    if request.method == 'POST':
        user = request.form['name']
        userl = request.form['namel']
        pas = request.form['pwd']
        email = request.form['email']
        if (email != ""):
            output = email_verifier(email)
            try:
                if output.format_check == True:
                    if characterCheaker(user) and characterCheaker(userl):
                        if len(pas) > 2:
                            c.execute("	SELECT * FROM User WHERE email=:email", {"email": email})
                            conn.commit()
                            if len(c.fetchall()) > 0:
                                return jsonify({"status": "err",
                                                "type":"email",
                                                "discription":"Existiong email"})
                            else:
                                c.execute(
                                    "INSERT INTO User (user_name,user_namel,password,email) VALUES (:user_name,:user_namel,:password,:email)",
                                    {'user_name': user,'user_namel':userl, 'password': pas, "email": email})
                                conn.commit()
                                c.execute("	SELECT user_id FROM User WHERE email=:email", {"email": email})
                                email_sender(email)
                                return jsonify({"status": "done",
                                                "type": "email_sent",
                                                "discription": "Check Email"})
                        else:
                            return jsonify({"status": "err",
                                            "type": "password",
                                            "discription": "invalid password"})
                    else:
                        return jsonify({"status": "err",
                                        "type": "name",
                                        "discription": "invalid name"})
            except Exception as err:
                return str(err)
            # return "plz enter correct email"
        # c.execute("	SELECT * FROM User WHERE user_name=:user",{"user":user})
        # print(c.fetchall())






@app.route('/sign-in.html',methods = ['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        pas = request.form['pas']
        email = request.form['email']
        conn = sqlite3.connect("FYP.db")
        c = conn.cursor()
        c.execute('	SELECT * FROM User WHERE email=:email AND password=:pas', {"email":email,"pas":pas})
        g = c.fetchall()
        if(len(g)==1):
            if g[0][4] == 1:
                session["Userid"] = g[0][0]
                session["Usename"] = g[0][3]
                return redirect(url_for('profile'))
            else:
                return render_template("email_sent_confirm.html")
    return render_template("sign-in.html")


@app.route('/index.html')
def profile():
    if session.get("Userid",None) is not None:
        userid=session.get("Userid")
        #####################
        profile_data = dbc.get_user_info(userid=userid)
        notification = dbc.get_user_nonconf_friendlist(userid=userid)
        friends = dbc.get_user_conf_friendlist(userid=userid)
        chat_info = dbc.get_user_chat_log(userid=userid)
        ######################
        data={"profile_data":profile_data,"notification":notification,"friends":friends,"chat_info":chat_info}
        #return data
        return render_template("index.html", data= data)


@app.route('/addfriend',methods=['POST'])
def addfriend():
    if session.get("Userid", None) is not None:
        user_id = session.get("Userid")
        email = request.form['name']
        return jsonify(dbc.insert_friend_table(user_id=user_id,email=email))

@app.route('/accpetfriend',methods=['POST'])
def accpetfriend():
    if session.get("Userid", None) is not None:
        user_id = session.get("Userid")
        email = request.form['email']
        data=dbc.accpet_friend_req(user_id=user_id,email=email)
        userinfo=dbc.get_user_info(user_id)
        if dbc.section_finder(data.friend_id)!=False:
            emit("conv_msg", json.dumps({"conid":data.conid,"Name":userinfo.fname+" "+userinfo.lname,"email":userinfo.email,"friend_id":user_id}), room=dbc.section_finder(data.friend_id))
        return jsonify(data)





@app.route('/delfriendreq',methods=['POST'])
def delfriendreq():
    if session.get("Userid", None) is not None:
        user_id = session.get("Userid")
        email = request.form['email']
        return jsonify(dbc.del_friend_req(user_id=user_id,email=email))


socketio = SocketIO(app,cors_allowed_origins="*")

def predict():
    return -1




@socketio.on('message')
def handleMessage(msg):
    print(msg)
    if (type(msg)==type({"ok":0})):
        s1 = json.dumps(msg)
        mg = json.loads(s1)
        print(parse.unquote_plus(mg['text']))
        print(msg)
        if(dbc.section_finder(mg['receiver'])==False):
            dbc.insert_msg(sender=session.get("Userid"), reciver=mg['receiver'], text=parse.unquote_plus(mg['text']), prediction=predict())
            dbc.insert_into_chat(con_id=mg['conversation'],msg_id=cal.find_new_text_id(session.get("Userid"), mg['receiver']))
        else:
            dbc.insert_msg(sender=session.get("Userid"), reciver=mg['receiver'], text=parse.unquote_plus(mg['text']), prediction=predict())
            dbc.insert_into_chat(con_id=mg['conversation'],msg_id=dbc.find_new_text_id(session.get("Userid"), mg['receiver']))
            emit("p_msg", json.dumps(msg), room=dbc.section_finder(mg['receiver']))

        #emit("p_msg",json.dumps(msg),room=request.sid)
    else:
        #print(request.sid)
        """conn = sqlite3.connect("FYP.db")
        c = conn.cursor()
        c.execute("	SELECT * FROM maper WHERE user_id=:user_id",{'user_id':msg})
        temp=c.fetchall()
        print(temp)"""
        if(dbc.section_finder(msg)==False):
            dbc.insert_into_maper(user_id=msg, sid=request.sid)
            #c.execute("INSERT INTO maper (user_id,sid) VALUES (:user_id,:sid)", { 'user_id':msg,'sid': request.sid})
            #conn.commit()
            #conn.close()
        else:
            dbc.insert_update_maper(user_id=msg, sid=request.sid)
            #c.execute("UPDATE maper SET sid=:sid WHERE user_id=:user_id",{'user_id':msg,'sid': request.sid})
            #conn.close


@app.route('/con/<token>')
def con(token):
    try:
        email = s.loads(token,salt='email-confirm', max_age = 30000)
    except:
        return "<h1>Error</h1>"

    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("	UPDATE User SET status = 1 WHERE email=:email", {"email": email})
    conn.commit()
    c.execute("	SELECT * FROM User WHERE email=:email", {"email": email})
    temp=c.fetchall()
    session ["Userid"] = temp[0][0]
    session ["Usename"] = temp[0][3]
    #redirect here
    return render_template("Profile.html")

@app.route('/email_sent_confirm.html')
def confirm():
    return render_template("email_sent_confirm.html")