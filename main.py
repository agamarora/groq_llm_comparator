import streamlit as st
import langchain_community
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

st.set_page_config(page_title="LLM Comparator", page_icon="📚", layout="wide")

def check_groq_key(groq_api_key):
    check_url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(check_url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False

st.sidebar.title("GROQ API Key")
groq_api_key = st.sidebar.text_input("Enter your API key", key="name", value="")


if groq_api_key == "":
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if check_groq_key(groq_api_key) == False:
            st.sidebar.warning("Please enter your GROQ API key.")
        else:
            st.sidebar.success("API key is valid")
    except Exception as e:
        st.sidebar.warning("Please enter your GROQ API key.")
else:
    groq_api_key = groq_api_key
    if check_groq_key(groq_api_key) == False:
        st.sidebar.warning("Please enter valid GROQ API key.")
    else:
        st.sidebar.success("API key is valid")






def create_groq_client(model, temp, top_p, max_tokens, sys_prompt, user_prompt, groq_api_key=groq_api_key):
    chat = ChatGroq(api_key=groq_api_key, model=model, temperature=temp, top_p=top_p, max_tokens=max_tokens)
    system = sys_prompt
    human = user_prompt
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    return chain.invoke({"text": user_prompt})

def main():
    st.title("LLM Comparator")
    st.markdown("""
                #### This tool allows you to compare the performance of different language models on the same prompt using GROQ. Select two models to compare and enter a prompt to compare the responses. You can also adjust the temperature, top-p, and max tokens for each model.
                ##### You can get your GROQ API key [here](https://console.groq.com/).
                """)
    model_options = {
    "LLaMA 8B": "llama3-8b-8192",
    "LLaMA 8B Instant": "llama-3.1-8b-instant",
    "LLaMA 70B": "llama3-70b-8192",
    "LLaMA 70B Versatile": "llama-3.1-70b-versatile",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B IT": "gemma-7b-it",
    "Gemma 2 9B IT": "gemma2-9b-it",
    "Llama Guard 8B": "llama-guard-3-8b",
    "Llava v1.5 7b Preview": "llava-v1.5-7b-4096-preview",
    }

    col1, col2 = st.columns(2)

    with col1:
        st.header("Model 1")
        model1 = st.selectbox("Select Model 1 to compare", list(model_options.keys()), key="m1")
        m1_index = list(model_options.keys()).index(model1)
        m1_label = list(model_options.keys())[m1_index]

    with col2:
        st.header("Model 2")
        model2 = st.selectbox("Select Model 2 to compare", list(model_options.keys()), key="m2")
        m2_index = list(model_options.keys()).index(model2)
        m2_label = list(model_options.keys())[m2_index]




    with col1: 
        with st.expander("Enter a prompt to compare", expanded=True):
            # st.header("Enter a prompt to compare")
            user_prompt = st.text_area("Prompt", height=235, key="prompt", value="What is AI and how can AI be used to improve the world? Limit your reponse to 250 words.")

    with col2:
        with st.expander("Advanced Settings", expanded=True):
            # st.header("Settings")
            temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5)
            top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9)
            max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4096, value=512)


    col10, col11 = st.columns([0.7, 0.3])
    
    
    with st.expander("Select Comparator Model", expanded=False):
        st.header("Comparator Model")
        comparator_model = st.selectbox("Model used to compare performance", list(model_options.keys()), key="comparator")
        comparator_model_label = comparator_model
        #add a tick box to enable/disable the comparator model
        comparator_enabled = st.checkbox("Enable Comparator Model", value=False)
        comp_sys_prompt =st.text_area("System Prompt", height=235, key="comp_sys_prompt", value=f"You are an expert in large language models. Please compare the performance of the two models step by step and qualitatively based on the prompt, reponse generated and reponse metadata that includes token utilisation and speed. Then provide a detailed analysis of the performance of each model based on relevance, adherence to the prompt, token performance. Limit your reponses to 250 words. \n\nPrompt for response generation from LLMs: \n{user_prompt}.\n\n")


    model1 = model_options[model1]
    model2 = model_options[model2]
    comparator_model = model_options[comparator_model]

    if comparator_enabled == True:
        compare_button = f"Compare {m1_label} and {m2_label} using {comparator_model_label}"
    else:
        compare_button = f"Compare {m1_label} and {m2_label}"

    if st.button(compare_button, key="compare_button", help=f'Comparing {m1_label} and {m2_label}', use_container_width=True):
        m1_response = create_groq_client(model1, temp, top_p, max_tokens, "You are a helpful AI assistant", user_prompt)
        m2_response = create_groq_client(model2, temp, top_p, max_tokens, "You are a helpful AI assistant", user_prompt)  
        m1_json = json.loads(m1_response.json())
        m1_ans = f"## Reponse from Model 1 [{m1_label}]:\n {m1_json['content']}\n"
        m1_metadata = f"## Metadata from Model 1 [{m1_label}]:\n {m1_json['response_metadata']} \n"
        m2_json = json.loads(m2_response.json())
        m2_ans = f"## Reponse from Model 2 [{m2_label}]:\n {m2_json['content']}\n"
        m2_metadata = f"## Metadata from Model 2 [{m2_label}]:\n {m2_json['response_metadata']}\n"
        if comparator_enabled == True:
            compare_string = str(m1_ans) + str(m1_metadata) + str(m2_ans) + str(m2_metadata)
            compare_string = compare_string.replace('{',"{{").replace('}',"}}")
            comp_prompt = f"Following are the responses from the two models. \n {compare_string}" 
            comp_response = create_groq_client(comparator_model, temp = 0.2, top_p = 0.95, max_tokens = 1024, sys_prompt=comp_sys_prompt, user_prompt=comp_prompt)
            comp_json = json.loads(comp_response.json())
            comp_ans = f"## Reponse from Comparator Model:\n {comp_json['content']}"

    
    col3, col4 = st.columns(2)

    try:
        with col3:
            with st.expander(f"Model1: {m1_label} Response", expanded=True):
                st.write(m1_json['content'])
            with st.expander(f"Model1: {m1_label} Response Metadata", expanded=False):
                st.json(m1_json['response_metadata'])
        with col4:
            with st.expander(f"Model2: {m2_label} Response", expanded=True):
                st.write(m2_json['content'])
            with st.expander(f"Model2: {m2_label} Response Metadata", expanded=False):
                st.json(m2_json['response_metadata'])
        if comparator_enabled == True:
            with st.expander(f"Comparator Model: {comparator_model_label} Response", expanded=True):
                st.markdown(comp_ans)
    except Exception as e:
        st.warning(f"Click on the {compare_button} button to compare the models.")


if __name__ == "__main__":
    main()


    