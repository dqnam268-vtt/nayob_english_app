// ==========================================
// CẤU HÌNH API
// ==========================================
const API_BASE_URL = "http://127.0.0.1:8000/api"; // Đổi thành URL thật khi đưa lên mạng

// ==========================================
// LOGIC HIỂN THỊ (RENDER)
// ==========================================

// Hàm lấy dữ liệu (Fetch) TỪ DATABASE PYTHON
async function fetchCourseData() {
    try {
        console.log("Đang kết nối tới Backend...");
        const response = await fetch(`${API_BASE_URL}/get_syllabus`);
        
        if (!response.ok) throw new Error("Lỗi mạng!");
        
        const data = await response.json();
        
        // Nếu DB rỗng, báo cho người dùng biết
        if (data.length === 0) {
            document.querySelector('.course-content').innerHTML = 
                '<p style="text-align:center; padding:20px;">Chưa có bài học nào. Hãy gọi API /api/seed_data để tạo dữ liệu mẫu.</p>';
            return;
        }

        renderSyllabus(data);
        console.log("Lấy dữ liệu thành công!", data);
    } catch (error) {
        console.error("Lỗi khi tải dữ liệu:", error);
        alert("Không thể kết nối đến Backend Python. Đảm bảo server đang chạy ở cổng 8000!");
    }
}

// Hàm vẽ giao diện bài học ra màn hình điện thoại
function renderSyllabus(weeksData) {
    const mainContent = document.querySelector('.course-content');
    mainContent.innerHTML = ''; // Xóa dữ liệu cứng trong HTML cũ

    weeksData.forEach(week => {
        // 1. Tạo bọc cho Tuần học
        const weekSection = document.createElement('div');
        weekSection.className = 'week-section';

        // 2. Tạo Tiêu đề Tuần
        const weekTitle = document.createElement('div');
        weekTitle.className = 'week-title';
        weekTitle.innerText = week.title;
        weekSection.appendChild(weekTitle);

        // 3. Tạo các nút Bài tập (Exercise)
        week.exercises.forEach(exe => {
            const exeBtn = document.createElement('button');
            exeBtn.className = 'exercise-btn';
            exeBtn.innerText = exe.title;
            
            // Bắt sự kiện khi học sinh chạm vào nút Exercise
            exeBtn.onclick = () => openActivities(exe.title, exe.activities);
            
            weekSection.appendChild(exeBtn);
        });

        mainContent.appendChild(weekSection);
    });
}

// ==========================================
// LOGIC TƯƠNG TÁC (INTERACTION)
// ==========================================

// Mở danh sách Activity khi bấm vào Exercise
function openActivities(exerciseTitle, activities) {
    // Tạm thời hiển thị danh sách bằng alert để test logic
    let activityList = activities.map((act, index) => `Hoạt động ${index + 1}: ${act}`).join('\n');
    alert(`Bạn đang mở: ${exerciseTitle}\n\nDanh sách nhiệm vụ:\n${activityList}\n\n(Hệ thống sẽ mở popup làm bài ở bước sau)`);
}

// Xử lý nút Feedback (Lá thư) GỬI VỀ DATABASE PYTHON
function setupFeedbackButton() {
    const feedbackBtn = document.getElementById('feedback-btn');
    
    if(feedbackBtn) {
        feedbackBtn.addEventListener('click', async () => {
            const userMsg = prompt("🎓 Bạn có thắc mắc gì về bài học này? Hãy nhập câu hỏi để thầy Nam giải đáp nhé:");
            
            if (userMsg && userMsg.trim() !== "") {
                try {
                    console.log("Đang gửi feedback về backend:", userMsg);
                    
                    // Gọi API POST gửi dữ liệu lên Backend
                    const response = await fetch(`${API_BASE_URL}/send_feedback`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ 
                            message: userMsg, 
                            location: "Màn hình chính App", 
                            user_id: 1 // Gán cứng user ID = 1 để test luồng dữ liệu
                        })
                    });

                    const result = await response.json();
                    if (result.status === "success") {
                        alert("Tin nhắn đã được lưu vào hệ thống! Thầy sẽ trả lời em sớm nhất có thể.");
                    }
                } catch (error) {
                    console.error("Lỗi gửi feedback:", error);
                    alert("Không gửi được tin nhắn. Kiểm tra lại kết nối mạng hoặc server Backend.");
                }
            }
        });
    }
}

// ==========================================
// KHỞI CHẠY ỨNG DỤNG
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // 1. Tải danh sách bài học từ Database
    fetchCourseData();
    
    // 2. Bật nút tính năng Lá thư
    setupFeedbackButton();
});