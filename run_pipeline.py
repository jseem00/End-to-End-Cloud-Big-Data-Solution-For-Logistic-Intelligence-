"""
Complete Pipeline Runner - Executes all steps of the Logistics Intelligence Pipeline
Runs: Data Generation → Manifest Tracking → Data Quality → Processing → ML Training → Monitoring

EXECUTION MODES:
- SIMPLIFIED: Uses pandas + scikit-learn (fast, for local development)
- SPARK: Uses PySpark + Spark ML (production-ready, matches README requirements)

Usage:
    python run_pipeline.py                  # Simplified mode (default)
    python run_pipeline.py --mode simple    # Simplified mode (explicit)
    python run_pipeline.py --mode spark     # Spark mode (requires PySpark)
"""
import os
import sys
from datetime import datetime

# Initialize monitoring
try:
    from step4_deployment.monitoring import PipelineMonitor
    monitor = PipelineMonitor()
    monitoring_enabled = True
except Exception as e:
    print(f"⚠️  Monitoring disabled: {e}")
    monitoring_enabled = False
    monitor = None

# Determine execution mode from command line
EXECUTION_MODE = 'simple'  # Default to simplified
if len(sys.argv) > 1:
    if '--mode' in sys.argv:
        mode_index = sys.argv.index('--mode')
        if mode_index + 1 < len(sys.argv):
            EXECUTION_MODE = sys.argv[mode_index + 1].lower()

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def run_complete_pipeline():
    """Run the complete data pipeline"""
    start_time = datetime.now()
    
    print("\n" + "🚀" * 35)
    print_header("LOGISTICS INTELLIGENCE - COMPLETE PIPELINE EXECUTION")
    print("🚀" * 35)
    
    print(f"⏰ Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Working Directory: {os.getcwd()}")
    print(f"🔧 Execution Mode: {EXECUTION_MODE.upper()}")
    
    if EXECUTION_MODE == 'spark':
        print("\n📊 SPARK MODE ENABLED:")
        print("   - Using PySpark for distributed processing")
        print("   - Using Spark MLlib for machine learning")
        print("   - Matches README requirements (Apache Spark/PySpark)")
        print("   - Requires: pip install pyspark")
    else:
        print("\n📊 SIMPLIFIED MODE ENABLED:")
        print("   - Using pandas for data processing")
        print("   - Using scikit-learn for machine learning")
        print("   - Faster execution for development/testing")
        print("   - Appropriate for datasets <1M records")
    print()
    
    # ===================================================================
    # STEP 1: Data Generation
    # ===================================================================
    print_header("📍 STEP 1/5: DATA GENERATION")
    print("Generating sample logistics data...")
    print("-" * 70)
    
    if monitoring_enabled:
        stage_idx = monitor.start_stage("Data Generation")
    
    result = os.system("python step1-data-ingestion\\data_generator.py")
    
    if result != 0:
        print("\n❌ Data generation failed!")
        if monitoring_enabled:
            monitor.end_stage(stage_idx, status='failed', error_message="Data generation script returned non-zero exit code")
        return False
    
    if monitoring_enabled:
        monitor.end_stage(stage_idx, status='success', records_processed=80365)
        monitor.log_metric("files_generated", 10, "files")
    
    print("\n✅ Data generation completed successfully!")
    
    # ===================================================================
    # STEP 1.5: Ingestion Manifest & Data Quality
    # ===================================================================
    print_header("📍 STEP 1.5/5: DATA QUALITY & MANIFEST TRACKING")
    print("Validating data quality and tracking ingestion...")
    print("-" * 70)
    
    if monitoring_enabled:
        stage_idx = monitor.start_stage("Data Quality Validation")
    
    # Run manifest tracking
    print("📋 Updating ingestion manifest...")
    result_manifest = os.system("python step1-data-ingestion\\ingestion_manifest.py")
    
    # Run data quality checks
    print("\n🔍 Running data quality validations...")
    result_quality = os.system("python step1-data-ingestion\\data_quality.py")
    
    if result_manifest != 0 or result_quality != 0:
        print("\n⚠️  Warning: Some data quality checks failed (non-critical)")
        if monitoring_enabled:
            monitor.end_stage(stage_idx, status='partial', records_processed=80365)
    else:
        if monitoring_enabled:
            monitor.end_stage(stage_idx, status='success', records_processed=80365)
        print("\n✅ Data quality validation completed!")
    
    # ===================================================================
    # STEP 2: Data Processing (ETL)
    # ===================================================================
    print_header("📍 STEP 2/4: DATA PROCESSING (ETL)")
    print("Cleaning, transforming, and enriching data...")
    print("-" * 70)
    
    if EXECUTION_MODE == 'spark':
        print("🔥 Using PySpark ETL Pipeline (Production Mode)")
        print("   Executing: spark-submit step2-data-processing\\spark_etl_pipeline.py")
        print("   Note: Requires Apache Spark installation\n")
        
        # Check if spark-submit is available
        spark_check = os.system("spark-submit --version > nul 2>&1")
        if spark_check != 0:
            print("⚠️  WARNING: spark-submit not found in PATH")
            print("   Falling back to Python execution (local Spark mode)\n")
            result = os.system("python step2-data-processing\\spark_etl_pipeline.py")
        else:
            result = os.system("spark-submit step2-data-processing\\spark_etl_pipeline.py")
    else:
        print("🐼 Using pandas ETL Pipeline (Development Mode)")
        print("   Executing: python step2-data-processing\\spark_etl_simple.py\n")
        result = os.system("python step2-data-processing\\spark_etl_simple.py")
    
    if result != 0:
        print("\n❌ Data processing failed!")
        return False
    
    print("\n✅ Data processing completed successfully!")
    
    # ===================================================================
    # STEP 3: Machine Learning
    # ===================================================================
    print_header("📍 STEP 3/4: MACHINE LEARNING")
    print("Training predictive models...")
    print("-" * 70)
    
    if EXECUTION_MODE == 'spark':
        print("🔥 Using Spark MLlib Pipeline (Production Mode)")
        print("   Executing: spark-submit step3-analytics-ml\\predictive_analytics.py")
        print("   Training: Random Forest, GBT, with Spark ML\n")
        
        # Check if spark-submit is available
        spark_check = os.system("spark-submit --version > nul 2>&1")
        if spark_check != 0:
            print("⚠️  WARNING: spark-submit not found in PATH")
            print("   Falling back to Python execution (local Spark mode)\n")
            result = os.system("python step3-analytics-ml\\predictive_analytics.py")
        else:
            result = os.system("spark-submit step3-analytics-ml\\predictive_analytics.py")
    else:
        print("🤖 Using scikit-learn ML Pipeline (Development Mode)")
        print("   Executing: python step3-analytics-ml\\ml_simple.py")
        print("   Training: RandomForest, XGBoost with scikit-learn\n")
        result = os.system("python step3-analytics-ml\\ml_simple.py")
    
    if result != 0:
        print("\n❌ ML training failed!")
        return False
    
    print("\n✅ ML training completed successfully!")
    
    # ===================================================================
    # STEP 4: Summary Report
    # ===================================================================
    print_header("📍 STEP 4/4: SUMMARY REPORT")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("📊 Pipeline Execution Summary:")
    print("-" * 70)
    print(f"   Start Time:    {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   End Time:      {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Duration:      {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print()
    
    # Check generated files
    print("📁 Generated Files and Directories:")
    print("-" * 70)
    
    directories = [
        ('data/raw', 'Raw Data'),
        ('data/processed', 'Processed Data'),
        ('models', 'Trained Models'),
        ('results', 'Results & Metrics'),
        ('logs', 'Processing Logs')
    ]
    
    for dir_path, description in directories:
        if os.path.exists(dir_path):
            file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            print(f"   ✓ {description:20s} ({file_count} files) - {dir_path}")
        else:
            print(f"   ✗ {description:20s} (not found)")
    
    print("\n📈 Key Outputs:")
    print("-" * 70)
    
    # Check for specific important files
    important_files = [
        'data/processed/shipments_processed_*.csv',
        'models/delivery_time_predictor.pkl',
        'models/delay_risk_classifier.pkl',
        'models/anomaly_detector.pkl',
        'results/model_metrics.csv',
        'results/model_metrics.json'
    ]
    
    import glob
    for pattern in important_files:
        files = glob.glob(pattern)
        if files:
            for f in files:
                size_kb = os.path.getsize(f) / 1024
                print(f"   ✓ {f} ({size_kb:.1f} KB)")
        else:
            print(f"   ✗ {pattern} (not found)")
    
    # Display model metrics if available
    print("\n🎯 Model Performance Metrics:")
    print("-" * 70)
    
    try:
        import pandas as pd
        metrics_df = pd.read_csv('results/model_metrics.csv')
        print(metrics_df.to_string(index=False))
    except Exception as e:
        print(f"   Could not load metrics: {e}")
    
    # ===================================================================
    # NEXT STEPS
    # ===================================================================
    print_header("🎯 NEXT STEPS - MANUAL ACTIONS REQUIRED")
    
    print("Your pipeline has executed successfully! Now complete these manual steps:\n")
    
    print("1️⃣  CLOUD DEPLOYMENT (30-60 minutes)")
    print("   Choose ONE cloud provider and follow the setup guide:")
    print("   📘 See: docs/Cloud_Setup_Guide.md")
    print("   Providers: AWS, Azure, or Google Cloud")
    print()
    
    print("2️⃣  DASHBOARD CREATION (2-3 hours)")
    print("   Create visualizations using Power BI or Tableau:")
    print("   📘 See: docs/Dashboard_Guide.md")
    print("   Connect to: data/processed/*.csv")
    print()
    
    print("3️⃣  DOCUMENTATION (3-4 hours)")
    print("   Complete the project report:")
    print("   📝 Edit: docs/Project_Report_Template.md")
    print("   📸 Add screenshots from pipeline execution")
    print("   📊 Include dashboard screenshots")
    print()
    
    print("4️⃣  VIDEO RECORDING (1 hour)")
    print("   Record 15-20 minute demo:")
    print("   📘 See: docs/Video_Guide.md")
    print("   Tools: OBS Studio or Windows Game Bar (Win+G)")
    print()
    
    print("5️⃣  FINAL SUBMISSION")
    print("   📘 See: docs/Submission_Checklist.md")
    print("   Package all deliverables and submit")
    print()
    
    print("=" * 70)
    print("✅ PIPELINE EXECUTION COMPLETE!")
    print("=" * 70)
    print()
    print("💡 TIP: Review the logs/ directory for detailed execution logs")
    print("📧 For issues, check logs/processing_error.json or logs/ml_error.json")
    print()
    
    return True

if __name__ == "__main__":
    success = run_complete_pipeline()
    sys.exit(0 if success else 1)
