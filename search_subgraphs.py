import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from collections import Counter

# Load GitHub token from .env
load_dotenv()
GITHUB_TOKEN="your_github_token_here"

if not GITHUB_TOKEN:
    raise EnvironmentError("❌ GITHUB_TOKEN not found. Please set it in your .env file.")

# GitHub REST API URL
SEARCH_URL = "https://api.github.com/search/code"

# Search query
QUERY = (
    "filename:subgraph.yaml OR filename:subgraph.yml "
    "-org:graphprotocol -org:graphops -org:edgeandnode"
)

# Headers
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def search_repositories(query, per_page=100, max_pages=10):
    repo_info = {}

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "per_page": per_page,
            "page": page
        }

        print(f"🔎 Fetching page {page}...")
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)

        if response.status_code == 403:
            print("⏳ Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            continue
        elif response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            break

        items = response.json().get("items", [])
        if not items:
            break

        for item in items:
            repo = item["repository"]
            full_name = repo["full_name"]

            if full_name not in repo_info:
                repo_info[full_name] = {
                    "repository": full_name,
                    "url": repo["html_url"],
                    "owner": repo["owner"]["login"],
                    "description": repo.get("description", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "last_updated": repo.get("pushed_at", "")
                }

        if len(items) < per_page:
            break

        time.sleep(1)

    return list(repo_info.values())

if __name__ == "__main__":
    repo_data = search_repositories(QUERY, per_page=100, max_pages=10)

    df = pd.DataFrame(repo_data)

    # Sort and parse date
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors='coerce')
    df = df.sort_values(by="last_updated", ascending=False)

    # Save CSV for dashboard
    output_path = "subgraph_repositories_filtered.csv"
    df.to_csv(output_path, index=False, columns=[
        "repository", "url", "owner", "description", "stars", "last_updated"
    ])

    # Report summary for console/log
    total = len(df)
    last_update = df["last_updated"].max()
    contributors = Counter(df["owner"])
    top_contributors = contributors.most_common(10)

    print(f"\n✅ Done. Total unique repositories: {total}")
    print(f"📄 Full list saved to: {output_path}")
    print(f"🕒 Last updated repository at: {last_update}")
    print("\n🌟 Top 10 Contributors:")
    for rank, (owner, count) in enumerate(top_contributors, 1):
        print(f"{rank}. {owner} — {count} repos")

    # Optionally export top contributors to JSON if needed
    top_path = "top_contributors.json"
    pd.DataFrame(top_contributors, columns=["owner", "repo_count"]).to_json(top_path, orient="records", indent=2)
    print(f"📁 Contributor summary saved to: {top_path}")
