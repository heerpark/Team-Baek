import streamlit as st
import pandas as pd
import time
from streamlit_text_rating.st_text_rater import st_text_rater # pip install streamlit-text-rating
from streamlit_chat import message # pip install streamlit-chat
from PIL import Image

# 데이터 읽어오기
def read_data(file):
    raw = pd.read_csv(file)
    return raw

# 이미지 크기 조정
def resize_image(image, size):
    return image.resize(size)

# 사이드바 필터
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

        if len(filtered_df) > 0:
            restaurant_list = filtered_df['음식점'].tolist()
            # 음식점 이름 옆에 평점 추가
            display_list = [f"{restaurant} \n (🟢: {naver}점, 🟡: {kakao}점)" for restaurant, naver, kakao in zip(filtered_df['음식점'], filtered_df['네이버 평점'], filtered_df['카카오 평점'])]   
            st.write("필터링된 음식점 중 보고싶은 가게를 선택하세요")
            selected_display = st.selectbox("🟢: 네이버 평점, 🟡: 카카오 평점", display_list, index=None, placeholder="음식점")

            # 선택된 display_list 항목에서 음식점 이름만 추출
            if selected_display:
                selected_restaurant_index = display_list.index(selected_display)
                selected_restaurant = restaurant_list[selected_restaurant_index]
                
                st.session_state.selected_restaurant = selected_restaurant
                st.write(f"선택한 음식점: {st.session_state.selected_restaurant}")
        else:
            st.write("조건에 맞는 음식점이 없습니다.")
    else:
        st.write("조건을 설정하고 '적용하기'를 눌러주세요.")

st.markdown(
    """
    <style>
        div:nth-child(1) > .stProgress > div > div > div > div {
            background-color: rgb(16 87 234 / 55%);
        }
        div:nth-child(2) > .stProgress > div > div > div > div {
            background-color: rgb(0 128 0 / 62%);
        }

        div:nth-child(3) > .stProgress > div > div > div > div {
            background-color: rgb(255 0 0 / 70%);
        }
    </style>""",
    unsafe_allow_html=True,
)

# 감성 점수 시각화
def show_sentimental_score(restaurant_name, category):
    restaurant_df = sent_rating[(sent_rating['restaurant'] == restaurant_name)]
    category_df = restaurant_df[restaurant_df['category'] == category]

    naver_score = category_df[category_df['platform'] == 'naver']['positivity'].values[0]
    kakao_score = category_df[category_df['platform'] == 'kakao']['positivity'].values[0]
    blog_score = category_df[category_df['platform'] == 'blog']['positivity'].values[0]

    progress_text1 = f"네이버 리뷰에서 분석한 {category}에 대한 감성 점수에요 :blue-background[**{round(naver_score)}**]"
    progress_text2 = f"카카오 리뷰에서 분석한 {category}에 대한 감성 점수에요 :green-background[**{round(kakao_score)}**]"
    progress_text3 = f"블로그 리뷰에서 분석한 {category}에 대한 감성 점수에요 :red-background[**{round(blog_score)}**]"

    my_bar1 = st.progress(0, text=progress_text1)
    my_bar2 = st.progress(0, text=progress_text2)
    my_bar3 = st.progress(0, text=progress_text3)

    my_bar1.empty()
    my_bar2.empty()
    my_bar3.empty()

    for percent_complete in range(100):
        time.sleep(0.005)
        if (percent_complete < round(naver_score)):
            my_bar1.progress(percent_complete + 1, text=progress_text1)
        if (percent_complete < round(kakao_score)):
            my_bar2.progress(percent_complete + 1, text=progress_text2)
        if (percent_complete < round(blog_score)):
            my_bar3.progress(percent_complete + 1, text=progress_text3)

# 리뷰 요약 가져오기
def get_summary(restaurant_name, category):
    restaurant_summary = summary[(summary['restaurant'] == restaurant_name)]
    value = restaurant_summary[restaurant_summary['category'] == category]['summary'].values[0]
    return value


# 데이터 읽어오기
rating = read_data('data/naver_and_kakao_star.csv')
kakao_map_review = read_data('data/kakao_restaurant_5.csv').reset_index()
naver_map_review = read_data('data/naver_restaurant_5.csv').reset_index()
summary = read_data('data/summary_category_update.csv')
sent_rating = read_data('data/clova_sent_rating.csv')

# 메인
def main():
    with st.sidebar:
        sidebar_filters()

    if "selected_restaurant" not in st.session_state:
        st.session_state.selected_restaurant = ''

    if st.session_state.selected_restaurant:
        restaurant_name = st.session_state.selected_restaurant

        # 페이지 제목
        st.title("🍽️ "+restaurant_name)

        ifno = st.columns(4)
        with ifno[0]:
            st.markdown("<p style='font-weight: bold'>" + f"🟢 네이버 평점: {rating[rating['음식점'] == restaurant_name]['네이버 평점'].values[0]} " + "</p>", unsafe_allow_html=True)
        with ifno[1]:
            st.markdown("<p style='font-weight: bold'>" + f"🟡 카카오 평점: {rating[rating['음식점'] == restaurant_name]['카카오 평점'].values[0]}" + "</p>", unsafe_allow_html=True)
        st.write("")

        path='img/'+restaurant_name 

        try: 
            # 이미지 열기
            image1 = Image.open(path+'/img1.png')
            image2 = Image.open(path+'/img2.png')

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
            tabs = st.tabs(["😋맛", "🙋서비스", "💰가격", "🌌분위기"])

            with tabs[0]:
                show_sentimental_score(restaurant_name, '맛')
                container = st.container(border=True, height=200)
                container.write(f"🤖인공지능이 요약한 맛에 대한 리뷰에요🤖\n\n {get_summary(restaurant_name, '맛')}")

            with tabs[1]:
                show_sentimental_score(restaurant_name, '서비스')
                container = st.container(border=True, height=200)
                container.write(f"🤖인공지능이 요약한 서비스에 대한 리뷰에요🤖\n\n {get_summary(restaurant_name, '서비스')}")

            with tabs[2]:
                show_sentimental_score(restaurant_name, '가격')
                container = st.container(border=True, height=200)
                container.write(f"🤖인공지능이 요약한 가격에 대한 리뷰에요🤖\n\n {get_summary(restaurant_name, '가격')}")

            with tabs[3]:
                show_sentimental_score(restaurant_name, '분위기')
                container = st.container(border=True, height=200)
                container.write(f"🤖인공지능이 요약한 분위기에 대한 리뷰에요🤖\n\n {get_summary(restaurant_name, '분위기')}")
            st.write("")

            kakao = kakao_map_review[kakao_map_review['음식점'] == restaurant_name].reset_index()
            naver = naver_map_review[naver_map_review['음식점'] == restaurant_name].reset_index()

            tab1, tab2, tab3 = st.tabs(["1~4", "5~8", "9~12"])

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

        except FileNotFoundError:
            pass

if __name__ == "__main__":
    main()
