import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# 한글 폰트 설정
def set_korean_font():
    """한글 폰트 설정 (맑은 고딕 또는 다른 한글 폰트 사용)"""
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows용
    plt.rcParams['axes.unicode_minus'] = False     # 마이너스(-) 기호 깨짐 방지

# 트리맵 생성 함수
def create_treemap(data):
    """
    주어진 데이터를 사용해 트리맵을 생성합니다.
    """
    set_korean_font()  # 한글 폰트 적용

    labels = [f"{dept}\n{prob}%" for dept, prob in data.items()]
    sizes = list(data.values())
    colors = plt.cm.Reds([prob / 100 for prob in sizes])  # 색상: 확률값에 따라 변화
    
    # 트리맵 그리기
    fig, ax = plt.subplots(figsize=(15, 10))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7, text_kwargs={'fontsize': 14})
    plt.axis('off')
    plt.title("부서별 확률 트리맵", fontsize=18, weight='bold')
    
    return fig

# tab3 함수
def display_tab3(csv_file):
    """
    Streamlit tab3 화면을 표시하는 함수. CSV 파일을 읽어 트리맵과 데이터프레임을 생성합니다.
    """
    st.markdown("## 모델 예측 결과: 의료 부서별 확률 트리맵")
    st.divider()

    # CSV 파일 업로드
    if csv_file is not None:
        # CSV 데이터를 읽어 데이터프레임 생성
        df = pd.read_csv(csv_file)

        # 데이터프레임을 딕셔너리로 변환 (컬럼명: '의료 부서', '확률 (%)')
        department_probs = dict(zip(df['의료 부서'], df['확률 (%)']))

        # 트리맵 시각화 버튼
        if st.button("트리맵 생성"):
            
            treemap, graph = st.tabs(["Treemap", "Data"])
            
            with treemap:
                container1 = st.container(border=True)
                with container1:
                    fig = create_treemap(department_probs)
                    st.pyplot(fig)
                    st.markdown("### 데이터 확인")
                   
                    st.data_editor(df,
                        column_config={
                            "확률 (%)": st.column_config.ProgressColumn(
                                "확률",
                                help="처리 확률을 나타냅니다",
                                format="%d%%",  # 퍼센트 형식
                                min_value=0,
                                max_value=100,
                            ),
                            "확인 여부": st.column_config.CheckboxColumn(
                                "확인",
                                help="처리 여부를 체크하세요",
                            ),
                             "check": st.column_config.CheckboxColumn(
                                "check",
                                help="가장 우선 항목 체크크",
                                default=False,
                            )
                        },
                        hide_index=True,  # 인덱스 숨기기
                        use_container_width=True  # 전체 폭 사용
                        )

            # 데이터프레임 표시
            with graph:
                container2 = st.container(border=True)
                with container2:
                    st.markdown("### 데이터 확인")
                    
                    st.bar_chart(df, x="의료 부서", y="확률 (%)",use_container_width=True)
              
    else:
        st.warning("CSV 파일을 업로드해주세요.")
