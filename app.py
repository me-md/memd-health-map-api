from flask import Flask, send_file, make_response, request
from plot import render_map
from quartile_plot import plot_map
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return 'We are up and running!'

@app.route('/api/v1/conditions_map', methods=['GET'])
def conditions_map_v1():
    args = request.args
    render_map(args['condition'])
    plt.savefig("MeMD_Map.png")
    return send_file('MeMD_Map.png', mimetype='image/gif')

@app.route('/api/v2/conditions_map', methods=['GET'])
def conditions_map_v2():
    args = request.args
    plot_map(args['condition'])
    plt.savefig("MeMD_Map.png")
    return send_file('MeMD_Map.png', mimetype='image/gif')


if __name__ == '__main__':
    app.run(debug=True)
