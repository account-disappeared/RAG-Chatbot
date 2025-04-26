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
* Upload your own files
* Delete unwanted files
* chat based on your files

### UI layout🖼️

![UI Layout](Screenshot-of-UI.png)

### Road Map 🗺️

#### API Improvements🛠️
- [ ] chatbot response not ideal *(in progress)*
- [ ] JSON format bug *(in progress)*
- [ ] Async Implementation
- [ ] Visible Logging
- [ ] Stable & affordable chatbot provider (No OpenAI)

#### UI Improvements🎨
- [ ] change UI language *(in progress)*
- [ ] rebuild frontend using React⚛️

#### General Development
- [ ] Dockerize🐋 both front and backend *(in progress)*
- [ ] Have an actual domain
- [ ] Secure the website
    - [ ] Authentication?
    - [ ] more...
