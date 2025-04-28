#!/usr/bin/env python3
"""
Лёгкий детектор спинов на базе заранее обученных весов YOLOv8.
Никаких скачиваний и обучения внутри пакета!
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Dict, Union

import cv2                                    # type: ignore
import mss                                    # type: ignore
import numpy as np                             # type: ignore
from ultralytics import YOLO                  # type: ignore  # docs: https://docs.ultralytics.com/usage/python/ :contentReference[oaicite:5]{index=5}

ENV_VAR = "DETECT_AND_CLICK_MODEL_PATH"
SEARCH_DIRS = [
    Path.cwd(),
    Path.home() / ".detect_and_click" / "models",
    Path(__file__).with_suffix("").parent / "models",
]                                             # Path.home – кроссплатформенно :contentReference[oaicite:6]{index=6}


class SpinDetector:
    """Негабаритный класс-обёртка вокруг Ultralytics YOLO."""

    def __init__(self, model_path: Union[str, Path, None] = None, conf: float = 0.5) -> None:
        self.model_path = self._resolve_weights(model_path)
        self.model = YOLO(str(self.model_path))
        self.conf = conf
        with mss.mss() as sct:                # пример в документации MSS :contentReference[oaicite:7]{index=7}
            self.screen_w = sct.monitors[1]["width"]
            self.screen_h = sct.monitors[1]["height"]

    # ---------- публичное API ----------
    def detect_from_frame(self, frame: np.ndarray) -> Dict:
        """Вернуть координаты самого уверенного бокса либо `{"found": False}`."""
        res = self.model(frame, conf=self.conf)[0]
        if not res.boxes:
            return {"found": False, "timestamp": time.time()}
        box = max(res.boxes, key=lambda b: float(b.conf[0]))
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        return {
            "found": True,
            "confidence": float(box.conf[0]),
            "center_x": int((x1 + x2) / 2),
            "center_y": int((y1 + y2) / 2),
            "timestamp": time.time(),
        }

    # ---------- служебные методы ----------
    def _resolve_weights(self, path_arg: Union[str, Path, None]) -> Path:
        if path_arg:
            p = Path(path_arg)
            if p.exists():
                return p
            raise FileNotFoundError(f"Указанный файл весов не найден: {p}")

        env = os.getenv(ENV_VAR)
        if env and Path(env).exists():
            return Path(env)

        for d in SEARCH_DIRS:
            cand = d / "best.pt"
            if cand.exists():
                return cand

        search_list = "\n  - " + "\n  - ".join(map(str, SEARCH_DIRS))
        raise FileNotFoundError(
            f"Весов модели не найдено.\n"
            f"Передайте --model /path/to/best.pt, либо установите {ENV_VAR},\n"
            f"либо положите best.pt в одну из директорий:{search_list}"
        )
