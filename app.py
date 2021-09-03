from flask import Flask, render_template, request, jsonify
import pickle
import logging
#import numpy as np
#import sklearn
app = Flask(__name__)
#logging.basicConfig(filename="log\\log_files\\test.log", format='%(asctime)s %(message)s')
#logger=logging.getLogger()
#logger.setLevel(logging.DEBUG)
try:
    #model=bz2.BZ2File('bz2_test.pbz2','rb')
    #model=pickle.load(data)
    model = pickle.load(open('final_model.pkl', 'rb'))
    state = pickle.load(open('state.pkl','rb'))
    category_name = pickle.load(open('category_name.pkl','rb'))
    c_city = pickle.load(open('customer_city.pkl','rb'))
    s_city = pickle.load(open('seller_city.pkl','rb'))
    standard_scaler = pickle.load(open('standard_scaler.pkl','rb'))
except Exception as e:
    print(e)
    #logger.info("Can't Load the pickle files")
@app.route('/',methods=['GET'])
def Home():
    """
        :Desc: This is the home api
        :return: index.html Template
    """
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    """
            :Desc: This is the predict api
            :return: If request method is Post returns output prediction by
             rendering result.html otherwise it Render index.html Template
    """
    try:
        if request.method == 'POST':
            #logger.info('Requested method : POST')
            order_status = request.form['order_status']
            if (order_status == 'approved'):
                order_status = 0
            elif (order_status == 'canceled'):
                order_status = 1
            elif (order_status == 'delivered'):
                order_status = 2
            elif (order_status == 'invoiced'):
                order_status = 3
            elif (order_status == 'processing'):
                order_status = 4
            else:
                order_status = 5
           

            payment_sequential = int(request.form['payment_sequential'])
            payment_type = request.form['payment_type']
            if (payment_type == 'boleto'):
                payment_type = 0
            elif (payment_type == 'credit_card'):
                payment_type = 1
            elif (payment_type == 'debit_card'):
                payment_type = 2
            else:
                payment_type = 3
            payment_installments = int(request.form['payment_installments'])
            payment_value = float(request.form['payment_value'])
            customer_city = request.form['customer_city']
            customer_city = c_city.transform([customer_city])[0]
            customer_state = request.form['customer_state']
            customer_state = state.transform([customer_state])[0]
            price = float(request.form['Price'])
            freight_value = float(request.form['freight_value'])
            product_category_name = request.form['product_category_name']
            product_category_name = category_name.transform([product_category_name])[0]
            product_photos_qty = int(request.form['product_photos_qty'])
            seller_city = request.form['seller_city']
            seller_city = s_city.transform([seller_city])[0]
            seller_state = request.form['seller_state']
            seller_state = state.transform([seller_state])[0]
            days_taken_to_deliver = int(request.form['days_taken_to_deliver'])



            scaled=standard_scaler.transform([[order_status, payment_sequential,
       payment_type, payment_installments, payment_value,
       customer_city, customer_state, price, freight_value,
       product_category_name, product_photos_qty, 
       seller_city, seller_state, days_taken_to_deliver]])

            prediction=model.predict(scaled)[0]
            #logger.log('Prediction Done')
            if prediction==1:
                return render_template('result.html',prediction_text="Customer is Not Satisfied")
            elif prediction==3:
                return render_template('result.html',prediction_text="Customer is Satisfied partially")
            else:
                return render_template('result.html', prediction_text="Customer is Satisfied")

        else:
            #logger.info('Requested method : NOT POST')
            return render_template('index.html')
    except Exception as e:
        #logger.info('Data Transformation failed')
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)