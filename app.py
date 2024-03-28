import streamlit as st
from scrape_data import get_data
import pandas as pd
import plotly.express as px
import cal_intrinsic_pe

st.set_page_config(page_title='stock data', layout='wide', page_icon="random")
st.header("DCF Valuation")
stock = st.text_input("Enter NSE/BSE symbol",'SBIN')
coc = st.slider('Cost of Capital (CoC): %', min_value=8.0, max_value=16.0,step=0.5,value=12.0)
roce = st.slider('Return on Capital Employed (RoCE): %', min_value=10.0, max_value=100.0,step=5.0,value=20.0)
gdhgp = st.slider('Growth during high growth period: $', min_value=8.0, max_value=20.0,step=1.0,value=12.0)
hgp = st.slider('High growth period(years)', min_value=10.0, max_value=20.0,step=1.0,value=15.0)
fp = st.slider('Fade period(years):', min_value=5.0, max_value=20.0,step=5.0,value=15.0)
tgr = st.slider('Terminal growth rate: %', min_value=0.0, max_value=7.5,step=1.0,value=5.0)
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
    st.subheader('Play with inputs to see changes in intrinsic PE and overvaluation: ')    
    intrinsic_PE = cal_intrinsic_pe.dcf(coc=coc,roce=roce,gdhgp=gdhgp,tgr=tgr,fp=int(fp),hgp=int(hgp))
    st.subheader(f'The calculated intrinsic PE is: {intrinsic_PE}')    