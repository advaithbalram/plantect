import http.server
import socketserver
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
sheet_id = '1KFknTsw6DXHUoho1ccXkSJiJ_bDt3vrTg3yL1roWYQ0'
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

# Remove duplicates and missing values
data = data.drop_duplicates().dropna()

# Split data into features and target
X = data.drop('label', axis=1)
y = data['label']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

class PredictionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the content
        content_length = int(self.headers['Content-Length'])

        # Read and parse the POST data
        post_data = self.rfile.read(content_length)
        data_list = json.loads(post_data.decode('utf-8'))

        data = data_list[0]

        try:
            # Prediction logic
            L = [data['N'], data['P'], data['K'], data['pH'], data['temperature'], data['humidity']]
            L = np.array(L).reshape(1, 6)

            p = clf.predict_proba(L)
            p = pd.DataFrame(data=np.round(p.T, 2), index=pd.unique(y), columns=['probabilities'])

            crop = data['crop']
            C = p[p['probabilities'] > 0.2].index.tolist()

            if p.loc[crop, 'probabilities'] >= 0.2:
                res = "Suitable"
                C.remove(crop)
            else:
                res = "Not Suitable"

            results_dict = {
                "res": res,
                "C": C
            }

            # Prepare the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results_dict).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

# Run the HTTP server
with socketserver.TCPServer(('0.0.0.0', 3001), PredictionHandler) as httpd:
    print('Serving at port 3001...')
    httpd.serve_forever()

