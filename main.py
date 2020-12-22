import json

from urllib import parse
from flask import Flask , request, render_template , url_for , session
from flask_socketio import SocketIO, send, emit
import sqlite3
#from emailverifier import Client
#from emailverifier import exceptions
#from flask_mail import Mail , Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import re
import profile
import data_base_calls as cal
import numpy as np
import pandas as pd
#coding: 'utf-8'


'''#####################################
from keras.models import Sequential
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding,GRU
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers import Bidirectional
from keras.layers import SimpleRNN
#######################################'''



conn = sqlite3.connect("FYP.db")
c = conn.cursor()


#c.execute("	DROP TABLE Conversation_log")
#c.execute("""CREATE TABLE Conversation_log (id  INTEGER PRIMARY KEY AUTOINCREMENT, user_id_1 INTEGER NOT NULL,user_id_2 INTEGER NOT NULL,FOREIGN KEY (user_id_1) REFERENCES User (user_id),FOREIGN KEY (user_id_2) REFERENCES User (user_id))""")



#c.execute("INSERT INTO Message (user_id,friend_id) VALUES (:user_id,:friend_id)", {'user_id': 1, 'friend_id': 2})
#c.execute("""CREATE TABLE User_info (user_id   INTEGER PRIMARY KEY, phone_number INTEGER NOT NULL,FOREIGN KEY (user_id) REFERENCES User (user_id))""")

#c.execute("INSERT INTO Friend_list (user_id,friend_id) VALUES (:user_id,:friend_id)", {'user_id': 1, 'friend_id': 2})
#c.execute("INSERT INTO Friend_list (user_id,friend_id) VALUES (:user_id,:friend_id)", {'user_id': 2, 'friend_id': 1})
#c.execute("INSERT INTO Conversation_log (user_id_1,user_id_2) VALUES ('3','2')")
#conn.commit()
#c.execute("INSERT INTO Message (id,sender,reciver,text,prediction) VALUES (:id,:sender,:reciver,:text,:prediction)", {'id': 1,'sender':2 ,'reciver':3,'text':"nice work",'prediction': -1})


#email verification
######################################################################################################################
######################################################################################################################
######################################################################################################################
#app = Flask(__name__)

######################################################################################################################
######################################################################################################################





"""@app.route('/login.html')
def login():
    return render_template("login.html")"""


"""@app.route('/signup.html',methods = ['POST', 'GET'])
def signup():
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    if request.method == 'POST':
        user = request.form['uname']
        pas = request.form['psw']
        email = request.form['email']
        if(email != ""):
            output=email_verifier(email)
            try:
                if output.format_check==True:
                    if characterCheaker(user):
                        if len(pas)>2:
                            c.execute("	SELECT * FROM User WHERE email=:email", {"email": email})
                            conn.commit()
                            if len(c.fetchall())>0:
                                return "Email already in system"
                            else:
                                c.execute("INSERT INTO User (user_name,password,email) VALUES (:user_name,:password,:email)", { 'user_name':user,'password': pas,"email":email})
                                conn.commit()
                                c.execute("	SELECT user_id FROM User WHERE email=:email", {"email": email})
                                print(c.fetchall())
                                return email_sender(email)
                        else:
                            return "invalid password"
                    else:
                        #invalid email
                        return render_template("signup.html")
            except Exception as err:
                    return str(err)
                #return "plz enter correct email"
        #c.execute("	SELECT * FROM User WHERE user_name=:user",{"user":user})
        #print(c.fetchall())

    else:
        return render_template("signup.html")"""




if __name__== '__main__':
    profile.app.run(debug=True)
    profile.socketio.run(profile.app)