import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


app = Flask(__name__) #Initialize the flask App
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

fraud = pickle.load(open('fraud.pkl','rb'))

# In-memory user store for demonstration (replace with DB in production)
users = {}

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		if username in users:
			flash('Username already exists!')
			return render_template('signup.html')
		users[username] = {'email': email, 'password': password}
		flash('Account created! Please log in.')
		return redirect('/login')
	return render_template('signup.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
	if request.method == 'POST':
		email = request.form['email']
		# In a real app, send reset link to email
		flash('If this email exists, a reset link has been sent.')
		return redirect('/login')
	return render_template('reset_password.html')
@app.route('/')

@app.route('/first')
def first():
	return render_template('first.html')



#@app.route('/future')
#def future():
#	return render_template('future.html')    

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['uname']
		password = request.form['pwd']
		if username in users and users[username]['password'] == password:
			flash('Login successful!')
			return redirect('/upload')
		elif username == 'admin' and password == 'admin':
			flash('Admin login successful!')
			return redirect('/upload')
		else:
			flash('Invalid Credentials!')
			return render_template('login.html')
	return render_template('login.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')  
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	


#@app.route('/home')
#def home():
 #   return render_template('home.html')

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    return render_template('prediction.html')


#@app.route('/upload')
#def upload_file():
#   return render_template('BatchPredict.html')



@app.route('/predict',methods=['POST'])
def predict():
	int_feature = [x for x in request.form.values()]
	 
	final_features = [np.array(int_feature)]
	 
	result=fraud.predict(final_features)
	if result == 1:
			result = "Transaction Fraudulent"
	else:
		result = 'Benign'
	
	return render_template('prediction.html', prediction_text= result)
    
@app.route('/performance')
def performance():
	return render_template('performance.html')
    
@app.route('/chart')
def chart():
	return render_template('chart.html')   
    
    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
