"""
MyoVerse - The AI toolkit for myocontrol research

MyoVerse is a cutting-edge research companion for unlocking the secrets hidden within 
biomechanical data. It's specifically designed for exploring the complex interplay 
between electromyography (EMG) signals, kinematics (movement), and kinetics (forces).

Leveraging PyTorch and PyTorch Lightning, MyoVerse provides:
- Data loaders and preprocessing filters tailored for biomechanical signals
- Peer-reviewed AI models and components for analysis and prediction tasks
- Essential utilities to streamline the research workflow

MyoVerse aims to accelerate research in predicting movement from muscle activity, 
analyzing forces during motion, and developing novel AI approaches for biomechanical challenges.

Note: MyoVerse is built for research and is continuously evolving.
"""

from icecream import install, ic
import datetime
import importlib.metadata
import os
import toml

# Try multiple methods to get the version
try:
    # Method 1: Try to read from pyproject.toml first
    package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pyproject_path = os.path.join(package_root, "pyproject.toml")
    
    if os.path.exists(pyproject_path):
        pyproject_data = toml.load(pyproject_path)
        __version__ = pyproject_data.get("project", {}).get("version", "unknown")
    
    # Method 2: If that fails or version is still unknown, try importlib.metadata
    if __version__ == "unknown":
        __version__ = importlib.metadata.version("MyoVerse")
        
except Exception:
    # If all methods fail, we at least have a default
    __version__ = "unknown"

install()


# Define a function to generate a prefix with ISO timestamp
def timestamp_prefix():
    timestamp = datetime.datetime.now().isoformat(timespec="milliseconds")
    return f"{timestamp} | MyoVerse {__version__} | "


# Configure IceCream to use the timestamp prefix function
ic.configureOutput(includeContext=True, prefix=timestamp_prefix)
