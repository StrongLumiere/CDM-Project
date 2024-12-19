import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
# from streamlit_aggrid import AgGrid, GridOptionsBuilder
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
# 환자 데이터
patient_data = {
    "ID": [101, 102, 103],  # 환자 ID 목록
    "Name": ["환자A", "환자B", "환자C"],  # 환자 이름 (선택 사항)
    "Visits": [
        [  # 환자 101의 방문 기록
            {"날짜": "2024-04-01", "입원시간": "10:30", "퇴원시간": "13:00", "ktas": "Level 1",
             "HR": [72, 75, 78], "SBP": [120, 122, 124], "DBP": [80, 82, 84], "DRUG": ["Drug A", "Drug B"]},
            {"날짜": "2024-05-15", "입원시간": "09:00", "퇴원시간": "11:30", "ktas": "Level 2",
             "HR": [70, 73, 76], "SBP": [118, 120, 122], "DBP": [78, 80, 82], "DRUG": ["Drug C"]}
        ],
        [  # 환자 102의 방문 기록
            {"날짜": "2024-04-02", "입원시간": "12:15", "퇴원시간": "15:00", "ktas": "Level 2",
             "HR": [95, 98, 100], "SBP": [150, 148, 145], "DBP": [90, 88, 85], "DRUG": ["Drug D"]},
            {"날짜": "2024-06-20", "입원시간": "14:00", "퇴원시간": "16:45", "ktas": "Level 3",
             "HR": [90, 92, 95], "SBP": [140, 138, 135], "DBP": [85, 83, 80], "DRUG": ["Drug E", "Drug F"]}
        ],
        [  # 환자 103의 방문 기록
            {"날짜": "2024-04-03", "입원시간": "14:45", "퇴원시간": "17:30", "ktas": "Level 3",
             "HR": [88, 85, 82], "SBP": [130, 128, 126], "DBP": [85, 83, 81], "DRUG": ["Drug H", "Drug I"]}
        ]
    ]
}

# 평균값 계산 함수
def calculate_averages(visits):
    hr_list = [hr for visit in visits for hr in visit["HR"]]
    sbp_list = [sbp for visit in visits for sbp in visit["SBP"]]
    dbp_list = [dbp for visit in visits for dbp in visit["DBP"]]
    return np.mean(hr_list), np.mean(sbp_list), np.mean(dbp_list)

# 메타데이터 시각화화
def meta_display(visit, average_hr, average_sbp, average_dbp):
    """
    개별 방문 정보를 표시하는 함수
    """
    
    # 입원시간, 퇴원시간, KTAS
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**입원시간:** {visit['입원시간']}")
        col2.markdown(f"**퇴원시간:** {visit['퇴원시간']}")
        col3.markdown(f"**KTAS:** {visit['ktas']}")
    
    # Vital Signs
    with st.container(border=True):
        st.subheader("**Vital Signs**")
        col1, col2, col3 = st.columns(3)
        hr_diff = np.mean(visit["HR"]) - average_hr
        col1.metric("HR (평균)", f"{np.mean(visit['HR']):.1f} bpm", f"{hr_diff:+.1f} bpm")

        sbp_diff = np.mean(visit["SBP"]) - average_sbp
        col2.metric("SBP (평균)", f"{np.mean(visit['SBP']):.1f} mmHg", f"{sbp_diff:+.1f} mmHg")

        dbp_diff = np.mean(visit["DBP"]) - average_dbp
        col3.metric("DBP (평균)", f"{np.mean(visit['DBP']):.1f} mmHg", f"{dbp_diff:+.1f} mmHg")
    
    # 처방된 약물
    with st.container(border=True):
        st.subheader("**처방된 약물**")
        st.write(", ".join(visit["DRUG"]))


def create_timeline_graph(visits):
 
    # 타임라인 데이터프레임 생성
    timeline_data = pd.DataFrame({
        "날짜": [visit["날짜"] for visit in visits],
        "ktas": [visit["ktas"] for visit in visits]
    })

    # Plotly 타임라인 그래프 생성
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_data["날짜"],
        y=[0] * len(timeline_data),  # Y축을 0으로 설정해 1차원 타임라인 구현
        mode="markers+text",
        marker=dict(size=12, color="blue", symbol="circle"),
        text=[f"KTAS: {ktas}" for ktas in timeline_data["ktas"]],
        textposition="top center",
        hoverinfo="text",
        name="방문 기록"
    ))

    # 레이아웃 설정
    fig.update_layout(
        title="환자 방문 타임라인",
        xaxis=dict(title="방문 날짜", showgrid=True),
        yaxis=dict(visible=False),  # Y축 숨김
        showlegend=False,
        height=300
    )

    return fig


  # AgGrid 설정
def aggrid_interactive_table(visits):

    df = pd.DataFrame(visits)

    builder = GridOptionsBuilder.from_dataframe(df)
    builder.configure_selection("single", use_checkbox=True)  # 단일 선택
    grid_options = builder.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        height=300,
        width="100%",
        theme="streamlit",
       
    )
    return grid_response    
