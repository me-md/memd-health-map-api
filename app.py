from flask import Flask, send_file, make_response, request
from plot import render_map
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/conditions_map', methods=['GET'])
def conditions_map():
    args = request.args
    render_map(args['condition'])
    plt.savefig("MeMD_Map.png")
    return send_file('MeMD_Map.png', mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True)
