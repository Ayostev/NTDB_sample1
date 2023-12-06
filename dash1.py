import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *

st.set_page_config(page_title="Dashbord",page_icon="🛣", layout="wide")
st.title(" :chart_with_upwards_trend: NATIONAL TRANSPORT DATABANK")
st.subheader("Kawo Traffic Flow Analytics")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)


#Fetch data
result=view_all_data()
df=pd.DataFrame(result, columns=["ID","Day","Direction","Period","Time","Car","Tricycle","Motor cycle","Mini Bus","Taxi", "Pickup/Lorry","Mid/Big Bus","Tanker/ Trailer","Total","PCU/hr"])

#side bar
st.sidebar.image("data/NTD_logo.png",caption="National Transport Databank")

#switcher
st.sidebar.header("Please filter")
direction=st.sidebar.multiselect(
    "Select Traffic Flow Direction",
    options=df["Direction"].unique(),
    default=df["Direction"].unique(),
)
day=st.sidebar.multiselect(
    "Select Day of the Week",
    options=df["Day"].unique(),
    default=df["Day"].unique(),
)
period=st.sidebar.multiselect(
    "Select Period of the Day",
    options=df["Period"].unique(),
    default=df["Period"].unique(),
)
time=st.sidebar.multiselect(
    "Select Time of the day",
    options=df["Time"].unique(),
    default=df["Time"].unique(),
)
df_selection=df.query(
    "Direction==@direction & Day==@day & Period==@period & Time==@time"
)

def Home():
    with st.expander("Tabular"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=[])
        st.write(df_selection[showData])

    #Compute top Analytics
    total_traffic_flow=df_selection["Total"].sum()
    traffic_mean=df_selection["Total"].mean()
    traffic_max=df_selection["Total"].max()
    car_mean=df_selection["Car"].mean()
    tricycle_mean=df_selection["Tricycle"].mean()
    motorcycle_mean=df_selection["Motor cycle"].mean()
    mini_mean=df_selection["Mini Bus"].mean()
    taxi_mean=df_selection["Taxi"].mean()
    
    total1,total2,total3,total4,total5,total6,total7,total8=st.columns(8,gap='large')
    with total1:
        st.info('Total Averge Daily Traffic', icon="🚦")
        st.metric(label="Total Hourly flow",value=f"{total_traffic_flow:,.0f}")

    with total2:
        st.info('Averge Daily Hourly Traffic', icon="🚦")
        st.metric(label="Avg.Hourly flow",value=f"{traffic_mean:,.0f}") 

    with total3:
        st.info('Hourly Max Traffic', icon="🚦")
        st.metric(label="Hourly Max",value=f"{traffic_max:,.0f}") 
    
    with total4:
        st.info('Car Flow', icon="🚦")
        st.metric(label="Avg. traffic",value=f"{car_mean:,.0f}") 
    
    with total5:
        st.info('Tricycle Flow', icon="🚦")
        st.metric(label="Avg. traffic",value=f"{tricycle_mean:,.0f}")

    with total6:
        st.info('Motorcycle Flow', icon="🚦")
        st.metric(label="Avg. traffic",value=f"{motorcycle_mean:,.0f}")

    with total7:
        st.info('Mini Bus Flow', icon="🚦")
        st.metric(label="Avg. traffic",value=f"{mini_mean:,.0f}")

    with total8:
        st.info('Taxi Flow', icon="🚦")
        st.metric(label="Avg. traffic",value=f"{taxi_mean:,.0f}")

    st.markdown("""---""")    

#Graph
def graphs():
    #traffic_mean=df_selection["Total"].mean()
    #total_traffic_flow=df_selection["Total"].sum()
    #traffic_mean=round(df_selection["Total"]).mean(),
    
    Day_by_Traffic = (
    df_selection.groupby(by="Day", as_index=True)
    ["Total"].mean()
    )

    fig_Total=px.bar(
        Day_by_Traffic,
        x=Day_by_Traffic.index,
        y="Total",
        orientation="v",
        title="<b> Daily Average Hourly Flow </b>",
        color_discrete_sequence=["#0083b8"]*len(Day_by_Traffic),
        template="plotly_white",
    )

    fig_Total.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )


#line Graph1

    Time_by_Traffic = (
    df_selection.groupby(by="Time", as_index=True)
    ["Total"].mean()
    )

    fig_Time=px.line(
        Time_by_Traffic,
        x=Time_by_Traffic.index,
        y="Total",
        orientation="v",
        title="<b> Average Hourly Flow </b>",
        color_discrete_sequence=["#0083b8"]*len(Time_by_Traffic),
        template="plotly_white",
    )

    fig_Time.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )


#Pie chart   

    fig_Direction=px.pie(df_selection,values="Total", names= "Direction", hole=0.5)
    fig_Direction.update_traces(title="Average Hourly Directional Flow", text=df_selection["Direction"],textposition = "outside")

    left,centre,right=st.columns(3)
    left.plotly_chart(fig_Total,use_container_width=True)
    left.plotly_chart(fig_Time,use_container_width=True)                
    right.plotly_chart(fig_Direction,use_container_width=True)
Home()
graphs()