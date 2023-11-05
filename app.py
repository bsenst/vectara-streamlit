import json
import requests
import streamlit as st

# Define the search term input field
search_term = st.text_input("Geben Sie einen Suchbegriff ein:")

url = "https://api.vectara.io:443/v1/query"
headers = {
    "Authorization": st.secrets.bearer_token,
    "customer-id": str(st.secrets.customer_id)
}

payload = {
    "query": [
        {
            "query": search_term,
            "queryContext": "",
            "start": 0,
            "numResults": 10,
            "contextConfig": {
                "charsBefore": 0,
                "charsAfter": 0,
                "sentencesBefore": 2,
                "sentencesAfter": 2,
                "startTag": "%START_SNIPPET%",
                "endTag": "%END_SNIPPET%"
            },
            "corpusKey": [
                {
                    "customerId": st.secrets.customer_id,
                    "corpusId": st.secrets.corpus_id,
                    "semantics": 0,
                    "metadataFilter": "",
                    "lexicalInterpolationConfig": {
                        "lambda": 0.025
                    },
                    "dim": []
                }
            ],
            "summary": [
                {
                    "maxSummarizedResults": 5,
                    "responseLang": "deu",
                    "summarizerPromptName": "vectara-summary-ext-v1.2.0"
                }
            ]
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

# Define the search results in the format provided
search_results = json.loads(response.text)

# Display search results
st.write(search_results)
