import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# === CONFIGURATION ===
sources = {
    "iptvidn": {
        "url": "http://iptvidn.com/",
        "playlist_bases": [
            "http://100.100.100.5:5000/channel/"
        ]
    },
    "bdiptv": {
        "url": "http://tv.bdiptv.net/",
        "playlist_bases": [
            "http://100.100.100.5:5001/channel/",
        ]
    }
}

group_map = {
    "lsports": "Live Sports",
    "sports": "Sports",
    "news": "News",
    "bangla": "Bangla",
    "hindi": "Hindi",
    "movies": "Movies",
    "music": "Music",
    "documentary": "Documentary",
    "kids": "Kids"
}

output_file = "dual_input_streams.txt"
channels_by_group = defaultdict(list)
total_channels = 0

# === PARSE EACH SOURCE ===
for source_name, config in sources.items():
    try:
        response = requests.get(config["url"])
        soup = BeautifulSoup(response.text, "html.parser")

        for div in soup.find_all("div", class_=True):
            classes = div.get("class", [])
            group_key = next((cls for cls in classes if cls in group_map), None)
            if not group_key:
                continue
            group_name = group_map[group_key]

            a_tag = div.find("a", onclick=True)
            if a_tag:
                match = re.search(r"stream=([\w\-]+)", a_tag["onclick"])
                if match:
                    stream_id = match.group(1)
                    stream_name = re.sub(r"[^\w]+", "_", stream_id).lower()
                    input_urls = [f"{base}{stream_id}/playlist.m3u8" for base in config["playlist_bases"]]
                    channels_by_group[group_name].append((stream_name, input_urls))
                    total_channels += 1
    except Exception as e:
        print(f"⚠️ Failed to parse {source_name}: {e}")

# === WRITE TO FILE ===
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# total channels: {total_channels}\n\n")
    for group in sorted(channels_by_group):
        f.write(f"# group: {group.lower()}\n")
        for name, urls in channels_by_group[group]:
            f.write(f"stream {name} {{\n")
            for url in urls:
                f.write(f"  input {url};\n")
            f.write("}\n\n")

print(f"✅ Exported {total_channels} channels with dual inputs to {output_file}")