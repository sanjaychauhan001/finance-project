import streamlit as st
from scrape_data import get_data
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='stock data', layout='wide', page_icon="random")
st.header("Hello")
stock = st.text_input("Enter NSE/BSE symbol",'SBIN')

btn = st.button("get result")
if btn:
    if stock == '':
        st.write("please fill")
        exit()
    stock = stock.upper()
    try:    
        get = get_data(stock)
        st.subheader(f"Stock Symbol: {stock}")
        st.subheader(f"Current PE: {get.find_current_PE()}")
        st.subheader(f"FY23PE: {get.FY23PE()}")
        st.subheader(f"5-yr median pre-tax RoCE: {get.find_median_roce()}")

        sales = get.find_sales_growth()
        profit = get.find_profit_growth()
        name = ['10 YRS','5 YRS','3 YRS','TTM']
        df = pd.DataFrame({'sales growth':sales,
                  "profit growh":profit},
                  index=name)
        st.dataframe(df.T)

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.bar(x=sales,y=name,orientation='h',width=700, height=450
                      ,labels=dict(x='sales growth (%)',y='Time period'))
            st.plotly_chart(fig1,use_container_width=True)

        with col2:
            fig2 = px.bar(x=profit,y=name,orientation='h',width=700, height=450
                      ,labels=dict(x='profit growth (%)',y='Time period'))
            st.plotly_chart(fig2,use_container_width=True)    
    except:
        st.error("Invalid symbol",icon="🚨")