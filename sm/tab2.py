import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
def set_korean_font():
    """한글 폰트 설정 (맑은 고딕 또는 다른 한글 폰트 사용)"""
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows용
    plt.rcParams['axes.unicode_minus'] = False     # 마이너스(-) 기호 깨짐 방지

# 확률에 따라 색상을 설정하는 함수
def get_background_color(probability):
    if probability > 80:
        return "#FF5050"  # 빨간색 
    elif 50 <= probability <= 80:
        return "#FFFF66"  # 노란색
    else:
        return "#00CC66"  # 초록색

# 컬럼과 바 차트 생성 함수
def create_expander_and_chart(df: pd.DataFrame):
  
    set_korean_font()  # 한글 폰트 설정
    
    df["확인여부"] = df["확률"][:] >= 50


    procedure, rank = st.tabs(["Treemap", "Data"])
    with procedure:
        with st.container(border=True):
            st.markdown("### 처리 확률 타일")
           # 각 행에 대해 컨테이너 생성
            for idx, row in df.iterrows():
                key = row["처리 종류"]
                value = row["확률"]
                
                # 배경색 가져오기
                bg_color = get_background_color(value)

                # HTML로 스타일링된 컨테이너와 체크박스 추가
             
                st.markdown(
                    f"""
                    <div style="
                        background-color: {bg_color};
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 10px;
                        border: 1px solid #ddd;
                    ">
                        <h4 style="margin: 10;">💉  <b>{key}</b>:                   {value}% 🎯</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                on = st.toggle("확인",key=f"checkbox_{idx}")
                if on:
                    st.write("Procedure check!")
              
                   

            ## 데이터 프레임임       
            st.data_editor(df,
                    column_config={
                        "확률": st.column_config.ProgressColumn(
                            "확률",
                            help="처리 확률을 나타냅니다",
                            format="%d%%",  # 퍼센트 형식
                            min_value=0,
                            max_value=100,
                        ),
                        "확인여부": st.column_config.CheckboxColumn(
                            "확인",
                            help="처리 여부를 체크하세요",
                        ),
                    },
                    hide_index=True,  # 인덱스 숨기기
                    use_container_width=True  # 전체 폭 사용
                    )

    with rank:
        with st.container(border=True)    :
            # 두 번째 Expander: Bar Chart 시각화
            st.bar_chart(df, x="처리 종류", y="확률", use_container_width=True)

# tab2 함수
def display_tab2(csv_file):
    """
    Streamlit tab2 화면을 표시하는 함수. CSV 파일을 읽어 타일과 Bar Chart를 Expander로 나란히 배치합니다.
    """
    st.markdown("## 처리 확률과 Bar Chart 시각화")
    st.divider()

    # CSV 파일 읽기
    if csv_file is not None:  
        df = pd.read_csv(csv_file)

        # 컬럼명 검증
        if "처리 종류" in df.columns and "확률" in df.columns:
            create_expander_and_chart(df)
        else:
            st.error("CSV 파일에 '처리 종류'와 '확률' 컬럼이 필요합니다.")
    else:
        st.warning("CSV 파일을 업로드해주세요.")
