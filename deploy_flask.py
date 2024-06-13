from flask import Flask, render_template, request,session
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
import resolution
import Mobile_UI
import Contact_info
import LoadTime
import screenshot
import pickle
import psycopg2
from psycopg2 import OperationalError
import pdfkit
import send_email


# --------------------------- create Databased connection ---------------------------

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print("The error '{e}' occurred")
    return connection

# --------------------------- Execute Database queries ---------------------------

connection=create_connection("website_evaluator","postgres",None,"localhost",5432)
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# --------------------------- Decode prediction number to class name ---------------------------
def decode_pred(pred_cnn):
    if pred_cnn == 0:
        return 'Bad'
    elif pred_cnn == 1:
        return 'Excellent'
    elif pred_cnn == 2:
        return 'Good'
    elif pred_cnn == 3:
        return 'Very bad'
    else:
        return'Very good'
        
# --------------------------- Evaluation Processes ---------------------------
def evaluation(new_url):
    # Extract the features.
    load_time = LoadTime.loadTime(new_url)
    contact_info= Contact_info.contact(new_url)
    mobile= Mobile_UI.mobile(new_url)
    res= resolution.resolution(new_url)
    
    # Create array of features values
    arr = np.array([[load_time, mobile, res, contact_info]])
    # Predict website using SVM model
    pred_svm = svm_model.predict(arr)
    pred_svm = decode_pred(pred_svm)

    # Predict website using CNN model
    img_url = screenshot.capture(new_url) # take screenshot of website
    img=image.load_img(img_url,target_size=(224,224))
    x=image.img_to_array(img) # conver image to array
    x=x/255 # normalization
    x=np.expand_dims(x,axis=0)
    img_data=preprocess_input(x)
    pred_cnn = np.argmax(cnn_model.predict(img_data), axis=1) # prediction
    pred_cnn = decode_pred(pred_cnn)
    
    return pred_svm, pred_cnn, load_time, contact_info, mobile, res
    
# --------------------------- Recommendations ---------------------------
def recommendations(load_time, contact_info, mobile, res):
    if load_time<=12.216:
        load_timereco= 'Your website has an excellent load time between 0.8-12.'
    else:
        load_timereco= 'Your website load time is ', load_time ,'. It needs to be less than or equal to 12.216s.'

    if contact_info==1:
        contact_inforeco='Your website has a contact information'
    else:
        contact_inforeco='Your website has no contact information. You need to provide at least one contact information such as phone number and email.'

    if mobile==1:
        mobilereco='Your website is mobile-friendly.'
    else:
        mobilereco='Your website is not mobile-friendly.'

    if res==0:
        resreco='Your website image resolution is excellent'
    else:
        resreco='Your website image resolution score is low'
        
    return load_timereco, contact_inforeco, mobilereco, resreco

        
# Load SVM and CNN models
filename = 'SVM.sav'
cnn_model=load_model('facefeatures_new_model.h5')
svm_model = pickle.load(open(filename, 'rb'))
 
app = Flask(__name__, template_folder='template')
app.secret_key="hi"

@app.route('/')

# --------------------------- First page when run the app ---------------------------
def man():
    return render_template('login.html')

# --------------------------- Result page (without login) ---------------------------
@app.route('/Start', methods=['POST'])
def home():
    new_url = request.form['URL'] # take input from user
    # Get evaluation result from evaluation method
    pred_svm, pred_cnn, load_time, contact_info, mobile, res = evaluation(new_url)
    # Get recommendation for all feature from recommendations method
    load_timereco, contact_inforeco, mobilereco, resreco = recommendations(load_time, contact_info, mobile, res)

    return render_template('Resultout.html',data_cnn=pred_cnn,data_svm = pred_svm,reco1=load_timereco,reco2=contact_inforeco,reco3=resreco,reco4=mobilereco)

