# Telegram Notify Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gửi Telegram notification vào group chat ngay khi một member push file evidence mới lên repo.

**Architecture:** GitHub Actions workflow trigger on push to any branch with path filter `members/**`. Script Python detect file `.md` added (status `A`) từ git diff, tính streak, gửi message qua Telegram Bot API. Double-notify prevention bằng cách chỉ xử lý file status `A` (added), bỏ qua `M` (modified).

**Tech Stack:** Python 3.x, `requests` library, Telegram Bot API, GitHub Actions

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `notify_telegram.py` | Create | Parse git diff, tính streak, gửi Telegram |
| `.github/workflows/notify-telegram.yml` | Create | Trigger workflow, chạy script |

---

### Task 1: Write `notify_telegram.py`

**Files:**
- Create: `notify_telegram.py`
- Test: manual test với `python notify_telegram.py` (xem Task 3)

- [ ] **Step 1: Tạo file `notify_telegram.py`**

```python
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


def get_added_evidence_files():
    """Return list of (username, date_str) for newly added evidence files in this commit."""
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "-r", "--name-status", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    added = []
    pattern = re.compile(r"^A\s+members/([^/]+)/(\d{4}-\d{2}-\d{2})\.md$")
    for line in result.stdout.splitlines():
        m = pattern.match(line)
        if m:
            username, date_str = m.group(1), m.group(2)
            added.append((username, date_str))
    return added


def get_current_streak(username):
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
    today = datetime.now().date()
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


def build_message(username, date_str, streak, commit_sha, repo_full_name):
    quote = random.choice(MOTIVATIONAL_QUOTES)
    commit_url = f"https://github.com/{repo_full_name}/commit/{commit_sha}"
    return (
        f"🎉 *{username}* đã gửi evidence\\!\n\n"
        f"📅 Ngày: {date_str}\n"
        f"🔥 Streak hiện tại: {streak} ngày\n"
        f"🔗 [Xem bài]({commit_url})\n\n"
        f"💪 _{quote}_"
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
        streak = get_current_streak(username)
        message = build_message(username, date_str, streak, commit_sha, repo_full_name)
        send_telegram(token, chat_id, message)
        print(f"Notified: {username} | {date_str} | streak={streak}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit file**

```bash
git add notify_telegram.py
git commit -m "feat: add telegram notification script"
```

---

### Task 2: Write `.github/workflows/notify-telegram.yml`

**Files:**
- Create: `.github/workflows/notify-telegram.yml`

- [ ] **Step 1: Tạo workflow file**

```yaml
name: Notify Telegram on Evidence Push

on:
  push:
    branches:
      - '**'
    paths:
      - 'members/**'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Send Telegram notification
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python notify_telegram.py
```

> **Lưu ý `fetch-depth: 2`:** Cần fetch ít nhất 2 commits để `git diff-tree HEAD` có parent để so sánh. Nếu là commit đầu tiên của repo thì diff-tree vẫn hoạt động đúng vì nó list tất cả file của commit đó.

- [ ] **Step 2: Commit file**

```bash
git add .github/workflows/notify-telegram.yml
git commit -m "feat: add github actions workflow for telegram notify"
```

---

### Task 3: Setup Secrets & Test End-to-End

**Files:** Không có file nào thay đổi — đây là bước config và verify.

- [ ] **Step 1: Tạo Telegram bot**

1. Mở Telegram, tìm `@BotFather`
2. Gửi `/newbot`, đặt tên và username cho bot
3. Copy token nhận được (dạng `123456:ABC-DEF...`)

- [ ] **Step 2: Lấy Chat ID của group**

1. Thêm bot vào group chat
2. Gửi 1 tin nhắn bất kỳ trong group
3. Truy cập URL sau (thay `<TOKEN>` bằng token thật):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Trong response JSON, tìm `result[0].message.chat.id` — đó là Chat ID (thường là số âm với group, ví dụ `-1001234567890`)

- [ ] **Step 3: Add Secrets vào GitHub repo**

1. Vào GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**:
   - Name: `TELEGRAM_BOT_TOKEN`, Value: token từ BotFather
   - Name: `TELEGRAM_CHAT_ID`, Value: chat ID từ bước trên

- [ ] **Step 4: Test bằng cách push một file evidence mới**

Tạo file test trong branch của bạn:
```bash
mkdir -p members/testuser
echo "# Test" > members/testuser/2026-04-10.md
git add members/testuser/2026-04-10.md
git commit -m "test: verify telegram notification"
git push origin <your-branch>
```

- [ ] **Step 5: Verify trên GitHub Actions**

Vào GitHub repo → **Actions** → tab **Notify Telegram on Evidence Push**. Kiểm tra workflow run mới nhất:
- Expected output: `Notified: testuser | 2026-04-10 | streak=1`
- Telegram group nhận được message với format đúng

- [ ] **Step 6: Cleanup file test**

```bash
rm -rf members/testuser
git add members/testuser
git commit -m "chore: remove test evidence file"
git push origin <your-branch>
```

> Lần push này cũng trigger workflow nhưng vì không có file `A` (added), script sẽ print `No new evidence files detected. Skipping notification.` và exit sạch.

---

## Notes cho Members

Sau khi setup xong, mỗi khi bất kỳ member nào push file `YYYY-MM-DD.md` mới vào folder của mình, Telegram group sẽ nhận notification trong vòng ~30 giây.
