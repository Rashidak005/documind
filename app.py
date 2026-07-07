import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr

from core.pipeline import process_document, ask_question, ask_multiple_documents, get_available_documents
from core.vector_store import delete_collection
from utils.file_handler import save_uploaded_file
from utils.formatter import format_document_info, format_answer, format_multi_source_answer, format_error

# --- Custom CSS ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-void: #0A0D14;
    --border-line: #232838;
    --text-primary: #ECEEF3;
    --text-muted: #8891A5;
    --violet: #8B5CF6;
    --cyan: #22D3EE;
}

* { box-sizing: border-box; }

html, body {
    overflow-x: hidden !important;
    background: var(--bg-void) !important;
}

.gradio-container {
    background: var(--bg-void) !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0 !important;
    max-width: 100% !important;
    position: relative;
    overflow-x: hidden !important;
}

/* ---- Aurora ambient blobs ---- */
.aurora-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(110px);
    opacity: 0.22;
    z-index: 0;
    pointer-events: none;
    animation: drift 22s ease-in-out infinite alternate;
}
#blob-1 { width: 420px; height: 420px; background: var(--violet); top: -160px; left: -120px; }
#blob-2 { width: 380px; height: 380px; background: var(--cyan); bottom: -160px; right: -120px; animation-delay: -8s; }

/* ---- Side light beams ---- */
.side-beam {
    position: fixed;
    width: 3px;
    z-index: 9999;
    pointer-events: none;
    border-radius: 2px;
    animation: beam-float 8s ease-in-out infinite;
}
#beam-left {
    left: 10px;
    top: 15%;
    height: 55vh;
    background: linear-gradient(180deg, transparent, rgba(255,255,255,0.95) 45%, var(--violet) 60%, transparent);
    box-shadow: 0 0 8px 1px rgba(255,255,255,0.9), 0 0 36px 6px rgba(139,92,246,0.7);
}
#beam-right {
    right: 10px;
    top: 32%;
    height: 55vh;
    background: linear-gradient(180deg, transparent, rgba(255,255,255,0.95) 45%, var(--cyan) 60%, transparent);
    box-shadow: 0 0 8px 1px rgba(255,255,255,0.9), 0 0 36px 6px rgba(34,211,238,0.7);
    animation-delay: -4s;
}
@keyframes beam-float {
    0%   { transform: translateY(0); }
    50%  { transform: translateY(70px); }
    100% { transform: translateY(0); }
}
@keyframes drift {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(30px, 40px) scale(1.08); }
}
@media (prefers-reduced-motion: reduce) {
    .aurora-blob, .side-beam { animation: none; }
}

/* ---- Navbar ---- */
#navbar {
    position: relative; z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 28px;
    border-bottom: 1px solid var(--border-line);
}
#logo-mark {
    width: 30px; height: 30px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    display: inline-flex; align-items:center; justify-content:center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; color: #0A0D14; font-size: 15px;
    margin-right: 10px;
}
#wordmark {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.35em;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
#tagline-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72em;
    color: var(--text-muted);
    border: 1px solid var(--border-line);
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 14px;
    letter-spacing: 0.03em;
}
.trace-node-label { font-family: 'JetBrains Mono', monospace; font-size: 9px; fill: var(--text-muted); letter-spacing: 0.05em; }

#body-row {
    position: relative; z-index: 1;
    padding: 16px 20px !important;
    gap: 16px !important;
}

#chatbox {
    overflow-y: auto !important;
}
#chatbox .message.bot { border-left: 2px solid var(--cyan) !important; }
#chatbox .message.user { border-left: 2px solid var(--violet) !important; }

/* ---- Glass panels ---- */
.panel-card {
    background: rgba(18, 22, 31, 0.88) !important;
    border: 1px solid var(--border-line) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    backdrop-filter: blur(14px);
    position: relative;
}
.panel-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--violet), var(--cyan));
    border-radius: 14px 14px 0 0;
    animation: pulse-glow 4s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { opacity: 0.45; box-shadow: 0 0 6px rgba(139, 92, 246, 0.3); }
    50%      { opacity: 0.9;  box-shadow: 0 0 14px rgba(34, 211, 238, 0.5); }
}
.panel-heading {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72em !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 10px !important;
    display: flex; align-items: center; gap: 6px;
}

