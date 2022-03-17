from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hj3klh42kj3h4jk23h3jkhjh3jk242h4jk3h4jk34hrrbfbdbf'

currentNum = ''
op = ''
num1 = ''
num2 = ''

@app.route('/')
def home():
    return render_template('index.html', currentNum = currentNum)

@app.route('/button-click/<string:numOp>/<string:choice>')
def buttonClick(numOp, choice):
    global currentNum, num1, num2, op

    if choice == 'number':
        currentNum = f'{currentNum}{numOp}'
    elif choice == 'operator':
        num1 = int(currentNum)
        if numOp == 'div':
            op = '/'
        else:
            op = numOp
        currentNum = ''
    elif choice == 'equality':
        num2 = currentNum
        try:
            currentNum = eval(f'{num1}{op}{num2}')
        except Exception:
            currentNum = 'Error: Error'
    elif choice == 'clear':
        currentNum = ''
        
    return redirect(url_for('home', currentNum = currentNum))
    


if __name__ == '__main__':
    app.run(debug=True)