# --------------------------- Send result to email ---------------------------
@app.route('/pdf/<data_cnn>/<data_svm>/<reco1>/<reco2>/<reco3>/<reco4>', methods=['POST'])
def pdf(data_cnn, data_svm, reco1, reco2, reco3, reco4):
    rendered = render_template('ResultPDF.html', data_cnn=data_cnn,data_svm = data_svm, reco1 = reco1,reco2=reco2,reco3=reco3, reco4=reco4)
    rendered2 = render_template('Resultout.html', data_cnn=data_cnn,data_svm = data_svm, reco1 = reco1,reco2=reco2,reco3=reco3, reco4=reco4)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(rendered, 'EvaluationResult.pdf', configuration = config)
    u_email = request.form.get('email')
    send_email.send('EvaluationResult.pdf',u_email)
    return rendered2

# --------------------------- Send result to email ---------------------------
@app.route('/pdf2/<data_cnn>/<data_svm>/<reco1>/<reco2>/<reco3>/<reco4>', methods=['POST'])
def pdf2(data_cnn, data_svm, reco1, reco2, reco3, reco4):
    rendered = render_template('ResultPDF.html', data_cnn=data_cnn,data_svm = data_svm, reco1 = reco1,reco2=reco2,reco3=reco3, reco4=reco4)
    rendered2 = render_template('Result.html', data_cnn=data_cnn,data_svm = data_svm, reco1 = reco1,reco2=reco2,reco3=reco3, reco4=reco4)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(rendered, 'EvaluationResult.pdf', configuration = config)
    u_email = request.form.get('email')
    send_email.send('EvaluationResult.pdf',u_email)
    return rendered2


# --------------------------- Navigate to the customer HomePage---------------------------
@app.route('/Home1')
def dd():
    x=session["Email"]
    x = x.split("@")
    return render_template('HomePage.html', info=x[0])
   
# ---------------------------Navigate to the customer AboutusPage ---------------------------
@app.route('/About US')
def dd1():
    x=session["Email"]
    x = x.split("@")
    return render_template('AboutusPage.html',info=x[0])

# --------------------------- Show all the pre-evaluations websites of the customer ---------------------------
@app.route('/MyResult')
def dd2():
    x=session["Email"]
    x = x.split("@")
    id1=session["ID"]
    websites = "SELECT * FROM websites WHERE dev_id = '{}'".format(id1)
    Record= execute_read_query(connection, websites)
    my_list=[]
    for n in range(len(Record)):
        t,i,z,f,t,d,e,s,u=Record[n]
        my_list.append(i)
    return render_template('MyP.html',my_list=my_list)

# ---------------------------Logout from the system---------------------------
@app.route('/Log out')
def dd3():
    return render_template('login.html')

# ---------------------------Navigate to Sign-up page---------------------------

@app.route('/Sign up')
def dd4():
    return render_template('Signup1.html')
    
# --------------------------- Navigate to the user About us Page -------------------------

@app.route('/About US1')
def dd5():
    return render_template('AboutusPageout.html')

# ---------------------------SIGN UP---------------------------

@app.route('/from_login', methods=['POST','GET'])
def login():
    email=request.form['Email']
    password=request.form['password']
    select_users = "SELECT * FROM developer WHERE email = '{}' AND password = '{}'".format(email,password)
    Record= execute_read_query(connection, select_users)
    if len(Record)==1:
        devid,users,password=Record[0]
    else:
        return render_template('login.html',info='The Email or the Password is not correct')
    if users!=email:
        return render_template('login.html')
    else:
        session["Email"]=email
        session["ID"]=devid
        x = users.split("@")
        return render_template('HomePage.html',info=x[0])

# ---------------------------SIGN UP---------------------------

@app.route('/from_signup', methods=['POST','GET'])
def signup():
    email=request.form['Email']
    password=request.form['password']
    select_users = "SELECT * FROM developer WHERE email = '{}'".format(email)
    Record= execute_read_query(connection, select_users)
    if len(Record)==1:
        return render_template('Signup1.html',info='The Email is alredy exsist')
    else:
        users = [(email, password)]
        user_records = ", ".join(["%s"] * len(users))
        insert_query = (f"INSERT INTO developer (email, password) VALUES {user_records}")
        connection.rollback()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(insert_query, users)
        x = email.split("@")
        session["Email"]=email
        return render_template('HomePage.html',info=x[0])

