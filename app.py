from flask import Flask, session, render_template, url_for, flash, request, redirect
from animation import graph
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# App config.
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def plot():    

    if request.method == "POST":
        confirms = []
        for i in range(6):
            confirm = not request.form.get(f"confirm_{i}", True) 
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

        potencia = not request.form.get("potencia", True) 
        corriente = not request.form.get("corriente", True) 
        presion = not request.form.get("presion", True) 

        graph(params, confirms, potencia, corriente, presion)

        return render_template("plot.html", image=url_for('static', filename="img/line.gif"), params=params)

    return render_template("plot.html", image=url_for('static', filename="img/line.gif"), params=[[0], [0], [0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])


if __name__ == "__main__":
    app.run(debug=True)