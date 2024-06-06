import streamlit as st
import pandas as pd
import time
from streamlit_text_rating.st_text_rater import st_text_rater # pip install streamlit-text-rating
from streamlit_chat import message # pip install streamlit-chat
from PIL import Image


# 가게 이름
restaurant_name = "하이레\n\n"

def show_sentimental_score(category, naver_score, kakao_score, blog_score):
    progress_text1 = f"네이버 리뷰에서 분석한 {category}에 대한 감성 점수에요"
    progress_text2 = f"카카오 리뷰에서 {category}에 대한 분석한 감성 점수에요"
    progress_text3 = f"블로그 리뷰에서 {category}에 대한 분석한 감성 점수에요"

    my_bar1 = st.progress(0, text=progress_text1)
    my_bar2 = st.progress(0, text=progress_text2)
    my_bar3 = st.progress(0, text=progress_text3)

    my_bar1.empty()
    my_bar2.empty()
    my_bar3.empty()
    for percent_complete in range(100):
        time.sleep(0.005)
        if (percent_complete < naver_score):
            my_bar1.progress(percent_complete + 1, text=progress_text1)
        if (percent_complete < kakao_score):
            my_bar2.progress(percent_complete + 1, text=progress_text2)
        if (percent_complete < blog_score):
            my_bar3.progress(percent_complete + 1, text=progress_text3)

def resize_image(image, size):
    return image.resize(size)

# 이미지 열기
image1 = Image.open('img/img1.png')
image2 = Image.open('img/img2.png')

# 이미지를 동일한 크기로 조정
target_size = (300, 300)
image1_resized = resize_image(image1, target_size)
image2_resized = resize_image(image2, target_size)


def main():
    # 페이지 제목
    st.title("🍽️"+restaurant_name)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image1_resized, use_column_width=True)
    with col2:
        st.image(image2_resized, use_column_width=True)
    st.write("")

    # Ai 분석결과 시각화
    tabs = st.tabs(["😋맛", "🙋서비스", "🧹청결", "🌌분위기"])

    with tabs[0]:
        show_sentimental_score('맛', 80, 90, 100)
        container = st.container(border=True, height=200)
        container.write("🤖인공지능이 요약한 맛에 대한 리뷰에요🤖\n\n하이레의 돈까스는 진짜 너무맛있어요. 특히 안심은 진짜 넘사입니다.")

    with tabs[1]:
        show_sentimental_score('서비스', 30, 10, 50)
        container = st.container(border=True, height=200)
        container.write("🤖인공지능이 요약한 서비스에 대한 리뷰에요🤖\n\n하이레는 사장님들 서비스가 장난이 아니에요")

    with tabs[2]:
        show_sentimental_score('청결', 80, 90, 80)
        container = st.container(border=True, height=200)
        container.write("🤖인공지능이 요약한 청결에 대한 리뷰에요🤖\n\n하이레 사장님들이 맨날 청소하더라고요 !! 믿고 갑니다.")

    with tabs[3]:
        show_sentimental_score('분위기', 100, 90, 100)
        container = st.container(border=True, height=200)
        container.write("🤖인공지능이 요약한 분위기에 대한 리뷰에요🤖\n\n하이레 들어온 순간 여기는 광운대가 아니라 오사카")
    st.write("")

    # 댓글
    tab1, tab2, tab3 = st.tabs(["1~5", "5~10", "10~15"])

    with tab1:
        for i in range(0, 3):
            message("naver" + str(i))
            message("kakao" + str(i), is_user=True)

    with tab2:
        for i in range(3, 6):
            message("naver" + str(i))
            message("kakao" + str(i), is_user=True)

    with tab3:
        for i in range(6, 9):
            message("naver" + str(i))
            message("kakao" + str(i), is_user=True)

    st.divider()

    # 음식집 평가
    st_text_rater(text=f"{restaurant_name}를 평가해주세요")


if __name__ == "__main__":
    main()