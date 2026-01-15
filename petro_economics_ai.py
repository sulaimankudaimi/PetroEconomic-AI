import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import yfinance as yf
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# --- إعدادات الواجهة ---
st.set_page_config(page_title="PetroEconomic AI Pro", layout="wide")

# CSS لتحسين المظهر الاحترافي
st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border-left: 5px solid #00f2ff; }
    h1 { color: #00f2ff !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. محرك الذكاء الاصطناعي وجلب الأسعار ---
@st.cache_data(ttl=3600)
def get_market_data():
    oil = yf.Ticker("BZ=F")
    hist = oil.history(period="5y")
    current_price = round(hist['Close'].iloc[-1], 2)
    return current_price, hist

live_price, market_hist = get_market_data()

# --- 2. القائمة الجانبية (بوابة البيانات) ---
with st.sidebar:
    st.title("📥 Data Gateway")
    uploaded_file = st.file_uploader("Upload Production History (CSV)", type=['csv'])
    st.markdown("---")
    capex = st.number_input("Initial Investment (CAPEX $)", 100000, 10000000, 1000000)
    opex_fixed = st.slider("Operating Cost (OPEX $/bbl)", 10, 60, 25)
    discount_rate = st.slider("Annual Discount Rate (%)", 5, 20, 10)

# --- 3. معالجة البيانات المالية والإنتاج ---
st.title("💎 PetroEconomic AI: Integrated Profitability Engine")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Production file loaded successfully!")
    
    # نفترض أن العمود الثاني هو الإنتاج
    prod_col = df.columns[1] 
    total_prod = df[prod_col].sum()
    avg_monthly_prod = df[prod_col].mean()
    
    # حساب الأرباح بناءً على الإنتاج الفعلي وسعر السوق
    revenue = total_prod * live_price
    costs = total_prod * opex_fixed
    net_profit = revenue - costs
    
    # عرض النتائج
    c1, c2, c3 = st.columns(3)
    c1.metric("Live Market Price", f"${live_price}")
    c2.metric("Total Field Revenue", f"${int(revenue):,}")
    c3.metric("Net Operational Profit", f"${int(net_profit):,}")

    # رسم بياني للتدفق النقدي بناءً على البيانات
    df['Monthly_Profit'] = (df[prod_col] * live_price) - (df[prod_col] * opex_fixed)
    df['Cumulative_Cashflow'] = df['Monthly_Profit'].cumsum() - capex
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Cumulative_Cashflow'], fill='tozeroy', name='Project Recovery', line=dict(color='#00f2ff')))
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_layout(template='plotly_dark', title="Real-Data Financial Payback Timeline")
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.info("💡 Please upload a Production CSV file to see real-data financial analysis. Using simulation mode now...")
    # هنا يمكن وضع كود المحاكاة السابق لكي لا تظهر الصفحة فارغة
