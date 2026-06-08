#!/usr/bin/env python3
"""
在合并后的 e.xml 里为频道追加 display-name 别名，
使播放器显示名（如 CCTV1综合）能匹配 EPG 节目单。

用法: python3 assets/epg_aliases.py e.xml
"""
import sys
import xml.etree.ElementTree as ET

# 格式: EPG 主名 -> [播放器里常见的别名]
ALIASES = {
    "CCTV1": ["CCTV1综合", "CCTV-1综合", "CCTV-1 综合", "CCTV-1", "cctv1"],
    "CCTV2": ["CCTV2财经", "CCTV-2财经", "CCTV-2", "cctv2"],
    "CCTV3": ["CCTV3综艺", "CCTV-3综艺", "CCTV-3", "cctv3"],
    "CCTV4": ["CCTV4中文国际", "CCTV4中文", "CCTV-4中文", "CCTV-4", "cctv4"],
    "CCTV5": ["CCTV5体育", "CCTV-5体育", "CCTV-5", "cctv5"],
    "CCTV5+": ["CCTV5+体育赛事", "CCTV+5+体育", "CCTV5PLUS", "CCTV5plus", "cctv5+"],
    "CCTV6": ["CCTV6电影", "CCTV-6电影", "CCTV-6", "cctv6"],
    "CCTV7": ["CCTV7国防", "CCTV7国防军事", "CCTV-7", "cctv7"],
    "CCTV8": ["CCTV8剧集", "CCTV8电视剧", "CCTV-8", "cctv8"],
    "CCTV9": ["CCTV9纪录", "CCTV-9", "cctv9"],
    "CCTV10": ["CCTV10科教", "CCTV-10科教", "CCTV-10", "cctv10"],
    "CCTV11": ["CCTV11戏曲", "CCTV-11戏曲", "CCTV-11", "cctv11"],
    "CCTV12": ["CCTV12社会", "CCTV12社会与法", "CCTV-12", "cctv12"],
    "CCTV13": ["CCTV13新闻", "CCTV-13新闻", "CCTV-13", "cctv13"],
    "CCTV14": ["CCTV14少儿", "CCTV-14少儿", "CCTV-14", "cctv14"],
    "CCTV15": ["CCTV15音乐", "CCTV-15音乐", "CCTV-15", "cctv15"],
    "CCTV16": ["CCTV16奥林", "CCTV16奥林匹克", "CCTV-16", "cctv16"],
    "CCTV17": ["CCTV17农业", "CCTV17农业农村", "CCTV-17", "cctv17"],
    "CCTV4欧洲": ["CCTV4EUO", "CCTV-4欧洲"],
    "CCTV4EUO": ["CCTV4欧洲", "CCTV-4欧洲"],
    "CCTV4AME": ["CCTV4美洲", "CCTV-4美洲"],
    "CCTV4美洲": ["CCTV4AME", "CCTV-4美洲"],
}

def add_aliases(path: str) -> int:
    tree = ET.parse(path)
    root = tree.getroot()
    added = 0

    for channel in root.findall("channel"):
        existing = {
            (dn.text or "").strip()
            for dn in channel.findall("display-name")
            if dn.text and dn.text.strip()
        }
        if not existing:
            continue

        new_names = set()
        for name in existing:
            for alias in ALIASES.get(name, []):
                if alias and alias not in existing:
                    new_names.add(alias)

        for alias in sorted(new_names):
            elem = ET.SubElement(channel, "display-name")
            elem.set("lang", "zh")
            elem.text = alias
            existing.add(alias)
            added += 1

    ET.register_namespace("", "")
    tree.write(path, encoding="UTF-8", xml_declaration=True)
    return added

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} e.xml", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    count = add_aliases(target)
    print(f"已为 e.xml 追加 {count} 个 display-name 别名")
