
import streamlit as st
import pyodbc
import pandas as pd


st.set_page_config(
    page_title="Harvard Art Museums Dashboard",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Harvard Art Museums")
st.subheader("Art Collection Analysis Dashboard")

st.markdown("---")

st.write(
    "Explore the Harvard Art Museums collection "
    "through metadata, classifications, media, and colors."
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🖼️ Artifacts Overview")
        st.write("Explore artifact details and collection metadata.")

    with st.container(border=True):
        st.subheader("📚 Classification Analysis")
        st.write("Explore art classifications and departments.")

with col2:
    with st.container(border=True):
        st.subheader("📷 Media Information")
        st.write("Explore image counts and media details.")

    with st.container(border=True):
        st.subheader("🎨 Color Analysis")
        st.write("Explore colors, hues, and color percentages.")

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=praba\\SQLEXPRESS;"
        "DATABASE=HarvardArtDB_New;"
        "Trusted_Connection=yes;"
    )  
  

try:
    connection = get_connection()

    metadata_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM dbo.artifact_metadata",
        connection
    ).iloc[0, 0]

    media_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM dbo.artifact_media",
        connection
    ).iloc[0, 0]

    colors_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM dbo.artifact_colors",
        connection
    ).iloc[0, 0]

    connection.close()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Artifacts", metadata_count)
    col2.metric("Media Records", media_count)
    col3.metric("Color Records", colors_count)

except Exception as error:
    st.warning(f"Unable to load dashboard metrics: {error}") 
    

st.sidebar.header("🎨 Classification Filter")

try:
    connection = get_connection()

    classification_data = pd.read_sql_query(
        """
        SELECT DISTINCT classification
        FROM dbo.artifact_metadata
        WHERE classification IS NOT NULL
        ORDER BY classification;
        """,
        connection
    )

    connection.close()

    classification_options = ["All Classifications"] + (
        classification_data["classification"].tolist()
    )

    selected_classification = st.sidebar.selectbox(
        "Select Classification",
        classification_options
    )

except Exception as error:
    st.sidebar.error(f"Unable to load classifications: {error}")
    selected_classification = "All Classifications"




st.write("Select a SQL question, view the query, and display the result.")


