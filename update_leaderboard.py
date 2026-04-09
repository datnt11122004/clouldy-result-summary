import os
from datetime import datetime

def update_leaderboard():
    members_dir = "members"
    if not os.path.exists(members_dir):
        return

    today = datetime.now().strftime("%Y-%m-%d")
    leaderboard_data = []

    # Quét tất cả folder trong members/
    for member_name in sorted(os.listdir(members_dir)):
        member_path = os.path.join(members_dir, member_name)

        if os.path.isdir(member_path):
            # Đếm số file .md (không tính README.md nếu có)
            files = [f for f in os.listdir(member_path) if f.endswith(".md") and f != "README.md"]
            total_days = len(files)

            # Check xem hôm nay đã nộp bài chưa
            has_done_today = "✅" if any(today in f for f in files) else "⏳"

            leaderboard_data.append(
                f"| **{member_name}** | [/members/{member_name}](./members/{member_name}) | {total_days:02d} | {has_done_today} |"
            )

    # Tạo nội dung bảng mới
    new_table = [
        "| Thành viên | Thư mục | Tổng số ngày | Trạng thái |",
        "| :--- | :--- | :---: | :--- |",
        *leaderboard_data
    ]
    table_content = "\n".join(new_table)

    # Đọc và ghi đè vào README.md
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = ""
    end_marker = ""

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    new_content = content[:start_idx] + "\n" + table_content + "\n" + content[end_idx:]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_leaderboard()