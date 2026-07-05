"""
Global configuration for Vehicle Health AI
"""

# ----------------------------
# Vehicle Information
# ----------------------------

VEHICLE_NAME = "Virtual Electric Vehicle"

# ----------------------------
# Update Interval
# ----------------------------

UPDATE_INTERVAL = 1  # seconds

# ----------------------------
# Sensor Thresholds
# ----------------------------

MAX_ENGINE_TEMP = 110
MAX_BRAKE_TEMP = 180
MAX_RPM = 7000

MIN_BATTERY_SOC = 20
MIN_BATTERY_SOH = 70

MAX_VIBRATION = 8.0

# ----------------------------
# AI Thresholds
# ----------------------------

ANOMALY_THRESHOLD = 0.75

# ----------------------------
# Dashboard
# ----------------------------

REFRESH_RATE = 1000

# ----------------------------
# Paths
# ----------------------------

MODEL_PATH = "models/random_forest.pkl"

DATABASE_PATH = "data/history.db"

LOG_PATH = "logs/application.log"

# ----------------------------
# Edge AI Sampling Configuration
# ----------------------------

# Sensor Sampling Rate
SENSOR_RATE_HZ = 10          # 10 samples/sec
SENSOR_INTERVAL = 0.1        # 100 ms

# AI Inference
AI_RATE_HZ = 1               # Once per second
AI_INTERVAL = 1.0

# Dashboard Refresh
DASHBOARD_RATE_HZ = 1
DASHBOARD_INTERVAL = 1.0

# Number of samples to retain
MAX_HISTORY = 300

# Dataset Generation
DATASET_SIZE = 100000