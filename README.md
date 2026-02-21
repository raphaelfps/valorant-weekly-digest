# 🎮 Valorant Weekly Digest

An automated Python bot that scrapes the latest Valorant news and VCT competitive results from [vlr.gg](https://www.vlr.gg) and delivers a formatted HTML email digest.

## What it does

- Scrapes the latest news articles from vlr.gg
- Fetches recent VCT match results with scores
- Builds a clean, dark-themed HTML email
- Sends it automatically to any Gmail address

## Example Output

The generated email includes:
- **Latest News** — top articles from vlr.gg with title and description
- **Recent VCT Results** — match scores with team names and tournament stage

## Requirements

- Python 3.8+
- A Gmail account with 2-step verification enabled
- A Gmail App Password

Install dependencies:

```bash
pip install requests beautifulsoup4 python-dotenv
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/raphaelfps/valorant-weekly-digest.git
cd valorant-weekly-digest
```

2. Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

3. Edit `.env` with your Gmail credentials:

```
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
EMAIL_TO=destination@gmail.com
```

> To generate a Gmail App Password, go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). Requires 2-step verification.

4. Run the bot:

```bash
python valorant_weekly.py
```

## Automating with Task Scheduler (Windows)

You can schedule this script to run every week automatically using Windows Task Scheduler — point it to `python valorant_weekly.py` and set your preferred schedule.

## Data Source

All data is scraped from [vlr.gg](https://www.vlr.gg), the leading Valorant esports statistics and news website.
