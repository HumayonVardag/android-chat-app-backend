import sqlite3
conn = sqlite3.connect("FYP.db")
c = conn.cursor()


#final commands for Database Creation
#c.execute("PRAGMA foreign_keys = ON")
#c.execute("""CREATE TABLE User ( user_id INTEGER PRIMARY KEY AUTOINCREMENT , password TEXT NOT NULL , email TEXT NOT NULL , user_name TEXT NOT NULL,status INTEGER DEFAULT 0 NOT NULL , user_namel TEXT NOT NULL) """)
#conn.commit()
#c.execute("""CREATE TABLE User_info (user_id   INTEGER PRIMARY KEY, phone_number INTEGER NOT NULL,FOREIGN KEY (user_id) REFERENCES User (user_id))""")
#conn.commit()
#c.execute("DROP TABLE Chat")
#c.execute("""CREATE TABLE Friend_list (user_id  INTEGER NOT NULL, friend_id INTEGER NOT NULL,status INTEGER DEFAULT 0 NOT NULL , FOREIGN KEY (user_id) REFERENCES User (user_id),FOREIGN KEY (friend_id) REFERENCES User (user_id))""")
#conn.commit()
#c.execute("""CREATE TABLE Conversation_log (id  INTEGER PRIMARY KEY AUTOINCREMENT, user_id_1 INTEGER NOT NULL,user_id_2 INTEGER NOT NULL,FOREIGN KEY (user_id_1) REFERENCES User (user_id),FOREIGN KEY (user_id_2) REFERENCES User (user_id))""")
#c.execute("	DROP TABLE Message")
#c.execute("	DROP TABLE Chat")
#conn.commit()
#c.execute("""CREATE TABLE Message (id  INTEGER PRIMARY KEY, sender INTEGER NOT NULL,reciver INTEGER NOT NULL,text VARCHAR(200),prediction INTEGER,  FOREIGN KEY (sender) REFERENCES User (user_id),FOREIGN KEY (reciver) REFERENCES User (user_id))""")
#conn.commit()
#c.execute("""CREATE TABLE Chat (cov_id  INTEGER , msg_id  INTEGER,  FOREIGN KEY (cov_id) REFERENCES Conversation_log (id),FOREIGN KEY (msg_id) REFERENCES Message (id))""")
#conn.commit()
c.execute("	DROP TABLE maper")

#c.execute("""ALTER TABLE User ADD user_namel TEXT""") #NOT NULL
c.execute("""CREATE TABLE maper (user_id   INTEGER PRIMARY KEY, sid TEXT NOT NULL,FOREIGN KEY (user_id) REFERENCES User (user_id))""")
conn.commit()
print("Messages")
c.execute("	SELECT * FROM Message WHERE 1")
print(c.fetchall())
print("Chat")
c.execute("	SELECT * FROM Chat WHERE 1")
print(c.fetchall())
print("Conv to user")
c.execute("	SELECT * FROM Conversation_log WHERE 1")
print(c.fetchall())
print("Friend lists")
c.execute("	SELECT * FROM Friend_list WHERE 1")
print(c.fetchall())
#conn.commit()
print("users")
c.execute("	SELECT * FROM User WHERE 1")
print(c.fetchall())
conn.commit()

conn.close()


def insert_friend_table(user_id,email):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute('	SELECT user_id FROM User WHERE email=:email ', {"email": email})
    conn.commit()
    g = c.fetchall()
    if (len(g) == 1):
        friend_id = g[0][0]
        c.execute('	SELECT * FROM Friend_list WHERE user_id=:user_id AND friend_id=:friend_id',
                  {"user_id": user_id, "friend_id": friend_id})
        conn.commit()
        g = c.fetchall()
        c.execute('	SELECT * FROM Friend_list WHERE user_id=:user_id AND friend_id=:friend_id',
                  {"user_id": friend_id, "friend_id": user_id})
        conn.commit()
        t = c.fetchall()
        print(len(g) , len(t))
        if (len(g) == 0 and len(t) == 0):
            c.execute("INSERT INTO Friend_list (user_id,friend_id,status) VALUES (:user_id,:friend_id,:status)",
                      {"user_id": user_id, "friend_id": friend_id,"status":-1})
            conn.commit()
            c.execute("INSERT INTO Friend_list (user_id,friend_id) VALUES (:user_id,:friend_id)",
                      {"user_id": friend_id, "friend_id": user_id})
            conn.commit()
            c.execute('	SELECT * FROM User WHERE user_id=:user_id', {"user_id": friend_id})
            conn.commit()
            g = c.fetchall()
            conn.close()
            return {"status": "sent", "name": g[0][3]}
        else:
            conn.close()
            return {"status": "pandding"}
    else:
        return {"status": "not_user"}



