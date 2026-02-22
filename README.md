# Valorant Weekly Digest — Automated News & Esports Email Bot

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-web%20scraping-59666C?style=flat&logo=python&logoColor=white)
![SMTP](https://img.shields.io/badge/Gmail%20SMTP-email%20delivery-EA4335?style=flat&logo=gmail&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat)

> **Automated Python bot** that scrapes the latest Valorant esports news and VCT match results from [vlr.gg](https://www.vlr.gg) and delivers a branded HTML email digest — fully hands-off after setup.

---

## Business Value

This project demonstrates a **production-ready automation pipeline** applicable to any business use case:

- **Any niche** — swap vlr.gg for any news site, product page, or data source
- **Any frequency** — daily, weekly, or on any custom schedule
- **Any audience** — one recipient or a list; internal teams or end customers
- **Zero manual effort** — once scheduled, runs indefinitely without human intervention

Typical client use cases: competitive intelligence reports, price monitoring alerts, social media digest emails, internal KPI summaries.

---

## Features

| Feature | Details |
|---|---|
| Web Scraping | Pulls 6 latest news articles from vlr.gg/news |
| Match Results | Fetches 5 most recent VCT competitive match scores |
| HTML Email | Responsive dark-themed branded email (620px, inline CSS) |
| SMTP Delivery | Sends via Gmail SMTP (SSL port 465) |
| Scheduling | Fully automatable via cron (Linux/macOS) or Task Scheduler (Windows) |
| Config via `.env` | Credentials stored securely in environment variables |

---

## Example Output

The bot generates and delivers an email like this:

```
┌─────────────────────────────────────────────┐
│ 🎮  VALORANT WEEKLY                         │
│     Competitive Digest         Feb 22, 2026 │
├─────────────────────────────────────────────┤
│ 📰 LATEST NEWS                              │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 1d ago                              │    │
│  │ Team Liquid drops roster ahead ...  │    │
│  │ The organization announced changes  │    │
│  │ to its VCT EMEA lineup following... │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 2d ago                              │    │
│  │ VCT Americas Week 3 preview         │    │
│  │ All eyes on the standings as NRG... │    │
│  └─────────────────────────────────────┘    │
│                                             │
├─────────────────────────────────────────────┤
│ 🏆 RECENT VCT RESULTS                       │
│                                             │
│  VCT Americas — Week 3                      │
│  NRG          2  vs  1  Cloud9             │
│                                             │
│  VCT EMEA — Kickoff                         │
│  Fnatic        0  vs  2  Team Liquid       │
│                                             │
├─────────────────────────────────────────────┤
│  Valorant Weekly Digest · Data from vlr.gg  │
└─────────────────────────────────────────────┘
```

*Actual email renders with dark background (#0f0f17), Valorant red accents (#ff4655), and clickable cards.*

---

## Tech Stack

- **[requests](https://docs.python-requests.org/)** — HTTP client for fetching web pages
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** — HTML parsing with CSS selectors
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Secure credential management via `.env`
- **smtplib / email.mime** — Standard library email composition and SMTP delivery
- **datetime** — Timestamped subject lines and footer

---

## Project Structure

```
news-email-bot/
├── valorant_weekly.py   # Main bot: scrape → build HTML → send email
├── .env.example         # Environment variable template (commit this)
├── .env                 # Your credentials (never commit this)
└── .gitignore
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/raphaelfps/valorant-weekly-digest.git
cd valorant-weekly-digest
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 python-dotenv
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_16_char_app_password
EMAIL_TO=destination@gmail.com
```

> **Gmail App Password required.** Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) to generate one. Requires 2-Step Verification to be enabled on your account.

### 4. Run the bot

```bash
python valorant_weekly.py
```

**Expected output:**

```
Scraping vlr.gg news...
  6 articles found
Scraping VCT results...
  5 matches found
Building email...
Sending email...
✅ Valorant Weekly sent to destination@gmail.com
```

---

## Automation

### Windows — Task Scheduler

1. Open **Task Scheduler** → Create Basic Task
2. Set trigger: **Weekly**, choose day and time
3. Action: **Start a program**
   - Program: `python`
   - Arguments: `C:\path\to\valorant_weekly.py`
4. Save and enable the task

### Linux / macOS — cron

```bash
# Run every Monday at 8:00 AM
crontab -e
0 8 * * 1 /usr/bin/python3 /path/to/valorant_weekly.py
```

---

## Customization

This bot is built as a **reusable pattern**. Adapting it to a new use case requires changing only two functions:

| What to change | Where |
|---|---|
| Data source URL and CSS selectors | `fetch_vlr_news()`, `fetch_vct_results()` |
| Email layout and branding | `build_html()` |
| Delivery schedule | Task Scheduler / cron config |

The scraping → HTML → SMTP pipeline stays the same regardless of niche.

---

## Data Source

All data is scraped from [vlr.gg](https://www.vlr.gg), the leading Valorant esports statistics and news platform.

---

## License

MIT — free to use, modify, and adapt for commercial projects.
