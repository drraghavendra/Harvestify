import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask
from flask import send_file
import pandas as pd
import numpy as np
app = Flask(__name__)

@app.route('/',methods=['GET'])
def base():
    return "API is up."
count = 0
@app.route('/heatmap',methods=['GET'])
def giveHeatMap():
    df = pd.read_csv('./SampleSensorValues.csv',skiprows=1)
    global count
    if count == df.shape[0]-1:
        count = 1
    else:
        count+=1
    del df[df.columns[0]]
    record = df.loc[count]
    print(count)
    
    arr = np.array(record)
    plt.clf()
    plt.figure(dpi = 200)
    plt.title("Farm Soil Moisture Level")
    figure = sns.heatmap(arr.reshape(5,4),annot = True, xticklabels = False,yticklabels = False)
    plt.savefig('Temp.png')
    return send_file('Temp.png', mimetype='image/png')

app.run('0.0.0.0',port = 5556)