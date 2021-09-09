from flask import Flask, config, jsonify, request
from auth.auth import auth_bp
from config.config import DevConfig

app = Flask(__name__)

# Using a production configuration
# app.config.from_object('ProdConfig')

# Using a development configuration
app.config.from_object(DevConfig)
 
app.register_blueprint(auth_bp, url_prefix='/api/auth')


@app.route('/')
def hello_world():
    print(request.form['name'])
    return 'Done', 200



if __name__ == '__main__':
    app.run(port=3000, debug=True)