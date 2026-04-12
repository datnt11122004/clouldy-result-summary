
| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |
| :---: | :--- | :---: | :---: | :---: |
| 🥇 | ngon-219 | 0 🔥 | 1 🏆 | ❌ Missing |
| 🥈 | datnt1112 | 0 🔥 | 1 🏆 | ❌ Missing |

| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |
| :---: | :--- | :---: | :---: | :---: |
| 🥇 | ngon-219 | 0 🔥 | 1 🏆 | ❌ Missing |
| 🥈 | datnt1112 | 0 🔥 | 1 🏆 | ❌ Missing |

| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |
| :---: | :--- | :---: | :---: | :---: |
| 🥇 | ngon-219 | 1 🔥 | 1 🏆 | ✅ Done |
| 🥈 | datnt1112 | 1 🔥 | 1 🏆 | ✅ Done |

| Thứ hạng | Thành viên | Chuỗi hiện tại | Chuỗi dài nhất | Trạng thái |
| :---: | :--- | :---: | :---: | :---: |
| 🥇 | ngon-219 | 1 🔥 | 1 🏆 | ✅ Done |
| 🥈 | datnt1112 | 1 🔥 | 1 🏆 | ✅ Done |

## 📊 Bảng Theo Dõi Tiến Độ (Leaderboard)

| Thành viên    | Thư mục                                   | Tổng số ngày   | Trạng thái |
|:--------------|:------------------------------------------|:--------------:|:-----------|
| **datnt1112** | [/members/datnt1112](./members/datnt1112) |       01       | ⏳          |
# 🚀 Cert-5-Daily: Kỷ Luật & Chinh Phục 🎯

Dự án này là nơi lưu trữ quá trình ôn luyện chứng chỉ hàng ngày của anh em. Với tiêu chí: **5 câu mỗi ngày - 15 phút tập trung - Tích tiểu thành đại.**

---

## 📂 Cấu trúc thư mục (Structure)

Mỗi thành viên sẽ có một folder riêng để quản lý nội dung mà không sợ xung đột (conflict) khi merge code.

```text
/members
  ├── [user_name]           # Tên của bạn (viết liền, không dấu)
  │   ├── assets/           # Nơi chứa ảnh chụp màn hình (screenshot)
  │   └── 2026-04-10.md     # File nhật ký theo ngày (định dạng YYYY-MM-DD.md)
```

🛠 Quy trình đóng góp (Workflow)
Để giữ cho "vườn cỏ" GitHub luôn xanh và tránh lỗi, anh em thực hiện theo các bước sau:

Cập nhật: git pull origin main để lấy dữ liệu mới nhất của mọi người.

Tạo file: Vào folder cá nhân, tạo file mới với tên là ngày hôm nay (VD: 2026-04-10.md).

Soạn bài: Viết tóm tắt 5 câu và chèn ảnh minh chứng vào file.

Đẩy bài:
```bash
git add .
git commit -m "feat: [tên-bạn] hoàn thành ngày [date]"
git push origin main
```

📝 Mẫu Nhật Ký (Daily Template)
Anh em có thể copy mẫu này vào file .md hàng ngày để thống nhất định dạng:
```markdown
# Nhật ký học tập - [Ngày/Tháng/Năm]

### 📸 Minh chứng (Screenshot)
![Kết quả học tập](./assets/ten-anh-chup-man-hinh.png)

### 📝 Tóm tắt 5 câu đã làm
1. **Câu 1:** [Chủ đề/Câu hỏi] - Kiến thức rút ra: ...
2. **Câu 2:** [Chủ đề/Câu hỏi] - Tip ghi nhớ: ...
3. **Câu 3:** [Chủ đề/Câu hỏi] - Lưu ý quan trọng: ...
4. **Câu 4:** ...
5. **Câu 5:** ...

---
**Ghi chú/Thảo luận:** (Ví dụ: Câu 3 hôm nay hơi khó, anh em có tài liệu nào về phần này không?)
```

💡 Một số mẹo nhỏ cho anh em
Tạo file nhanh: Nếu dùng Linux/macOS hoặc Git Bash, bạn có thể dùng lệnh này trong folder của mình để tạo file ngày hôm nay:
mkdir -p assets && touch "$(date +%F).md"

Chèn ảnh: Nhớ lưu ảnh vào folder assets và dùng đường dẫn tương đối ./assets/ten-anh.png để GitHub hiển thị được ảnh.

Kỷ luật: Chỉ mất 10-15 phút thôi, cố gắng đừng để đứt chuỗi (streak) nhé!

Chăm chỉ hôm nay, Cert về tay mai sau! 🚀