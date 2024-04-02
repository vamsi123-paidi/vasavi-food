from flask import Flask, render_template, request,jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import stripe
import sqlite3
stripe.api_key = "sk_test_51O9e3JSFzk0D6VrYz2cSozO1Jfmq79bEhR8REPUGD28vbfg0HfnJ4krNnPyNYij2RVXc2gCKShWRbuv8a4bgs6z6004iVVF4T4"  # Test mode
app = Flask(__name__, static_url_path='/static')
app.secret_key = '7388bb75420f83b9b0f0a8b5377dc9cb'

def insert_user_data(data):
    
        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }

            connection = mysql.connector.connect(**db_config)

            cursor = connection.cursor()

            insert_query = "INSERT INTO users (full_name, phone, email, password, college_id, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, data)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True

        except mysql.connector.Error as e:
            print("Error:", e)
            return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        college_id = request.form['college_id']
        gender = request.form['gender']
        
        hashed_password = generate_password_hash(password)
        
        data = (full_name, phone, email, hashed_password, college_id, gender)
        
        if insert_user_data(data):
            return "User data inserted successfully."
        else:
            return "Failed to insert user data."

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            select_query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            
            if result:
                hashed_password = result[0]
                if check_password_hash(hashed_password, password):
                    session['email'] = email
                    cursor.close()
                    connection.close()
                    return redirect(url_for('dashboard'))
                else:
                    cursor.close()
                    connection.close()
                    return "Invalid credentials"
            else:
                cursor.close()
                connection.close()
                return "User not found"
        
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return "Database error"

    return render_template('index.html')



