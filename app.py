from flask import Flask
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'CarClub'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            sql_insert_statement = "insert into carclub.user_information(user_name, user_username, user_password) values ( '{}', '{}', '{}');".format(_name, _email, _password)
            print(sql_insert_statement)
            cursor.execute(sql_insert_statement)
            conn.commit()
            cursor.close()
            # cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showAll', methods=['POST', 'GET'])
def showAll():
    conn = mysql.connect()
    cursor = conn.cursor()
    # _hashed_password = generate_password_hash(_password)
    sql_query_statement = "select * from carclub.user_information"
    print(sql_query_statement)
    cursor.execute(sql_query_statement)
    results = cursor.fetchall()
    show_html = ''
    for x in results:
        temp = "<p> Name: " + x[1] + "</br>Username: " + x[2] + "</p></br></br>"
        print(x)
        print()
        show_html += temp
    cursor.close()
    return show_html


# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    # This is the main function for the application.
    app.run()
