import json
import os
import pickle

import numpy as np
import pandas as pd


def lambda_handler(event, context):
    if 'body' in event:
        try:
            event = json.loads(event['body'])  
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid JSON format in request body.')
            }

    action = event.get('action')

    if action == 'upload':
        return upload_and_train(event)
    elif action == 'predict':
        return make_prediction(event)
    elif action == 'update':
        return update_model(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid action. Use "upload", "predict", or "update".')
        }


def upload_and_train(event):
    csv_data = event.get('csv_data')

    if not csv_data:
        return {'statusCode': 400, 'body': json.dumps('No CSV data provided.')}

    with open('/tmp/processed_data.csv', 'w') as f:
        f.write(csv_data)

    print("CSV Data Written to File:", csv_data)

    df = pd.read_csv('/tmp/processed_data.csv')

    print("Columns in CSV:", df.columns.tolist())

    df = preprocess_data(df)

    X = df[['year', 'odometer', 'engine_power', 'accident_status']].values
    y = df['price_usd'].values
    X_b = np.c_[np.ones((X.shape[0], 1)), X]

    theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

    with open('/tmp/model.pkl', 'wb') as model_file:
        pickle.dump(theta_best, model_file)

    return {
        'statusCode': 200,
        'body': json.dumps('Model trained and saved successfully!')
    }


def make_prediction(event):
    input_data = event.get('input_data')

    if not input_data:
        return {'statusCode': 400, 'body': json.dumps('No input data provided.')}

    if not os.path.exists('/tmp/model.pkl'):
        return {'statusCode': 400, 'body': json.dumps('No trained model found. Please upload and train first.')}

    with open('/tmp/model.pkl', 'rb') as model_file:
        theta_best = pickle.load(model_file)

    input_with_intercept = [1] + input_data
    prediction = np.dot(theta_best, input_with_intercept)

    return {
        'statusCode': 200,
        'body': json.dumps({'predicted_price': round(prediction, 2)})
    }

def update_model(event):
    new_csv_data = event.get('csv_data')

    if not new_csv_data:
        return {'statusCode': 400, 'body': json.dumps('No CSV data provided for update.')}

    with open('/tmp/processed_data.csv', 'a') as f:
        f.write('\n' + new_csv_data)

    df = pd.read_csv('/tmp/processed_data.csv')
    df = preprocess_data(df)

    X = df[['year', 'odometer', 'engine_power', 'accident_status']].values
    y = df['price_usd'].values
    X_b = np.c_[np.ones((X.shape[0], 1)), X]

    theta_best = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

    with open('/tmp/model.pkl', 'wb') as model_file:
        pickle.dump(theta_best, model_file)

    return {
        'statusCode': 200,
        'body': json.dumps('Model updated and saved successfully!')
    }

def preprocess_data(df):
    required_columns = ['year', 'odometer', 'engine_power', 'accident_status', 'price_usd']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in the dataset: {missing_columns}")
    
    df['engine_power'] = df['engine_power'].astype(str).str.replace(' л.', '', regex=False).astype(float)
    df['accident_status'] = df['accident_status'].astype(int)
    df['odometer'] = df['odometer'].astype(int)
    
    return df


