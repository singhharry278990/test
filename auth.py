
"""
declaration of auth0 web-services.
"""
import json

import requests
import bcrypt
import pymysql

def db_connection():
    dbconnection = pymysql.connect(
        user='deepak',
        password='NewPass@123',
        host='iesl-dev-db-syd.cdiah0tmq8hx.ap-southeast-2.rds.amazonaws.com',
        port=3306,
        database='mandep_demo',
        cursorclass=pymysql.cursors.DictCursor)

    return dbconnection

auth_url = 'dummy-auth-dev.us.auth0.com'
clientId = '2iwDEP7LDfDHxGXG2bEKVKHe7u8aqBZ2'
clientSecret = 'DJDS4aAkLkORrCWtwkBU9g9FpXP1XwTnjezSAeuTwRHKI7Eh7ZQC-hrXF2q5w20P'
audience = 'https://dummy-auth-dev.us.auth0.com/api/v2/'
grant_type = 'client_credentials'
connection = 'dummy-dev'
single_page_client_Id = 'QjlMDil80AwDXSr5qhXkaCey6L9AWLoQ'

def encrypt_pass(body):
    password = body.get('password')
    byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte, salt)
    return hashed

def registration(body):
        db = db_connection()
        curr = db.cursor()
        status = False
        fullName = body.get('full_name')
        userEmail = body.get('user_name')
        password = body.get('password')
        """Create user account on auth0"""
        url = f"https://{auth_url}/dbconnections/signup"
        body = {
            "client_id": clientId,
            "connection": connection,
            "email": userEmail,
            "password": password,
            "name": fullName
        }
        response = requests.post(url, data=body)
        user = response.json()
        user_id = user.get('_id')
        if response.status_code == 200:
            context = {"create_user_account_response": str(response.text)}
            print(context)
        else:
            context = {"create_user_account_Error": str(response.text)}
            print(context)
        encrypt = encrypt_pass(body)
        pas = encrypt.decode('utf-8')
        # try:
        query = "INSERT INTO myfarm (full_name, user_name, password, user_id)" \
                f"VALUES ('{fullName}','{userEmail}', '{pas}', '{user_id}')"
        if curr.execute(query):
            db.commit()
            lastRowId = curr.lastrowid
            curr.execute("select * from myfarm")
            data = curr.fetchall()
            context = {'status': 200, 'message': data}
            print(context)
            # except pymysql.err.IntegrityError as e:
            #     context = {'status': 400, 'message': str(e)}
        # else:
        #     context = {'status': 405, 'message': 'Not inserted completed rows '}
        #     print(context)

registration({'full_name': 'harry', 'user_name': 'harry127@gmail.com', 'password': 'H1234567@' })