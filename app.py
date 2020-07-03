from flask import Flask, session, render_template, url_for, flash, request, redirect, make_response
from functools import wraps, update_wrapper
from animation import graph
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime


# App config.
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)


@app.route("/", methods=["GET", "POST"])
@nocache
def plot():    

    if request.method == "POST":
        confirms = []
        for i in range(6):
            confirm = "1" if request.form.get(f"confirm_{i}") else False
            confirms.append(confirm)
        
        params = []
        cants = {1: 1, 2: 1, 3:2, 4:3, 5:3, 6:3}
        for i in range(1, 7):
            c = cants[i]
            p = []
            for j in range(1, c+1):
                if request.form.get(f"param{i}{j}"):
                    p.append(float(request.form.get(f"param{i}{j}")))
                else:
                    p.append(0)
            params.append(p)

        potencia = "1" if request.form.get("potencia") else False
        corriente = "1" if request.form.get("corriente") else False
        presion = "1" if request.form.get("presion") else False
        puntos = "1" if request.form.get("puntos") else False   
        graph(params, confirms, potencia, corriente, presion, puntos)

        return render_template("plot.html", image=url_for('static', filename="img/line.gif"), params=params, confirms=confirms, plot=[corriente, potencia, presion, puntos])

    return render_template("plot.html", image=url_for('static', filename="img/line.gif"), params=[[0], [0], [0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], confirms=[0, 0, 0, 0, 0, 0], plot=[0, 0, 0, 0])


if __name__ == "__main__":
    app.run(debug=True)