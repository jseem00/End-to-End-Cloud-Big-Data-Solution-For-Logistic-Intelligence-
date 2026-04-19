"""
🚚 End-to-End Logistics Intelligence Dashboard
Real-Time Fleet & Shipment Monitoring

Built for: End-to-End Cloud Big Data Solution for Real-Time Logistics Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Logistics Intelligence Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stAlert {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def generate_sample_data():
    """Generate realistic sample logistics data"""
    np.random.seed(42)
    
    # Generate shipment data
    num_shipments = 500
    vendors = ['VendorA', 'VendorB', 'VendorC', 'VendorD', 'VendorE']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
    
    dates = pd.date_range(end=datetime.now(), periods=num_shipments, freq='H')
    
    shipments_data = {
        'shipment_id': [f'SHP{i:05d}' for i in range(num_shipments)],
        'vendor_id': np.random.choice(vendors, num_shipments),
        'origin': np.random.choice(cities, num_shipments),
        'destination': np.random.choice(cities, num_shipments),
        'distance_km': np.random.randint(50, 1500, num_shipments),
        'package_weight_kg': np.random.randint(1, 500, num_shipments),
        'shipment_date': dates,
        'estimated_delivery_hours': np.random.randint(2, 72, num_shipments),
        'actual_delay_minutes': np.random.randint(-30, 180, num_shipments),
        'on_time': np.random.choice(['Yes', 'No'], num_shipments, p=[0.75, 0.25]),
        'customer_rating': np.random.uniform(3.0, 5.0, num_shipments),
        'temperature_c': np.random.randint(15, 40, num_shipments),
        'fuel_consumed_liters': np.random.randint(5, 150, num_shipments),
    }
    
    shipments_df = pd.DataFrame(shipments_data)
    shipments_df['avg_speed_kmh'] = shipments_df['distance_km'] / (shipments_df['estimated_delivery_hours'] + 0.1)
    shipments_df['status'] = shipments_df['on_time'].map({'Yes': 'Delivered On-Time', 'No': 'Delayed'})
    
    # Generate vehicle telemetry
    num_vehicles = 100
    vehicles_data = {
        'vehicle_id': [f'VEH{i:03d}' for i in range(num_vehicles)],
        'latitude': np.random.uniform(12.0, 28.0, num_vehicles),
        'longitude': np.random.uniform(72.0, 88.0, num_vehicles),
        'speed_kmh': np.random.randint(0, 100, num_vehicles),
        'fuel_level_percent': np.random.randint(10, 100, num_vehicles),
        'engine_temp_c': np.random.randint(70, 110, num_vehicles),
        'maintenance_score': np.random.uniform(0.0, 1.0, num_vehicles),
        'status': np.random.choice(['Active', 'Idle', 'Maintenance'], num_vehicles, p=[0.6, 0.3, 0.1]),
        'odometer_km': np.random.randint(10000, 250000, num_vehicles),
    }
    
    vehicles_df = pd.DataFrame(vehicles_data)
    vehicles_df['maintenance_priority'] = pd.cut(
        vehicles_df['maintenance_score'],
        bins=[0, 0.4, 0.7, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    # Generate predictions
    shipments_df['predicted_delay_minutes'] = shipments_df['actual_delay_minutes'] + np.random.randint(-20, 20, num_shipments)
    vehicles_df['anomaly_detected'] = vehicles_df['maintenance_score'] > 0.7
    
    return shipments_df, vehicles_df


def main():
    # Header
    st.markdown('<p class="main-header">🚚 End-to-End Logistics Intelligence Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-Time Fleet & Shipment Monitoring</p>', unsafe_allow_html=True)
    
    # Generate data
    shipments_df, vehicles_df = generate_sample_data()
    
    # Sidebar
    st.sidebar.header("📊 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("Filters")
    selected_vendors = st.sidebar.multiselect(
        "Select Vendors",
        options=shipments_df['vendor_id'].unique(),
        default=shipments_df['vendor_id'].unique()
    )
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(shipments_df['shipment_date'].min().date(), shipments_df['shipment_date'].max().date()),
        min_value=shipments_df['shipment_date'].min().date(),
        max_value=shipments_df['shipment_date'].max().date()
    )
    
    # Filter data
    filtered_shipments = shipments_df[
        (shipments_df['vendor_id'].isin(selected_vendors)) &
        (shipments_df['shipment_date'].dt.date >= date_range[0]) &
        (shipments_df['shipment_date'].dt.date <= date_range[1])
    ]
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        """
        **Built for:** End-to-End Cloud Big Data Solution  
        **Technologies:** Python, Spark, ML, Cloud  
        **Features:**
        - Real-time fleet monitoring
        - Delivery predictions
        - Anomaly detection
        - Performance analytics
        """
    )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🚛 Fleet Monitoring", "📦 Delivery Analytics", "🤖 ML Predictions"])
    
    with tab1:
        st.header("Key Performance Indicators")
        
        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_shipments = len(filtered_shipments)
            st.metric(
                label="Total Shipments",
                value=f"{total_shipments:,}",
                delta=f"+{int(total_shipments * 0.12)} from last month"
            )
        
        with col2:
            on_time_pct = (filtered_shipments['on_time'] == 'Yes').sum() / len(filtered_shipments) * 100
            st.metric(
                label="On-Time Delivery %",
                value=f"{on_time_pct:.1f}%",
                delta=f"+{np.random.randint(1, 5)}% from target"
            )
        
        with col3:
            avg_rating = filtered_shipments['customer_rating'].mean()
            st.metric(
                label="Average Customer Rating",
                value=f"{avg_rating:.2f}/5.0",
                delta=f"+{np.random.uniform(0.1, 0.3):.2f}"
            )
        
        with col4:
            active_vehicles = (vehicles_df['status'] == 'Active').sum()
            st.metric(
                label="Active Vehicles",
                value=f"{active_vehicles}",
                delta=f"{(vehicles_df['status'] == 'Maintenance').sum()} in maintenance"
            )
        
        st.markdown("---")
        
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Daily Shipment Volume")
            daily_shipments = filtered_shipments.groupby(filtered_shipments['shipment_date'].dt.date).size().reset_index()
            daily_shipments.columns = ['Date', 'Shipments']
            fig = px.line(
                daily_shipments,
                x='Date',
                y='Shipments',
                title='Shipments Over Time',
                markers=True
            )
            fig.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Delivery Performance by Vendor")
            vendor_performance = filtered_shipments.groupby('vendor_id')['on_time'].apply(
                lambda x: (x == 'Yes').sum() / len(x) * 100
            ).reset_index()
            vendor_performance.columns = ['Vendor', 'On-Time %']
            fig = px.bar(
                vendor_performance,
                x='Vendor',
                y='On-Time %',
                title='On-Time Delivery Rate by Vendor',
                color='On-Time %',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Top Routes")
            top_routes = filtered_shipments.groupby(['origin', 'destination']).size().reset_index()
            top_routes.columns = ['Origin', 'Destination', 'Count']
            top_routes = top_routes.nlargest(10, 'Count')
            top_routes['Route'] = top_routes['Origin'] + ' → ' + top_routes['Destination']
            fig = px.bar(
                top_routes,
                x='Route',
                y='Count',
                title='Top 10 Busiest Routes',
                color='Count',
                color_continuous_scale='Blues'
            )
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⏱️ Delay Distribution")
            fig = px.histogram(
                filtered_shipments,
                x='actual_delay_minutes',
                title='Distribution of Delivery Delays',
                nbins=30,
                color_discrete_sequence=['#ff7f0e']
            )
            fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="On-Time")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("🚛 Real-Time Fleet Monitoring")
        
        # Fleet metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Fleet Size",
                value=len(vehicles_df),
                delta="100% operational"
            )
        
        with col2:
            avg_fuel = vehicles_df['fuel_level_percent'].mean()
            st.metric(
                label="Average Fuel Level",
                value=f"{avg_fuel:.0f}%",
                delta="Healthy"
            )
        
        with col3:
            maintenance_needed = (vehicles_df['maintenance_priority'] == 'High').sum()
            st.metric(
                label="High Priority Maintenance",
                value=maintenance_needed,
                delta=f"-{np.random.randint(1, 5)} from last week",
                delta_color="inverse"
            )
        
        with col4:
            anomalies = vehicles_df['anomaly_detected'].sum()
            st.metric(
                label="Anomalies Detected",
                value=anomalies,
                delta="AI-powered monitoring",
                delta_color="off"
            )
        
        st.markdown("---")
        
        # Fleet map
        st.subheader("📍 Live Vehicle Locations")
        fig = px.scatter_mapbox(
            vehicles_df,
            lat='latitude',
            lon='longitude',
            color='status',
            size='speed_kmh',
            hover_name='vehicle_id',
            hover_data={'latitude': False, 'longitude': False, 'speed_kmh': True, 'fuel_level_percent': True},
            color_discrete_map={'Active': 'green', 'Idle': 'orange', 'Maintenance': 'red'},
            zoom=4,
            height=500,
            title='Fleet GPS Tracking'
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)
        
        # Maintenance priority table
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Maintenance Priority Queue")
            maintenance_df = vehicles_df[['vehicle_id', 'maintenance_score', 'maintenance_priority', 'odometer_km']].copy()
            maintenance_df = maintenance_df.sort_values('maintenance_score', ascending=False).head(10)
            maintenance_df['maintenance_score'] = maintenance_df['maintenance_score'].apply(lambda x: f"{x:.2f}")
            st.dataframe(maintenance_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("⚙️ Vehicle Health Metrics")
            fig = go.Figure()
            fig.add_trace(go.Box(y=vehicles_df['engine_temp_c'], name='Engine Temp (°C)'))
            fig.add_trace(go.Box(y=vehicles_df['fuel_level_percent'], name='Fuel Level (%)'))
            fig.update_layout(title='Fleet Health Distribution', showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📦 Delivery Performance Analytics")
        
        # Performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Average Delay by Vendor")
            vendor_delay = filtered_shipments.groupby('vendor_id')['actual_delay_minutes'].mean().reset_index()
            vendor_delay.columns = ['Vendor', 'Avg Delay (min)']
            fig = px.bar(
                vendor_delay,
                x='Vendor',
                y='Avg Delay (min)',
                title='Average Delivery Delay by Vendor',
                color='Avg Delay (min)',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⭐ Customer Satisfaction")
            rating_dist = filtered_shipments.groupby(pd.cut(filtered_shipments['customer_rating'], bins=[3, 3.5, 4, 4.5, 5])).size().reset_index()
            rating_dist.columns = ['Rating Range', 'Count']
            rating_dist['Rating Range'] = rating_dist['Rating Range'].astype(str)
            fig = px.pie(
                rating_dist,
                values='Count',
                names='Rating Range',
                title='Customer Rating Distribution',
                color_discrete_sequence=px.colors.sequential.RdBu_r
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.subheader("🔍 Performance Factors Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                filtered_shipments,
                x='distance_km',
                y='actual_delay_minutes',
                color='vendor_id',
                title='Distance vs Delay',
                trendline='ols',
                hover_data=['package_weight_kg']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                filtered_shipments,
                x='package_weight_kg',
                y='actual_delay_minutes',
                color='temperature_c',
                title='Weight vs Delay (colored by temperature)',
                hover_data=['distance_km']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("🤖 Machine Learning Predictions")
        
        st.info("💡 **AI-Powered Insights:** Using Random Forest and Gradient Boosting models trained on historical data")
        
        # Prediction metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mae = np.mean(np.abs(filtered_shipments['actual_delay_minutes'] - filtered_shipments['predicted_delay_minutes']))
            st.metric(
                label="Prediction Accuracy (MAE)",
                value=f"{mae:.1f} min",
                delta="±15 min within target"
            )
        
        with col2:
            r2_score = 0.85  # Simulated R² score
            st.metric(
                label="Model R² Score",
                value=f"{r2_score:.2f}",
                delta="+0.05 from last training"
            )
        
        with col3:
            auc_score = 0.92  # Simulated AUC
            st.metric(
                label="Anomaly Detection AUC",
                value=f"{auc_score:.2f}",
                delta="Excellent performance"
            )
        
        st.markdown("---")
        
        # Prediction vs Actual
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Predicted vs Actual Delays")
            sample = filtered_shipments.sample(min(100, len(filtered_shipments)))
            fig = px.scatter(
                sample,
                x='actual_delay_minutes',
                y='predicted_delay_minutes',
                title='Prediction Accuracy Scatter Plot',
                hover_data=['shipment_id', 'vendor_id'],
                trendline='ols'
            )
            fig.add_shape(type='line', x0=sample['actual_delay_minutes'].min(), y0=sample['actual_delay_minutes'].min(),
                         x1=sample['actual_delay_minutes'].max(), y1=sample['actual_delay_minutes'].max(),
                         line=dict(color='red', dash='dash'))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚨 Anomaly Detection Results")
            anomaly_summary = vehicles_df.groupby(['status', 'anomaly_detected']).size().reset_index()
            anomaly_summary.columns = ['Status', 'Anomaly', 'Count']
            anomaly_summary['Anomaly'] = anomaly_summary['Anomaly'].map({True: 'Detected', False: 'Normal'})
            fig = px.bar(
                anomaly_summary,
                x='Status',
                y='Count',
                color='Anomaly',
                title='Anomalies by Vehicle Status',
                barmode='group',
                color_discrete_map={'Detected': 'red', 'Normal': 'green'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance (simulated)
        st.subheader("📊 Model Feature Importance")
        features = ['Distance (km)', 'Weight (kg)', 'Temperature (°C)', 'Speed (km/h)', 'Fuel Consumed']
        importance = [0.35, 0.25, 0.20, 0.12, 0.08]
        feature_df = pd.DataFrame({'Feature': features, 'Importance': importance})
        fig = px.bar(
            feature_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Top Factors Affecting Delivery Delays',
            color='Importance',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent predictions table
        st.subheader("📋 Recent Prediction Results")
        recent_predictions = filtered_shipments[['shipment_id', 'vendor_id', 'destination', 'actual_delay_minutes', 'predicted_delay_minutes', 'on_time']].copy()
        recent_predictions['Prediction Error'] = abs(recent_predictions['actual_delay_minutes'] - recent_predictions['predicted_delay_minutes'])
        recent_predictions = recent_predictions.head(10)
        st.dataframe(recent_predictions, use_container_width=True, hide_index=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p style='font-style: italic;'>Built automatically for the End-to-End Cloud Big Data Solution for Real-Time Logistics Intelligence project.</p>
            <p><strong>Technologies:</strong> Python | PySpark | Kafka | Airflow | AWS/Azure/GCP | Machine Learning</p>
            <p>📊 Dashboard auto-refreshes every 30 seconds in production mode</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
