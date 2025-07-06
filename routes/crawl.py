### crawl apis
from fastapi import APIRouter 
from fastapi.responses import JSONResponse

import sys
import os
your_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'producer'))
sys.path.append(your_file_path)
from crawl_from_link import download_video_audio, create_browser, crawl_youtube_comments

COMMENT_XPATH = '//*[@id="content-text"]'
BASE_URL = 'https://www.youtube.com/watch?v='

# thời gian nghỉ giữa hai lần cuộn trang
TIME_1 = 2
TIME_2 = 5

router = APIRouter()

@router.get("/crawl/{video_id}")
async def crawl(video_id: str):
    print(video_id)
    
    if not video_id:
        return JSONResponse(status_code=400, content={'status_code': 400, 'message': 'Missing video_id parameter'})
    
    # Download video & audio
    response = download_video_audio(video_id)
    status_code = response.get('status_code', 500)

    if status_code == 200:
        # Crawl comments
        browser = create_browser(headless=True, disable_gpu=True)
        comments_elements = crawl_youtube_comments(
            browser=browser,
            video_id=video_id,
            base_url=BASE_URL,
            comment_xpath=COMMENT_XPATH,
            time_1=TIME_1,
            time_2=TIME_2
        )
        comment_texts = [comment.text for comment in comments_elements]
        response['data']['comments'] = comment_texts
        browser.quit()

    return JSONResponse(status_code=status_code, content=response)