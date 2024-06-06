import streamlit as st
import pandas as pd
import time
from streamlit_text_rating.st_text_rater import st_text_rater # pip install streamlit-text-rating
from streamlit_chat import message # pip install streamlit-chat
from PIL import Image

def read_data(file):
    raw = pd.read_csv(file)
    return raw

rating = read_data('./naver_and_kakao_star.csv')
kakao_map_review = read_data('./kakao_restaurant_5.csv')
naver_map_review = read_data('./naver_restaurant_5.csv')
kakao_map_review=kakao_map_review.reset_index()
naver_map_review=naver_map_review.reset_index()

def sidebar_filters():
    st.title("평점 범위를 선택하세요.")
    st.write("평점을 선택하면 해당하는 음식점을 추천해드립니다.")

    slider = st.columns(2)

    with slider[0]:
        slider_naver = st.slider("네이버의 평점을 선택하세요", 0.0, 5.0, (0.0, 5.0), step=0.1)

    with slider[1]:
        slider_kakao = st.slider("카카오의 평점을 선택하세요", 0.0, 5.0, (0.0, 5.0), step=0.1)

    start_button = st.button("적용하기")

    if start_button or "filtered_df" in st.session_state:
        if start_button:
            filtered_df = rating[(rating['네이버 평점'] >= slider_naver[0]) & (rating['네이버 평점'] <= slider_naver[1])]
            filtered_df = filtered_df[(filtered_df['카카오 평점'] >= slider_kakao[0]) & (filtered_df['카카오 평점'] <= slider_kakao[1])]

            st.session_state.filtered_df = filtered_df
        else:
            filtered_df = st.session_state.filtered_df

        if "selected_restaurant" not in st.session_state:
            st.session_state.selected_restaurant = ''

        if len(filtered_df) > 0:
            restaurant_list = filtered_df['음식점'].tolist()
            selected_restaurant = st.selectbox("필터링된 음식점을 선택하세요", restaurant_list)
            st.session_state.selected_restaurant = selected_restaurant
            st.write(f"선택한 음식점: {st.session_state.selected_restaurant}")
        else:
            st.write("조건에 맞는 음식점이 없습니다.")
    else:
        st.write("조건을 설정하고 '적용하기'를 눌러주세요.")

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



def main():
    with st.sidebar:
        sidebar_filters()

    restaurant_name='미선택'

    # if "selected_restaurant" in st.session_state and st.session_state.selected_restaurant:
    #     restaurant_data = rating[rating["음식점"] == st.session_state.selected_restaurant].iloc[0]
    #     #show_restaurant_info(restaurant_data)
    #     st.divider()
    #     st_text_rater(text=f"{st.session_state.selected_restaurant}를 평가해주세요")
    # else:
    #     st.title("음식점을 선택해주세요")
    #     st.write("사이드바에서 조건을 설정하고 '적용하기' 버튼을 눌러 음식점을 선택하세요.")

    #sidebar에서 선택한 음식점이름 가져오기

    if "selected_restaurant" not in st.session_state:
        st.session_state.selected_restaurant = ''

    if st.session_state.selected_restaurant:
        restaurant_name = st.session_state.selected_restaurant
    else:
        st.title("아직 선택되지 않았습니다.")

    # 페이지 제목
    st.title("🍽️"+restaurant_name)
    st.write("")

    path='img/'+restaurant_name

    # 이미지 열기
    image1 = Image.open(path+'/img1.jpg')
    image2 = Image.open(path+'/img2.jpg')

    # 이미지를 동일한 크기로 조정
    target_size = (300, 300)
    image1_resized = resize_image(image1, target_size)
    image2_resized = resize_image(image2, target_size)

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

    kakao = kakao_map_review[kakao_map_review['음식점'] == restaurant_name]
    kakao=kakao.reset_index()
    naver = naver_map_review[naver_map_review['음식점'] == restaurant_name]
    naver=naver.reset_index()

    tab1, tab2, tab3 = st.tabs(["1~4", "4~8", "8~12"])

    with tab1:
        for i in range(0, 4):
            message("naver\n" + naver['리뷰'][i])
            message("kakao\n" + kakao['리뷰'][i], is_user=True)

    with tab2:
        for i in range(4, 8):
            message("naver\n" + naver['리뷰'][i])
            message("kakao\n" + kakao['리뷰'][i], is_user=True)

    with tab3:
        for i in range(8, 12):
            message("naver\n" + naver['리뷰'][i])
            message("kakao\n" + kakao['리뷰'][i], is_user=True)

    st.divider()

    # 음식집 평가
    st_text_rater(text=f"{restaurant_name}를 평가해주세요")

if __name__ == "__main__":
    main()