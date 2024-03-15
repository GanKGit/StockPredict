import pandas as pd
import plotly.graph_objects as go
import plotly
from flask import Flask, render_template
import json

app = Flask("Website")

@app.route("/")
def home():
    return render_template("home.html")

# Lookup function

app = Flask(__name__)

def create_plot(x_plot, y_plot):
    data = [
        go.Scatter(x=x_plot, y=y_plot, mode='lines+markers', line=dict(color='royalblue', width=3))
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def generate_data(p_v, q_v, s_v):
    last = int(round(float(s_v[0])/10,0)*10 + 10)

    first = int(last * 0.7)
    increment = int((last - first)/18)

    xaxis = list(range(first, last, increment))

    yaxis_cr = []
    for cols in range(0, len(p_v)):
        nl=[]
        for x in xaxis:
            nl.append(0 if x >= s_v[cols] else (s_v[cols] - x)*q_v[cols])
        yaxis_cr.append(nl)

    p_q = [a * b for a, b in zip(p_v, q_v)]
    pq = sum(p_q)
    pq=-pq

    yaxis_cr.append([pq]* len(xaxis))

    print("CR:")
    print(yaxis_cr)

    yaxis_tr = zip(*yaxis_cr)

    print("TR:")
    print(yaxis_tr)

    yaxis = [sum(a) for a in yaxis_tr]

    print("YAXIS:")
    print(yaxis)

    out = list(zip(xaxis, yaxis))

    return out

@app.route("/line/<input_data>/<CorP>")
def index(input_data, CorP):
    tokens = input_data.split(";")
    total = len(tokens)
    print(total)
    div = int(total / 3)
    print(div)
    p_v = tokens[0:div]
    q_v = tokens[div:div * 2]
    s_v = tokens[div * 2:div * 3]

    p_v = [float(i) for i in p_v]
    q_v = [float(i) for i in q_v]
    s_v = [float(i) for i in s_v]

    xyaxis = generate_data(p_v, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    line = create_plot(unzip_v[0],unzip_v[1])

    p_vn = [x * 2 for x in p_v]
    xyaxis = generate_data(p_vn, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    line2 = create_plot(unzip_v[0],unzip_v[1])

    p_vn = [x * 3 for x in p_v]
    xyaxis = generate_data(p_vn, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    line3 = create_plot(unzip_v[0],unzip_v[1])

    charts=render_template('index.html', plot=line, plot2=line2, plot3=line3, title1="As-Is Premium", title2="2X Premium", title3="3X Premium")

    return charts #this has changed


if __name__ == '__main__':
    app.run()


