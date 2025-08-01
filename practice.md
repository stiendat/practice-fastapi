# Bài tập tuần 3: Xây dựng Backend cho Ứng dụng Quản lý Thư viện

# Bối cảnh dự án
Trong bài tập này, bạn sẽ đảm nhận vai trò xây dựng hệ thống backend cho một Ứng dụng Quản lý Thư viện. Mục tiêu là tạo ra một bộ API mạnh mẽ, cho phép người dùng (cụ thể là thủ thư) có thể quản lý hiệu quả các hoạt động cốt lõi của thư viện.

# Yêu cầu chức năng
Hệ thống backend cần đáp ứng được 3 nhóm chức năng chính sau:

## Quản lý Sách:

* Thêm, xóa, sửa và xem thông tin chi tiết của từng cuốn sách (ví dụ: tên sách, tác giả, năm xuất bản).

* Theo dõi và cập nhật số lượng sách hiện có trong thư viện.

## Quản lý Người mượn:

* Thêm, xóa, sửa và xem thông tin của người mượn sách (ví dụ: họ tên, email, số điện thoại).

## Quản lý Mượn/Trả sách:

* Ghi nhận thông tin khi một người dùng mượn sách (người mượn là ai, sách nào được mượn, ngày mượn, ngày dự kiến trả).

* Ghi nhận thông tin khi sách được trả, đồng thời cập nhật lại số lượng sách trong kho.

## Dữ liệu cung cấp
Trong thư mục test_data/, có một file .csv chứa dữ liệu mẫu về một số đầu sách. Bạn sẽ sử dụng file này để nhập dữ liệu ban đầu cho hệ thống của mình.

# Nhiệm vụ cần thực hiện
## Nhiệm vụ 1: Thiết kế Data Model
Dựa trên các yêu cầu chức năng, hãy thiết kế một data model cho cơ sở dữ liệu quan hệ.

Vẽ sơ đồ ERD (Entity Relationship Diagram) để mô tả cấu trúc và mối quan hệ giữa các bảng.

## Nhiệm vụ 2: Xây dựng Cơ sở dữ liệu và Import dữ liệu
Sử dụng SQLAlchemy, định nghĩa các model tương ứng với data model bạn đã thiết kế.

Thiết lập kết nối tới cơ sở dữ liệu (sử dụng PostgreSQL).

Viết một script Python để đọc dữ liệu từ file .csv và import vào bảng Books trong database của bạn.

## Nhiệm vụ 3: Xây dựng các API cơ bản
Sử dụng FastAPI, hãy xây dựng các API để thực hiện các chức năng đã nêu. Dưới đây là một số gợi ý về các endpoint cần có:

API Quản lý Sách:

* GET /books: Lấy danh sách tất cả các sách.

* GET /books/{book_id}: Lấy thông tin chi tiết của một sách.

* POST /books: Thêm một sách mới.

API Quản lý Người mượn:

* GET /users: Lấy danh sách người mượn.

* POST /users: Thêm một người mượn mới.

API Mượn/Trả sách:

* POST /rent: Tạo một bản ghi mượn sách mới (yêu cầu user_id và book_id).

* POST /return: Ghi nhận việc trả sách (yêu cầu book_id hoặc rental_id).

# Tiêu chí đánh giá
* Data model được thiết kế hợp lý, rõ ràng và đáp ứng đủ yêu cầu.

* Dữ liệu từ file .csv được import vào database thành công.

* Các API hoạt động đúng chức năng, tuân thủ theo các nguyên tắc RESTful.

* Code được tổ chức sạch sẽ, dễ đọc và có cấu trúc thư mục rõ ràng.
