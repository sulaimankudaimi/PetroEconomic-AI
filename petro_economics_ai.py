import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import yfinance as yf
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="PetroEconomic AI Pro", layout="wide")

# --- 2. حل مشكلة وضوح النصوص عبر CSS متطور ---
st.markdown("""
    <style>
    /* الخلفية والنصوص العامة */
    .main { 
        background-color: #05070a !important; 
        color: #ffffff !important; 
    }
    
    /* العناوين الرئيسية */
    h1 {
        color: #00f2ff !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px rgba(0, 242, 255, 0.4);
        text-align: center;
        padding-bottom: 20px;
    }

    /* وضوح الأرقام (Metrics) */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    /* تحسين وضوح القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #00f2ff !important;
    }
    .st-emotion-cache-16idsys p {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* صناديق المعلومات */
    .stAlert {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك البيانات والذكاء الاصطناعي ---
@st.cache_data(ttl=3600)
def get_market_intelligence():
    try:
        oil = yf.Ticker("BZ=F")
        hist = oil.history(period="5y")
        current = round(hist['Close'].iloc[-1], 2)
        return current, hist
    except:
        return 75.0, pd.DataFrame() # سعر افتراضي في حال فشل الاتصال

live_price, market_hist = get_market_intelligence()

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff;'>📥 Data Gateway</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Production CSV", type=['csv'])
    st.markdown("---")
    capex = st.number_input("Initial CAPEX ($)", 100000, 10000000, 1500000)
    opex_fixed = st.slider("OPEX ($/bbl)", 10, 60, 25)
    discount_rate = st.slider("Annual Discount Rate (%)", 5, 20, 12)

# --- 5. العرض الرئيسي ---
st.markdown("<h1>💎 PetroEconomic AI: Strategic Profitability Engine</h1>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # التحليل المالي بناءً على الملف المرفوع
    prod_col = df.columns[1]
    df['Revenue'] = df[prod_col] * live_price
    df['Costs'] = df[prod_col] * opex_fixed
    df['Net_Profit'] = df['Revenue'] - df['Costs']
    df['Cumulative_CF'] = df['Net_Profit'].cumsum() - capex
    
    # حساب المقاييس
    npv = npf.npv(discount_rate/1200, df['Net_Profit']) - capex
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Live Market Price", f"${live_price}")
    c2.metric("Estimated NPV", f"${int(npv):,}")
    c3.metric("Total Recovery", f"{int(df[prod_col].sum()):,} bbl")
    
    st.markdown("### 📈 Cumulative Cash Flow Analysis")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Cumulative_CF'], fill='tozeroy', line=dict(color='#00f2ff', width=3)))
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_layout(template='plotly_dark', xaxis_title="Months", yaxis_title="Cash Balance ($)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👋 Welcome Engineer Sulaiman. Please upload 'Sample_Production.csv' from your repository to activate the engine.")
    st.image("https://img.icons8.com/clouds/500/money-box.png", width=150)
