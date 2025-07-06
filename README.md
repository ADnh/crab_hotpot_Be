
# crab_hotpot_Be

Just for fun :D

Mọi người làm nhớ lưu lại thư viện sử dụng để bổ sung vào requirements nhé

### Run terminal "python .\main.py"


# Phần crawler
## Thông tin
- **Cấu hình**: Có thể thay đổi một số config ở file api.py (thời gian giữa hai lần cuộn trang, COMMENT_XPATH, BASE_URL)
- **Response**: trả về theo định dạng json (status_code, message, data['comments', 'video_path', 'wav_path', 'mp3_path'])
- **Video có định dạng**: mp4, độ phân giải mặc định là 720p ( nếu video không hỗ trợ 720p thì sẽ tải về ưu tiên tải về 480 đến 360 đến 240)
- **File âm thanh**: gồm hai định dạng là .wav, .mp3
- **Thư mục lưu trữ**: ./temp (sau khi AI xử lý xong thì xóa các file trong /temp để giải phóng lưu lượng)
- **api crawl**: http://127.0.0.1:8000/crawl_apis/crawl/<id_video>