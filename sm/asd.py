import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

# 데이터 준비
data = pd.DataFrame({
    "날짜": ["2024-04-01", "2024-05-15", "2024-06-20"],
    "입원시간": ["10:30", "09:00", "14:00"],
    "퇴원시간": ["13:00", "11:30", "16:45"],
    "KTAS": ["Level 1", "Level 2", "Level 3"]
})

# AgGrid 설정
def aggrid_interactive_table(df: pd.DataFrame):
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

# Streamlit 앱 메인
def main():
    st.title("📅 AgGrid 클릭 이벤트 예제")

    st.subheader("방문 데이터")
    response = aggrid_interactive_table(data)

    # 선택된 행 출력
    if response["selected_rows"]:
        selected_row = response["selected_rows"][0]
        st.subheader("🔎 선택된 방문 정보")
        st.write(f"**날짜:** {selected_row['날짜']}")
        st.write(f"**입원시간:** {selected_row['입원시간']}")
        st.write(f"**퇴원시간:** {selected_row['퇴원시간']}")
        st.write(f"**KTAS 등급:** {selected_row['KTAS']}")

if __name__ == "__main__":
    main()
