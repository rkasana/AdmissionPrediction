from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__) # initialize a flask app

@app.route('/',methods=['GET']) # route to display the home page
@cross_origin()
def homePage():
    return render_template('index.html')


@app.route('/predict',methods=['POST','GET']) # route to show the prediction
@cross_origin()
def index():
    if request.method=='POST':
        try:
            # read the inputs given by the user
            gre_score = float(request.form.get('gre_score'))
            toefl_score = float(request.form.get('toefl_score'))
            university_rating=float(request.form.get('university_rating'))
            sop = float(request.form.get('sop'))
            lor = float(request.form.get('lor'))
            cgpa = float(request.form.get('cgpa'))
            is_research = request.form.get('research')
            if is_research == 'yes':
                research = 1
            else:
                research = 0
            filename='finalized_model.pickle'
            loaded_model = pickle.load(open(filename,'rb')) # loading the machine learning model
            # prediction using the loaded model file
            prediction = loaded_model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            print("prediction is", prediction)
            # Showing the prediction results in a UI
            return render_template('results.html', prediction=round(100*prediction[0]))
        except Exception as e:
            print('The exception message is:',e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__=="__main__":
    # app.run(host='127.0.0.1',port=8001,debug=True)
    app.run(debug=True)
