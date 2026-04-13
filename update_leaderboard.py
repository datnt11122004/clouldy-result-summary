import os
from datetime import datetime, timedelta

def get_streaks(dates):
    """Tính toán Current Streak (Chuỗi hiện tại) và Max Streak (Chuỗi dài nhất)"""
    if not dates:
        return 0, 0

    # Chuyển string sang date object, loại bỏ trùng và sắp xếp tăng dần
    sorted_dates = sorted(list(set([datetime.strptime(d, "%Y-%m-%d").date() for d in dates])))
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # 1. Tính Max Streak (Chuỗi dài nhất từng đạt được)
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

    # 2. Tính Current Streak (Chuỗi hiện tại)
    # Nếu không có bài hôm nay và cũng không có bài hôm qua -> Streak về 0
    current_streak = 0
    if today in sorted_dates or yesterday in sorted_dates:
        # Nếu hôm nay chưa có thì bắt đầu đếm từ hôm qua
        start_date = today if today in sorted_dates else yesterday
        current_streak = 1
        check_date = start_date - timedelta(days=1)

        # Duyệt ngược danh sách để đếm chuỗi liên tục
        try:
            idx = sorted_dates.index(start_date) - 1
            while idx >= 0:
                if sorted_dates[idx] == check_date:
                    current_streak += 1
                    check_date -= timedelta(days=1)
                    idx -= 1
                else:
                    break
        except ValueError:
            pass

    return current_streak, max_streak

def main():
    members_dir = "members"
    readme_path = "README.md"

    if not os.path.exists(members_dir):
        print("❌ Thư mục members/ không tồn tại!")
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    results = []

    # Quét thư mục con trong members/
    for member in os.listdir(members_dir):
        path = os.path.join(members_dir, member)
        if os.path.isdir(path):
            # Lấy các file có định dạng YYYY-MM-DD.md
            dates = [f.replace(".md", "") for f in os.listdir(path) if f.endswith(".md") and f != "README.md"]
            curr, maxi = get_streaks(dates)
            status = "✅ Đã xong" if today_str in dates else "⏳ Chờ bài"

            results.append({
                "name": member,
                "curr": curr,
                "max": maxi,
                "status": status,
                "folder": f"[/members/{member}](./members/{member})"
            })

    # Sắp xếp theo: Chuỗi hiện tại (giảm dần) > Chuỗi dài nhất (giảm dần)
    results.sort(key=lambda x: (x['curr'], x['max']), reverse=True)

    # Tạo bảng Markdown
    table_lines = [
        "| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |",
        "| :---: | :--- | :---: | :---: | :---: |"
    ]

    for i, res in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else str(i)
        table_lines.append(f"| {medal} | **{res['name']}** | {res['curr']} 🔥 | {res['max']} 🏆 | {res['status']} |")

    table_content = "\n" + "\n".join(table_lines) + "\n"

    # Ghi đè vào README.md tại vị trí marker
    if not os.path.exists(readme_path):
        print("❌ Không tìm thấy README.md")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- LEADERBOARD_START -->"
    end_marker = "<!-- LEADERBOARD_END -->"

    if start_marker not in content or end_marker not in content:
        print("❌ Thiếu marker trong README.md!")
        return

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    new_readme = content[:start_idx] + "\n" + table_content + "\n" + content[end_idx:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("✅ Cập nhật Leaderboard thành công!")

if __name__ == "__main__":
    main()