import sqlite3
from utility import *
from datetime import datetime, timedelta
import hashlib
import numpy as np

class DBOps:
    def __init__(self, config):
        self.con = sqlite3.connect(config["AUTH_DB_PATH"])
        self.table_name = config["AUTH_TABLE_NAME"]
        self.interest_mapping_table_name = config["INTEREST_MAPPING_TABLE_NAME"]
        self.event_table_name = config["EVENT_TABLE_NAME"]
        self.event_recommendation_table_name = config["EVENT_RECOMMENDATION_TABLE_NAME"]
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
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.event_table_name}(
            "eventID" TEXT,
            "WordIndex" TEXT,
            "eventName" TEXT,
            "eventDescription" TEXT,
            "eventDate" TIMESTAMP,
            "eventAddress" TEXT
        )""")
        self.con.commit()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.event_recommendation_table_name}(
            "eventID" TEXT,
            "userID" INTEGER
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

def get_word_index():
    config = read_config()
    db=DBOps(config)
    query="SELECT userID, WordIndex FROM "+config['INTEREST_MAPPING_TABLE_NAME']
    val=()
    data = db.executeQuery(query, val, return_mode = True)
    result = []
    for d in data:
        result.append([d[0],d[1]])
    return result

def create_index():
    date_component = datetime.now() + timedelta(days = np.random.randint(-100, 100))
    return hashlib.md5(date_component.strftime("%Y-%m-%d").encode()).hexdigest()[ : 16]

def save_event(word_indexes, event_name, event_description, event_date, event_address):
    config = read_config()
    db=DBOps(config)
    event_id = create_index()
    query="INSERT INTO "+config['EVENT_TABLE_NAME']+" (eventID, WordIndex, eventName, eventDescription, eventDate, eventAddress) VALUES (?, ?, ?, ?, ?, ?)"
    check_query = "SELECT COUNT(*) FROM "+config['EVENT_TABLE_NAME']+" WHERE eventName = ? AND WordIndex = ?"
    for word_index in word_indexes:
        val=(event_name, word_index)
        count = db.executeQuery(check_query, val)
        if count[0][0] != 0:
            continue
        val1 = (event_id, word_index, event_name, event_description, event_date, event_address)
        db.executeQuery(query, val1, return_mode = False)
    db.destruct()
    return

def get_events(userID = None):
    config = read_config()
    db=DBOps(config)
    if userID is None:
        query = f"""
            SELECT
                eventID,
                eventName,
                eventDescription,
                eventDate,
                eventAddress,
                GROUP_CONCAT(WordIndex) as WordIndex 
            FROM 
                {config['EVENT_TABLE_NAME']}
            GROUP BY 1,2,3,4,5 
        """
        val = ()
    else:
        query = f"""
            SELECT
                a.eventID,
                a.eventName,
                a.eventDescription,
                a.eventDate,
                a.eventAddress,
                GROUP_CONCAT(a.WordIndex) as WordIndex 
            FROM 
                {config['EVENT_TABLE_NAME']} a
            INNER JOIN
                {config['EVENT_RECOMMENDATION_TABLE_NAME']} b
            ON
                a.eventID = b.eventID
            WHERE
                b.userID = ?
            GROUP BY 1,2,3,4,5 
        """
        val = (userID,)
    data=db.executeQuery(query, val = val)
    words = []
    event_name = []
    event_description = []
    event_date = []
    event_address = []
    event_id = []
    for row in data:
        event_id.append(row[0])
        event_name.append(row[1])
        words.append(row[5].split(','))
        event_description.append(row[2])
        event_date.append(row[3])
        event_address.append(row[4])
    db.destruct()
    return {
        "event_id" : event_id,
        "event_tags" : words,
        "event_name" : event_name,
        "event_description" : event_description,
        "event_date" : event_date,
        "event_address" : event_address
    }

def get_event_id(WordIndex):
    config = read_config()
    db=DBOps(config)
    query = f"""
    SELECT 
        eventID
    FROM
        {config['EVENT_TABLE_NAME']}
    WHERE
        WordIndex = ?
    GROUP BY 1
    """
    data = db.executeQuery(query, val = (WordIndex,))
    result = []
    for i in range(len(data)):
        result.append(data[i][0])
    return result

def save_recommendation(data, mode = "replace"):
    config = read_config()
    db=DBOps(config)
    data.drop_duplicates().to_sql(name = db.event_recommendation_table_name, con = db.con, if_exists = mode, index = False)