[Introduction]
The repository contains [WIP] end-2-end code for the event recommendation engine. 

- Pretrained BERT model is used to create embeddings for context words which are essentially word tags for events. 
- The query word which is expression of interest is also passed through the model to compute the embedding. 
- Top <K> context words are fetched using cosine similarity metric and events having these words as tags are recommended.


TODO:
    1. Modify the vector DB to be persistent. -> Done
    2. Create following backend APIs: -> In Progress
        a. Auth Token issue / check -> Done
        b. User Signup -> Done
        c. Event Induction -> Done
        d. Event Invitation -> TBU
        e. Event Aceeptance -> TBU
        f. Event Deletion -> TBU
        g. Event Recommendation -> TBU
        h. Password Change -> Done
        i. Logout -> Done
        j. Add Interest -> Done
        k. Delete Interest -> Done
        l. View Interest -> Done
        m. Change Profile Pic -> Done
        n. Change Password -> Done
    3. Create the frontend screens -> In-Progress


PS C:\Users\dell\Desktop\temp\Event_Recommendation_Engine> python -m pip install -r requirements.txt  # Install the dependencies.

========================================================================================================================

PS C:\Users\dell\Desktop\temp\Event_Recommendation_Engine> cd data   # This folder contains the db files.
PS C:\Users\dell\Desktop\temp\Event_Recommendation_Engine\data> python # Shell for python terminal
Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3 # Library for connecting to DB
>>> con = sqlite3.connect("auth_db.db") # Create the connector to DB
>>> cursor = con.cursor() # Cursor to the DB object
>>> cursor.execute("SELECT * FROM CREDENTIALS") # Method to execute SQL query on the DB table.
<sqlite3.Cursor object at 0x00000237C9F68A40>
>>> cursor.fetchall()  # Method to fetch the results of SQL query executed.
[('admin01', 'admin01@123', 'admin', './static/PROFILE_PIC/admin01download.jpg', 'admin01@aieventmanager.com', 1, 1), ('user01', 'user01@123', 'user', './static/PROFILE_PIC/user01download.jpg', 'user01@aieventmanager.in', 2, 1), ('user02', 'user02@123', 'user', './static/PROFILE_PIC/user02download.jpg', 'user02@aieventmanager.in', 3, 0)]
>>> cursor.execute("UPDATE CREDENTIALS SET isActive = 1 WHERE username = 'user02'")  # Changing the active status of the user where username is user02
<sqlite3.Cursor object at 0x00000237C9F68A40>
>>> con.commit() # Permanently save the changes into the DB table.
>>> cursor.execute("SELECT * FROM CREDENTIALS")
<sqlite3.Cursor object at 0x00000237C9F68A40>
>>> cursor.fetchall()
[('admin01', 'admin01@123', 'admin', './static/PROFILE_PIC/admin01download.jpg', 'admin01@aieventmanager.com', 1, 1), ('user01', 'user01@123', 'user', './static/PROFILE_PIC/user01download.jpg', 'user01@aieventmanager.in', 2, 1), ('user02', 'user02@123', 'user', './static/PROFILE_PIC/user02download.jpg', 'user02@aieventmanager.in', 3, 1)]
>>> cursor.execute("UPDATE CREDENTIALS SET type = 'admin' WHERE username = 'user02'")
<sqlite3.Cursor object at 0x00000237C9F68A40>
>>> con.commit()

========================================================================================

# Following command to run the app

PS C:\Users\dell\Desktop\temp\Event_Recommendation_Engine> cd .\source\
PS C:\Users\dell\Desktop\temp\Event_Recommendation_Engine\source> python .\app.py

=======================================================================================


1. Image in the Events. -> Done
2. Delete from the view All Events (For Admin). -> Done
3. Add the recommendations for newly inducted users. -> Done
4. User's list of all the event subsribers. -> Done

=======================================================================================