@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']

        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_data:
                full_name, phone, college_id, gender = user_data
                return render_template('dashboard.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
            else:
                return "User data not found."

        except mysql.connector.Error as e:
            print("Error:", e)
            return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'email' in session:
        if request.method == 'POST':
            full_name = request.form['full_name']
            phone = request.form['phone']
            college_id = request.form['college_id']
            email = session['email']

            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                update_query = "UPDATE users SET full_name = %s, phone = %s, college_id = %s WHERE email = %s"
                cursor.execute(update_query, (full_name, phone, college_id, email))
                connection.commit()

                cursor.close()
                connection.close()

                return redirect(url_for('dashboard'))

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to update user data."

        else:
            email = session['email']
            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
                cursor.execute(select_query, (email,))
                user_data = cursor.fetchone()

                cursor.close()
                connection.close()

                if user_data:
                    full_name, phone, college_id, gender = user_data
                    return render_template('edit_profile.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
                else:
                    return "User data not found."

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
   
    session.clear()
    return redirect(url_for('index')) 

@app.route('/property_list2')
def property_list2():
    return render_template('property_list2.html')

@app.route('/property_list1')
def property_list1():
    return render_template('property_list1.html')

@app.route('/property_list3')
def property_list3():
    return render_template('property_list3.html')

@app.route('/property_list4')
def property_list4():
    return render_template('property_list4.html')

@app.route('/property_list5')
def property_list5():
    return render_template('property_list5.html')

@app.route('/index_after_login')
def index_after_login():
    return render_template('index_after_login.html')

@app.route('/property_list1_after_login')
def property_list1_after_login():
    return render_template('property_list1_after_login.html')


@app.route('/property_list2_after_login')
def property_list2_after_login():
    return render_template('property_list2_after_login.html')

@app.route('/property_list3_after_login')
def property_list3_after_login():
    return render_template('property_list3_after_login.html')

@app.route('/property_list4_after_login')
def property_list4_after_login():
    return render_template('property_list4_after_login.html')

@app.route('/property_list5_after_login')
def property_list5_after_login():
    return render_template('property_list5_after_login.html')


@app.route('/juice1')
def juice1():
    return render_template('juice1.html')

@app.route('/juice2')
def juice2():
    return render_template('juice2.html')

@app.route('/juice3')
def juice3():
    return render_template('juice3.html')

@app.route('/juice4')
def juice4():
    return render_template('juice4.html')

@app.route('/juice5')
def juice5():
    return render_template('juice5.html')

@app.route('/juice6')
def juice6():
    return render_template('juice6.html')

@app.route('/juice7')
def juice7():
    return render_template('juice7.html')

@app.route('/juice8')
def juice8():
    return render_template('juice8.html')

@app.route('/juice9')
def juice9():
    return render_template('juice9.html')

@app.route('/juice10')
def juice10():
    return render_template('juice10.html')

@app.route('/juice11')
def juice11():
    return render_template('juice11.html')

@app.route('/juice12')
def juice12():
    return render_template('juice12.html')

@app.route('/juice13')
def juice13():
    return render_template('juice13.html')

@app.route('/juice14')
def juice14():
    return render_template('juice14.html')

@app.route('/juice15')
def juice15():
    return render_template('juice15.html')

@app.route('/juice16')
def juice16():
    return render_template('juice16.html')

@app.route('/juice17')
def juice17():
    return render_template('juice17.html')

@app.route('/juice18')
def juice18():
    return render_template('juice18.html')

@app.route('/juice19')
def juice19():
    return render_template('juice19.html')

@app.route('/juice20')
def juice20():
    return render_template('juice20.html')

@app.route('/property_detail')
def property_detail():
    return render_template('property_detail.html')

@app.route('/property_details1')
def property_details1():
    return render_template('property_details1.html')

@app.route('/property_details2')
def property_details2():
    return render_template('property_details2.html')

@app.route('/property_details3')
def property_details3():
    return render_template('property_details3.html')

@app.route('/property_details4')
def property_details4():
    return render_template('property_details4.html')

@app.route('/property_details5')
def property_details5():
    return render_template('property_details5.html')

@app.route('/property_details16')
def property_details6():
    return render_template('property_details6.html')

@app.route('/property_details7')
def property_details7():
    return render_template('property_details7.html')

@app.route('/property_details8')
def property_details8():
    return render_template('property_details8.html')

@app.route('/property_details9')
def property_details9():
    return render_template('property_details9.html')

@app.route('/property_details10')
def property_details10():
    return render_template('property_details10.html')

@app.route('/property_details11')
def property_details11():
    return render_template('property_details11.html')

@app.route('/property_details12')
def property_details12():
    return render_template('property_details12.html')

@app.route('/property_details13')
def property_details13():
    return render_template('property_details13.html')

@app.route('/property_details14')
def property_details14():
    return render_template('property_details14.html')

@app.route('/property_details15')
def property_details15():
    return render_template('property_details15.html')

@app.route('/property_details16')
def property_details16():
    return render_template('property_details16.html')

@app.route('/property_details17')
def property_details17():
    return render_template('property_details17.html')

@app.route('/property_details18')
def property_details18():
    return render_template('property_details18.html')

@app.route('/property_details19')
def property_details19():
    return render_template('property_details19.html')

@app.route('/property_details20')
def property_details20():
    return render_template('property_details20.html')

@app.route('/property_details21')
def property_details21():
    return render_template('property_details21.html')

@app.route('/property_details22')
def property_details22():
    return render_template('property_details22.html')

@app.route('/property_details23')
def property_details23():
    return render_template('property_details23.html')

@app.route('/property_details24')
def property_details24():
    return render_template('property_details24.html')

@app.route('/property_details25')
def property_details25():
    return render_template('property_details25.html')

@app.route('/property_details26')
def property_details26():
    return render_template('property_details26.html')

@app.route('/property_details27')
def property_details27():
    return render_template('property_details27.html')


@app.route('/s1')
def s1():
    return render_template('s1.html')
@app.route('/s2')
def s2():
    return render_template('s2.html')
@app.route('/s3')
def s3():
    return render_template('s3.html')
@app.route('/s4')
def s4():
    return render_template('s4.html')
@app.route('/s5')
def s5():
    return render_template('s5.html')
@app.route('/s6')
def s6():
    return render_template('s6.html')
@app.route('/s7')
def s7():
    return render_template('s7.html')
@app.route('/s8')
def s8():
    return render_template('s8.html')
@app.route('/s9')
def s9():
    return render_template('s9.html')
@app.route('/s10')
def s10():
    return render_template('s10.html')
@app.route('/s11')
def s11():
    return render_template('s11.html')
@app.route('/s12')
def s12():
    return render_template('s12.html')
@app.route('/s13')
def s13():
    return render_template('s13.html')
@app.route('/s14')
def s14():
    return render_template('s14.html')
@app.route('/s15')
def s15():
    return render_template('s15.html')
@app.route('/s16')
def s16():
    return render_template('s16.html')
@app.route('/s17')
def s17():
    return render_template('s17.html')
@app.route('/s18')
def s18():
    return render_template('s18.html')
@app.route('/s19')
def s19():
    return render_template('s19.html')
@app.route('/s20')
def s20():
    return render_template('s20.html')
@app.route('/s21')
def s21():
    return render_template('s21.html')
@app.route('/s22')
def s22():
    return render_template('s22.html')
@app.route('/s23')
def s23():
    return render_template('s23.html')


@app.route('/t1')
def t1():
    return render_template('t1.html')
@app.route('/t2')
def t2():
    return render_template('t2.html')
@app.route('/t3')
def t3():
    return render_template('t3.html')
@app.route('/t4')
def t4():
    return render_template('t4.html')
@app.route('/t5')
def t5():
    return render_template('t5.html')
@app.route('/t6')
def t6():
    return render_template('t6.html')
@app.route('/t7')
def t7():
    return render_template('t7.html')
@app.route('/t8')
def t8():
    return render_template('t8.html')
@app.route('/t9')
def t9():
    return render_template('t9.html')
@app.route('/t10')
def t10():
    return render_template('t10.html')
@app.route('/t11')
def t11():
    return render_template('t11.html')
@app.route('/t12')
def t12():
    return render_template('t12.html')
@app.route('/t13')
def t13():
    return render_template('t13.html')
@app.route('/t14')
def t14():
    return render_template('t14.html')

@app.route('/tiffin1')
def tiffin1():
    return render_template('tiffin1.html')

@app.route('/tiffin2')
def tiffin2():
    return render_template('tiffin2.html')

@app.route('/tiffin3')
def tiffin3():
    return render_template('tiffin3.html')

@app.route('/tiffin4')
def tiffin4():
    return render_template('tiffin4.html')

@app.route('/tiffin5')
def tiffin5():
    return render_template('tiffin5.html')

@app.route('/tiffin6')
def tiffin6():
    return render_template('tiffin6.html')

@app.route('/tiffin7')
def tiffin7():
    return render_template('tiffin7.html')

@app.route('/tiffin8')
def tiffin8():
    return render_template('tiffin8.html')

@app.route('/tiffin9')
def tiffin9():
    return render_template('tiffin9.html')

@app.route('/tiffin10')
def tiffin10():
    return render_template('tiffin10.html')

@app.route('/tiffin11')
def tiffin11():
    return render_template('tiffin11.html')

@app.route('/tiffin12')
def tiffin12():
    return render_template('tiffin12.html')

@app.route('/tiffin13')
def tiffin13():
    return render_template('tiffin13.html')

@app.route('/tiffin14')
def tiffin14():
    return render_template('tiffin14.html')

@app.route('/tiffin15')
def tiffin15():
    return render_template('tiffin15.html')

@app.route('/tiffin17')
def tiffin17():
    return render_template('tiffin17.html')

@app.route('/tiffin18')
def tiffin18():
    return render_template('tiffin18.html')

@app.route('/tiffin19')
def tiffin19():
    return render_template('tiffin19.html')

@app.route('/tiffin20')
def tiffin20():
    return render_template('tiffin20.html')

@app.route('/tiffin21')
def tiffin21():
    return render_template('tiffin21.html')

@app.route('/tiffin22')
def tiffin22():
    return render_template('tiffin22.html')

@app.route('/tiffin23')
def tiffin23():
    return render_template('tiffin23.html')

@app.route('/tiffin24')
def tiffin24():
    return render_template('tiffin24.html')

@app.route('/tiffin25')
def tiffin25():
    return render_template('tiffin25.html')

@app.route('/tiffin26')
def tiffin26():
    return render_template('tiffin26.html')

@app.route('/tiffin27')
def tiffin27():
    return render_template('tiffin27.html')
    
@app.route('/tiffin28')
def tiffin28():
    return render_template('tiffin28.html')
    
@app.route('/tiffin29')
def tiffin29():
    return render_template('tiffin29.html')
@app.route('/tiffin30')
def tiffin30():
    return render_template('tiffin30.html')
@app.route('/tiffinnine')
def tiffinnine():
    return render_template('tiffinnine.html')










# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'canteen'  # Replace with your MySQL database name
}

@app.route('/create-rating', methods=['POST'])
def create_rating():
    try:
        email = request.json['email']  # Assuming the email is sent in the JSON request body
        rating_item = "Coconut"  # Hardcoding the rating item for this example
        rating_value = request.json['rating_value']  # Assuming the rating_value is sent in the JSON request body

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve the user ID based on the email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()

        if user_id is None:
            return jsonify({"error": "User not found"}), 404

        # Check if the rating item exists; if not, create it
        cursor.execute("SELECT id FROM ratings WHERE rating_item = %s", (rating_item,))
        rating_id = cursor.fetchone()

        if rating_id is None:
            cursor.execute("INSERT INTO ratings (rating_item) VALUES (%s)", (rating_item,))
            conn.commit()
            rating_id = cursor.lastrowid

        # Check if the user has already rated this item
        cursor.execute("SELECT id FROM user_ratings WHERE user_id = %s AND rating_id = %s", (user_id[0], rating_id))
        existing_rating = cursor.fetchone()

        if existing_rating is None:
            # Insert the rating into the 'user_ratings' table
            insert_query = "INSERT INTO user_ratings (user_id, rating_id, rating_value) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_id[0], rating_id, rating_value))
        else:
            return jsonify({"error": "Rating already given and cannot be changed"}), 400

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Rating created successfully"})

    except mysql.connector.Error as db_error:
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/like', methods=['POST'])
def like_property():
    try:
        email = request.json['email']  # Assuming the email is sent in the JSON request body

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve the user ID based on the email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()

        if user_id is None:
            return jsonify({"error": "User not found"}), 404

        # Implement your logic to handle liking the Coconut property here
        # You can update a 'likes' field in your properties table or create a new 'likes' table

        # Commit the transaction and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Property liked successfully"})

    except mysql.connector.Error as db_error:
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/order', methods=['GET', 'POST'])
def order():
    # Handle order submission logic here, such as processing the order form data
    # For now, we'll simply render an order submission template
    return render_template('order.html')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # Get the payment method ID from the request
        payment_method = request.json['payment_method']

        # Create a PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            payment_method=payment_method,
            amount=1000,  # the amount in cents
            currency='usd',
            confirmation_method='manual',
            confirm=True,
        )

        # Send the client secret to the frontend
        return jsonify({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 50

if __name__ == '__main__':
    app.run(debug=True)



