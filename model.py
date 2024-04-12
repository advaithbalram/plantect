from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Initialize Flask app
app = Flask(__name__)

# Load data
sheet_id = '1KFknTsw6DXHUoho1ccXkSJiJ_bDt3vrTg3yL1roWYQ0'
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

# Remove duplicates and missing values
data = data.drop_duplicates()
data.dropna(inplace = True)


# Split data into features and target
X = data.drop('label', axis=1)
y = data['label']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Prediction route
# Prediction route
@app.route('/', methods=['POST'])
def predict():
    try:
        # Parse JSON data from the request
        data_list = request.json

        for data in data_list:
            # Prediction logic
            L = [data['N'], data['P'], data['K'], data['pH'], data['temperature'], data['humidity']]
            L = np.array(L).reshape(1, 6)

            p = clf.predict_proba(L)
            p = pd.DataFrame(data=np.round(p.T, 2), index=pd.unique(y), columns=['probabilities'])

            crop = data['crop']
            C = p[p['probabilities'] > 0.2].index.tolist()

            if crop in p.index and p.loc[crop, 'probabilities'] >= 0.2:
                res = "Suitable"
                if crop in C:
                    C.remove(crop)
            else:
                res = "Not Suitable"

            results_dict = {
                "res": res,
                "C": C
            }

        return jsonify(results_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
