"""
Detect-and-Click: библиотека для детекции объектов на экране
и автоматического клика по ним.
"""

from .detector import SpinDetector            # noqa: F401
from .clicker import DetectAndClick           # noqa: F401

__all__ = ["SpinDetector", "DetectAndClick"]
__version__ = "0.2.0"
