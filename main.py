from decimal import DivisionByZero
from flask import Flask, render_template, redirect, request, url_for
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hj3klh42kj3h4jk23h3jkhjh3jk242h4jk3h4jk34hrrbfbdbf'


currentNum = ''     # -- TODO need to find a way to eliminate the need for these variables
op = ''
num1 = ''
num2 = ''

@app.route('/', methods=['POST', 'GET'])
def home():
    global option
    bmiValue = ''
    totalMaterialCost = ''

    try:        # -- trys to find an option in args before defaulting to the first option 'graphic calculator'
        option = request.args['option']
    except:
        option = 'graphic-calc'

    if request.method == 'POST':
        if option == 'bmi-calc':    # -- Confirms the form being submitted is for the bmi-calculator
            feet = request.form.get('feet')
            inches = request.form.get('inches')
            pounds = request.form.get('pound')
            kilograms = (float(pounds) / 2.205)
            meters = ((float(feet) * 12) + float(inches)) / 39.37
            bmiValue = kilograms / math.pow(meters, 2)
            bmiValue = '{:.2f}'.format(bmiValue)
        if option == 'material-calc':
            material = request.form.get('material')
            cost = request.form.get('cost')
            totalMaterialCost = str(float(material) * float(cost))

            

    return render_template('index.html', currentNum = currentNum, option = option, bmiValue = bmiValue, totalMaterialCost = totalMaterialCost)

@app.route('/button-click/<string:numOp>/<string:choice>')      # -- Click options for Graphic calculator
def buttonClick(numOp, choice):
    global currentNum, num1, num2, op

    if choice == 'number':
        currentNum = f'{currentNum}{numOp}'
    elif choice == 'operator':
        num1 = float(currentNum)
        op = numOp
        currentNum = ''
    elif choice == 'equality':
        num2 = float(currentNum)

        if op == 'pow':
            try:
                currentNum = math.pow(num1, num2)
            except OverflowError:
                currentNum = 'Error: Out of Range'
        elif op == 'div':
            op = '/'
            try:
                currentNum = eval(f'{num1}{op}{num2}')
            except ZeroDivisionError:
                currentNum = 'ERROR:CANT DIVIDE BY 0'
        else:        
            currentNum = eval(f'{num1}{op}{num2}')
    elif choice == 'clear':
        currentNum = ''
    elif choice == 'negative':
        currentNum = f'-{currentNum}'
    elif choice == 'square-root':
        currentNum = math.sqrt(int(currentNum))
    elif choice == 'square':
        currentNum = float(currentNum) ** 2
        
    return redirect(url_for('home', currentNum = currentNum))


if __name__ == '__main__':
    app.run(debug=True)