def find_new_text_id(sender,receiver):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("SELECT  * from Message WHERE reciver=:reciver AND sender=:sender ",
              {'sender': sender, 'reciver': receiver})
    conn.commit()
    allmsg = c.fetchall()
    msgid = allmsg[-1][0]
    conn.close()
    return msgid


def insert_msg(sender,reciver,text,prediction):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("INSERT INTO Message (sender,reciver,text,prediction) VALUES (:sender,:reciver,:text,:prediction)",
              {'sender':sender, 'reciver':reciver, 'text':text, 'prediction':prediction})
    print(text)
    conn.commit()
    conn.close()

def insert_into_chat(con_id,msg_id):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("INSERT INTO Chat (cov_id, msg_id) VALUES (:cov_id,:msg_id)",{'cov_id':con_id, 'msg_id':msg_id})
    conn.commit()
    conn.close()

def section_finder(friend):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("	SELECT sid FROM maper WHERE user_id=:user_id", {'user_id':friend})
    receiver_sid = c.fetchall()
    conn.close()
    if (len(receiver_sid) == 0):
        return False
    else:
        return receiver_sid[0][0]

def insert_into_maper(user_id,sid):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("INSERT INTO maper (user_id,sid) VALUES (:user_id,:sid)", {'user_id':user_id, 'sid':sid})
    conn.commit()
    conn.close()

def insert_update_maper(user_id,sid):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute("UPDATE maper SET sid=:sid WHERE user_id=:user_id",{ 'user_id':user_id,'sid':sid})
    conn.commit()
    conn.close()


#get User profile info
def get_user_info(userid):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute('	SELECT * FROM User WHERE user_id=:user_id ', {"user_id": userid})
    conn.commit()
    g = c.fetchall()
    conn.close()
    return {"userid": userid, "fname": str(g[0][3]), "lname": str(g[0][5]), "email": str(g[0][2]),"password": str(g[0][1])}

#get User friend names confirmed
def get_user_conf_friendlist(userid):
    conn = sqlite3.connect("FYP.db")
    ffn=[]
    fe=[]
    fln=[]
    c = conn.cursor()
    c.execute('SELECT friend_id FROM Friend_list WHERE user_id=:user_id AND status = 1', {"user_id": userid})
    conn.commit()
    temp = c.fetchall()
    if len(temp) != 0:
        for i in temp:
            c.execute('SELECT email,user_name FROM User WHERE user_id=:user_id', {"user_id": i[0]})
            conn.commit()
            g = c.fetchall()
            ffn.append(g[0][1])
            fe.append(g[0][0])
    conn.close()
    return {"name":ffn,"email":fe}

def get_user_nonconf_friendlist(userid):
    conn = sqlite3.connect("FYP.db")
    ffn = []
    fe = []
    frs = []
    c = conn.cursor()
    c.execute('SELECT friend_id,status FROM Friend_list WHERE user_id=:user_id AND ( status = 0 OR status =-1 )', {"user_id": userid})
    conn.commit()
    temp = c.fetchall()
    if len(temp) != 0:
        for i in temp:
            c.execute('SELECT email,user_name FROM User WHERE user_id=:user_id', {"user_id": i[0]})
            conn.commit()
            g = c.fetchall()
            ffn.append(g[0][1])
            fe.append(g[0][0])
            frs.append(i[1])
            conn.commit()
    conn.close()
    return {"name": ffn, "email": fe , "status":frs}

