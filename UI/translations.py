available_languages = ["en", "fr", "zh"]

translations = {
    "en": {
        # App title and general UI
        "app_title": "Langchain RAG Chatbot",
        "select_model": "Select Model",
        "chat_placeholder": "Query:",
        "generating": "Generating response...",
        "api_error": "Failed to get a response from the API. Please try again.",

        # Sidebar
        "upload_document": "Upload Document",
        "choose_file": "Choose a file",
        "upload_button": "Upload",
        "uploading": "Uploading...",
        "upload_success": "File '{filename}' uploaded successfully with ID {file_id}.",
        "uploaded_documents": "Uploaded Documents",
        "refresh_documents": "Refresh Document List",
        "refreshing": "Refreshing...",
        "select_to_delete": "Select a document to delete",
        "delete_button": "Delete Selected Document",
        "deleting": "Deleting...",
        "delete_success": "Document with ID {file_id} deleted successfully.",
        "delete_error": "Failed to delete document with ID {file_id}.",

        # Chat details
        "details": "Details",
        "generated_answer": "Generated Answer",
        "model_used": "Model Used",
        "session_id": "Session ID",

        # Language selector
        "select_language": "Select Language",
        "auto_detected": "Auto-detected from browser ({browser_lang})",
    },
    "fr": {
        # App title and general UI
        "app_title": "Chatbot RAG Langchain",
        "select_model": "Sélectionner le Modèle",
        "chat_placeholder": "Question :",
        "generating": "Génération de la réponse...",
        "api_error": "Échec de l'obtention d'une réponse de l'API. Veuillez réessayer.",

        # Sidebar
        "upload_document": "Télécharger un Document",
        "choose_file": "Choisir un fichier",
        "upload_button": "Télécharger",
        "uploading": "Téléchargement en cours...",
        "upload_success": "Fichier '{filename}' téléchargé avec succès avec l'ID {file_id}.",
        "uploaded_documents": "Documents Téléchargés",
        "refresh_documents": "Actualiser la Liste des Documents",
        "refreshing": "Actualisation...",
        "select_to_delete": "Sélectionnez un document à supprimer",
        "delete_button": "Supprimer le Document Sélectionné",
        "deleting": "Suppression...",
        "delete_success": "Document avec l'ID {file_id} supprimé avec succès.",
        "delete_error": "Échec de la suppression du document avec l'ID {file_id}.",

        # Chat details
        "details": "Détails",
        "generated_answer": "Réponse Générée",
        "model_used": "Modèle Utilisé",
        "session_id": "ID de Session",

        # Language selector
        "select_language": "Choisir la Langue",
        "auto_detected": "Détecté automatiquement du navigateur ({browser_lang})",
    },
    "zh": {
        # 应用标题及通用界面
        "app_title": "Langchain RAG 聊天机器人",
        "select_model": "选择模型",
        "chat_placeholder": "查询：",
        "generating": "正在生成回复…",
        "api_error": "无法从 API 获取回复，请重试。",

        # 侧边栏
        "upload_document": "上传文档",
        "choose_file": "选择文件",
        "upload_button": "上传",
        "uploading": "正在上传…",
        "upload_success": "文件 '{filename}' 上传成功，ID 为 {file_id}。",
        "uploaded_documents": "已上传的文档",
        "refresh_documents": "刷新文档列表",
        "refreshing": "正在刷新…",
        "select_to_delete": "选择要删除的文档",
        "delete_button": "删除选中文档",
        "deleting": "正在删除…",
        "delete_success": "ID 为 {file_id} 的文档已成功删除。",
        "delete_error": "删除 ID 为 {file_id} 的文档失败。",

        # 聊天详情
        "details": "详细信息",
        "generated_answer": "生成的回答",
        "model_used": "使用的模型",
        "session_id": "会话 ID",

        # 语言选择器
        "select_language": "选择语言",
        "auto_detected": "自动从浏览器检测 ({browser_lang})",
    }
}


def get_text(key, lang="en", **kwargs):
    """Get the text for the given key in the selected language with formatting."""
    try:
        text = translations[lang][key]
        # Apply any format string parameters
        if kwargs:
            return text.format(**kwargs)
        return text
    except KeyError:
        # Fallback to English if translation not found
        try:
            return translations["en"][key]
        except KeyError:
            return key