/* ---- Upload dropzone ---- */
#upload-zone {
    border: 1px dashed var(--border-line) !important;
    border-radius: 10px !important;
    background: rgba(255,255,255,0.015) !important;
    position: relative;
    transition: border-color 0.25s ease;
}
#upload-zone:hover { border-color: var(--cyan) !important; }
#upload-zone::after {
    content: "";
    position: absolute;
    left: 0; right: 0; top: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0;
}
#upload-zone:hover::after { opacity: 1; animation: scan 1.6s ease-in-out infinite; }
@keyframes scan { 0% { top: 0%; } 50% { top: 96%; } 100% { top: 0%; } }

/* ---- Buttons ---- */
button.primary {
    background: linear-gradient(90deg, var(--violet), var(--cyan)) !important;
    border: none !important;
    color: #0A0D14 !important;
    font-weight: 600 !important;
    transition: box-shadow 0.25s ease, transform 0.15s ease;
}
button.primary:hover {
    box-shadow: 0 4px 24px rgba(139, 92, 246, 0.35);
    transform: translateY(-1px);
}

.gr-dropdown, textarea, input[type="text"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--border-line) !important;
    color: var(--text-primary) !important;
}

#chatbox:empty::before {
    content: "Upload a document on the left, then ask it anything.";
    display: block;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    text-align: center;
    padding-top: 60px;
}

footer { display: none !important; }
"""

navbar_html = """
<div id="navbar">
    <div style="display:flex; align-items:center;">
        <span id="logo-mark">D</span>
        <span id="wordmark">DocuMind</span>
        <span id="tagline-pill">RAG · GROQ · CHROMADB</span>
    </div>
    <svg viewBox="0 0 260 40" width="220" height="40" xmlns="http://www.w3.org/2000/svg">
        <path d="M 20 20 L 130 20 L 240 20" stroke="#232838" stroke-width="1.5" fill="none" stroke-dasharray="4 4"/>
        <circle r="3.5" fill="#22D3EE">
            <animateMotion dur="3.5s" repeatCount="indefinite" path="M 20 20 L 130 20 L 240 20" />
        </circle>
        <circle cx="20" cy="20" r="5" fill="#0A0D14" stroke="#8B5CF6" stroke-width="2"/>
        <text x="20" y="35" text-anchor="middle" class="trace-node-label">DOC</text>
        <circle cx="130" cy="20" r="5" fill="#0A0D14" stroke="#8B5CF6" stroke-width="2"/>
        <text x="130" y="35" text-anchor="middle" class="trace-node-label">SEARCH</text>
        <circle cx="240" cy="20" r="5" fill="#0A0D14" stroke="#22D3EE" stroke-width="2"/>
        <text x="240" y="35" text-anchor="middle" class="trace-node-label">ANSWER</text>
    </svg>
