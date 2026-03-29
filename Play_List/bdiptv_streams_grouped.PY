import requests
from bs4 import BeautifulSoup
import re

# === CONFIGURATION ===
source_url = "http://tv.bdiptv.net/"
playlist_base = "http://100.100.100.4:5001/channel/"
output_file = "bdiptv_streams_grouped.txt"

# === GROUP MAPPING ===
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

# === FETCH HTML SOURCE ===
response = requests.get(source_url)
soup = BeautifulSoup(response.text, "html.parser")

# === PARSE CHANNELS ===
channels_by_group = {}
total_channels = 0

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
            input_url = f"{playlist_base}{stream_id}/playlist.m3u8"
            channels_by_group.setdefault(group_name, []).append((stream_name, input_url))
            total_channels += 1

# === WRITE TO FILE ===
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# total channels: {total_channels}\n\n")
    for group in sorted(channels_by_group):
        f.write(f"# group: {group.lower()}\n")
        for name, url in channels_by_group[group]:
            f.write(f"stream {name} {{\n")
            f.write(f"  input {url};\n")
            f.write("}\n\n")

print(f"✅ Exported {total_channels} grouped streams to {output_file}")