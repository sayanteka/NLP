import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
#from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import plotly.graph_objs as go
import os
import random
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="StreamlitDashboard", page_icon=":bar_chart:",layout="wide")
st.markdown("<h1 id='title'> Car Price Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<style>#title{text-align:center;}</style>", unsafe_allow_html=True)
st.markdown("<style>div.block-container{padding-top:2rem;text-align:center;}</style>", unsafe_allow_html=True)
df = pd.read_csv("Car Predictions Output csv.csv", encoding = "ISO-8859-1")
engine_type = df['enginetype'].unique().tolist()
cylinder_number = df['cylindernumber'].unique().tolist()
fuel_type = df['fueltype'].unique().tolist()
phase_type = df['Phase'].unique().tolist()

st.sidebar.header("Filter Options")

Engine_Type = st.sidebar.multiselect('Filter Engine Type:', engine_type, engine_type, key='engine_type')
Cylinder_Number = st.sidebar.multiselect('Filter Cylinder Type:', cylinder_number, cylinder_number, key='cylinder_number')
Fuel_Type = st.sidebar.multiselect('Filter Fuel Type:', fuel_type, fuel_type, key='fuel_type')
Phase_Type = st.sidebar.multiselect('Filter Phase Type:', phase_type, phase_type, key='phase_type')

new_df = (
    df['enginetype'].isin(Engine_Type) &
    df['cylindernumber'].isin(Cylinder_Number) &
    df['fueltype'].isin(Fuel_Type) &
    df['Phase'].isin(Phase_Type)
)
filtered_df = df[new_df]

grouped_df = filtered_df.groupby('carbody')['car_ID'].count().reset_index()
new_title = '<p style="font-family:Times New Roman; color:Black; font-size:33px;font-weight:bold;">Count of cars vs car body</p>'
st.markdown(new_title, unsafe_allow_html=True)
     #st.header("Count of cars by car body")
fig = px.bar(
        grouped_df,
        x='carbody',
        y="car_ID",
        text_auto=".2s",
        height=400,
        width=600,
        color_discrete_sequence=['#38B39B'])
fig.update_traces(
       textfont_size=20, textangle=0, textposition="outside", cliponaxis=False)
fig.update_layout(xaxis=dict(categoryorder='total descending'),margin=dict(l=15, r=15, t=15, b=15))
#here margin indicates whether it is away from title or close to title
#close to title=margin is less like 15 if away from title increase the margin
fig.update_xaxes(title_text="Carbody", title_font=dict(size=15, family="Arial",color="black"),tickfont=dict(size=15, family="Arial", color="black"))
fig.update_yaxes(title_text="Number of cars", title_font=dict(size=15, family="Arial",color="black"),tickfont=dict(size=15, family="Arial", color="black"))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.plotly_chart(fig, use_container_width=False)


grouped_df = filtered_df.groupby('carbody')['price'].mean().reset_index()

new_title = '<p style="font-family:Times New Roman; color:Black; font-size:27px;font-weight:bold;">Average price vs car body</p>'
st.markdown(new_title, unsafe_allow_html=True)
        #st.header("Average price per car body")
fig = px.bar(
        grouped_df,
        x="carbody",
        y="price",
        text=["$" + format(price, ".2f") for price in grouped_df["price"]],
        text_auto=".2s",
        color_discrete_sequence=["rgba(255, 43, 43, 0.2)"],
        height=400,
        width=600)



fig.update_layout(xaxis=dict(categoryorder='total descending'))
fig.update_layout(
        margin=dict(l=15, r=15, t=15, b=15))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
max_price = max(grouped_df["price"])
interval = 5000  # 5k
tickvals = list(range(0, int(max_price) + interval, interval))
ticktext = ["$" + str(val // 1000) + "k" if val > 0 else "0" for val in tickvals]

# Update the y-axis tick labels
fig.update_yaxes(tickvals=tickvals, ticktext=ticktext)
fig.update_traces(
    textfont_size=20,
    textangle=0,
    textposition="outside",
    cliponaxis=False)

st.plotly_chart(fig, use_container_width=False)