</div>
"""

ambient_html = """
<div class="aurora-blob" id="blob-1"></div>
<div class="aurora-blob" id="blob-2"></div>
<div class="side-beam" id="beam-left"></div>
<div class="side-beam" id="beam-right"></div>
"""

# ============================================================
# Backend logic
# ============================================================

def handle_upload(temp_file):
    if temp_file is None:
        return format_error("Please choose a file first."), gr.update(), "*No document selected.*"

    try:
        # Save with a unique name on disk (prevents overwriting different files)
        saved_path = save_uploaded_file(temp_file.name)

        # But use the ORIGINAL filename for the collection name, so re-uploading
        # the same document reuses the same collection instead of creating a duplicate
        original_name = os.path.basename(temp_file.name)

        result = process_document(saved_path, original_name)
        all_docs = get_available_documents()

        status = f"✅ **{original_name}** processed successfully."
        summary_md = format_document_info(result)

        return status, gr.update(choices=all_docs, value=[result["collection_name"]]), summary_md

    except ValueError as e:
        return format_error(str(e)), gr.update(), "*No document selected.*"
    except Exception as e:
        return format_error(f"Something went wrong: {e}"), gr.update(), "*No document selected.*"


def handle_ask(question, selected_docs, history):
    history = history or []

    if not selected_docs:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": "⚠️ Please select at least one document from the sidebar first."})
        return history, ""

    if not question or not question.strip():
        return history, ""

    try:
        if len(selected_docs) == 1:
            raw_answer = ask_question(question, selected_docs[0])
            answer = format_answer(raw_answer)
        else:
            raw_answer, chunks_with_sources = ask_multiple_documents(question, selected_docs)
            answer = format_multi_source_answer(raw_answer, chunks_with_sources)
    except Exception as e:
        answer = format_error(f"Could not generate an answer: {e}")

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})

    return history, ""


def handle_delete(selected_docs):
    """
    Deletes every currently selected document's collection from ChromaDB
    and refreshes the dropdown with whatever documents remain.
    """
    if not selected_docs:
        return "*Select a document first.*", gr.update()

    try:
        for doc in selected_docs:
            delete_collection(doc)
        remaining_docs = get_available_documents()
        return f"🗑️ Deleted {len(selected_docs)} document(s).", gr.update(choices=remaining_docs, value=[])
    except Exception as e:
        return format_error(f"Could not delete: {e}"), gr.update()


def load_existing_documents():
    docs = get_available_documents()
    return gr.update(choices=docs)


# ============================================================
# UI layout
# ============================================================

with gr.Blocks(title="DocuMind") as demo:

    gr.HTML(ambient_html)
    gr.HTML(navbar_html)

    with gr.Row(elem_id="body-row"):

        with gr.Column(scale=1, elem_id="sidebar-col", elem_classes="panel-card"):
            gr.Markdown("📤 UPLOAD", elem_classes="panel-heading")

            file_upload = gr.File(
                label="",
                file_types=[".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"],
                elem_id="upload-zone"
            )

            upload_button = gr.Button("Process Document", variant="primary")
            upload_status = gr.Markdown("")

            gr.Markdown("📚 YOUR DOCUMENTS", elem_classes="panel-heading")
            gr.Markdown("*Select one document to ask it directly, or select several to search across all of them at once.*")

            document_dropdown = gr.Dropdown(
                label="",
                choices=[],
                interactive=True,
                multiselect=True
            )

            delete_button = gr.Button("🗑️ Delete Selected Document(s)", variant="secondary")

            document_summary = gr.Markdown("*Upload a document to see its summary here.*")

        with gr.Column(scale=2, elem_id="chat-col", elem_classes="panel-card"):
            gr.Markdown("💬 ASK", elem_classes="panel-heading")

            chatbot = gr.Chatbot(
                label=None,
                show_label=False,
                elem_id="chatbox",
                height=460
            )

            with gr.Row():
                question_input = gr.Textbox(
                    placeholder="Ask something about the selected document(s)…",
                    show_label=False,
                    scale=4
                )
                ask_button = gr.Button("Ask", variant="primary", scale=1)

    upload_button.click(
        fn=handle_upload,
        inputs=[file_upload],
        outputs=[upload_status, document_dropdown, document_summary]
    )

    ask_button.click(
        fn=handle_ask,
        inputs=[question_input, document_dropdown, chatbot],
        outputs=[chatbot, question_input]
    )

    question_input.submit(
        fn=handle_ask,
        inputs=[question_input, document_dropdown, chatbot],
        outputs=[chatbot, question_input]
    )

    delete_button.click(
        fn=handle_delete,
        inputs=[document_dropdown],
        outputs=[document_summary, document_dropdown]
    )

    demo.load(fn=load_existing_documents, outputs=[document_dropdown])


if __name__ == "__main__":
    demo.launch(css=custom_css, theme=gr.themes.Base(primary_hue="violet", neutral_hue="slate"))