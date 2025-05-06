# RAG-Chatbot 🤖

### Include both the backend API and the frontend UI.

---

LLM logic was written using Langchain🦜

API was written using FastAPI ⚡

Frontend was written using Streamlit 👑

---

### Important Contributors:

[KeeganCarey](https://github.com/KeeganCarey)

---

> [!NOTE]
> Supported Languages: English, French, Simplified Chinese
> 
> Chat-GPT translated: Traditional Chinese, Spanish, Italian, German and Japanese

---

### API Reference💾

| API name      | Function                                                                                                                                                      |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/chat`       | Use the model and chain specified in `langchain_utils.py` to chat. It preserves chat history based on the session ID generated.                               |
| `/upload-doc` | Use Choma DB and a specified embeddings model in `chroma_utils.py` to automatically split and index the uploaded document. Support `.docx` `.pdf` and `.txt`. |
| `/list-docs`  | List the documents embedded in Chroma DB. When initialized, a folder named `chroma_db` should be created.                                                     |
| `/delete-doc` | Delete the chosen document from Chroma |                                                                                                                       | 

---

### Functions🧩:
* set the language of the UI automatically based on your browser settings
* Upload your own files
* Delete unwanted files
* chat based on your files

---

### UI layout🖼️

![UI Layout](Screenshot-of-UI.png)

---

### Road Map 🗺️

#### API Improvements🛠️
- [x] string manipulation for llm output *(Completed)*
- [x] end of sentence tokens *(Completed)*
- [x] dynamic chunking sizes *(Completed)*
- [x] better prompts *(Completed)*
- [x] better embeddings model *(Completed)*
- [ ] Dynamic prompting for different tasks
- [ ] hybrid search
- [ ] Async Implementation
- [ ] Visible Logging
- [ ] Stable & affordable chatbot provider (Claude???)
- [ ] Web Search & Web Scraping

#### UI Improvements🎨
- [x] change UI language *(Completed)*
- [ ] Enable Streaming *(in progress)*
- [ ] custom CSS styling for Streamlit Widgets *(in progress)*
- [ ] rebuild frontend using React⚛️

#### General Development
- [ ] A button to clear chat history *(in progress)*
- [ ] auto-clean chat history *(in progress)*
- [x] when deleting a file, it automatically refreshes the document list *(completed)*
- [ ] Return sources *(in progress)*
- [ ] Dockerize🐋 both front and backend
- [ ] optimization for Chain logic
- [ ] Have an actual domain
- [ ] Secure the website
    - [ ] Authentication?
    - [ ] more...

---

### Changelog📃

#### 0.1 --- ***Initial Release: 2025/4/23***🎇 
- Added the `/chat` `/upload-doc` `/list-docs` and `/delete-doc` endpoints (function specified below)
- Added the Streamlit webUI, able to use all the 4 endpoints listed above and can also choose a llm chat model (only supports HuggingFace Endpoint)
- Added error messages when error occurs
- used [jinaai/jina-embeddings-v2-base-zh](https://huggingface.co/jinaai/jina-embeddings-v2-base-zh) as the embedding model

#### 0.2 --- ***Localization Update: 2025/4/25***🌐
- Added localization for *English* and *French*
- Added `translations.py`, a new option in the sidebar `select language`
- Added a new function `get_text()`, which replaces all UI text with the selected language
- All translations are implemented using python dictionaries

  ##### 0.2.1
- Added localization for *Simplified Chinese*

  ##### 0.2.2
- fixed the issue of the web page not automatically updating after the user chose another language

  ##### 0.2.3
- fixed the issue of the language options not disappearing after the user chooses a new language

#### 0.3 --- ***Auto-language Detection Update: 2025/4/26***🔤
- Installed a new python library (`streamlit-browser-language`) that detects the user's preferred browser language
- Introduced auto-language detection, the UI language will be set to your browser's display language

  ##### 0.3.1
- fixed the issue of language not being able to be detected due to the mishandling of string output from the `streamlit-browser-language` package

  ##### 0.3.2
- fixed the issue of web page reloading when the user selects the same language

#### 0.4 --- ***Operation: Health: 2025/5/1***💊
- fixed the issue of the LLM keeps generating questions and answers unrelated to the original human input
    - added a stop token when calling the llm: `stop_sequences=["Human:"]`
- fixed the issue of the LLM outputting unnecessary information in its response (response includes `?\nAI:`)
    - added a custom function ` slice_output()` to cut everything before `AI:`
  ##### 0.4.1 --- 2025/5/4
- migrated to a newer embeddings model, [jinaai/jina-embeddings-v3](https://huggingface.co/jinaai/jina-embeddings-v3)
    - now supports over 100 languages, check their [official page](https://huggingface.co/jinaai/jina-embeddings-v3#supported-languages)
- Improved 'text_splitter" to adjust for languages without word boundaries (Chinese, Japanese.etc.)
    - Add ASCII full-stop `.`, Unicode fullwidth full stop `．` (used in Chinese text), and
    - ideographic full stop `。` (used in Japanese and Chinese), Zero-width space used in Thai, Myanmar, Kmer, and Japanese
    - ASCII comma `,`, Unicode fullwidth comma `，`, and Unicode ideographic comma `、`
- Dynamic chunking was implemented, which decides the sizes of the split chunks depneding on the overall character/size of the document
    - Before Dynamic Chunking (`chunk_size=1000`):
 
      Moreover, Blondin's achievements tapped into a fundamental human fascination with risk and the limits of human capability. We are drawn to those who push          boundaries, who venture into the realm of the seemingly impossible. Blondin embodied this spirit of exploration, not of geographical frontiers, but of the         frontiers of human skill and nerve. His walks across the Niagara were a powerful demonstration of what dedication, training, and an indomitable will could         achieve. In a world that often feels constrained by limitations, Blondin offered a thrilling glimpse of human potential unleashed.
      Finally, Blondin's legacy has been carefully preserved and romanticized through history. Stories of his daring feats have been passed down, often                  embellished, contributing to his almost mythical status. He represents a bygone era of grand spectacle and individual heroism, a time when a single person         could capture the world's imagination with a breathtaking display of skill and courage.

    - After Dynamic Chunking
      
      Finally, Blondin's legacy has been carefully preserved and romanticized through history. Stories of his daring feats have been passed down, often                  embellished, contributing to his almost mythical status. He represents a bygone era of grand spectacle and individual heroism, a time when a single person         could capture the world's imagination with a breathtaking display of skill and courage.
- Fixed the issue of Document List not reflecting the changes when a user deletes a document
    - added `st.rerun()` to refresh the UI
- Even MORE languages
    - Added Chat-GPT translated localization for *Spanish*, *Italian*, *German* and *Japanese*
- BETTER promts
    - Improved existing prompts: `contextualize_q_system_prompt`, `prompt` and `fusion_prompt` for better direction following and better response 
