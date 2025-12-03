from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)

app = application

## Route for a home page

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    try:
        # collect form values (use request.form.get to read POSTed form fields)
        gender = request.form.get('gender')
        race_ethnicity = request.form.get('race_ethnicity')
        parental_level_of_education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_preparation_course = request.form.get('test_preparation_course')

        # reading/writing scores: try to convert to int, fallback to 0 if not provided / invalid
        try:
            reading_score = int(request.form.get('reading_score', 0))
        except (ValueError, TypeError):
            reading_score = 0

        try:
            writing_score = int(request.form.get('writing_score', 0))
        except (ValueError, TypeError):
            writing_score = 0

        # build CustomData object
        input_data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )

        # convert to dataframe for the pipeline
        input_df = input_data.get_data_as_data_frame()

        # create pipeline and predict
        pipeline = PredictPipeline()
        # assuming PredictPipeline exposes a `predict` method that takes a dataframe
        prediction = pipeline.predict(input_df)

        # format prediction for display (handle array-like returns)
        if isinstance(prediction, (list, tuple, np.ndarray, pd.Series)):
            result = round(float(prediction[0]), 2)
        else:
            result = round(float(prediction), 2)

        return render_template('home.html', prediction_text=result)

    except Exception as e:
        # return error on the same page; in production you would log the error
        return render_template('home.html', prediction_text=f'Error during prediction: {e}')

if __name__ == "__main__":
    app.run(port=5001, debug=True)