# --------------------------- Result page (for login users) ---------------------------

@app.route('/homepage', methods=['POST'])
def interd():
    new_url = request.form['URL'] # take input from user
    # Get evaluation result from evaluation method
    pred_svm, pred_cnn, load_time, contact_info, mobile, res = evaluation(new_url)
    # Get recommendation for all feature from recommendations method
    load_timereco, contact_inforeco, mobilereco, resreco = recommendations(load_time, contact_info, mobile, res)

    x=session["Email"]
    x = x.split("@")
    select_users = "SELECT * FROM websites WHERE url = '{}'".format(new_url)
    Record= execute_read_query(connection, select_users)
    if len(Record)==1:
        return render_template('Result.html',info=x[0],data_cnn=pred_cnn,data_svm = pred_svm, reco1=load_timereco,reco2=contact_inforeco,reco3=resreco,reco4=mobilereco)
    else:
        users = [(new_url, load_timereco,contact_inforeco,resreco,mobilereco,pred_cnn,pred_svm,session["ID"])]
        user_records = ", ".join(["%s"] * len(users))
        insert_query = (f"INSERT INTO websites (url, web_recom1,web_recom2,web_recom3,web_recom4,cnn_grade,svm_grade,dev_id) VALUES {user_records}")
        connection.rollback()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(insert_query, users)
        return render_template('Result.html',info=x[0],data_cnn=pred_cnn,data_svm = pred_svm, reco1=load_timereco,reco2=contact_inforeco,reco3=resreco,reco4=mobilereco)

# ---------------------------GO to the result page from MY-Result---------------------------

@app.route('/Result', methods=['POST','GET'])
def Result():
    new_url = request.form.get('bton')
    id1=session["ID"]
    websites = "SELECT * FROM websites WHERE url = '{}' AND dev_id = '{}' ".format(new_url,id1)
    Record= execute_read_query(connection, websites)
    t,i,z,f,t,d,e,s,u=Record[0]
    x=session["Email"]
    x = x.split("@")
    return render_template('Result.html',info=x[0],data_cnn=e,data_svm = s, reco1=z,reco2=f,reco3=t,reco4=d)

# --------------------------- LOGIN USING RESULTT PAGE  ---------------------------

@app.route('/loginR/<data_cnn>/<data_svm>/<reco1>/<reco2>/<reco3>/<reco4>', methods=['POST'])
def loginR(data_cnn, data_svm, reco1, reco2, reco3, reco4):
    email=request.form['Email']
    password=request.form['password']
    select_users = "SELECT * FROM developer WHERE email = '{}' AND password = '{}'".format(email,password)
    Record= execute_read_query(connection, select_users)
    if len(Record)==1:
        devid,users,password=Record[0]
    else:
        return render_template('Resultout.html',info='The Email or the Password is not correct')
    if users!=email:
        return render_template('Resultout.html')
    else:
        session["Email"]=email
        session["ID"]=devid
        x = users.split("@")
        return render_template('Result.html',info=x[0],data_cnn = data_cnn, data_svm = data_svm, reco1=reco1, reco2=reco2, reco3=reco3, reco4=reco4)

# --------------------------- LOGIN USING ABOUT-US PAGE  ---------------------------

@app.route('/loginA', methods=['POST','GET'])
def loginA():
    email=request.form['Email']
    password=request.form['password']
    select_users = "SELECT * FROM developer WHERE email = '{}' AND password = '{}'".format(email,password)
    Record= execute_read_query(connection, select_users)
    if len(Record)==1:
        devid,users,password=Record[0]
    else:
        return render_template('AboutusPageout.html',info='The Email or the Password is not correct')
    if users!=email:
        return render_template('AboutusPageout.html')
    else:
        session["Email"]=email
        session["ID"]=devid
        x = users.split("@")
        return render_template('AboutusPage.html',info=x[0])


# --------------------------- Start the app---------------------------
if __name__ == "__main__":
    app.run(debug=True)
