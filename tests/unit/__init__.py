import os
import sys

# Get the parent directory of the Flask app
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = os.path.join(parent_dir, "src")
# Add the parent directory to sys.path
sys.path.insert(0, src)
