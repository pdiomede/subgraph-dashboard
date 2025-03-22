# 📊 Subgraph & Substreams GitHub Dashboard

This repository contains a Python script and interactive dashboards that track the adoption of Subgraphs (`subgraph.yaml` / `subgraph.yml`) and Substreams (`substreams.yaml` / `substreams.yml`) across GitHub.

---

## 🚀 Live Dashboards

Explore the dashboards online:

- **[Subgraphs Dashboard](https://subgraph-dashboard.vercel.app)**
- **[Substreams Dashboard](https://subgraph-dashboard.vercel.app/index2.html)**

*Dashboards update daily.*

---

## 🔧 Technologies

- Python 3
- GitHub REST API
- `dotenv` for environment variable management
- `pandas` for CSV processing
- HTML + JavaScript for dashboard
- Cron for scheduled automation

---


## 🧪 How to Run Locally

1. Clone the repository:

   ```bash
   git clone git@github.com:pdiomede/subgraph-dashboard.git
   cd subgraph-dashboard
   ```

2. Create a `.env` file and add your GitHub token:

   ```env
   GITHUB_TOKEN=your_github_token_here
   ```

3. Run the script manually:

   ```bash
   python3 search_subgraphs_clean.py
   ```

4. Open `index.html` in a browser to explore the dashboard.

---

## ⚙️ Automating with Cron (macOS / Linux)

To keep your dashboard updated **automatically every day**, use a cron job.

### 🔹 Step 1: Create a Shell Script

In the root of your project folder, create a file named `update_and_push.sh`:

```bash
#!/bin/bash

cd /Users/pdiomede/Desktop/phython  # <-- update to your actual project path

# Run the data collection script
python3 search_subgraphs_clean.py

# Add and commit only if changes exist
git add subgraph_repositories_filtered.csv top_contributors.json
git commit -m "🔄 Daily update: $(date +'%Y-%m-%d %H:%M')" || echo "No changes to commit"
git push origin main
```

Make it executable:

```bash
chmod +x update_and_push.sh
```

### 🔹 Step 2: Schedule the Script with Cron

1. Open your crontab:

   ```bash
   crontab -e
   ```

2. Add this line at the bottom:

   ```bash
   0 9 * * * /Users/pdiomede/Desktop/phython/update_and_push.sh >> /Users/pdiomede/Desktop/phython/cron.log 2>&1
   ```

   This runs your update script every day at **9:00 AM** and logs the output to `cron.log`.

---

## 📊 Data Summary

- `subgraph_repositories_filtered.csv`: main dataset
- `top_contributors.json`: top 10 contributors for dashboard
- Data is sorted by last updated and stars
- Dashboard includes filters, pagination, and summary view

---

## 🙌 Contributions

This dashboard is built by Paolo Diomede for the developer community in The Graph ecosystem.

Feel free to fork or suggest improvements!
