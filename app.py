from flask import Flask, send_file, make_response
from plot import render_map
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/plots/conditions_map', methods=['GET'])
def conditions_map():
    render_map("stroke")
    plt.savefig("stroke-map.png")
    return send_file('stroke-map.png', mimetype='image/gif')
    # bytes_obj = render_map("stroke")
    #
    # return send_file(bytes_obj,
    #                  attachment_filename='plot.png',
    #                  mimetype='image/png')
    #

if __name__ == '__main__':
    app.run(debug=True)
