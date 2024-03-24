import sqlite3
from utility import *

class DBOps:
    def __init__(self, config):
        self.con = sqlite3.connect(config["AUTH_DB_PATH"])
        self.table_name = config["AUTH_TABLE_NAME"]
        self.interest_mapping_table_name = config["INTEREST_MAPPING_TABLE_NAME"]
        cur = self.con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name}(
            "username" TEXT,
            "password" TEXT,
            "type" TEXT,
            "profilePic" TEXT,
            "email" TEXT,
            "userID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "isActive" INTEGER
        )""")
        self.con.commit()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.interest_mapping_table_name}(
            "userID" INTEGER,
            "WordIndex" TEXT
        )""")
        self.con.commit()
    def executeQuery(self, query, val, return_mode = True):
        cur = self.con.cursor()

        if return_mode == True:
            cur.execute(query, val)
            response = cur.fetchall()
            return response
        else:
            cur.execute(query, val)
            self.con.commit()
        
    def destruct(self):
        self.con.commit()
        self.con.close()

def checkCredentials(userId,password):
    config = read_config()
    db=DBOps(config)
    query="SELECT count(*) FROM "+config['AUTH_TABLE_NAME']+" WHERE username=? AND password=?"
    val=(userId,password)
    count=db.executeQuery(query, val)
    if((count[0][0]==1) and (checkActiveStatus(userId)==True)):
        status=True
        msg="You are successfully logged in!"
        category='alert alert-success'
        query_data="SELECT username,email,profilePic,type,userID FROM "+config['AUTH_TABLE_NAME']+" WHERE username=?"
        val=(userId,)
        res=db.executeQuery(query_data, val)
    elif((count[0][0]==1) and (checkActiveStatus(userId)==False)):
        status=False
        msg="Your account is pending to be activated by administrator!"
        res=""
        category='alert alert-danger'
    else:
        status=False
        msg="Wrong "+config['AUTH_TABLE_NAME']+"!"
        res=""
        category='alert alert-danger'
    db.destruct()        
    return status, res, msg, category

def checkActiveStatus(userId):
    config = read_config()
    db=DBOps(config)
    query="SELECT count(*) FROM "+config['AUTH_TABLE_NAME']+" WHERE username=? AND isActive=?"
    val=(userId,1)
    count=db.executeQuery(query, val)
    db.destruct()
    if count[0][0]==1:
        return True
    else:
        return False

def register(userId,password,email,profilePath):
    config = read_config()
    db=DBOps(config)
    query_check="SELECT count(*) FROM "+config['AUTH_TABLE_NAME']+" WHERE username=?"
    val=(userId,)
    count=db.executeQuery(query_check, val)
    if count[0][0]!=0:
        db.destruct()
        return False 
    else:   
        query="INSERT INTO "+config['AUTH_TABLE_NAME']+"(username,password,email,profilePic,type,isActive) VALUES (?,?,?,?,?,?)"
        val=(userId,password,email,profilePath,'user',1)
        db.executeQuery(query, val, return_mode=False)
        db.destruct()
        return True

def getUsers():
    config = read_config()
    db=DBOps(config)
    query="SELECT userID,profilePic,username,email,isActive FROM "+config['AUTH_TABLE_NAME']+" WHERE type='user'"
    data=db.executeQuery(query, val = ())
    db.destruct()
    return data

def activate(id):
    config = read_config()
    db=DBOps(config)
    query="UPDATE "+config['AUTH_TABLE_NAME']+" SET isActive=1 WHERE userID=?"
    val=(id,)
    data=db.executeQuery(query,val, return_mode=False)
    db.destruct()
    return

def deactivate(id):
    config = read_config()
    db=DBOps(config)
    query="UPDATE "+config['AUTH_TABLE_NAME']+" SET isActive=0 WHERE userID=?"
    val=(id,)
    data=db.executeQuery(query,val, return_mode=False)
    db.destruct()
    return

def changeUserName(id,newName):
    config = read_config()
    db=DBOps(config)
    query="UPDATE "+config['AUTH_TABLE_NAME']+" SET username=? WHERE userID=?"
    val=(newName,id)
    data=db.executeQuery(query,val, return_mode=False)
    db.destruct()
    return

def changePassword(id,newPass):
    config = read_config()
    db=DBOps(config)
    query="UPDATE "+config['AUTH_TABLE_NAME']+" SET password=? WHERE userID=?"
    val=(newPass,id)
    data=db.executeQuery(query,val, return_mode=False)
    db.destruct()
    return

def changeEmail(id,newEmail):
    config = read_config()
    db=DBOps(config)
    query="UPDATE "+config['AUTH_TABLE_NAME']+" SET email=? WHERE userID=?"
    val=(newEmail,id)
    data=db.executeQuery(query,val, return_mode=False)
    db.destruct()
    return

def save_word_index_mapping(word_indexes, userId):
    config = read_config()
    db=DBOps(config)
    query="INSERT INTO "+config['INTEREST_MAPPING_TABLE_NAME']+" (userID, WordIndex) VALUES (?, ?)"
    check_query = "SELECT COUNT(*) FROM "+config['INTEREST_MAPPING_TABLE_NAME']+" WHERE userID = ? AND WordIndex = ?"
    for word_index in word_indexes:
        val=(userId, word_index)
        count = db.executeQuery(check_query, val)
        if count[0][0] != 0:
            continue
        db.executeQuery(query, val, return_mode = False)
    db.destruct()
    return

def delete_word_index_mapping(word_indexes, userId):
    config = read_config()
    db=DBOps(config)
    query="DELETE FROM "+config['INTEREST_MAPPING_TABLE_NAME']+" WHERE userID = ? AND WordIndex = ?"
    check_query = "SELECT COUNT(*) FROM "+config['INTEREST_MAPPING_TABLE_NAME']+" WHERE userID = ? AND WordIndex = ?"
    for word_index in word_indexes:
        val=(userId, word_index)
        count = db.executeQuery(check_query, val)
        if count[0][0] == 0:
            continue
        db.executeQuery(query, val, return_mode = False)
    db.destruct()
    return

def get_word_index_mapping(userId):
    config = read_config()
    db=DBOps(config)
    query="SELECT WordIndex FROM "+config['INTEREST_MAPPING_TABLE_NAME']+" WHERE userID = ? "
    val=(userId,)
    data = db.executeQuery(query, val, return_mode = True)
    result = []
    for d in data:
        result.append(d[0])
    return result