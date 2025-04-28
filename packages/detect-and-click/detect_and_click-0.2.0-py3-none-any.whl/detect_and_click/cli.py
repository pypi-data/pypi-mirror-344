#!/usr/bin/env python3
"""
CLI-оболочка detect-and-click
"""
import argparse
from detect_and_click.clicker import DetectAndClick


def main() -> None:
    parser = argparse.ArgumentParser("detect-and-click")
    parser.add_argument("--model", type=str, help="Путь к весам best.pt (если не задано — ищем автоматически)")
    parser.add_argument("--conf", type=float, default=0.5, help="Порог уверенности YOLO")
    parser.add_argument("--delay", type=float, default=0.4, help="Задержка между кликами, сек")
    parser.add_argument("--no-display", action="store_true", help="Не показывать окно OpenCV")
    parser.add_argument("--region", type=str, help="Зона захвата: left,top,width,height")
    args = parser.parse_args()

    region = None
    if args.region:
        try:
            l, t, w, h = map(int, args.region.split(","))
            region = {"left": l, "top": t, "width": w, "height": h}
        except ValueError:
            parser.error("--region: формат left,top,width,height")

    dac = DetectAndClick(model_path=args.model, conf=args.conf, delay=args.delay)
    dac.run(display=not args.no_display, region=region)


if __name__ == "__main__":
    main()