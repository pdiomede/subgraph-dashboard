
import os
import shutil
from datetime import datetime, timedelta

# Function to reliably fetch GitHub owner avatar URL
def github_avatar(owner):
    return f"https://github.com/{owner}.png"

dashboard_files = ["index.html", "index2.html"]
archive_folder = "./archive"

if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)

yesterday = datetime.now() - timedelta(days=1)
date_suffix = yesterday.strftime("%m%d%Y")

for file in dashboard_files:
    if os.path.exists(file):
        archived_file_name = f"{os.path.splitext(file)[0]}_{date_suffix}.html"
        archived_path = os.path.join(archive_folder, archived_file_name)
        shutil.move(file, archived_path)
        print(f"✅ Archived {file} to {archived_path}")


import pandas as pd
import json
from datetime import datetime

# Function to generate HTML dashboard
def generate_dashboard(csv_file, metadata_file, output_file, dashboard_title, dashboard, other, other_dashboard_link):
    df = pd.read_csv(csv_file)
    df.sort_values(by="stars", ascending=False, inplace=True)

    # Load metadata
    with open(metadata_file) as f:
        metadata = json.load(f)

    # HTML and JavaScript template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{dashboard_title}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
        <script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.8/js/dataTables.bootstrap5.min.js"></script>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap5.min.css">

        <style>
            .toggle-btn {{
                position: absolute;
                top: 20px;
                right: 20px;
                background-color: #444;
                color: #fff;
                padding: 8px 12px;
                border-radius: 20px;
                cursor: pointer;
                box-shadow: 0 3px 6px rgba(0,0,0,0.3);
                user-select: none;
            }}
            .toggle-btn:hover {{
                background-color: #555;
            }}

            /* Custom Table Borders */
            .table-bordered-custom {{
                border: 2px solid #4a90e2; /* Border color and width */
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}

            .table-bordered-custom th,
            .table-bordered-custom td {{
                border-bottom: 1px solid #555;
            }}

            .table-bordered-custom th {{
                background-color: #333;
            }}

            body.bg-light .table-bordered-custom {{
                border-color: #4a90e2;
            }}

            body.bg-light .table-bordered-custom th {{
                background-color: #ddd;
                color: #222;
            }}

            body.bg-light .table-bordered-custom td {{
                color: #333;
                background-color: #fff;
            }}
        </style>

        <script>
            function toggleTheme() {{
                const body = document.body;
                const table = document.getElementById('dashboard');

                if (body.classList.contains('bg-dark')) {{
                    body.classList.replace('bg-dark', 'bg-light');
                    body.classList.replace('text-white', 'text-dark');
                    table.classList.replace('table-dark', 'table-light');
                }} else {{
                    body.classList.replace('bg-light', 'bg-dark');
                    body.classList.replace('text-dark', 'text-white');
                    table.classList.replace('table-light', 'table-dark');
                }}
            }}
        </script>

    </head>
    
    <body class="bg-dark text-white">
        <div class="toggle-btn" onclick="toggleTheme()">🌓<span style="margin-left: 10px; font-size: 14px; color: #aaa;">v1.0.2</span></div>

        <div class="container py-4 position-relative">
            <h1 class="display-5 fw-bold text-center">{dashboard_title}</h1>

            <p class="text-start mt-4">This is the list of GitHub repositories using {dashboard}, for {other} click 
            <a href="{other_dashboard_link}" class="text-decoration-none text-info">here</a>.
            
            <br/>
            Excluding:
            <img src="https://avatars.githubusercontent.com/graphprotocol" alt="graphprotocol" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;">
            <a href="https://github.com/graphprotocol" target="_blank">graphprotocol</a>, 
            <img src="https://avatars.githubusercontent.com/edgeandnode" alt="edgeandnode" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;">
            <a href="https://github.com/edgeandnode" target="_blank">edgeandnode</a>, 
            <img src="https://avatars.githubusercontent.com/streamingfast" alt="streamingfast" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;">
            <a href="https://github.com/streamingfast" target="_blank">streamingfast</a>, 
            <img src="https://avatars.githubusercontent.com/pinax-network" alt="pinax" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;">
            <a href="https://github.com/pinax-network" target="_blank">pinax</a>, 
            <img src="https://avatars.githubusercontent.com/graphops" alt="graphops" style="width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;">
            <a href="https://github.com/graphops" target="_blank">graphops</a>.
            
            </p>

            <div class="text-start mb-3">
                🔍 Total available GitHub results: {metadata['total_count']}<br>
                📦 Repositories collected: {metadata['repo_count']}<br>
                🕒 Report generated on: {metadata['generated_at']}
            </div>

            <table id="dashboard" class="table table-dark table-striped table-hover table-bordered-custom" style="width:100%">
                <thead>
                    <tr>
                        <th>Repository</th>
                        <th>Owner</th>
                        <th>Stars</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                
                <tbody>
                    {''.join(f"""
                    <tr>
                        <td>
                            <a href='{row['url']}' class='text-info' target='_blank'>🔗 {row['repository']}</a>
                        </td>
                        <td>
                            <img src='{github_avatar(row['owner'])}' alt='{row['owner']}' style='width:24px;height:24px;border-radius:50%;vertical-align:middle;margin-right:6px;'>
                            <a href='https://github.com/{row['owner']}' target='_blank'>{row['owner']}</a>
                        </td>
                        <td>{row['stars']}</td>
                        <td>{row['last_updated']}</td>
                    </tr>
                    """ for index, row in df.iterrows())}
                </tbody>

            </table>
        </div>
        <script>
            $(document).ready(function() {{
                $('#dashboard').DataTable({{
                    paging: true,
                    pageLength: 50,
                    lengthChange: false,
                    searching: true,
                    ordering: true,
                    order: [[2, 'desc']]
                }});
            }});
        </script>
    </body>
    </html>
    """

    # Write HTML content to file
    with open(output_file, "w") as file:
        file.write(html_content)

# Generate dashboards
generate_dashboard("subgraph_repositories_filtered.csv", "subgraph_metadata.json", "index.html", "Subgraphs Dashboard", "Subgraphs","Substreams","index2.html")
generate_dashboard("substreams_repositories_filtered.csv", "substreams_metadata.json", "index2.html", "Substreams Dashboard", "Substreams", "Subgraphs", "index.html")
