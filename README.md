# RAG-Chatbot 🤖

### Include both the backend API and the frontend UI.

---

API was written using FastAPI ⚡

Frontend was written using Streamlit 👑

---

### API Reference💾

| API name      | Function                                                                                                                                                      |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/chat`       | Use the model and chain specified in `langchain_utils.py` to chat. It preserves chat history based on the session ID generated.                               |
| `/upload-doc` | Use Choma DB and a specified embeddings model in `chroma_utils.py` to automatically split and index the uploaded document. Support `.docx` `.pdf` and `.txt`. |
| `/list-docs`  | List the documents embedded in Chroma DB. When initialized, a folder named `chroma_db` should be created.                                                     |
| `/delete-doc` | Delete the chosen document from Chroma |                                                                                                                       | 

### Functions🧩:
* set the language of the UI automatically based on your browser settings
* Upload your own files
* Delete unwanted files
* chat based on your files

### UI layout🖼️

![UI Layout](Screenshot-of-UI.png)

### Road Map 🗺️

#### API Improvements🛠️
- [ ] string manipulation for llm output *(in progress)*
- [ ] end of sentence tokens *(in progress)*
- [ ] dynamic chunking sizes *(in progress)*
- [ ] hybrid search
- [ ] Async Implementation
- [ ] Visible Logging
- [ ] Stable & affordable chatbot provider (No OpenAI)

#### UI Improvements🎨
- [x] change UI language *(Completed)*
- [ ] rebuild frontend using React⚛️

#### General Development
- [ ] A button to clear chat history *(in progress)*
- [ ] auto-clean chat history *(in progress)*
- [ ] Dockerize🐋 both front and backend *(in progress)*
- [ ] optimization for Chain logic
- [ ] Have an actual domain
- [ ] Secure the website
    - [ ] Authentication?
    - [ ] more...

### Changelog
