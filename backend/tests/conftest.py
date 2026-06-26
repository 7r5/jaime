import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# Ensure the backend package can be imported when tests run from backend/ or backend/tests/
os.environ.setdefault("PYTHONPATH", str(ROOT_DIR))
