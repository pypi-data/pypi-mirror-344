#!/usr/bin/env python3
"""
Модуль объединяет детектор и автокликер.
"""
from __future__ import annotations

import sys
import time
from typing import Dict, Optional

import cv2                                    # type: ignore
import mss                                    # type: ignore
from .detector import SpinDetector

# pyautogui — опциональная зависимость
try:
    import pyautogui                          # type: ignore  # docs: https://pyautogui.readthedocs.io
    HAS_AUTOGUI = True
    PYA_SIZE = pyautogui.size()
except ImportError:
    HAS_AUTOGUI = False
    PYA_SIZE = (0, 0)


class DetectAndClick:
    """Класс-фасад: цикл захвата, детекции и клика."""

    def __init__(self, model_path: Optional[str] = None, conf: float = 0.5, delay: float = 0.4) -> None:
        self.detector = SpinDetector(model_path, conf)
        self.delay = delay
        self.last_click = 0.0
        self.scale = self._calc_scale()

    # ---------- основной цикл ----------
    def run(self, display: bool = True, region: Optional[Dict] = None) -> None:
        print("Press Q to quit. Auto-clicking is always enabled.")
        with mss.mss() as sct:
            monitor = region or sct.monitors[1]
            while True:
                frame = self._grab_frame(sct, monitor)
                coords = self.detector.detect_from_frame(frame)
                if coords["found"]:
                    self._maybe_click(coords)
                if display:
                    self._display(frame, coords)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        cv2.destroyAllWindows()

    # ---------- вспомогательные ----------
    def _calc_scale(self) -> float:
        with mss.mss() as sct:
            w_mss, h_mss = sct.monitors[1]["width"], sct.monitors[1]["height"]
        if not HAS_AUTOGUI:
            return 1.0
        w, h = PYA_SIZE
        return (w / w_mss + h / h_mss) / 2

    def _grab_frame(self, sct: "mss.mss", monitor: Dict) -> "np.ndarray":  # noqa: F821
        import numpy as np
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def _maybe_click(self, c: Dict) -> None:
        if not HAS_AUTOGUI or time.time() - self.last_click < self.delay:
            return
        x = int(c["center_x"] * self.scale)
        y = int(c["center_y"] * self.scale)
        try:
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.click()
            self.last_click = time.time()
            print(f"\rClicked at ({x},{y})     ", end="")
        except Exception as exc:   # pylint: disable=broad-except
            print(f"\n⚠️  Click failed: {exc}")

    def _display(self, frame, c: Dict) -> None:
        if c.get("found"):
            cv2.drawMarker(frame, (c["center_x"], c["center_y"]), (0, 255, 255), cv2.MARKER_CROSS, 20, 2)
        cv2.imshow("Detect-and-Click", frame)