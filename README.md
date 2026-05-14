# 🤖 Egypt Jobs AI

> **A free, open-source platform aggregating AI & ML job opportunities in Egypt — updated automatically every 12 hours via GitHub Actions.**

🌐 **Live Site:** `https://YOUR_USERNAME.github.io/Egypt-Jobs-AI`

---

## ✨ Features

- 🔍 **Real-time search** by job title, company, or keyword
- 🏷️ **Smart filters** — Full-time, Internship, Remote
- ⚡ **Zero cost** — Fully hosted on GitHub Pages (no servers)
- 🤖 **Auto-updated** — GitHub Actions runs every 12 hours to fetch new opportunities
- 📱 **Fully responsive** — Mobile-first design

---

## 🗂️ Project Structure

```
Egypt-Jobs-AI/
├── index.html                  # Main UI page
├── css/
│   └── styles.css              # Dark-mode, modern styling
├── js/
│   └── app.js                  # Dynamic rendering, search & filters
├── data/
│   └── jobs.json               # Job database (auto-updated)
├── scripts/
│   └── scraper.py              # Python scraper for live job data
└── .github/
    └── workflows/
        └── update_jobs.yml     # GitHub Actions automation workflow
```

---

## 🚀 Deployment to GitHub Pages

1. **Fork or clone** this repository to your GitHub account.
2. Go to **Settings → Pages**.
3. Under **Source**, select `main` branch and `/ (root)` folder.
4. Click **Save**. Your site will be live in a few minutes at:
   ```
   https://YOUR_USERNAME.github.io/Egypt-Jobs-AI
   ```

---

## ⚙️ Setting Up Live Job Fetching

To enable live job data from LinkedIn via RapidAPI:

1. Sign up at [RapidAPI](https://rapidapi.com) and subscribe to the **LinkedIn Jobs Search** API.
2. Copy your API Key.
3. In your GitHub repository, go to **Settings → Secrets and variables → Actions**.
4. Add a new secret named `RAPIDAPI_KEY` and paste your key.

The GitHub Actions workflow will automatically use this key every time it runs.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, Vanilla CSS, JavaScript |
| Data Store | `data/jobs.json` (static JSON file) |
| Automation | Python 3 + GitHub Actions |
| Hosting | GitHub Pages (100% free) |

---

## 📜 License

MIT License — Free to use, modify, and distribute.

---

*Made with ❤️ by Shahd Shaban — Designed for the Egyptian AI community.*
