
import json
from bs4 import BeautifulSoup

def inject_metadata_to_html(html_path, metadata_path):
    with open(metadata_path) as f:
        metadata = json.load(f)

    with open(html_path) as f:
        soup = BeautifulSoup(f, "html.parser")

    for script in soup.find_all("script"):
        if script.string and "fetch(" in script.string and "meta-info" in script.string:
            script.decompose()

    meta_div = soup.find("div", id="meta-info")
    if meta_div:
        meta_div.clear()
        content = f"""
<p><strong>🔍 Total available GitHub results:</strong> {metadata['total_count']}</p>
<p><strong>📦 Repositories collected:</strong> {metadata['repo_count']}</p>
<p><strong>🕒 Report generated on:</strong> {metadata['generated_at']}</p>
"""
        meta_div.append(BeautifulSoup(content, "html.parser"))

    with open(html_path, "w") as f:
        f.write(str(soup))
    print(f"✅ Updated: {html_path}")

# Inject metadata into both dashboards
inject_metadata_to_html("index.html", "subgraph_metadata.json")
inject_metadata_to_html("index2.html", "substreams_metadata.json")

