
from flask import Flask, render_template
import services

# create application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    services.RegisterServices(app)
    app.run(host='0.0.0.0', port=5050) # debug=True, use_reloader=True)