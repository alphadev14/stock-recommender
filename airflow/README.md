# 🚀 Airflow Local Setup with Docker Compose

Đây là hướng dẫn để khởi chạy Apache Airflow phiên bản `2.9.1` sử dụng `LocalExecutor` bằng `Docker Compose`.

---

## 📁 Cấu trúc thư mục

Trước khi bắt đầu, đảm bảo bạn có cấu trúc sau trong project:

```
.
├── docker-compose.yaml
├── dags/         # chứa các DAG (workflow)
├── logs/         # log của Airflow
└── plugins/      # plugin custom (nếu có)
```

> 📌 **Ghi chú**: Nếu các thư mục `dags`, `logs`, `plugins` chưa tồn tại, hãy tạo bằng:

```bash
mkdir -p dags logs plugins
```

---

## 🐳 Khởi chạy Airflow với Docker Compose

### 1️⃣ Khởi tạo cơ sở dữ liệu

```bash
docker compose run airflow-webserver airflow db init
```

> 📝 Ghi chú: Lệnh này sẽ tạo database schema cần thiết cho Airflow (PostgreSQL đã cấu hình sẵn trong file `docker-compose.yaml`).

---

### 2️⃣ Tạo tài khoản người dùng admin

```bash
docker compose run airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

> 🧠 Ghi chú:
>
> - `--role Admin`: bạn cần role này để truy cập toàn bộ chức năng của Airflow UI.
> - Bạn có thể đổi thông tin user nếu muốn.

---

### 3️⃣ Khởi động Airflow (webserver, scheduler, postgres)

```bash
docker compose up -d
```

> ⏳ Mất vài giây để webserver khởi động, bạn có thể kiểm tra logs bằng:

```bash
docker compose logs -f airflow-webserver
```

---

## 🌐 Truy cập Airflow

Mở trình duyệt và truy cập địa chỉ:

```
http://localhost:8081
```

> 🔐 Đăng nhập bằng tài khoản bạn đã tạo ở bước 2.

---

## ⚙️ Tùy chỉnh cổng web UI (tuỳ chọn)

Trong file `docker-compose.yaml`, bạn có thể thay đổi dòng:

```yaml
ports:
  - "8081:8080"
```

Ví dụ muốn đổi sang port `9090`, sửa thành:

```yaml
- "9090:8080"
```

> ✅ Truy cập sẽ là: `http://localhost:9090`

---

## 🧹 Dọn dẹp (nếu cần reset lại)

Dừng và xóa tất cả container, network, volume:

```bash
docker compose down -v
```

---

## 🧪 Kiểm tra container

Xem trạng thái các dịch vụ đang chạy:

```bash
docker compose ps
```

---

## 📬 Liên hệ & Khắc phục sự cố

Nếu bạn gặp lỗi khi khởi chạy, hãy thử:

- Kiểm tra logs:
  ```bash
  docker compose logs
  ```
- Đảm bảo port không bị trùng (8081 hoặc 9090)
- Thử reset bằng lệnh:
  ```bash
  docker compose down -v
  ```

---

Chúc bạn cài đặt thành công Apache Airflow 🎉