# 데모그라피 정보
def create_demographics_table(patient_data):
    # Demographics 요약 데이터 생성
    demographics = {
        "ID": patient_data["ID"],
        "Name": patient_data["Name"],
        "방문 횟수": [len(visits) for visits in patient_data["Visits"]],  # 방문 횟수 계산
    }
    return pd.DataFrame(demographics)

# 라인 차트 데이터 생성 함수
def create_chart_data(visits, key):
    chart_data = pd.DataFrame({
        "날짜": [visit["날짜"] for visit in visits],
        f"{key}": [sum(visit[key]) / len(visit[key]) for visit in visits]  # 평균값 계산
    })
    chart_data.set_index("날짜", inplace=True)
    return chart_data




# 환자 방문 정보 표시 함수
def display_tab1():
    
    st.title("환자 방문 정보 시각화")
    pa, demo = st.tabs(["Patient overview", "Demography"])
    
    # 탭1
    with pa:
        # 환자 선택 드롭다운
        patient_names = [f"{patient_data['Name'][i]} (ID: {patient_data['ID'][i]})" for i in range(len(patient_data["ID"]))]
        patient_idx = st.selectbox("환자를 선택하세요", range(len(patient_data["ID"])), format_func=lambda x: patient_names[x])
        with st.spinner('Wait for it...'):
            time.sleep(0.2)


        # 선택된 환자의 방문 기록
        st.subheader(f"{patient_names[patient_idx]}")
        data= patient_data["Visits"][patient_idx] # 선택한 환자의 모든 의료기록
        average_hr, average_sbp, average_dbp = calculate_averages(data) # 개인 전체 평균
        print(data)
        
        # 타임라인
        fig=create_timeline_graph(data)
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
            aggrid_interactive_table(data)

        # 날짜 리스트
        date = [visit_day['날짜'] for visit_day in data]
    
        with st.container(border=True):
                # 탭 생성
                tab_avg, tab_hr_avg, tab_sbpdbp_avg, tab_hr, tab_sbpdbp  = st.tabs(["📊 평균", "🫀 HR(AVG)", "💉 SBP/DBP(AVG)", "🫀 HR(1day)", "💉 SBP/DBP(1day)"])
                
                # 평균 탭
                
                with tab_avg:
                    st.subheader("평균 데이터")
                    avg_data = pd.DataFrame({
                        "측정값": ["HR avg", "SBP avg", "DBP avg"],
                        "평균값": [average_hr, average_sbp, average_dbp]
                    })
                    st.bar_chart(avg_data.set_index("측정값"), width=5)

                # HR 탭
                with tab_hr_avg:
                    st.subheader("HR 데이터 평균 추이")
                    hr_chart_data = create_chart_data(data, "HR")
                    st.line_chart(hr_chart_data, x_label= '시간', y_label='HR(bpm)')

                # SBP/DBP 탭
                with tab_sbpdbp_avg:
                    st.subheader("SBP/DBP 데이터 평균 추이")
                    sbp_chart_data = create_chart_data(data, "SBP")
                    dbp_chart_data = create_chart_data(data, "DBP")
                    st.line_chart(pd.concat([sbp_chart_data, dbp_chart_data], axis=1), color=['#00CC66','#FF0066'],x_label= '시간', y_label='BP(mmHg)')

                with tab_hr:
                    selected_date = st.selectbox("날짜를 선택하세요", date, key=1)
                    st.subheader(f"HR {selected_date}")
                    for visit_day in data: # 한 환자의 날짜별로의 의료기록을 시각화화  
                        if visit_day['날짜']== selected_date:
                                st.line_chart(visit_day['HR'],x_label= '시간', y_label='HR(bpm)')
                   
                
                with tab_sbpdbp:
                    selected_date = st.selectbox("날짜를 선택하세요", date, key=2)
                    st.subheader(f"SBP/DBP {selected_date}")
                    for visit_day in data: # 한 환자의 날짜별로의 의료기록을 시각화화  
                        if visit_day['날짜']== selected_date:
                               bp = pd.concat([pd.Series(visit_day['SBP'], name='SBP'),
                                    pd.Series(visit_day['DBP'], name='DBP')], axis=1)
                               st.line_chart(bp, color=['#00CC66','#FF0066'], x_label= '시간', y_label='BP(mmHg)')


        with st.container(border=True):   
            # 메타 시각화
            st.subheader("환자정보")
            selected_date = st.selectbox("날짜를 선택하세요",date,key=3)  
            with st.spinner('Wait for it...'):
                        time.sleep(0.2)
            for visit_day in data: # 한 환자의 날짜별로의 의료기록을 시각화화  
                if visit_day['날짜']== selected_date:
                    meta_display(visit_day, average_hr, average_sbp, average_dbp)

    # 탭2
    with demo:
        # Demographics 테이블 표시
        with st.container(border=True):
            demographics_df = create_demographics_table(patient_data)
            st.subheader("Demographics 정보")
            aggrid_interactive_table(demographics_df)           
