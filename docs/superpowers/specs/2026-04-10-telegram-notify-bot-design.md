# Design: Telegram Notification Bot for Evidence Push

**Date:** 2026-04-10
**Status:** Approved

---

## Overview

Khi một member push evidence (file `.md`) lên repo, một GitHub Actions workflow sẽ detect commit đó và gửi notification vào Telegram group ngay lập tức. Mục tiêu: tạo động lực đua tranh, không ai push âm thầm mà không ai biết.

---

## Architecture

### Trigger

- **Workflow file:** `.github/workflows/notify-telegram.yml`
- **Trigger:** `on: push` to any branch (`**`)
- **Path filter:** chỉ chạy khi có file thay đổi trong `members/**`

### Components

**1. `notify_telegram.py`** — Script Python chính

Chạy trong GitHub Actions, thực hiện:
1. Đọc git diff của commit vừa push (`git diff-tree --no-commit-id -r --name-status HEAD`)
2. Filter các file có status `A` (added) và match pattern `members/<username>/YYYY-MM-DD.md`
3. Với mỗi file mới:
   - Parse `username` và `date` từ path
   - Tính current streak: đếm file `.md` liên tiếp trong `members/<username>/` (reuse logic từ `update_leaderboard.py`)
   - Gửi Telegram message qua Bot API

**2. `.github/workflows/notify-telegram.yml`** — Workflow definition

```yaml
on:
  push:
    branches: ['**']
    paths: ['members/**']
```

Checkout repo, setup Python, chạy `notify_telegram.py`.

---

## Message Format

```
🎉 <username> đã gửi evidence!

📅 Ngày: YYYY-MM-DD
🔥 Streak hiện tại: N ngày
🔗 Xem bài: https://github.com/<owner>/<repo>/commit/<sha>

💪 "<motivational quote>"
```

Motivational quotes: ~10 câu hardcode trong script, chọn random mỗi lần.

---

## Double-Notify Prevention

Chỉ notify khi file có git status `A` (added), không phải `M` (modified) hay `D` (deleted). Nếu member sửa lại nội dung file trong ngày, sẽ không bị spam notification.

---

## Secrets Required

| Secret | Mô tả |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | Token từ @BotFather trên Telegram |
| `TELEGRAM_CHAT_ID` | ID của group chat Telegram |

Setup 1 lần tại: GitHub repo → Settings → Secrets and variables → Actions.

---

## File Structure Changes

```
.github/
  workflows/
    notify-telegram.yml     # NEW
notify_telegram.py          # NEW
```

Không sửa code hiện có.

---

## Out of Scope

- DM riêng cho từng member
- Nhắc nhở người chưa push (covered bởi workflow leaderboard hiện tại)
- Web dashboard hay UI
