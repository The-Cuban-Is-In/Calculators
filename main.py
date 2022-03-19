from decimal import DivisionByZero
from typing import OrderedDict
from flask import Flask, render_template, redirect, request, url_for
from werkzeug import exceptions

import math
import werkzeug



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hj3klh42kj3h4jk23h3jkhjh3jk242h4jk3h4jk34hrrbfbdbf'

@app.route('/', methods=['POST', 'GET'])
def home():
    bmiValue = ''
    
    totalMaterialCost = ''
    
    try:
        totalMaterials = request.form.get('materials')
    except:
        totalMaterials = 0

    try:
        currentNum = request.args["currentNum"]
        bmiValue = ''
        totalMaterialCost = ''
    except KeyError:
        currentNum = ''
    
    try:
        materialSelect = request.args['materialSelect']
    except KeyError:
        materialSelect = True
    
    try:
        option = request.args['option']  
    except exceptions.BadRequestKeyError:
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

        if option == 'material-calc':   #-- POST requests for Material Calc
            
            if materialSelect:      # -- Confirms is on material select or not
                print(materialSelect)
                totalMaterials = request.form.get('materials')
                materialSelect = False
                
            if materialSelect == False:       # -- Confirms is on material select or not
                trash = []
                materialValues = []
                costValues = []
                print(materialSelect)
                for materials in range(len(request.form)):
                    if request.form.get(f'material{materials + 1}') == None or request.form.get(f'cost{materials + 1}') == None:
                        try:
                            trash.append(request.form.get(f'material{materials + 1}'))
                        except:
                            trash.append(request.form.get(f'cost{materials + 1}'))
                    else:
                        materialValues.append((float(request.form.get(f'material{materials + 1}')), float(request.form.get(f'cost{materials + 1}'))))
                del trash
                for a,b in materialValues:
                    costValues.append(a * b)

                totalMaterialCost = f'${sum(costValues) :.2f}'
                materialSelect = False
            if request.form.get('back-button') == 'back':
                materialSelect = True
        
        if option == 'graphic-calc':        # -- Confirms the form being submitted is for the graphic-calculator
            try:
                if 'number' in request.form:
                    currentNum = '{}{}'.format(currentNum, request.form.get('number') )   
                elif 'clear' in request.form:
                    currentNum = ''    
                elif 'operator' in request.form:
                    global num1, op
                    op = request.form.get('operator')
                    num1 = request.args['currentNum']
                    currentNum  = ''

                if 'equal' in request.form:
                    global num2
                    num2 = request.args['currentNum']                        
                    currentNum = math.pow(float(num1), float(num2)) if op == 'exponent' else str(float(eval(f'{num1}{op}{num2}')))

                if 'square' in request.form:
                    currentNum = float(currentNum) ** 2
                
                if 'square-root' in request.form:
                    currentNum = math.sqrt(float(currentNum))

                if 'negative' in request.form:
                    currentNum = '{}'.format(currentNum.strip('-')) if currentNum == '-{}'.format(currentNum.strip('-')) else f'-{currentNum}'

                if 'decimal' in request.form:
                    tempNum = currentNum.strip('.')
                    currentNum = f'{tempNum}' if currentNum == f'{tempNum}.' else f'{currentNum}.'

            except OverflowError:
                currentNum = 'ERROR: Range to high'
            except ZeroDivisionError:
                currentNum = 'ERROR: division by zero'
            except ValueError:
                pass
            
    return render_template('index.html',        
        option = option,
        bmiValue = bmiValue,
        totalMaterialCost = totalMaterialCost,
        currentNum = currentNum,
        totalMaterials = totalMaterials,
        materialSelect = materialSelect
        )


if __name__ == '__main__':
    app.run(debug=True)