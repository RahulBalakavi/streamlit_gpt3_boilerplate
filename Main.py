import os
import pandas
import streamlit as st
from model import GeneralModel


def app():

    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = st.sidebar.text_input("APIkey", type="password")
    # Using the streamlit cache
    @st.cache
    def process_prompt(table_name, question, comma_sep_col_names):

        return pred.model_prediction(table_name=table_name.strip(), question=question.strip(),
                                     comma_sep_col_names=comma_sep_col_names.strip(), api_key=api_key)

    if api_key:

        # Setting up the Title
        st.title("Welcome to eNLite 2.0")

        # st.write("---")

        table_name = st.text_area(
            "Enter table name",
            value="crimes",
            max_chars=50,
            height=20,
        )

        comma_sep_col_names = st.text_area(
            "Enter comma separated column names to represent table schema",
            value="Identifier,Case Number,Crime Date,Block,Illinois Uniform Crime Reporting Code,Primary Type,"
                  "Description,Location Description,Arrest,Domestic,Beat,District,Ward,Community Area,FBI Code,"
                  "X Coordinate,Y Coordinate,Crime Year,Updated On,Latitude,Longitude,Location",
            max_chars=150,
            height=50,
        )

        uploaded_file = st.file_uploader("Or Choose a CSV file. This will overwrite the above properties")
        if uploaded_file is not None:
            table_name = os.path.splitext(uploaded_file.name)[0]
            file_type = os.path.splitext(uploaded_file.name)[1]
            print(file_type)
            if '.csv' != file_type:
                st.write("Only CSV type files are allowed to be uploaded. Please refresh page and try again.")
                return
            print(table_name)
            full_file_df = pandas.read_csv(uploaded_file, warn_bad_lines=True, error_bad_lines=False)
            comma_sep_col_names = ','.join(list(full_file_df.columns.values))
            print(comma_sep_col_names)
            num_lines = len(full_file_df.index)
            print(num_lines)
            df = full_file_df.head()
            print(df.values)
            st.write(df)

        question = st.text_area(
            "Enter question to translate to SQL",
            placeholder="How many thefts happened in 2001",
            max_chars=150,
            height=50,
        )

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                report_text = process_prompt(table_name, question, comma_sep_col_names)
                st.markdown(report_text)
    else:
        st.error("🔑 Please enter API Key")
