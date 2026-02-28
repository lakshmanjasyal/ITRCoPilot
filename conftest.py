"""Pytest configuration and fixtures for ksum project."""
import sys
from pathlib import Path

# Add backend to path for all tests
backend_path = Path(__file__).parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))
