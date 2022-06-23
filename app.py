from datetime import date, datetime ,timedelta
import talib
import streamlit as st
import akshare as ak
import mplfinance as mpf
import pandas as pd

#标题
st.title('kTrainer')

##设置持有天数的session_state
#if 'count' not in st.session_state:
#    st.session_state.count = 0
#设置买入标志位，用于判断股票的模拟买入状态
if 'isbought' not in st.session_state:
    st.session_state.isbought = False


#TODO:增加板块数据
@st.cache
def load_data(name):
    df = ak.stock_zh_a_hist(symbol=name,period="daily",adjust="qfq")
    #数据处理
    df["日期"] = pd.to_datetime(df["日期"])#修改日期为坐标
    df.set_index("日期", inplace=True)
    df.rename(columns={		#重新命名，mplfinance规定数据标题必须是
    "日期": "Date",     #Date,Open,Close,High,Low,Volume
    "开盘": "Open",
    "收盘": "Close",
    "最高": "High",
    "最低": "Low",
    "成交量": "Volume",
    },inplace=True) 
    df['ma5'] = talib.MA(df['Close'], timeperiod=5, matype=0)
    df['ma21'] = talib.MA(df['Close'], timeperiod=21, matype=0)
    df['ma55'] = talib.MA(df['Close'], timeperiod=55, matype=0)
                                        
    return df


#TODO:初始化持有天数为0 !
with st.sidebar:
    time_interval = st.slider('显示K线区间(天)', 30,720)
    date_to = st.date_input('选择某一天', date(2021, 10, 1))
    doi = st.number_input('持有天数',min_value=0,step=1)
    name = st.text_input('股票代码')
    df = load_data(name)

#TODO:显示股票名称
#stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
#st.subheader(stock_individual_info_em_df.loc['股票简称'])

if st.checkbox('show data'):
    df
    

#忽略假期
bd = pd.tseries.offsets.BusinessDay(doi)
df1 = df.loc[:date_to+bd]
df2 = df1.tail(time_interval)


#TODO:增加legend
# 绘图
#fig,ax = mpf.plot(df2, type="candle", title="Candlestick for MSFT", ylabel="price($)",mav=(5,21,55),volume=True,figratio=(2, 1),returnfig=True)
#
#st.pyplot(fig)
ap = mpf.make_addplot(df2[['ma5','ma21','ma55']])
fig,ax = mpf.plot(df2, addplot=ap, type='candle', volume=True, figratio=(2,1), returnfig=True)

st.pyplot(fig)

#TODO:买入卖出逻辑
if st.session_state.isbought:       #如果已经买入
    btn1='买入'                     #显示持有按钮
    btn2='观望'                     #显示卖出按钮
else:                               #如果还未买入
    btn1='持有'                     #显示持有按钮
    btn2='卖出'                     #显示卖出按钮

if st.button(btn1):                     #点击买入或者持有状态下 
    st.session_state.isbought = True    #买入标记为真
    st.session_state.count += 1         #持有天数加一
if st.button(btn2):                     
    st.session_state.isbought = False   #买入标记为假
    st.session_state.count = 0          #持有天数清零

#TODO:显示最新的持有日期 !
#TODO:计算收益率
st.write('收益率计算')

