"""
Простейший юнит-тест (запуск: pytest -q)
"""
import numpy as np
from detect_and_click.detector import SpinDetector


def test_detector_no_weights(tmp_path):
    # создаём заглушку весов (модель загружать не будем)
    dummy = tmp_path / "best.pt"
    dummy.touch()
    det = SpinDetector(model_path=dummy, conf=0.01)
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    out = det.detect_from_frame(frame)
    assert "found" in out
