#!/usr/bin/env python3
# Requires: Python 3.9+
"""
检查 Markdown 文档中的内部链接是否有效
"""
from __future__ import annotations

import re
import argparse
from pathlib import Path


def extract_links(markdown_file: Path) -> list[tuple[str, str]]:
    """提取 Markdown 文件中的所有链接"""
    content = markdown_file.read_text(encoding="utf-8")
    # 匹配 [text](path) 格式的链接
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, content)


def check_link(link: str, base_dir: Path) -> bool:
    """检查链接是否有效"""
    # 移除锚点
    path = link.split("#")[0]
    if not path or path.startswith("http"):
        return True

    target = base_dir / path
    return target.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description="检查 Markdown 文档中的内部链接")
    parser.add_argument("docs_dir", type=Path, help="文档目录")
    args = parser.parse_args()

    docs_dir = args.docs_dir
    if not docs_dir.exists():
        print(f"❌ 目录不存在: {docs_dir}")
        exit(1)

    all_links_ok = True

    for md_file in docs_dir.rglob("*.md"):
        links = extract_links(md_file)
        for text, link in links:
            if not check_link(link, md_file.parent):
                print(f"❌ {md_file.relative_to(docs_dir)}: [{text}]({link})")
                all_links_ok = False

    if all_links_ok:
        print("✅ 所有链接检查通过")
    else:
        exit(1)


if __name__ == "__main__":
    main()
