# LLM Comparator

This repository contains an application designed to compare two different Large Language Models (LLMs) provided by [Groq](https://console.groq.com/).

## Overview

The LLM Comparator app allows users to input text and receive responses from two different LLMs, making it easy to compare their outputs side-by-side.

## Features

- Compare responses from two different Groq LLMs
- User-friendly interface built with Streamlit
- Utilizes the `langchain-groq` library for seamless integration with Groq's LLMs
- Comparator model that can compare the responses from two models on adherence to prompts, relevance and coherence of reponse.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/agamarora/groq_llm_comparator.git
    cd llm_comparator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. You would need a Groq API key. You can go to `https://console.groq.com/` and register for a free API key.


## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run main.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to use the app.

3. Add your Groq API key in the sidebar.

4. Select models to compare. [Optional] You can use a comparator model to expand on the analysis.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Groq for providing the LLMs with amazing inference speeds
- The developers of `langchain-groq` for their excellent library
