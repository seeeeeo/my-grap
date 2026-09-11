import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 제목 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("KOBIS 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수와 추이를 시각화합니다.")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> datetime)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ==============================================================================
# SECTION 1: 개별 영화의 일별 관객 수 추이
# ==============================================================================
st.markdown("---")
st.header("📌 1. 영화별 일별 관객 수 추이")

# 영화 목록 추출 (영화명 기준 오름차순 정렬)
movie_list = sorted(df['영화명'].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    movie_list,
    index=0
)

# 선택한 영화 데이터 필터링
filtered_df = df[df['영화명'] == selected_movie].sort_values('날짜')

if not filtered_df.empty:
    # Plotly 선 그래프 생성
    fig1 = px.line(
        filtered_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True,
        hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d'}
    )
    
    # 툴팁 및 스타일 레이아웃 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
    )
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객 수 (명)",
        hovermode="x unified"
    )

    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

# 사용자 작성 영역: 이 그래프로 알 수 있는 것
st.info("💡 **이 그래프로 알 수 있는 것:** *(여기에 해석을 작성하세요)*")


# ==============================================================================
# SECTION 2: (추가 예정 구역)
# ==============================================================================
st.markdown("---")
st.header("📌 2. [추가 예정 구역]")
st.text("앞으로 새로운 시간 관련 그래프가 이곳에 추가될 예정입니다.")

# 사용자 작성 영역 예시
st.info("💡 **이 그래프로 알 수 있는 것:** *(여기에 해석을 작성하세요)*")
