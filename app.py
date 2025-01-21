from flask import Flask, render_template, request, jsonify
import os
import sys
import pandas as pd
from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictPipeline
from dataclasses import dataclass
from src.utils import double_log_transform, cube_root_transform
from src.logger import logging
from src.exception import CustomError

@dataclass
class AppConfig:
    default_data_path = 'notebook/Data/creditcard.csv'
    train_data_description_path = 'artifacts/train_data_describe.csv'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/train_page', methods=['GET'])
def train_page():
    return render_template('training_page.html')

@app.route('/train', methods=['GET'])
def train():
    file_path = request.args.get('file', AppConfig.default_data_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            training_pipeline = TrainingPipeline()
            training_pipeline.run_pipeline(0.6, file_path)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'File not found.'}), 404

@app.route('/predict_page', methods = ['GET', 'POST'])
def predict_route():
    try:
        if request.method == 'GET':
            df = pd.read_csv(AppConfig.train_data_description_path, index_col = 0)
            variables = df.columns.tolist() 
            variable_data = {}

            for var in variables:
                variable_data[var] = {
                    'min': round(df.loc['min', var], 2),
                    'median': round(df.loc['50%', var], 2),
                    'max': round(df.loc['max', var], 2)
                    }
            return render_template('prediction_page.html', variable_data = variable_data)
        else:
            df = pd.DataFrame({key:float(value) for key, value in request.get_json().items()}, index = [0])
            prediction_pipeline = PredictPipeline()
            result = prediction_pipeline.run_pipeline(df)
            return  jsonify({'result': result, 'message': 'Prediction Completed Successfully!!.'})
    except:
        error_obj = CustomError(*sys.exc_info())
        logging.error(error_obj, exc_info = True)
        return render_template('404.html'), 404
    
@app.route('/404', methods=['GET'])
def error_404():
    return render_template('404.html')

# execution starts here
if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000) 