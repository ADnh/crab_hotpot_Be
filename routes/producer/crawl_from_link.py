from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import time
import random

import subprocess
import os
from moviepy.editor import AudioFileClip


def random_sleep(time_1 = 5, time_2 = 8):
    # Tạo một số ngẫu nhiên trong khoảng 1 đến 5 giây
    time_to_sleep = random.uniform(time_1, time_2)
    time.sleep(time_to_sleep)

def create_browser(headless=False, disable_gpu=True):
    """
    Hàm tạo và khởi động trình duyệt Chrome với các tùy chọn.

    :param headless: Chạy trình duyệt ở chế độ ẩn (mặc định False).
    :param disable_gpu: Tắt GPU để tránh lỗi (mặc định True).
    :return: Đối tượng WebDriver của Chrome.
    """
    options = webdriver.ChromeOptions()
    
    # Chạy trình duyệt ở chế độ ẩn (nếu cần)
    if headless:
        options.add_argument("--headless")

    # Tắt GPU để tránh lỗi (mặc định bật)
    if disable_gpu:
        options.add_argument("--disable-gpu")
    
    # Mở trình duyệt Chrome
    browser = webdriver.Chrome(options=options)
    
    return browser

def wait_for_element(browser, xpath, timeout=30):
    """
    Chờ đợi một phần tử xuất hiện trên trang, tránh lỗi khi phần tử chưa tải xong, khi
    phần tử xuất hiện trước thời gian timeout, chương trình tiếp tục ngay lập tức. 
    Nếu sau timeout mà phần tử vẫn chưa xuất hiện, Selenium báo lỗi TimeoutException.
    
    :param browser: WebDriver của Chrome.
    :param xpath: Xpath của phần tử cần đợi.
    :param timeout: Số giây tối đa để đợi (mặc định là 10 giây).
    """
    WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def crawl_youtube_comments(browser, video_id, base_url, comment_xpath, time_1, time_2):
    """
    Hàm thu thập bình luận từ YouTube và lưu vào file Excel.
    
    :param browser: browser chorme
    :param video_id: ID của video YouTube cần thu thập bình luận.
    :param base_url: base url YouTube.
    :param comment_xpath: xpath comment YouTube.
    :param time_sleep: .
    
    
    :param scroll_pause: Thời gian dừng sau mỗi lần cuộn (mặc định 5 giây).
    :param headless: Chạy trình duyệt ở chế độ ẩn (mặc định False).
    :param output_file: Tên file Excel để lưu bình luận (mặc định "youtube_comments.xlsx").
    :return: Số lượng bình luận đã thu thập được.
    """
    url = base_url + video_id
    browser.get(url)

    # check lai
    # browser.maximize_window()
    # wait_for_element(browser, comment_xpath)
    time.sleep(5)  # Chờ trang tải thêm nội dung
    body = browser.find_element(By.TAG_NAME, 'body')
    # Cuộn xuống liên tục để tải tất cả bình luận
    last_height = 0
    while True:
        body.send_keys(Keys.END)  # Nhấn phím End để cuộn xuống cuối trang
        random_sleep(time_1, time_2)  # Chờ trang tải thêm nội dung

        # Lấy chiều cao mới của trang sau khi cuộn
        new_height = browser.execute_script("return document.documentElement.scrollHeight")

        # Nếu chiều cao không thay đổi => Không còn nội dung mới => Dừng cuộn
        if new_height == last_height:
            break

        last_height = new_height
    comments_elements = browser.find_elements(By.XPATH, comment_xpath)
    return comments_elements
    


def convert_webm_to_wav_and_mp3(input_path, wav_output=None, mp3_output=None):
    # Nếu không chỉ định đầu ra, tự sinh từ tên file gốc
    base_name = os.path.splitext(input_path)[0]
    if wav_output is None:
        wav_output = base_name + ".wav"
    if mp3_output is None:
        mp3_output = base_name + ".mp3"

    # Kiểm tra file đầu vào
    if not os.path.exists(input_path):
        return {
            "status_code": 500,
            "message": " File audio không tồn tại."
        }

    try:
        # Load audio từ file .webm
        audio = AudioFileClip(input_path)
        # Ghi ra file WAV
        audio.write_audiofile(wav_output)
        # Ghi ra file MP3
        audio.write_audiofile(mp3_output)
    except Exception as e:
        return {
            "status_code": 500,
            "message": " Lỗi chuyển đổi audio."
        }




def download_video_audio(video_id, resolutions = ["720", "480", "360", "240"], output_dir="temp"):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

    url = f"https://www.youtube.com/watch?v={video_id}"

    # Đầu ra: video (mp4) và audio (webm)
    video_out = os.path.join(output_dir, video_id + ".mp4")
    audio_out = os.path.join(output_dir, video_id + ".webm")
    wav_out = os.path.join(output_dir, video_id + ".wav")
    mp3_out = os.path.join(output_dir, video_id + ".mp3")
    
    # =========================
    # Tải video theo thứ tự ưu tiên: 720p → 480p → 360p
    # =========================
    video_downloaded = False
    for resolution in resolutions:
        try:
            subprocess.run([
                "yt-dlp",
                "-f", f"bestvideo[height={resolution}][ext=mp4]",
                "-o", video_out,
                url
            ], check=True)
            video_downloaded = True
            break  # Dừng khi tải thành công
        except subprocess.CalledProcessError:
            pass

    if not video_downloaded:
        return {
            "status_code": 404,
            "message": "Video không tồn tại hoặc không thể crawl hoặc Không thể tải video với độ phân giải 720p, 480p, 360p, 240p."
        }

    # =========================
    # Tải audio định dạng webm
    # =========================
    try:
        subprocess.run([
            "yt-dlp",
            "-f", "bestaudio[ext=webm]",
            "-o", audio_out,
            url
        ], check=True)
        convert_webm_to_wav_and_mp3(audio_out, wav_out, mp3_out)
    except subprocess.CalledProcessError as e:
        return {
            "status_code": 500,
            "message": "Lỗi khi tải audio."
        }
    return {
        "status_code": 200,
        "message": "Crawl thành công",
        "data": {
            "video_path": video_out,
            # "audio_path": audio_out,
            "wav_path": wav_out,
            "mp3_path": mp3_out
        }
    }
    
