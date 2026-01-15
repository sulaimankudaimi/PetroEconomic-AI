# --- التنسيق المطور لضمان الوضوح الفائق ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .main { 
        background-color: #05070a !important; 
        color: #ffffff !important; 
    }
    
    /* جعل العناوين ضخمة وواضحة جداً وبألوان فوسفورية */
    h1 {
        color: #00f2ff !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 8px rgba(0, 242, 255, 0.5);
        text-align: center;
        padding: 10px;
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #00f2ff;
        padding-bottom: 5px;
    }

    /* تحسين وضوح الـ Metrics (الأرقام الكبيرة) */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* تحسين وضوح الجداول */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #111827 !important;
        border-radius: 10px;
        border: 1px solid #00f2ff;
    }

    /* وضوح القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #00f2ff !important;
    }
    .st-emotion-cache-16idsys p {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    
    /* تنبيهات واضحة */
    .stAlert {
        background-color: #1a202c !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)
