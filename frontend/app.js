// ==========================================
// CẤU HÌNH API
// ==========================================
const API_BASE_URL = "https://nayob-english-app.onrender.com"; // Đổi thành URL thật khi đưa lên mạng (VD: URL của Render)

// ==========================================
// LOGIC ĐĂNG NHẬP (AUTH)
// ==========================================
function setupLogin() {
    const loginBtn = document.getElementById('login-btn');
    const userValInput = document.getElementById('username');
    const passValInput = document.getElementById('password');
    const errorMsg = document.getElementById('login-error');

    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            const userVal = userValInput.value.trim();
            const passVal = passValInput.value.trim();

            if (!userVal || !passVal) {
                errorMsg.innerText = "Vui lòng nhập đầy đủ tài khoản và mật khẩu!";
                errorMsg.style.display = 'block';
                return;
            }

            try {
                // Thay đổi text nút bấm để tạo cảm giác đang tải
                loginBtn.innerText = "Đang kết nối...";
                loginBtn.disabled = true;

                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: userVal, password: passVal })
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // Lưu thông tin học sinh vào bộ nhớ trình duyệt điện thoại
                    localStorage.setItem('student_id', data.user_id);
                    localStorage.setItem('student_name', data.username);
                    
                    // Chuyển đổi màn hình: Ẩn form login, hiện giao diện bài học
                    document.getElementById('login-section').style.display = 'none';
                    document.getElementById('main-app').style.display = 'block';
                    
                    // Bắt đầu tải danh sách bài học
                    fetchCourseData();
                } else {
                    errorMsg.innerText = "Sai tên đăng nhập hoặc mật khẩu!";
                    errorMsg.style.display = 'block';
                }
            } catch (error) {
                console.error("Lỗi đăng nhập:", error);
                errorMsg.innerText = "Lỗi kết nối đến máy chủ! Vui lòng thử lại.";
                errorMsg.style.display = 'block';
            } finally {
                // Khôi phục trạng thái nút bấm
                loginBtn.innerText = "Vào Học";
                loginBtn.disabled = false;
            }
        });
    }
}

// ==========================================
// LOGIC HIỂN THỊ (RENDER)
// ==========================================

// Hàm lấy dữ liệu (Fetch) TỪ DATABASE PYTHON
async function fetchCourseData() {
    try {
        console.log("Đang kết nối tới Backend để lấy bài học...");
        const response = await fetch(`${API_BASE_URL}/get_syllabus`);
        
        if (!response.ok) throw new Error("Lỗi mạng!");
        
        const data = await response.json();
        
        // Nếu DB rỗng, báo cho người dùng biết
        if (data.length === 0) {
            document.querySelector('.course-content').innerHTML = 
                '<p style="text-align:center; padding:20px;">Chưa có bài học nào. Hãy liên hệ admin để tạo bài học.</p>';
            return;
        }

        renderSyllabus(data);
        console.log("Lấy dữ liệu thành công!");
    } catch (error) {
        console.error("Lỗi khi tải dữ liệu:", error);
        alert("Không thể kết nối đến Backend Python. Đảm bảo server đang chạy ở cổng 8000!");
    }
}

// Hàm vẽ giao diện bài học ra màn hình điện thoại
function renderSyllabus(weeksData) {
    const mainContent = document.querySelector('.course-content');
    mainContent.innerHTML = ''; // Xóa dữ liệu tĩnh

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
                    // Lấy ID học sinh đã lưu lúc đăng nhập (Mặc định là 1 nếu lỗi)
                    const studentId = localStorage.getItem('student_id') || 1;
                    
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
                            user_id: parseInt(studentId) // Lấy đúng ID của học sinh đang đăng nhập
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
    // 1. Kích hoạt tính năng Lắng nghe sự kiện Đăng nhập
    setupLogin();
    
    // 2. Bật nút tính năng Lá thư
    setupFeedbackButton();
    
    // Kiểm tra xem trước đó học sinh đã đăng nhập chưa (Tùy chọn nâng cao UI)
    const savedStudentId = localStorage.getItem('student_id');
    if (savedStudentId) {
        // Nếu đã từng đăng nhập, bỏ qua form login và vào thẳng app
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('main-app').style.display = 'block';
        fetchCourseData();
    }
});