questions = {

     "1. Byzantine culture artifacts from the 11th century": """
    SELECT *
    FROM artifact_metadata
    WHERE culture ='Byzantine'
      AND 
          century = '11th century';
    """,
   

    "2. Find all unique cultures": """
    SELECT DISTINCT culture
    FROM dbo.artifact_metadata
    WHERE culture IS NOT NULL;
    """,

    "3. Artifacts from the Archaic Period": """
    SELECT *
    FROM dbo.artifact_metadata
    WHERE period = 'Archaic period';
    """,

    "4. Titles ordered by accession year descending": """
    SELECT title, accessionyear
    FROM dbo.artifact_metadata
    ORDER BY accessionyear DESC;
    """,

    "5. Count artifacts per department": """
    SELECT department, COUNT(*) AS artifact_count
    FROM dbo.artifact_metadata
    GROUP BY department
    ORDER BY artifact_count DESC;
    """,

    
   "6. Artifacts with more than one image": """
    SELECT a.id, a.title, a.classification, m.imagecount
    FROM dbo.artifact_metadata AS a
    INNER JOIN dbo.artifact_media AS m
        ON a.id = m.objectid
    WHERE m.imagecount > 1;
     """,


    "7. Average rank of all artifacts": """
    SELECT AVG(CAST([rank] AS FLOAT)) AS average_rank
    FROM dbo.artifact_media;
    """,

   
    "8. Artifacts where color count exceeds media count": """
    SELECT
        a.id,
        a.title,
        a.classification,
        m.colorcount,
        m.mediacount
    FROM dbo.artifact_metadata AS a
    INNER JOIN dbo.artifact_media AS m
        ON a.id = m.objectid
    WHERE m.colorcount > m.mediacount;
    """,


    "9. Artifacts created between 1500 and 1600": """
    SELECT m.title, a.datebegin, a.dateend
    FROM artifact_metadata AS m
    INNER JOIN artifact_media AS a
       ON m.id = a.objectid
    WHERE a.datebegin <= 1600
    AND a.dateend >= 1500;
    """,

    "10. Artifacts with no media files": """
    SELECT COUNT(*) AS artifacts_without_media
    FROM artifact_media
    WHERE mediacount = 0;
    """,

    "11. Find distinct hues": """
    SELECT DISTINCT hue
    FROM dbo.artifact_colors
    WHERE hue IS NOT NULL
    ORDER BY hue;
    """,

    "12. Top five most frequently used colors": """
    SELECT TOP 5 color, COUNT(*) AS frequency
    FROM dbo.artifact_colors
    GROUP BY color
    ORDER BY frequency DESC;
    """,

    "13. Average color coverage percentage per hue": """
    SELECT hue,
           AVG(CAST([percent] AS FLOAT)) AS average_percentage
    FROM dbo.artifact_colors
    WHERE hue IS NOT NULL
    GROUP BY hue
    ORDER BY average_percentage DESC;
    """,

    "14. Find all colors for an artifact ID": """
    SELECT objectid, color, hue, [percent]
    FROM dbo.artifact_colors
    WHERE objectid = ?;
    """,

    "15. Total number of color entries": """
    SELECT COUNT(*) AS total_color_entries
    FROM dbo.artifact_colors;
    """,

    "16. Titles and hues for Byzantine culture": """
    SELECT a.title, c.hue
    FROM dbo.artifact_metadata AS a
    INNER JOIN dbo.artifact_colors AS c
        ON a.id = c.objectid
    WHERE a.culture LIKE '%Byzantine%';
    """,

    "17. Each title and its associated hues": """
    SELECT a.title, c.hue
    FROM dbo.artifact_metadata AS a
    LEFT JOIN dbo.artifact_colors AS c
        ON a.id = c.objectid
    ORDER BY a.title;
    """,

    "18. Titles, cultures, and media ranks where period is not null": """
    SELECT a.title, a.culture, m.[rank]
    FROM dbo.artifact_metadata AS a
    INNER JOIN dbo.artifact_media AS m
        ON a.id = m.objectid
    WHERE a.period IS NOT NULL;
    """,

    "19. Top 10 ranked artifacts that include Grey hue": """
    WITH RankedArtifacts AS (
        SELECT objectid, [rank],
               ROW_NUMBER() OVER (ORDER BY [rank] ASC) AS rank_position
        FROM dbo.artifact_media
        WHERE [rank] IS NOT NULL
    )
    SELECT a.title, r.[rank], c.hue
    FROM RankedArtifacts AS r
    INNER JOIN dbo.artifact_metadata AS a
        ON a.id = r.objectid
    INNER JOIN dbo.artifact_colors AS c
        ON a.id = c.objectid
    WHERE r.rank_position <= 10
      AND c.hue = 'Grey'
    ORDER BY r.rank_position;
    """,

    
"20. Artifact count and average media count per classification": """
    SELECT
        a.classification,
        COUNT(*) AS artifact_count,
        AVG(CAST(m.mediacount AS FLOAT)) AS average_media_count
    FROM dbo.artifact_metadata AS a
    INNER JOIN dbo.artifact_media AS m
        ON a.id = m.objectid
    GROUP BY a.classification
    ORDER BY artifact_count DESC;
""",

}



selected_question = st.selectbox(
    "Choose your SQL question",
    list(questions.keys())
)


st.subheader("SQL Query")
st.code(questions[selected_question], language="sql")

artifact_id = None

if selected_question.startswith("14."):
    artifact_id = st.number_input(
        "Enter Artifact ID",
        min_value=1,
        step=1
    )


if st.button("Run SQL Query"):
    try:
        connection = get_connection()

        if selected_question.startswith("14."):
            result = pd.read_sql_query(
                questions[selected_question],
                connection,
                params=[artifact_id]
            )
        else:
            result = pd.read_sql_query(
                questions[selected_question],
                connection
            )

        st.subheader("Query Result")
        st.success(f"Query completed. Rows returned: {len(result)}")
        st.dataframe(result, use_container_width=True)

        # Display a chart when the result is suitable
        if len(result.columns) >= 2:
            numeric_columns = result.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:
                st.subheader("Visualization")
                chart_column = st.selectbox(
                    "Choose a numeric column to visualize",
                    numeric_columns,
                    key="chart_column"
                )

                label_column = result.columns[0]

                if label_column != chart_column:
                    chart_data = result[
                        [label_column, chart_column]
                    ].dropna()

                    if len(chart_data) > 0:
                        chart_data = chart_data.set_index(label_column)
                        st.bar_chart(chart_data[chart_column])
     
        connection.close()

    except Exception as error:
        st.error("Unable to execute the query.")
        st.exception(error)
