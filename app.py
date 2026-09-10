from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

# ==========================================
# CẤU HÌNH APPSHEET API (Dành cho Dashboard)
# ==========================================
APP_ID = "3243eaeb-1306-4893-972e-2f5860f86759"
ACCESS_KEY = "V2-ANsul-mY9Y4-hrLbN-BDAzm-nKdyz-NYz01-knObY-PJfqw"

def get_appsheet_data(table_name):
    """Hàm gọi API của AppSheet để đọc dữ liệu (Action: Find)"""
    url = f"https://api.appsheet.com/api/v2/apps/{APP_ID}/tables/{table_name}/Action"
    headers = {
        "ApplicationAccessKey": ACCESS_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "Action": "Find",
        "Properties": {
            "Locale": "vi-VN",
            "Timezone": "SE Asia Standard Time"
        },
        "Rows": []
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Lỗi khi đọc bảng {table_name}:", response.text)
        return []
    
# Màn hình 1: Chọn dịch vụ (Landing Page)
@app.route('/')
def index():
    return render_template('index.html')
# Màn hình Đăng nhập chọn vai trò
@app.route('/login')
def login():
    return render_template('login.html')
# Màn hình 2: Đặt lịch hẹn

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        patient_name = request.form.get('patient_name')
        doctor_email = request.form.get('doctor_email') # Nhận email bác sĩ được chọn
        date = request.form.get('date')
        time = request.form.get('time')
        symptoms = request.form.get('symptoms')
        
        # Code lưu dữ liệu (POST lên AppSheet) sẽ nằm ở đây sau này
        
        return redirect(url_for('tracking', patient=patient_name))
    
    # --- PHẦN THÊM MỚI ---
    # Kéo dữ liệu Users từ AppSheet và lọc ra Bác sĩ
    users = get_appsheet_data("Users")
    doctors = [user for user in users if user.get('Role') == 'Bác sĩ']
    
    service_type = request.args.get('type', 'home_care')
    # Truyền biến doctors sang HTML
    return render_template('booking.html', service_type=service_type, doctors=doctors)

# Màn hình 3: Theo dõi ca khám
@app.route('/tracking')
def tracking():
    patient_name = request.args.get('patient', 'Bà Mai')
    return render_template('tracking.html', patient=patient_name)

# ==========================================
# ROUTE MỚI: MÀN HÌNH DEMO BÁC SĨ (Kéo từ AppSheet)
# ==========================================
@app.route('/demo-dashboard')
def demo_dashboard():
    # 1. Kéo dữ liệu qua API từ 2 bảng
    users = get_appsheet_data("Users")
    appointments = get_appsheet_data("Appointments")
    
    # 2. Lọc danh sách Bác sĩ
    doctors = [user for user in users if user.get('Role') == 'Bác sĩ']
    
    # 3. Đẩy lên file HTML
    return render_template('demo_dashboard.html', doctors=doctors, appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True, port=5000)