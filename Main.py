import streamlit as st
from model import GeneralModel


def app():

    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = "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"
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

        question = st.text_area(
            "Enter question to translate to SQL",
            value="How many theft were happened in 2001",
            max_chars=150,
            height=50,
        )

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                report_text = process_prompt(table_name, question, comma_sep_col_names)
                st.markdown(report_text)
    else:
        st.error("🔑 Please enter API Key")
