import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Streamlit app
def main():
    st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
    st.subheader("🔔 Analytics Dashboard")
    st.markdown("##")

    # Ask for CSV file
    csv_file = st.file_uploader("Upload CSV file")
    if csv_file is not None:
        df = pd.read_csv(csv_file)

        # Sidebar options
        selected_option = st.sidebar.radio("Select Section", ("Basic Information", "Statistics", "Generated Graphs"))

        if selected_option == "Basic Information":
            st.header("Basic Information")
            total_rows = df.shape[0]
            total_columns = df.shape[1]

            total1, total2, total3 = st.columns(3)
            with total1:
                st.info('Number of Rows', icon="📌")
                st.metric(label="", value=f"{total_rows}")

            with total2:
                st.info('Number of Columns', icon="📌")
                st.metric(label="", value=f"{total_columns}")

            with total3:
                st.info('Column Names', icon="📌")
                st.write(', '.join(df.columns))

            st.info('Number of Unique Values per Column', icon="📌")
            for column in df.columns:
                unique_values = df[column].nunique()
                st.write(f"- {column}: {unique_values}")

        elif selected_option == "Statistics":
            st.header("Important Statistics")
            numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

            selected_columns = st.multiselect("Select Columns", options=numeric_columns)
            if st.button("Generate Statistics"):
                for column in selected_columns:
                    total = df[column].sum()
                    mean_value = df[column].mean()
                    median_value = df[column].median()
                    mode_value = df[column].mode().iloc[0]

                    st.info(f"{column}", icon="📌")
                    row1, row2 = st.columns(2)
                    with row1:
                        st.metric(label="Sum", value=f"{total:,.0f}")
                        st.metric(label="Average", value=f"{mean_value:,.2f}")
                    with row2:
                        st.metric(label="Median", value=f"{median_value:,.2f}")
                        st.metric(label="Most Frequent", value=f"{mode_value:,.0f}")

        elif selected_option == "Generated Graphs":
            st.header("Generated Graphs")
            visualization_type = st.selectbox("Select Visualization Type", ("Area", "Liquid Fill", "Bar", "Scatter", "Pie"))

            st.header("Select Reliable Columns")

            if visualization_type == "Area":
                required_column_types = ["int64", "float64"]
                required_columns = 2
                required_column_info = "Please select 2 columns of type 'int64' or 'float64'."
            elif visualization_type == "Liquid Fill":
                required_column_types = ["int64", "float64"]
                required_columns = 1
                required_column_info = "Please select 1 column of type 'int64' or 'float64'."
            elif visualization_type == "Bar":
                required_column_types = ["int64", "float64"]
                required_columns = 1
                required_column_info = "Please select 1 column of type 'int64' or 'float64'."
            elif visualization_type == "Scatter":
                required_column_types = ["int64", "float64"]
                required_columns = 2
                required_column_info = "Please select 2 columns of type 'int64' or 'float64'."
            elif visualization_type == "Pie":
                required_column_types = ["object"]
                required_columns = 1
                required_column_info = "Please select 1 column of type 'object'."
            else:
                required_column_types = []
                required_columns = 0
                required_column_info = ""

            available_columns = [column for column in df.columns if df[column].dtype in required_column_types]

            st.info(required_column_info)
            reliable_columns = st.multiselect("Select Columns", options=available_columns)

            if st.button("Generate Graphs"):
                if len(reliable_columns) == required_columns:
                    for column in reliable_columns:
                        if visualization_type == "Area":
                            options = {
                                "title": {"text": f"Area Chart for '{column}'"},
                                "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}}},
                                "legend": {"data": [column]},
                                "toolbox": {"feature": {"saveAsImage": {}}},
                                "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
                                "xAxis": [{"type": "category", "boundaryGap": False, "data": df.index.tolist()}],
                                "yAxis": [{"type": "value"}],
                                "series": [{"name": column, "type": "line", "stack": "总量", "areaStyle": {}, "emphasis": {"focus": "series"}, "data": df[column].tolist()}],
                            }
                            st_echarts(options=options, height="400px")

                        elif visualization_type == "Liquid Fill":
                            liquidfill_option = {"series": [{"type": "liquidFill", "data": [0.6, 0.5, 0.4, 0.3]}]}
                            st_echarts(liquidfill_option)

                        elif visualization_type == "Bar":
                            options = {"xAxis": {"type": "category", "data": df.index.tolist()}, "yAxis": {"type": "value"}, "series": [{"data": df[column].tolist(), "type": "bar"}]}
                            st_echarts(options=options, height="500px")

                        elif visualization_type == "Scatter":
                            options = {"xAxis": {}, "yAxis": {}, "series": [{"symbolSize": 20, "data": df[[column]].values.tolist(), "type": "scatter"}]}
                            st_echarts(options=options, height="500px")

                        elif visualization_type == "Pie":
                            options = {
                                "title": {"text": f"Pie Chart for '{column}'", "subtext": "Purely fictional", "left": "center"},
                                "tooltip": {"trigger": "item"},
                                "legend": {"orient": "vertical", "left": "left"},
                                "series": [
                                    {
                                        "name": column,
                                        "type": "pie",
                                        "radius": "50%",
                                        "data": [{"value": val, "name": index} for index, val in df[column].value_counts().items()],
                                        "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
                                    }
                                ],
                            }
                            st_echarts(options=options, height="600px")
                else:
                    st.error(f"Please select {required_columns} columns with the specified column type.")

# Run the app
if __name__ == "__main__":
    main()