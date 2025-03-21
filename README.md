# 📊 Subgraph GitHub Dashboard

This project tracks public usage of `subgraph.yaml` / `subgraph.yml` files across GitHub.

It includes:
- ✅ A Python script that scans GitHub for subgraph projects
- ✅ A CSV export with filtered data
- ✅ A public HTML dashboard to explore the results
- ✅ Daily automation via a cron job

## 🔧 Technologies
- Python 3
- GitHub REST API
- dotenv for token management
- Pandas for CSV processing
- HTML, JavaScript for dashboard

## 🚀 Live Dashboard
View the latest results here: [https://subgraph-dashboard.vercel.app](https://subgraph-dashboard.vercel.app)

## 🧪 How to Run Locally

1. Clone the repo
2. Create a `.env` file and add your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```
3. Run the script:
   ```bash
   python3 search_subgraphs_clean.py
   ```
4. Open `index.html` in your browser

## 📅 Automation (macOS)

To update and push results daily:

1. Add `update_and_push.sh` in your project folder:

   ```bash
   #!/bin/bash
   cd /path/to/project
   python3 search_subgraphs_clean.py
   git add subgraph_repositories_filtered.csv
   git commit -m "🔄 Daily update: $(date +'%Y-%m-%d %H:%M')" || echo "No changes"
   git push origin main
   ```

2. Make it executable:

   ```bash
   chmod +x update_and_push.sh
   ```

3. Add it to your crontab:

   ```bash
   crontab -e
   ```

   And insert:

   ```bash
   0 9 * * * /path/to/project/update_and_push.sh
   ```

## 🛡 GitHub Token Safety

- Your token is never stored in the repo
- `.env` is excluded via `.gitignore`

## 🙌 Contributions

This dashboard is built by Paolo for the Web3 and subgraph community.

Feel free to fork or suggest improvements!
