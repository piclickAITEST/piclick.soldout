from flask import Flask, request, render_template, send_from_directory, jsonify, Response, redirect
from handler.soldout import soldout

app = Flask(__name__)



app.register_blueprint(soldout, url_prefix="/soldout")

@app.route('/')
def index():
  return 'flask health'

if __name__ == '__main__':
  
  app.run(host="0.0.0.0", port=8888, debug=True)