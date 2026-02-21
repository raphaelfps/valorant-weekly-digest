import requests
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER     = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
EMAIL_TO       = os.getenv("EMAIL_TO")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ── 1. SCRAPING VLR.GG NEWS ───────────────────────────────────────────────────

def fetch_vlr_news(limit=6):
    url = "https://www.vlr.gg/news"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    for item in soup.select("a.wf-module-item")[:limit]:
        divs = item.find_all("div", recursive=False)
        inner = divs[0].find_all("div") if divs else []

        title = inner[0].get_text(strip=True) if len(inner) > 0 else "No title"
        desc  = inner[1].get_text(strip=True) if len(inner) > 1 else ""
        date  = inner[2].get_text(strip=True) if len(inner) > 2 else ""
        link  = "https://www.vlr.gg" + item.get("href", "")

        articles.append({
            "title": title,
            "desc":  desc,
            "date":  date,
            "link":  link,
        })

    return articles

# ── 2. SCRAPING VCT RESULTS ───────────────────────────────────────────────────

def fetch_vct_results(limit=5):
    url = "https://www.vlr.gg/matches/results"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []
    for item in soup.select("a.match-item")[:limit]:
        teams = item.select(".match-item-vs-team-name")
        scores = item.select(".match-item-vs-team-score")
        event = item.select_one(".match-item-event-series")
        link = "https://www.vlr.gg" + item.get("href", "")

        if len(teams) >= 2:
            matches.append({
                "team1":  teams[0].get_text(strip=True),
                "team2":  teams[1].get_text(strip=True),
                "score1": scores[0].get_text(strip=True) if len(scores) > 0 else "-",
                "score2": scores[1].get_text(strip=True) if len(scores) > 1 else "-",
                "event":  event.get_text(strip=True) if event else "",
                "link":   link,
            })

    return matches

# ── 3. MONTAR HTML ────────────────────────────────────────────────────────────

def build_html(news, matches):
    today = datetime.now().strftime("%B %d, %Y")

    # News section
    news_html = ""
    for a in news:
        news_html += f"""
        <a href="{a['link']}" style="display:block;text-decoration:none;background:#1e1e2e;border-radius:8px;padding:16px;margin-bottom:10px;border-left:3px solid #ff4655;">
            <p style="margin:0 0 2px;font-size:11px;color:#888;">{a['date']}</p>
            <p style="margin:0 0 6px;font-size:15px;font-weight:700;color:#ffffff;">{a['title']}</p>
            <p style="margin:0;font-size:12px;color:#aaa;line-height:1.5;">{a['desc']}</p>
        </a>
        """

    # Matches section
    matches_html = ""
    for m in matches:
        s1, s2 = m['score1'], m['score2']
        c1 = "#ff4655" if s1 > s2 else "#aaa"
        c2 = "#ff4655" if s2 > s1 else "#aaa"

        matches_html += f"""
        <a href="{m['link']}" style="display:block;text-decoration:none;background:#1e1e2e;border-radius:8px;padding:14px 16px;margin-bottom:8px;">
            <p style="margin:0 0 8px;font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;">{m['event']}</p>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:14px;font-weight:700;color:#ffffff;width:40%;text-align:left;">{m['team1']}</span>
                <span style="font-size:18px;font-weight:900;color:{c1};width:10%;text-align:center;">{s1}</span>
                <span style="font-size:12px;color:#555;width:10%;text-align:center;">vs</span>
                <span style="font-size:18px;font-weight:900;color:{c2};width:10%;text-align:center;">{s2}</span>
                <span style="font-size:14px;font-weight:700;color:#ffffff;width:40%;text-align:right;">{m['team2']}</span>
            </div>
        </a>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#0f0f17;font-family:'Segoe UI',Arial,sans-serif;">
        <div style="max-width:620px;margin:0 auto;padding:24px 16px;">

            <!-- Header -->
            <div style="background:linear-gradient(135deg,#1e1e2e,#2a1a2e);border-radius:12px;padding:28px 28px 20px;margin-bottom:20px;border-top:3px solid #ff4655;">
                <div style="display:flex;align-items:center;margin-bottom:8px;">
                    <span style="font-size:28px;margin-right:12px;">🎮</span>
                    <div>
                        <h1 style="margin:0;color:#ffffff;font-size:22px;letter-spacing:1px;">VALORANT WEEKLY</h1>
                        <p style="margin:4px 0 0;color:#ff4655;font-size:11px;text-transform:uppercase;letter-spacing:2px;">Competitive Digest</p>
                    </div>
                </div>
                <p style="margin:12px 0 0;color:#666;font-size:12px;">{today}</p>
            </div>

            <!-- News -->
            <div style="margin-bottom:24px;">
                <h2 style="margin:0 0 12px;color:#ff4655;font-size:12px;text-transform:uppercase;letter-spacing:2px;">📰 Latest News</h2>
                {news_html}
            </div>

            <!-- VCT Results -->
            <div style="margin-bottom:24px;">
                <h2 style="margin:0 0 12px;color:#ff4655;font-size:12px;text-transform:uppercase;letter-spacing:2px;">🏆 Recent VCT Results</h2>
                {matches_html}
            </div>

            <!-- Footer -->
            <div style="text-align:center;padding:16px;">
                <p style="margin:0;color:#444;font-size:11px;">Valorant Weekly Digest · {today} · Data from vlr.gg</p>
            </div>

        </div>
    </body>
    </html>
    """
    return html

# ── 4. ENVIAR EMAIL ───────────────────────────────────────────────────────────

def send_email(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎮 Valorant Weekly — {datetime.now().strftime('%B %d, %Y')}"
    msg["From"]    = GMAIL_USER
    msg["To"]      = EMAIL_TO

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, EMAIL_TO, msg.as_string())

# ── 5. MAIN ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Scraping vlr.gg news...")
    news = fetch_vlr_news()
    print(f"  {len(news)} articles found")

    print("Scraping VCT results...")
    matches = fetch_vct_results()
    print(f"  {len(matches)} matches found")

    print("Building email...")
    html = build_html(news, matches)

    print("Sending email...")
    send_email(html)
    print(f"✅ Valorant Weekly sent to {EMAIL_TO}")
