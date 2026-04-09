import os
from datetime import datetime, timedelta

def get_streaks(dates):
    if not dates:
        return 0, 0

    # Chuyển đổi string sang object date và sắp xếp tăng dần
    sorted_dates = sorted(list(set([datetime.strptime(d, "%Y-%m-%d").date() for d in dates])))
    today = datetime.now().date()

    # 1. Tính Chuỗi dài nhất (Max Streak)
    max_streak = 0
    curr_max = 0
    if sorted_dates:
        max_streak = 1
        curr_max = 1
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] == sorted_dates[i-1] + timedelta(days=1):
                curr_max += 1
            else:
                curr_max = 1
            max_streak = max(max_streak, curr_max)

    # 2. Tính Chuỗi hiện tại (Current Streak)
    # Quy tắc: Tại thời điểm 23:30, nếu không có file ngày hôm nay -> Reset về 0
    current_streak = 0
    if today in sorted_dates:
        current_streak = 1
        check_date = today - timedelta(days=1)
        # Duyệt ngược về quá khứ
        idx = len(sorted_dates) - 2
        while idx >= 0:
            if sorted_dates[idx] == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
                idx -= 1
            else:
                break

    return current_streak, max_streak

def main():
    members_dir = "members"
    if not os.path.exists(members_dir): return

    today_str = datetime.now().strftime("%Y-%m-%d")
    results = []

    for member in os.listdir(members_dir):
        path = os.path.join(members_dir, member)
        if os.path.isdir(path):
            # Lấy danh sách ngày từ tên file YYYY-MM-DD.md
            dates = [f.replace(".md", "") for f in os.listdir(path) if f.endswith(".md") and f != "README.md"]
            curr, maxi = get_streaks(dates)
            status = "✅ Done" if today_str in dates else "❌ Missing"
            results.append({
                "name": member,
                "curr": curr,
                "max": maxi,
                "status": status,
                "path": f"[/members/{member}](./members/{member})"
            })

    # Sắp xếp: Chuỗi hiện tại giảm dần, sau đó đến Chuỗi dài nhất
    results.sort(key=lambda x: (x['curr'], x['max']), reverse=True)

    # Tạo nội dung bảng Markdown
    table = ["| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |",
             "| :---: | :--- | :---: | :---: | :---: |"]

    for i, res in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else str(i)
        table.append(f"| {medal} | {res['name']} | {res['curr']} 🔥 | {res['max']} 🏆 | {res['status']} |")

    # Ghi vào README.md
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_m, end_m = "", ""
    new_content = content[:content.find(start_m)+len(start_m)] + "\n" + "\n".join(table) + "\n" + content[content.find(end_m):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()