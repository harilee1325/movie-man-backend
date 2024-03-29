from flask import Flask, request, jsonify,send_from_directory
import json as simplejson
import json
from pymongo import MongoClient
from bson.json_util import dumps
import random
import os


client = MongoClient('mongodb://Harilee:harilee1329@haridatabase-shard-00-00-egsq3.mongodb.net:27017,haridatabase-shard-00-01-egsq3.mongodb.net:27017,haridatabase-shard-00-02-egsq3.mongodb.net:27017/test?ssl=true&replicaSet=hariDatabase-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.db


app = Flask(__name__)

@app.route("/")
def hello():
   # db.user_profile_movie_man.remove()
    return "Welcome to Movie Man!"



@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


                               

@app.route("/login/<string:username>/<string:password>", methods=['GET'])
def login_method(username,password):

    try:
        # logging in an already registered user
        count = 0

        login_obj = db.user_profile_movie_man.find_one({'username':username,'password':password})
        
        if login_obj == None:
            return dumps({'success': 'no', 'msg': 'invalid credentials', 'result':None})
        else:
            output = {'username': login_obj['username'], 'mail':login_obj['email']
                    , 'user_id': login_obj['user_id'], 'password': login_obj['password']}
            return dumps({'success':'yes','msg':'successfuly logged in','result': output})

        # for record in login_obj:
        #     if record['username'] == username:
        #         if record['password'] == password:
        #             count = 1
                   
        #             return dumps({'success':'yes','msg':'successfuly logged in','result': output})
        #             break
        #         else:
        #             continue
        #     else:
        #         continue
        # if count == 0:
        #     return dumps({'success': 'no', 'msg': 'invalid credentials', 'result':None})

    except Exception as e:
        return dumps({'error' : str(e)})


#route to create user
@app.route("/sign-up", methods = ['POST'])
def create_user():
    try:
        # accepts data in the body of the method
        user_name = request.form['username']
        user_email = request.form['email']
        password = request.form['password']

        count = db.user_profile_movie_man.count()
        print (count)
        if count > 0 :
            # checking if the user is already registered
            validate_obj = db.user_profile_movie_man.find()
            for record in validate_obj :
                if record['username'] == user_name:
                    return dumps({'success':'no', 'msg':'username already exist','result':None})
                    break
                elif record['email'] == user_email:
                    return dumps({'success':'no', 'msg':'email is already in use', 'result':None})
                    break
                else:
                    continue


            if user_name and user_email and password:

                    user_id = get_random_default()
                    count = db.user_profile_movie_man.count()
                    i = 0
                    check_id_obj = db.user_profile_movie_man.find()
                    while(1):
                        for record in check_id_obj:
                            i=i+1
                            if record['user_id'] == user_id:
                                i=i-1
                                user_id = get_random_default()
                                break
                        if (i == count):
                            break
                        else :
                            continue
                            
                    status = db.user_profile_movie_man.insert({
                        "user_id" : user_id+user_name,
                        "username" : user_name,
                        "email" : user_email,
                        "password" : password
                    })
            data = db.user_profile_movie_man.find_one({'_id': status})

            output = {'username': data['username'], 'mail':data['email']
            , 'user_id': data['user_id'], 'password': data['password']}

            return dumps({'success':'yes','msg':'New user successfuly added','result' : output})
        else :
            # adding the first user to the database
            if user_name and user_email and password:
                status = db.user_profile_movie_man.insert({
                        "user_id" : get_random_default()+user_name,
                        "username" : user_name,
                        "email" : user_email,
                        "password" : password
                    })
                    
            data = db.user_profile_movie_man.find_one({'_id': status})

            output = {'username': data['username'], 'mail':data['email']
            , 'user_id': data['user_id'], 'password': data['password']}

            return dumps({'success':'yes','msg':'New user successfuly added','result' : output})

    except Exception as e:
        return dumps({'error' : str(e)})


@app.route('/forgot-password/<string:user_email>', methods=['GET'])
def forgot_password_method(user_email):
    try:
        # checking if the email id exits or not
        data = db.user_profile_movie_man.find_one({'email':user_email})
        
        #if data is none then there is no data
        if data == None:
            return dumps ({'success': 'no','msg':'Mail id not found' })
        else :
            return dumps ({'success': 'yes','msg':'Mail is found' ,'result':data})

    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/forgot-change-password', methods=['POST'])
def change_password_forgot():
    try:

        user_email = request.form['email']
        password = request.form['new_password']
        db.user_profile_movie_man.update_one(
                {"email":user_email},
                {"$set":{'password':password}}
        )
        return dumps ({'success': 'yes','msg':'New password has been set'})

    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/get-userdata/<string:username>', methods=['GET'])
def get_user_data(username):
    try :
        user_data_obj = db.user_profile_movie_man.find_one({'username':username})
        if user_data_obj == None :
            return dumps ({'success':'no', 'msg':'No such user found',})
        else:
            output = {'username': user_data_obj['username'], 'mail':user_data_obj['email']
            , 'user_id': user_data_obj['user_id'], 'password': user_data_obj['password']}

            return dumps({'success':'yes','msg':'user found','result' : output})
    except Exception as e:
        return dumps({'error' : str(e)})






def get_random_default():
    
    return str(random.randint(10000,99999))
if __name__ == '__main__':
    app.run()