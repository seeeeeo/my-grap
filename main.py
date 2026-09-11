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

    # 영화명과 날짜가 없는 행 제거
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
# 첫 번째 그래프
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
    st.warning("선택한 영화의 데이터가 없습니다.")


# 그래프 해석
st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "날짜에 따라 선택한 영화의 일일 관객 수가 "
    "어떻게 변했는지 확인할 수 있습니다."
)


# --------------------------------------------------
# 선택한 영화 데이터 보기
# --------------------------------------------------
with st.expander("🔎 선택한 영화의 데이터 보기"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ==================================================
# SECTION 2
# ==================================================
st.markdown("---")
st.header("📌 2. 일관객 합계가 가장 큰 영화 TOP 5")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 영화 5편의 "
    "날짜별 관객 수를 비교합니다."
)


# --------------------------------------------------
# 영화별 전체 일관객 합계 계산
# --------------------------------------------------
movie_totals = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 상위 5편
top5_movies = movie_totals.head(5).index.tolist()


# --------------------------------------------------
# TOP 5 영화 데이터만 가져오기
# --------------------------------------------------
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()


# --------------------------------------------------
# 날짜별로 데이터 정리
# 없는 날짜는 0명으로 처리
# --------------------------------------------------

# 전체 기간의 날짜
all_dates = pd.date_range(
    start=df["날짜"].min(),
    end=df["날짜"].max(),
    freq="D"
)

# 영화 × 날짜 조합 만들기
movie_date = pd.MultiIndex.from_product(
    [top5_movies, all_dates],
    names=["영화명", "날짜"]
)

# 일관객 합계를 영화/날짜별로 계산
top5_daily = (
    top5_df.groupby(
        ["영화명", "날짜"],
        as_index=False
    )["일관객"]
    .sum()
)

# 모든 날짜를 채우기
top5_daily = (
    top5_daily
    .set_index(["영화명", "날짜"])
    .reindex(movie_date, fill_value=0)
    .reset_index()
)


# --------------------------------------------------
# 두 번째 그래프
# --------------------------------------------------
fig2 = px.line(
    top5_daily,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일일 관객 수(명)",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "<b>영화:</b> %{fullData.name}"
        "<br>"
        "<b>날짜:</b> %{x|%Y-%m-%d}"
        "<br>"
        "<b>관객수:</b> %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="관객 수 (명)",
    hovermode="x unified",
    height=600,
    legend_title="영화"
)

# 그래프 출력
st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# TOP 5 목록
# --------------------------------------------------
st.subheader("🏆 이 기간 일관객 합계 TOP 5")

top5_table = movie_totals.head(5).reset_index()
top5_table.columns = ["영화명", "기간 일관객 합계"]

top5_table["기간 일관객 합계"] = (
    top5_table["기간 일관객 합계"]
    .round()
    .astype(int)
)

st.dataframe(
    top5_table,
    use_container_width=True,
    hide_index=True
)


# 그래프 해석
st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "전체 기간 동안 관객 수가 가장 많았던 영화 5편의 "
    "날짜별 관객 수 변화를 한눈에 비교할 수 있습니다. "
    "그래프의 범례를 클릭하면 원하는 영화의 선을 "
    "켜거나 끌 수 있습니다."
)


# --------------------------------------------------
# SECTION 3
# --------------------------------------------------
st.markdown("---")
st.header("📌 3. 추가 예정 구역")

st.text(
    "앞으로 새로운 시간 관련 그래프가 "
    "이곳에 추가될 예정입니다."
)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** "
    "추가 그래프가 만들어지면 여기에 설명을 넣을 수 있습니다."
)
