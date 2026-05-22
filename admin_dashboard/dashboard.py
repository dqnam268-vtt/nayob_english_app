import streamlit as st
import pandas as pd

# Cấu hình trang cơ bản (Mở rộng toàn màn hình, tiêu đề tab)
st.set_page_config(
    page_title="Hệ thống Quản trị - English Class",
    page_icon="🎓",
    layout="wide"
)

# Thêm CSS tùy chỉnh để làm đẹp giao diện và căn giữa footer
st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: bold; color: #0c4a6e; }
    .sub-header { font-size: 20px; color: #4CAF50; margin-bottom: 20px; }
    .footer { text-align: center; margin-top: 50px; font-size: 14px; color: #888; }
    .feedback-box { border-left: 4px solid #f9a8d4; padding-left: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Header chính
st.markdown('<div class="main-header">🎓 Bảng Điều Khiển Giảng Viên</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Quản lý tiến độ học tập và tương tác của học sinh</div>', unsafe_allow_html=True)

# Khởi tạo 3 Tabs chính cho Dashboard
tab1, tab2, tab3 = st.tabs(["📊 Thống kê Tiến độ", "✉️ Hộp thư (Inbox)", "⭐ Đánh giá Khóa học"])

# ==========================================
# TAB 1: THỐNG KÊ TIẾN ĐỘ
# ==========================================
with tab1:
    st.markdown("### 📈 Tiến độ hoàn thành bài tập theo Tuần")
    
    # Dữ liệu mô phỏng (Mock data) - Sau này bạn thay bằng lệnh query từ SQLAlchemy
    # Ví dụ: db.query(Progress).all()
    mock_progress_data = {
        "Học sinh": ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E"],
        "Week 1 (%)": [100, 100, 66, 33, 100],
        "Week 2 (%)": [100, 66, 0, 0, 33],
        "Tổng tiến độ (%)": [100, 83, 33, 16, 66]
    }
    df_progress = pd.DataFrame(mock_progress_data)
    
    # Hiển thị biểu đồ cột
    st.bar_chart(df_progress.set_index("Học sinh")[["Week 1 (%)", "Week 2 (%)"]], height=350)
    
    # Hiển thị bảng dữ liệu chi tiết
    st.markdown("**Bảng dữ liệu chi tiết lớp học:**")
    st.dataframe(df_progress, use_container_width=True)

# ==========================================
# TAB 2: HỘP THƯ (INBOX TỪ ICON LÁ THƯ)
# ==========================================
with tab2:
    st.markdown("### 📬 Giải đáp thắc mắc từ học sinh")
    
    # Dữ liệu mô phỏng tin nhắn
    feedbacks = [
        {"id": 1, "student": "Lê Văn C", "location": "Week 1 - Exercise 2 - Activity 3", "msg": "Thầy ơi, câu này em không hiểu tại sao lại dùng thì Hiện tại hoàn thành ạ?", "status": "Chưa trả lời"},
        {"id": 2, "student": "Phạm Thị D", "location": "Week 2 - Exercise 1 - Video", "msg": "Video tải bị chậm, em xem bị giật hình ạ.", "status": "Chưa trả lời"}
    ]
    
    for fb in feedbacks:
        with st.expander(f"🔴 Tin nhắn mới từ: {fb['student']} (Tại: {fb['location']})"):
            st.markdown(f'<div class="feedback-box"><b>Nội dung:</b> {fb["msg"]}</div>', unsafe_allow_html=True)
            reply = st.text_area("Nhập câu trả lời của bạn:", key=f"reply_{fb['id']}")
            if st.button("Gửi phản hồi", key=f"btn_{fb['id']}"):
                st.success(f"Đã gửi phản hồi cho {fb['student']} thành công!")
                # Chỗ này sẽ gọi lệnh Update Database: is_resolved = True

# ==========================================
# TAB 3: ĐÁNH GIÁ CHẤT LƯỢNG (PIZZA 4P's STYLE)
# ==========================================
with tab3:
    st.markdown("### 🌟 Phản hồi chất lượng ứng dụng (CSAT)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Điểm đánh giá trung bình", "4.8/5.0", "Tăng 0.2 so với tháng trước")
    col2.metric("Số học sinh hoàn thành 100%", "1/5", "20% tỷ lệ hoàn thành")
    col3.metric("Tổng lượt đánh giá", "1", "")
    
    st.divider()
    st.markdown("**Những đánh giá gần đây:**")
    
    # Hiển thị comment của học sinh
    st.info("⭐⭐⭐⭐⭐ - *Nguyễn Văn A*\n\nỨng dụng làm bài tập rất mượt, em rất thích phần kéo thả từ vựng!")

# ==========================================
# FOOTER BẢN QUYỀN THƯƠNG HIỆU
# ==========================================
st.markdown("---")
st.markdown('<div class="footer">Phát triển và thiết kế bởi <b>NamY</b> | Phiên bản 1.0.0</div>', unsafe_allow_html=True)