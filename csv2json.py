#!/usr/bin/env python3
"""CSV → JSON 変換スクリプト。"""

import argparse
import csv
import json
import sys
from pathlib import Path


def convert(input_path: Path, output_path: Path | None = None, *, indent: int = 2) -> None:
    with open(input_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    result = json.dumps(rows, ensure_ascii=False, indent=indent)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result + "\n")
        print(f"{len(rows)} rows -> {output_path}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="CSV を JSON に変換")
    parser.add_argument("input", type=Path, help="入力 CSV ファイル")
    parser.add_argument("-o", "--output", type=Path, help="出力 JSON ファイル（省略時は stdout）")
    parser.add_argument("--indent", type=int, default=2, help="インデント幅")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"エラー: {args.input} が見つかりません", file=sys.stderr)
        sys.exit(1)

    convert(args.input, args.output, indent=args.indent)


if __name__ == "__main__":
    main()
