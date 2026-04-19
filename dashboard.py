import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Logistics Intelligence Dashboard", layout="wide", page_icon="🚚")

# Custom styling for premium feel
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1 { color: #1e3a8a; font-weight: bold; }
    h2, h3 { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

st.title("🚚 End-to-End Logistics Intelligence Dashboard")
st.markdown("### Real-Time Fleet & Shipment Monitoring")

@st.cache_data
def load_data():
    # Load latest processed shipments data
    files = glob.glob('data/processed/shipments_processed_*.csv')
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    return df

df = load_data()

if df is not None:
    # Top KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Shipments", f"{len(df):,}")
    with col2:
        delayed = len(df[df['status'] == 'Delayed'])
        st.metric("Delayed Shipments", f"{delayed:,}", delta=f"{-(delayed/len(df)*100):.1f}%", delta_color="inverse")
    with col3:
        avg_risk = df['risk_score'].mean()
        st.metric("Average Risk Score", f"{avg_risk:.2f}")
    with col4:
        active_vehicles = df['vehicle_id'].nunique()
        st.metric("Active Vehicles", f"{active_vehicles:,}")
        
    st.markdown("---")
    
    # Visualizations
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Shipment Status Distribution")
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        st.bar_chart(status_counts.set_index('Status'))
        
    with col_b:
        st.subheader("Risk Score by Vendor")
        risk_by_vendor = df.groupby('vendor_id')['risk_score'].mean().reset_index()
        st.line_chart(risk_by_vendor.set_index('vendor_id'))

    st.markdown("---")
    
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Top Origin Cities by Volume")
        origin_counts = df['origin_city'].value_counts().head(10)
        st.bar_chart(origin_counts)
        
    with col_d:
        st.subheader("Vehicle Types Usage")
        vehicle_counts = df['vehicle_type'].value_counts()
        st.bar_chart(vehicle_counts)
        
    st.markdown("---")
    st.subheader("Recent High-Risk Shipments")
    high_risk = df[df['risk_score'] > 0.8].sort_values(by='risk_score', ascending=False).head(10)
    st.dataframe(high_risk[['shipment_id', 'vendor_id', 'origin_city', 'destination_city', 'status', 'risk_score']], use_container_width=True)

else:
    st.warning("⚠️ No processed data found! Please run the data pipeline first: `python run_pipeline.py`")

st.markdown("---")
st.markdown("*Built automatically for the End-to-End Cloud Big Data Solution for Real-Time Logistics Intelligence project.*")
