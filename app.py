from flask import redirect, url_for
from flask import Flask, Markup, render_template, request
from Services.RepaymentService import RepaymentService
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# create the forms
class LoginForm(FlaskForm):
    customerID = StringField('customerID', validators=[DataRequired()])
    submit = SubmitField('Fetch')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    result = []
    if request.method =='POST':

        cust_id = request.form['customerID']
        print(cust_id)
        repay = RepaymentService()
        customer_summ = repay.get_cust_summary(cust_id)
        # result.append(customer_summ[0])
        print(type(customer_summ))
        return redirect(url_for('home', customer_summ=customer_summ))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)