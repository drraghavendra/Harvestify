import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
import plotly.express as px
import joblib
import numpy as np

style.use('fivethirtyeight')
st.title("Harvestify Heatmap ")
file=open('count.txt','r')
count = file.read()
count=int(count.strip())
file.close()
print(count)
def giveHeatMap(count):
    df = pd.read_csv('./SampleSensorValues.csv',skiprows=1)
    del df[df.columns[0]]
    record = df.loc[count]
    print(count)
    arr = np.array(record)
    figure,ax=plt.subplots()
    figure.set_figheight(10)
    figure.set_figwidth(15)
    plt.title("Farm Soil Moisture Level")
    ax = sns.heatmap(arr.reshape(5,4),annot = True, xticklabels = False,yticklabels = False)
    return figure
if st.sidebar.button('Reset'):
    count=0
    file=open('count.txt','w')
    file.write(str(count))
    file.close()
if st.sidebar.button('Refresh') or st.sidebar.checkbox("Show",value=True):
    count=count+1
    if count > 38:
        count=0
    file=open('count.txt','w')
    file.write(str(count))
    file.close()
    figure=giveHeatMap(count)
    st.pyplot(figure)