import json
import requests
import streamlit as st

# Define the search term input field
search_term = st.text_input("Geben Sie einen Suchbegriff ein:", placeholder="Welches Antibiotikum ist bei Pyelonephritis einzusetzen?")

if search_term:
    url = "https://api.vectara.io:443/v1/query"
    headers = {
        "x-api-key": st.secrets.api_key,
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
    summary = search_results["responseSet"][0]["summary"][0]["text"]
    st.write(summary)

    documents = search_results["responseSet"][0]["document"]
    for i, el in enumerate(search_results["responseSet"][0]["response"]):
        st.caption("["+str(i+1)+"] "+documents[el["documentIndex"]]["id"]+", "+str(el["score"]))
        st.write(" ".join(el["text"].split()).replace("*","").replace("%START_SNIPPET%","").replace("%END_SNIPPET%",""))
