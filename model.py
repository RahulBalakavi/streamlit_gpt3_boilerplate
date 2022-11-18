import openai

poem = """Write a poem with the following words: 
---
{input}
---
This is the poem: """

nl_to_sql = """### Postgres SQL tables, with their properties and column values:
#
# {table_name}({comma_sep_col_names})
{values}
### {question}
SELECT"""


def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key


class GeneralModel:
    def __init__(self):
        print("Model Intilization--->")
        # set_openai_key(API_KEY)

    def query(self, prompt, myKwargs={}):
        """
        wrapper for the API to save the prompt and the result
        """

        # arguments to send the API
        kwargs = {
            "engine": "code-davinci-002",
            "temperature": 0.1,
            "max_tokens": 500,
            "best_of": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": ["###"],
        }

        for kwarg in myKwargs:
            kwargs[kwarg] = myKwargs[kwarg]

        r = openai.Completion.create(prompt=prompt, **kwargs)["choices"][0][
            "text"
        ].strip()
        return r

    def model_prediction(self, table_name, question, comma_sep_col_names, values, api_key):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)
        output = self.query(
            nl_to_sql.format(table_name=table_name, question=question, comma_sep_col_names=comma_sep_col_names,
                             values=values))
        print(nl_to_sql.format(table_name=table_name, question=question, comma_sep_col_names=comma_sep_col_names,
                               values=values))
        return 'SELECT ' + output
