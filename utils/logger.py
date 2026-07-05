import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/application.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("VehicleHealthAI")