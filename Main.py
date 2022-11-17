import os
import pandas
import streamlit as st
import sqlite3 as sq
from model import GeneralModel


def app():
    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = st.sidebar.text_input("APIkey", type="password")

    # Using the streamlit cache
    def process_prompt(table_name, question, comma_sep_col_names, values):

        return pred.model_prediction(table_name=table_name.strip(), question=question.strip(),
                                     comma_sep_col_names=comma_sep_col_names.strip(),
                                     values=values.strip(), api_key=api_key, )

    if api_key:

        # Setting up the Title
        st.title("Welcome to eNLite 2.0")

        # st.write("---")

        # table_name = st.text_area(
        #     "Enter table name",
        #     value="crimes",
        #     max_chars=50,
        #     height=20,
        # )
        #

        uploaded_file = st.file_uploader("Choose CSV file")
        values_str = ""
        col_names = []
        comma_sep_col_names = ""
        if uploaded_file is not None:
            table_name = os.path.splitext(uploaded_file.name)[0]
            table_name = table_name + "_ts"
            file_type = os.path.splitext(uploaded_file.name)[1]
            print(file_type)
            if '.csv' != file_type:
                st.write("Only CSV type files are allowed to be uploaded. Please refresh page and try again.")
                return
            print(table_name)
            full_file_df = pandas.read_csv(uploaded_file, warn_bad_lines=True, error_bad_lines=False)
            comma_sep_col_names = ','.join(list(full_file_df.columns.values))
            col_names = full_file_df.columns.values;
            print(comma_sep_col_names)
            num_lines = len(full_file_df.index)
            print(num_lines)
            conn = sq.connect('{}.sqlite'.format(table_name))  # creates file
            full_file_df.to_sql(table_name, conn, if_exists='replace', index=False)  # writes to file
            conn.close()

            df = full_file_df.head()
            for value_arr in df.values:
                values_str += '#values(' + ','.join(map(str, value_arr)) + ')\n'
            print(df.values)
            print("values = %s", values_str)
            st.write(df)

        comma_sep_col_names_filtered = comma_sep_col_names

        if comma_sep_col_names:
            col_names_filtered = st.multiselect(
                'Select only needed column names',
                col_names,
                col_names)
            comma_sep_col_names_filtered = ','.join(col_names_filtered)

        question = st.text_area(
            "Enter question to translate to SQL",
            placeholder="How many thefts happened in 2001",
            max_chars=150,
            height=50,
        )

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                report_text = process_prompt(table_name, question, comma_sep_col_names_filtered, values=values_str)
                sql = report_text.split(';', 1)[0] + ";"
                sql = sql.replace("\n", "")
                st.subheader(sql)
                conn = sq.connect('{}.sqlite'.format(table_name))
                df = pandas.read_sql(sql, conn)
                conn.close()
                st.write(df)

    else:
        st.error("🔑 Please enter API Key")
