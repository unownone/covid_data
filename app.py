from flask import Flask,render_template,jsonify,request
from config import Config
import scrape

app = Flask(__name__)
app.config.from_object(Config)



@app.route('/covid',methods=['GET'])
def main():
    return jsonify(scrape.main_function())

if __name__ == '__main__':
    app.run(debug=False)