def get_user_chat_log(userid):
    conn = sqlite3.connect("FYP.db")
    chatid = []
    chatother=[]
    chatothername=[]
    chatms= []
    c = conn.cursor()
    c.execute('SELECT * FROM Conversation_log WHERE (user_id_1=:user_id_1 AND user_id_2=:user_id_2) OR (user_id_2=:user_id_1 AND user_id_2=:user_id_1)',
              {"user_id_1": userid, "user_id_2": userid})
    conn.commit()
    temp = c.fetchall()
    if len(temp) != 0:
        for i in temp:
            chatid.append(i[0])
            if i[1] == userid:
                chatother.append(i[2])
                c.execute('SELECT user_name FROM User WHERE user_id=:user_id ', {"user_id": i[2]})
                conn.commit()
                chatothername.append(c.fetchall()[0][0])

            else:
                chatother.append(i[1])
                c.execute('SELECT user_name FROM User WHERE user_id=:user_id ', {"user_id": i[1]})
                conn.commit()
                chatothername.append(c.fetchall()[0][0])
            c.execute('SELECT * FROM Chat WHERE cov_id=:cov_id', {"cov_id": i[0]})
            conn.commit()
            chats = c.fetchall()
            if len(chats) != 0:
                templist = list()
                for j in chats:
                    print(j)
                    c.execute('SELECT * FROM Message WHERE id=:id', {"id": j[1]})
                    conn.commit()
                    templist.append(c.fetchall()[0])
                chatms.append(templist)
            else:
                templist = list()
                chatms.append(templist)
        conn.close()
        return {"id":chatid,"other":chatother,"other_name":chatothername,"messege":chatms}
    else:
        conn.close()
        return {"id": chatid, "other": chatother, "other_name": chatothername, "messege": chatms}


def get_id_by_email(email):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    c.execute('	SELECT user_id FROM User WHERE email=:email ', {"email": email})
    conn.commit()
    g = c.fetchall()
    conn.close()
    if len(g)==1:
        return g[0][0]
    else:
        -1

def accpet_friend_req(user_id,email):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    friend_id=get_id_by_email(email)
    c.execute("UPDATE Friend_list SET status=1 WHERE user_id=:user_id AND friend_id=:friend_id", {'user_id': user_id, 'friend_id':friend_id})
    conn.commit()
    c.execute("UPDATE Friend_list SET status=1 WHERE user_id=:user_id AND friend_id=:friend_id",{'user_id':friend_id, 'friend_id': user_id})
    conn.commit()
    c.execute("INSERT INTO Conversation_log (user_id_1,user_id_2) VALUES (:user_id,:friend_id)",{'friend_id':friend_id, 'user_id':user_id})
    conn.commit()
    c.execute('SELECT * FROM Conversation_log WHERE (user_id_1=:user_id_1 AND user_id_2=:user_id_2) OR (user_id_2=:user_id_1 AND user_id_2=:user_id_1)',{"user_id_1": friend_id, "user_id_2": user_id})
    conn.commit()
    g = c.fetchall()
    conversation_id=''
    temp={}
    if(len(g)==1):
        temp=get_user_info(friend_id)
        conversation_id=g[0][0]
    conn.close()
    return {"status":"done","conid":conversation_id,"Name":temp.fname+" "+temp.lname,"friend_id":friend_id}


def del_friend_req(user_id,email):
    conn = sqlite3.connect("FYP.db")
    c = conn.cursor()
    friend_id=get_id_by_email(email)
    c.execute("DELETE FROM Friend_list WHERE user_id=:user_id AND friend_id=:friend_id",{'user_id': user_id, 'friend_id': friend_id})
    conn.commit()
    c.execute("DELETE FROM Friend_list WHERE user_id=:user_id AND friend_id=:friend_id", {'user_id':friend_id, 'friend_id': user_id})
    conn.commit()
    c.execute('SELECT * FROM Conversation_log WHERE user_id_1=:user_id_1 AND user_id_2=:user_id_2',
              {"user_id_1": friend_id, "user_id_2": user_id})
    conn.close()
    return {"status": "done"}