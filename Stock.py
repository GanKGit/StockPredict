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

    op1 = []
    op2 = []
    op3 = []
    op4 = []

    for x in xaxis:
        if x >= s_v[0]:
            op1.append(0)
        else:
            op1.append((s_v[0] - x)*q_v[0])

        if x >= s_v[1]:
            op2.append(0)
        else:
            op2.append((s_v[1] - x)*q_v[1])

        if x >= s_v[2]:
            op3.append(0)
        else:
            op3.append((s_v[2] - x)*q_v[2])

        if x >= s_v[3]:
            op4.append(0)
        else:
            op4.append((s_v[3] - x)*q_v[3])


    p_q = [a * b for a, b in zip(p_v, q_v)]
    pq = sum(p_q)
    pq=-pq

    op5= [pq]* len(op1)
    yaxis = [a +b+c+d+e for a, b, c, d, e in zip(op1, op2, op3, op4, op5)]

    print("XAXIS:")
    print(xaxis)

    print("YAXIS:")
    print(yaxis)

    out = list(zip(xaxis, yaxis))

    print("OUT::::::::")
    print(out)

    return out

@app.route("/line/<p1>/<p2>/<p3>/<p4>/<q1>/<q2>/<q3>/<q4>/<s1>/<s2>/<s3>/<s4>")
def index(p1, p2, p3, p4,q1,q2,q3,q4,s1,s2,s3,s4):
    p_v = [float(p1), float(p2), float(p3), float(p4)]
    q_v = [float(q1), float(q2), float(q3), float(q4)]
    s_v = [float(s1), float(s2), float(s3), float(s4)]

    xyaxis = generate_data(p_v, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    print("unzip_v :")
    print(str(unzip_v))
    line = create_plot(unzip_v[0],unzip_v[1])

    p_vn = [x * 1.5 for x in p_v]
    xyaxis = generate_data(p_vn, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    line2 = create_plot(unzip_v[0],unzip_v[1])

    p_vn = [x * 2 for x in p_v]
    xyaxis = generate_data(p_vn, q_v, s_v)
    unzip_v = ([ a for a,b in xyaxis ], [ b for a,b in xyaxis ])
    line3 = create_plot(unzip_v[0],unzip_v[1])

    charts=render_template('index.html', plot=line, plot2=line2, plot3=line3)

    return charts #this has changed


if __name__ == '__main__':
    app.run()
