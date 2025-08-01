erDiagram
    BOOKS {
        int id PK "Mã sách (Khóa chính)"
        string ISBN "Mã ISBN"
        string title "Tên sách"
        string author "Tác giả"
        int publication_year "Năm xuất bản"
        string publisher "Nhà xuất bản"
        string image_url_s "Ảnh bìa cỡ nhỏ"
        string image_url_m "Ảnh bìa cỡ trung bình"
        string image_url_l "Ảnh bìa cỡ lớn"
        timestamp created_at "Thời điểm tạo"
        timestamp modified_at "Thời điểm cập nhật cuối"
    }

    INVENTORY {
        int id PK "Mã tồn kho"
        int book_id FK "Tham chiếu đến sách"
        int total_copies "Tổng số bản sách"
        int available_copies "Số bản hiện còn"
        int borrowed_copies "Số bản đang mượn"
        int lost_copies "Số bản đã mất"
        int damaged_copies "Số bản hỏng"
        timestamp created_at "Thời điểm tạo"
        timestamp modified_at "Thời điểm cập nhật cuối"
    }

    BOOK_COPIES {
        int id PK "Mã bản sao sách"
        int book_id FK "Tham chiếu sách gốc"
        enum status "available / borrowed / lost / damaged"
        timestamp created_at "Thời điểm tạo"
        timestamp modified_at "Thời điểm cập nhật cuối"
    }

    USERS {
        int id PK "Mã người mượn"
        string name "Họ và tên"
        string email UK "Email (Duy nhất)"
        string phone_number "Số điện thoại"
        timestamp created_at "Thời điểm tạo"
        timestamp modified_at "Thời điểm cập nhật cuối"
    }

    RENTALS {
        int id PK "Mã lượt mượn"
        int user_id FK "Người mượn"
        datetime rental_date "Ngày mượn"
        datetime due_date "Ngày dự kiến trả"
        datetime return_date "Ngày trả thực tế (nullable)"
        timestamp created_at "Thời điểm tạo"
        timestamp modified_at "Thời điểm cập nhật cuối"
    }

    RENTAL_ITEMS {
        int id PK "Mã chi tiết mượn"
        int rental_id FK "Thuộc lượt mượn"
        int book_copy_id FK "Bản sao được mượn"
        timestamp created_at "Thời điểm tạo"
    }

    BOOKS ||--o{ BOOK_COPIES : "gồm"
    BOOKS ||--|| INVENTORY : "quản lý tồn kho"
    USERS ||--o{ RENTALS : "thực hiện"
    RENTALS ||--o{ RENTAL_ITEMS : "gồm các"
    BOOK_COPIES ||--o{ RENTAL_ITEMS : "được mượn trong"


