import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 제목
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption(
    "KOBIS 일별 박스오피스 데이터를 바탕으로 "
    "시간의 흐름에 따른 영화 관객 수와 추이를 시각화합니다."
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

    df = pd.read_csv(url)

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 관객 수 숫자로 변환
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    ).fillna(0)

    # 영화명이 없는 행 제거
    df = df.dropna(subset=["영화명", "날짜"])

    return df


# 데이터 불러오기
try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# --------------------------------------------------
# SECTION 1
# --------------------------------------------------
st.markdown("---")
st.header("📌 1. 영화별 일별 관객 수 추이")

# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().unique()
)

# 영화 선택
selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    movie_list
)

# 선택한 영화 데이터
filtered_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)


# --------------------------------------------------
# 그래프
# --------------------------------------------------
if not filtered_df.empty:

    fig1 = px.line(
        filtered_df,
        x="날짜",
        y="일관객",
        title=f"'{selected_movie}' 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일일 관객 수(명)"
        },
        markers=True
    )

    fig1.update_traces(
        hovertemplate=(
            "<b>날짜:</b> %{x|%Y-%m-%d}"
            "<br>"
            "<b>관객수:</b> %{y:,}명"
            "<extra></extra>"
        )
    )

    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객 수 (명)",
        hovermode="x unified",
        height=550
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

else:
    st.warning(
        "선택한 영화의 데이터가 없습니다."
    )


# --------------------------------------------------
# 그래프 해석
# --------------------------------------------------
st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "날짜에 따라 선택한 영화의 일일 관객 수가 "
    "어떻게 변했는지 확인할 수 있습니다."
)


# --------------------------------------------------
# 데이터 확인
# --------------------------------------------------
with st.expander("🔎 선택한 영화의 데이터 보기"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# --------------------------------------------------
# SECTION 2
# --------------------------------------------------
st.markdown("---")
st.header("📌 2. 추가 예정 구역")

st.text(
    "앞으로 새로운 시간 관련 그래프가 "
    "이곳에 추가될 예정입니다."
)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "추가 그래프가 만들어지면 여기에 설명을 넣을 수 있습니다."
)
