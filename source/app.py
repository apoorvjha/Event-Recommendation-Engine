from flask import Flask, request
from embedding_model import *
from utility import *
from vector_database_builder import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username',None)
        session.pop('email',None)
        session.pop('profilePic',None)
        session.pop('type',None)
        session.pop('userId',None)        
        flash("Successfully logged out!",'alert alert-success')        
    return redirect(url_for('index'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/loginBack',methods=['POST'])
def login_back():
    if request.method=='POST':
        userId=request.form['userId']
        password=request.form['password']
        status,res,msg,category=Auth.checkCredentials(userId,password)
        flash(msg,category)
        if status==True:
            session['username']=res[0][0]
            session['email']=res[0][1]
            session['profilePic']=res[0][2]
            session['type']=res[0][3]
            session['userId']=res[0][4]
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        flash("Unsupported method of request! Please use POST instead.",'alert alert-danger')
        return redirect(url_for('index'))
@app.route('/registerBack',methods=['POST'])
def registerBack():
    if request.method=='POST':
        userId=request.form['userId']
        password=request.form['password']
        email=request.form['email']
        profilePic=request.files['profilePic']
        fileName=userId + secure_filename(profilePic.filename)
        profilePic.save('../data/static/PROFILE_PIC/'+fileName)
        profilePath='../data/static/PROFILE_PIC/'+fileName
        status=Auth.register(userId,password,email,profilePath)
        if status==True:
            # as we advance, incorporate functionality of OTP verification as well.
            flash("You are successfully registered!.",'alert alert-success') 
            return redirect(url_for('index'))
        else:
            flash("User with provided data already exists! ",'alert alert-danger')
            return redirect(url_for('register'))
    else:
        flash("Unsupported method of registration! Please use the registration tab instead.",'alert alert-danger')
        return redirect(url_for("HomePage"))
@app.route('/users')
def getUsers():
    if session['type']=='admin':
        response={"users" : []}
        users=Auth.getUsers()
        for i in users:
            response["users"].append({"userID" : i[0],"profilePic" : i[1], "username" : i[2], "email" : i[3],"isActive" : i[4]})
        return response
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}

@app.route('/activate/<id>')
def activate(id):
    if session['type']=='admin':
        Auth.activate(id)
        #flash("User activated successfully!","alert alert-success")
        return {"status" : 200}
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}

@app.route('/deactivate/<id>')
def deactivate(id):
    if session['type']=='admin':
        Auth.deactivate(id)
        #flash("User deactivated successfully!","alert alert-success")
        return {"status" : 200}
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}
@app.route('/settings')
def settings():
    return render_template('settings.html')
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/changeCredentials',methods=['POST'])
def changeCredentials():
    if session['userId']:
        if request.method=='POST':
            mode=request.form['mode']
            value=request.form["value"]
            if mode==0:
                Auth.changeUserName(session['userId'],value)
            elif mode==1:
                Auth.changePassword(session['userId'],value)
            else:
                Auth.changeEmail(session['userId'],value)
            return {"status" : 200}
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}

@app.route('/changeProfilePicture',methods=['POST'])
def changeProfPic():
    if session['userId']:
        if request.method=='POST':
            # change profile pic.
            profilePic=request.files['profpic']	
            fileName=session['profilePic']
            profilePic.save(fileName)
            flash("Profile pic changed successfully!","alert alert-success")
            return redirect(url_for('index'))
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}


@app.route("/api/v1/set_context_phrases", methods = ["POST"])
def set_context_phrases():
    if request.method == 'POST':
        context_words = request.get_json()["context_phrases"]
        try:
            config = read_config()
            vector_database = VectorDatabase(config["VECTOR_DB"], config["VECTOR_STORE_TABLE_NAME"])
            embedding_matrix = get_embedding(config, context_words)
            vector_database.insert(
                context_words,
                embedding_matrix.cpu().numpy().tolist()
            )
            vector_database.save_vector_db()
            vector_database.destruct()
            return f"Context words has been inserted successfully into vector DB!", 200
        except Exception as e:
            return f"Failed to set context words into vector DB due to {e}", 400
    else:
        return f"HTTP method {request.method} not allowed!", 404

@app.route("/api/v1/get_k_closest_phrases", methods = ["POST"])
def get_k_closest_phrases():
    if request.method == 'POST':
        query_words = request.get_json()["query_phrases"]
        try:
            config = read_config()
            vector_database = VectorDatabase(config["VECTOR_DB"], config["VECTOR_STORE_TABLE_NAME"])
            search_word_embedding = get_embedding(config, query_words)
            k = config["TOP_K"]
            response = {}
            for i in range(len(query_words)):
                matching_words = vector_database.search(search_word_embedding.cpu().numpy().tolist()[i], k = k)
                response[query_words[i]] = matching_words['Value'].tolist()
            vector_database.destruct()
            return json.dumps(response), 200
        except Exception as e:
            print(e)
            return f"Failed to set context words into vector DB due to {e}", 400
    else:
        return f"HTTP method {request.method} not allowed!", 404 


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        port = 8080,
        debug = True
    )