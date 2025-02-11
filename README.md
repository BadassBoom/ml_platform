# Task Platform
The API is hosted on AWS Lambda and exposed via API Gateway.

# 🛠 Prerequisites
1. Python 3 installed on your machine.
2. Install the requests, pandas, numpy libraries if you haven't already:

# 🚀 How to Run the Test Script
1. Clone repo:
   
   `git clone https://github.com/BadassBoom/ml_platform.git`.
   
3. Run the script from your terminal:

   `python test_function.py`.

# Expected Output

- Upload Response:
  ```
  {
    "statusCode": 200,
    "body": "Model trained and saved successfully!"
  }
  ```
  
- Prediction Response:
  ```
  {
    "statusCode": 200,
    "body": {
      "predicted_price": 10250.75  // (Example price; will vary based on data)
    }
  }
  ```

- Update Response:
  ```
  {
    "statusCode": 200,
    "body": "Model updated and saved successfully!"
  }
  ```
# Explanation of API Actions
Upload (upload):

- Sends CSV data to train a new linear regression model.
- Required key: `csv_data` (CSV formatted string).
- Predict (predict):

Makes a price prediction based on the provided input features.
- Required key: "input_data" (list of values in the format [year, odometer, engine_power, accident_status]).
  
Update (update):
- Adds new data to the existing dataset and retrains the model.
- Required key: `csv_data` (new data to be appended in CSV format).

# Why I Didn't Use scikit-learn for Model Training
While scikit-learn is a powerful library for machine learning tasks, I opted not to use it in this project for the following reasons:

1. AWS Lambda Size Constraints:
AWS Lambda has a deployment package size limit of 50 MB (compressed) and 250 MB (uncompressed), including layers. scikit-learn along with its dependencies (like NumPy, SciPy) exceeds this limit, making it challenging to deploy directly.

2. Lightweight & Efficient Approach:
Instead of using scikit-learn's LinearRegression, I implemented linear regression manually using NumPy. This keeps the code lightweight, fast, and compatible with AWS Lambda's size limitations.

3. Focus on Simplicity:
Given that model performance isn't a high priority (as mentioned in the task description), using NumPy for linear regression is sufficient and provides more control over the model training process.



# Troubleshooting
If the prediction fails, ensure you have uploaded data first (upload action).

# Security Note
This script uses a public API URL for demonstration purposes. 
