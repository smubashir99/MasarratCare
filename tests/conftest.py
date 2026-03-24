import sys
import os

# backend folder ko path mein add karo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# tests ke liye DB initialize karo
from db import init_db
init_db()