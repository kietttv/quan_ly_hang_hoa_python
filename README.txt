Run bằng cách chạy file main.py

Cấu trúc của dự án 
project/
│
├── resources/
│   ├── db/  
│   │    └── database.sqlite    # db
│   └── images/  
│       └── default_img.png     # images
│
├── models/                     # Chứa các model của dự án
│   ├── __init__.py             # File khởi tạo package
│   ├── database.py             # Kết nối cơ sở dữ liệu
│   ├── nhap_hang.py            # Model Nhập hàng
│   └── ban_hang.py             # Model Bán hàng
│
├── views/                      # Chứa giao diện (Tkinter)
│   ├── __init__.py             # File khởi tạo package
│   ├── main_view.py            # Giao diện chính của ứng dụng
│   ├── nhap_hang_view.py       # Giao diện nhập hàng
│   └── ban_hang_view.py        # Giao diện bán hàng
│
├── controllers/                # Chứa logic điều khiển (chuyển tiếp dữ liệu từ views tới models)
│   ├── __init__.py             # File khởi tạo package
│   ├── nhap_hang_controller.py # Logic điều khiển cho nhập hàng
│   └── ban_hang_controller.py  # Logic điều khiển cho bán hàng
│
├── utils/                      # Các tiện ích khác, ví dụ như xử lý ngày tháng, validation,...
│   ├── __init__.py             # File khởi tạo package
│   └── utils.py                # Các hàm tiện ích
│
├── config.py                   # File cấu hình chung (chẳng hạn như kết nối DB, cài đặt giao diện,...)
├── run.py                      # File khởi động chương trình
└── requirements.txt            # Các thư viện cần thiết cho dự án (tkinter, sqlite3,...)

