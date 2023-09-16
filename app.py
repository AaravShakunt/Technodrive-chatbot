import pickle
from flask import Flask, render_template, request
from explainer import explain_predict
from cleaner import cleaner
import numpy as np
app = Flask(__name__)



# Load the machine learning model from the pickle file
with open('model.pkl', 'rb') as file:
    print(type(file))
    loaded_model = pickle.load(file)

res_dic={0:"Patient doesn't have Breast Cancer",1:"Patient has Breast Cancer"}

# Define the attribute names corresponding to the input features
attribute_names = [
    'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity',
    'mean concave points', 'mean symmetry', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error',
    'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error',
    'fractal dimension error', 'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness',
    'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension'
]

@app.route('/', methods=['GET', 'POST'])
def breast_cancer_detection():
    if request.method == 'POST':
        # Collect user input for each attribute and create a list
        X_test = []
        for attribute_name in attribute_names:
            value = float(request.form[attribute_name])
            X_test.append(value)

        X_test=np.array(X_test)
        with open("sample.txt", "w") as output_file:
            y_pred = explain_predict([X_test], loaded_model, output_file)
        y_pred=res_dic[int(y_pred[0])]
        result = cleaner("sample.txt")

        explanation_items = result.split('\n')[:-1]
        last_line= result.split('\n')[-1]

        # Assign the list of explanation items to 'explanation_items' and the last line to 'last_line'
        # explanation_items, last_line = explanation_items if len(explanation_items) > 1 else ([], result)

        # Pass both 'explanation_items' and 'last_line' to the template
        return render_template('result.html', y_pred=y_pred, explanation_items=explanation_items, last_line=last_line)
    
    return render_template('form.html', attribute_names=attribute_names)

if __name__ == '__main__':
    app.run(debug=True)