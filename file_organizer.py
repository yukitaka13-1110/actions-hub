#!/usr/bin/env python3
"""ファイルを拡張子ごとにサブディレクトリに整理するスクリプト。"""

import argparse
import shutil
import sys
from pathlib import Path

# 拡張子 → カテゴリ
CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"},
    "archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "others"


def organize(target_dir: Path, *, dry_run: bool = False) -> None:
    if not target_dir.is_dir():
        print(f"エラー: {target_dir} はディレクトリではありません", file=sys.stderr)
        sys.exit(1)

    moved = 0
    for file in target_dir.iterdir():
        if file.is_dir() or file.name.startswith("."):
            continue

        category = get_category(file.suffix)
        dest_dir = target_dir / category
        dest = dest_dir / file.name

        if dry_run:
            print(f"  {file.name} -> {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest))
            print(f"  {file.name} -> {category}/")
        moved += 1

    print(f"\n{moved} files {'would be ' if dry_run else ''}organized.")


def main():
    parser = argparse.ArgumentParser(description="ファイルを拡張子ごとに整理")
    parser.add_argument("directory", type=Path, help="整理対象のディレクトリ")
    parser.add_argument("--dry-run", action="store_true", help="実際には移動せず確認のみ")
    args = parser.parse_args()

    organize(args.directory, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
