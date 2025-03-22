import pandas as pd
from datetime import datetime, timezone

# Read CSV files
subgraph_df = pd.read_csv("subgraph_repositories_filtered.csv")
substreams_df = pd.read_csv("substreams_repositories_filtered.csv")

def generate_table_rows(df):
    rows = []
    for _, row in df.iterrows():
        owner = row["owner"]
        avatar = f"https://avatars.githubusercontent.com/{owner}"
        row_html = f"""
        <tr>
            <td><a href="{row['url']}" target="_blank">{row['repository']}</a></td>
            <td><a href="https://github.com/{owner}" target="_blank">
                <img src="{avatar}" alt="{owner}" style="width:20px; vertical-align:middle; border-radius:50%;"/> {owner}
            </a></td>
            <td>{row['stars']}</td>
            <td>{row['last_updated']}</td>
        </tr>"""
        rows.append(row_html)
    return "\n".join(rows)

# Metadata
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# Template parts
pre_tbody = r"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Subgraph Dashboard</title>
<link href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css" rel="stylesheet"/>
<style>
    body {
      font-family: Arial, sans-serif;
      margin: 40px;
      background-color: #121212;
      color: #f0f0f0;
    }
    a {
      color: #4ea1ff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .light-mode {
      background-color: #ffffff;
      color: #000000;
    }
    .toggle-btn {
      position: absolute;
      top: 20px;
      right: 40px;
      cursor: pointer;
    }
    table img {
      vertical-align: middle;
      border-radius: 50%;
      width: 20px;
      margin-right: 8px;
    }
    .meta {
      margin-bottom: 20px;
    }
  </style>
<style>
table.datatable {
  border: 2px solid #4ea1ff;
  border-radius: 8px;
  overflow: hidden;
}
table.datatable thead {
  background-color: #1e1e1e;
}
table.datatable th, table.datatable td {
  border-bottom: 1px solid #333;
  padding: 12px;
}
</style>
<style>
  thead th.sortable::after {
    content: " ⇅";
    font-size: 12px;
    color: #888;
  }
  body.light-mode table.datatable thead {
    background-color: #e0e0e0 !important;
    color: #000 !important;
  }
</style>
</head>
<body>
<h1>Subgraph Dashboard</h1>

  <p class="description">This is the list of GitHub repositories using Subgraphs. Excluding: <img src="https://avatars.githubusercontent.com/graphprotocol" alt="graphprotocol" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;"> <a href="https://github.com/graphprotocol" target="_blank">graphprotocol</a>, <img src="https://avatars.githubusercontent.com/edgeandnode" alt="edgeandnode" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;"> <a href="https://github.com/edgeandnode" target="_blank">edgeandnode</a>, <img src="https://avatars.githubusercontent.com/streamingfast" alt="streamingfast" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;"> <a href="https://github.com/streamingfast" target="_blank">streamingfast</a>, <img src="https://avatars.githubusercontent.com/graphops" alt="graphops" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;"> <a href="https://github.com/graphops" target="_blank">graphops</a>.</p>

<a href="index2.html">→ You can access here the Substreams Dashboard</a>
<div class="toggle-btn" onclick="toggleTheme()">🌓<span style="margin-left: 10px; font-size: 14px; color: #aaa;">v1.0.1</span></div>
<div class="meta" id="meta-info">
<p><strong>🔍 Total available GitHub results:</strong> 3808</p>
<p><strong>📦 Repositories collected:</strong> 460</p>
<p><strong>🕒 Report generated on:</strong> 2025-03-22 14:14:14 UTC</p>
</div>
<table class="datatable datatable" id="table">
<thead>
<tr>
<th>repository</th>
<th>owner</th>
<th>stars</th>
<th>last updated</th>
</tr>
</thead>"""
post_tbody = r"""</table>
<script defer="" src="https://cdn.jsdelivr.net/npm/simple-datatables@latest"></script>
<script defer="" src="https://cdn.jsdelivr.net/npm/simple-datatables@latest"></script>
<script>
  window.addEventListener("load", function () {
    const table = document.querySelector("#table");
    if (table) {
      new simpleDatatables.DataTable(table, {
        perPage: 50,
        searchable: true,
        sortable: true,
        fixedHeight: true,
        labels: {
          placeholder: "🔍 Search...",
          perPage: "",
        },
      });
    }
  });

  function toggleTheme() {
    document.body.classList.toggle("light-mode");
  }
</script>

<script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" defer></script>
<script>
  window.addEventListener("DOMContentLoaded", () => {
    const table = document.querySelector("#table");
    new simpleDatatables.DataTable(table, {
      perPage: 50,          // 👈 Show 50 rows per page
      perPageSelect: false  // 👈 Hide the dropdown
    });
  });
</script>


</body>
</html>"""

# Generate both files
def write_dashboard(df, output_path, total_results):
    html_rows = generate_table_rows(df)
    html = f"{pre_tbody}<tbody>{html_rows}</tbody>{post_tbody}"
    html = html.replace("3808", str(total_results))
    html = html.replace("460", str(len(df)))
    html = html.replace("2025-03-22 14:14:14 UTC", now)
    with open(output_path, "w") as f:
        f.write(html)

write_dashboard(subgraph_df, "index.html", total_results=3808)
write_dashboard(substreams_df, "index2.html", total_results=526)
