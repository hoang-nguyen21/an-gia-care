from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Màn hình 1: Chọn dịch vụ (Landing Page)
@app.route('/')
def index():
    return render_template('index.html')

# Màn hình 2: Đặt lịch hẹn
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Ở đây bạn có thể bắt dữ liệu form để lưu vào database
        service_type = request.form.get('service_type')
        patient_name = request.form.get('patient_name')
        date = request.form.get('date')
        time = request.form.get('time')
        symptoms = request.form.get('symptoms')
        
        # Sau khi đặt thành công, chuyển sang màn hình theo dõi
        return redirect(url_for('tracking', patient=patient_name))
    
    # Lấy loại dịch vụ từ URL (nếu có)
    service_type = request.args.get('type', 'home_care')
    return render_template('booking.html', service_type=service_type)

# Màn hình 3: Theo dõi ca khám
@app.route('/tracking')
def tracking():
    patient_name = request.args.get('patient', 'Bà Mai')
    return render_template('tracking.html', patient=patient_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)