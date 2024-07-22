# Article Research Tool

## Introduction
It is a versatile platform for extracting insights and answering questions from various online content types by providing URLs.

## Installation
To utilize this locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Manshi-Rathour/Content-Query-Tool
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Content-Query-Tool
   ```

3. **Set Up a Virtual Environment**:
   Create and activate a virtual environment for dependency management:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Dependencies**:
   Install the necessary packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API Keys**:
   Set up your API keys in a `.env` file. Create a `.env` file in the root directory and add the following line:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

6. **Run the Application**:
   Launch the application using Streamlit:
   ```bash
   streamlit run main.py
   ```



## Preview
<a href="https://article-research-tool.streamlit.app/" target="_blank">Visit the WebApp</a>
