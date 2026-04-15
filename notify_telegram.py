import os
import re
import subprocess
import random
import requests
from datetime import datetime, timedelta

MOTIVATIONAL_QUOTES = [
    "Consistency is the key to mastery. Keep going!",
    "Small steps every day lead to big results.",
    "You showed up today. That already puts you ahead.",
    "1% better every day. That's 37x better in a year.",
    "The secret of getting ahead is getting started.",
    "Don't break the chain! 🔗",
    "Discipline is choosing between what you want now and what you want most.",
    "Every expert was once a beginner. Keep pushing!",
    "Your future self will thank you for this.",
    "Progress, not perfection. You're doing great!",
]


# def get_added_evidence_files():
#     """Return list of (username, date_str) for newly added evidence files in this commit."""
#     result = subprocess.run(
#         ["git", "diff-tree", "--no-commit-id", "-r", "--name-status", "HEAD"],
#         capture_output=True,
#         text=True,
#         check=True,
#     )
#     added = []
#     pattern = re.compile(r"^A\s+members/([^/]+)/(\d{4}-\d{2}-\d{2})\.md$")
#     for line in result.stdout.splitlines():
#         m = pattern.match(line)
#         if m:
#             username, date_str = m.group(1), m.group(2)
#             added.append((username, date_str))
#     return added

def get_added_evidence_files():
    before = os.environ.get("GITHUB_EVENT_BEFORE")
    after = os.environ.get("GITHUB_SHA")

    if not before or before == "0000000000000000000000000000000000000000":
        # fallback nếu commit đầu tiên
        diff_cmd = ["git", "show", "--name-status", after]
    else:
        diff_cmd = ["git", "diff", "--name-status", before, after]

    result = subprocess.run(
        diff_cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    added = []
    pattern = re.compile(r"^A\s+members/([^/]+)/(\d{4}-\d{2}-\d{2})\.md$")

    for line in result.stdout.splitlines():
        print("DEBUG:", line)  # 👈 thêm log
        m = pattern.match(line)
        if m:
            username, date_str = m.group(1), m.group(2)
            added.append((username, date_str))

    return added

    

def get_current_streak(username, date_str):
    """Count current consecutive streak for a member."""
    member_dir = os.path.join("members", username)
    if not os.path.isdir(member_dir):
        return 1
    dates = [
        f.replace(".md", "")
        for f in os.listdir(member_dir)
        if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f)
    ]
    if not dates:
        return 1
    sorted_dates = sorted(
        set(datetime.strptime(d, "%Y-%m-%d").date() for d in dates)
    )
    today = datetime.strptime(date_str, "%Y-%m-%d").date()
    if today not in sorted_dates:
        # File just pushed may not yet be on disk in the runner;
        # treat today as included.
        sorted_dates = sorted(sorted_dates | {today})
    streak = 1
    check = today - timedelta(days=1)
    for d in reversed(sorted_dates[:-1]):
        if d == check:
            streak += 1
            check -= timedelta(days=1)
        else:
            break
    return streak


def escape_md(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    special = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([' + re.escape(special) + r'])', r'\\\1', text)


def build_message(username, date_str, streak, commit_sha, repo_full_name):
    quote = random.choice(MOTIVATIONAL_QUOTES)
    commit_url = f"https://github.com/{repo_full_name}/commit/{commit_sha}"
    safe_username = escape_md(username)
    safe_date = escape_md(date_str)
    safe_quote = escape_md(quote)
    return (
        f"🎉 *{safe_username}* đã gửi evidence\\!\n\n"
        f"📅 Ngày: {safe_date}\n"
        f"🔥 Streak hiện tại: {streak} ngày\n"
        f"🔗 [Xem bài]({commit_url})\n\n"
        f"💪 _{safe_quote}_"
    )


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    commit_sha = os.environ.get("GITHUB_SHA", "HEAD")
    repo_full_name = os.environ.get("GITHUB_REPOSITORY", "owner/repo")

    added_files = get_added_evidence_files()
    if not added_files:
        print("No new evidence files detected. Skipping notification.")
        return

    for username, date_str in added_files:
        streak = get_current_streak(username, date_str)
        message = build_message(username, date_str, streak, commit_sha, repo_full_name)
        try:
            send_telegram(token, chat_id, message)
            print(f"Notified: {username} | {date_str} | streak={streak}")
        except requests.HTTPError as e:
            print(f"ERROR sending for {username}: {e.response.text}")
        except requests.RequestException as e:
            print(f"ERROR sending for {username}: {e}")


if __name__ == "__main__":
    main()
