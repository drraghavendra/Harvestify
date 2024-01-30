import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
import plotly.express as px
import joblib

style.use('fivethirtyeight')
st.title("Harvestify Yield Explorer "+u"\U0001F33D")
crop=pd.read_csv('Processed_Yield.csv')
del crop['Unnamed: 0']

if st.sidebar.checkbox('Show Statewise Average Yeild'):
    avg_yield=crop.groupby('State_Name').mean()
    st.subheader("Statewise Average Yield Per Year")
    st.table(avg_yield)

if st.sidebar.checkbox('Show Seasonal Harvest'):
    st.subheader('Yeild Per Season')
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    ax=sns.barplot(crop['Season'],crop['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Crops'):
    st.subheader('Top Crops')
    num=st.sidebar.slider("Number of Crops",5,10)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    top=crop.groupby('Crop').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['Crop'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing States'):
    st.subheader('Top States')
    num=st.sidebar.slider("Number of States",5,10)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    top=crop.groupby('State_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['State_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing States Cropwise'):
    st.subheader('Top States')
    num=st.sidebar.slider("Number of States",5,10,key=1)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    crop_input=st.sidebar.selectbox('Select Crop',list(crop['Crop'].unique()),key=2)
    top=crop[crop['Crop']==crop_input].groupby('State_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['State_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing Districts'):
    st.subheader('Top States')
    num=st.sidebar.slider("Number of Districts",5,10)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    top=crop.groupby('District_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['District_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing Districts Cropwise'):
    st.subheader('Top States')
    num=st.sidebar.slider("Number of Districts",5,10,key=1)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    crop_input=st.sidebar.selectbox('Select Crop',list(crop['Crop'].unique()),key=1)
    top=crop[crop['Crop']==crop_input].groupby('District_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['District_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing Districts in a State'):
    st.subheader('Top States')
    state_selected=st.sidebar.selectbox('Select State',list(crop['State_Name'].unique()))
    num=st.sidebar.slider("Number of Districts",5,10,key=2)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    top=crop[crop['State_Name']==state_selected].groupby('District_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['District_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

if st.sidebar.checkbox('Show Top Producing Districts in a State Cropwise'):
    st.subheader('Top States')
    state_selected=st.sidebar.selectbox('Select State',list(crop['State_Name'].unique()),key=1)
    num=st.sidebar.slider("Number of Districts",5,10,key=3)
    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)
    top=crop[crop['State_Name']==state_selected]
    crop_input=st.sidebar.selectbox('Select Crop',list(top['Crop'].unique()))
    top=top[top['Crop']==crop_input].groupby('District_Name').mean()
    top.sort_values(by=['Production (in Tonnes)'],inplace=True,ascending=False)
    top=top.head(num)
    top=top.reset_index()
    ax=sns.barplot(top['District_Name'],top['Production (in Tonnes)'],ci=None)
    st.pyplot(fig)

st.text("")
st.write("Please Select the State")
state=st.selectbox('',list(crop['State_Name'].unique()))
st.text("")
st.write("Please Select the District")
district=st.selectbox('',list(crop[crop['State_Name']==state]['District_Name'].unique()))
st.text("")
st.write("Please Select the Season")
season=st.selectbox('',list(crop['Season'].unique()))
st.text("")
st.write("Please Select the Crop")
crop_selected=st.selectbox('',list(crop['Crop'].unique()))
st.text("")
st.write("Please Enter Field Area in Hecteres")
area=st.number_input('',min_value=min(crop['Area (in Hectares)']))
st.text("")
data=[[state,district,season,crop_selected,area]]
data=pd.DataFrame(data)
data.columns=['State_Name','District_Name','Season','Crop','Area (in Hectares)']

if st.button('Predict'):
    st.write("Your Input is: ")
    st.table(data)
    enc=joblib.load('encoder.pkl')
    data[['State_Name','District_Name','Season','Crop']]=enc.transform(data[['State_Name','District_Name','Season','Crop']])
    model=joblib.load('yield_predictor.pkl')
    pred=model.predict(data)
    pred=pred[0]
    pred=max(pred,0)
    st.info("Predicted Yield is "+str(pred)+" Tonnes")
