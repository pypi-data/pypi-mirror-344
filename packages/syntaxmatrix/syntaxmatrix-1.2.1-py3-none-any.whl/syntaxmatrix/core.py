# syntaxmatrix/core.py
import os
import requests
import webbrowser
import time
from flask import Flask, session
from collections import OrderedDict
from . import db, routes
from .themes import DEFAULT_THEMES
import uuid
import io, base64
from openai import OpenAI
from flask import session, has_request_context
from .plottings import render_plotly, pyplot as render_pyplot
from .file_processor import process_admin_pdf_files



class SyntaxMUI:
    def __init__(self, 
                 host="127.0.0.1", 
                 port=5050, 
                 user_icon="👩🏿‍🦲",
                 bot_icon="👀",
                 site_icon="𓊂", 
                 site_title="smx", 
                 site_logo="SMX",
                 project_title="SyntaxMatrix UI", 
                 theme_name="light"):
        self.app = Flask(__name__)
        self.app.secret_key = "syntaxmatrix_secret"
        self.host = host
        self.port = port
        self.user_icon = user_icon
        self.bot_icon = bot_icon
        self.site_icon = site_icon
        self.site_title = site_title
        self.site_logo = site_logo
        self.project_title = project_title
        self.page = ""
        self.ui_mode = "default"
        self.theme_toggle_enabled = False
        
        db.init_db()
        self.pages = db.get_pages()

        db.init_pdf_chunks_table()
        self.pdf_chunks = db.get_pdf_chunks()
        
        self.widgets = OrderedDict()
        self.theme = DEFAULT_THEMES.get(theme_name, DEFAULT_THEMES["light"])
        
        # Ephemeral buffer initialized
        self.system_output_buffer = ""
        
        # NEW: Unique token for each app launch.
        self.app_token = str(uuid.uuid4())
        
        # In-memory store for admin PDF chunks
        self.admin_pdf_chunks = {}

        routes.setup_routes(self)

        # In-memory store of user‑uploaded chunks, scoped per chat session
        self.user_file_chunks = {}

    def load_pdf_chunks(self, directory: str = "uploads/sys"):
        """
        Process all PDFs in `directory`, store chunks in DB and cache in-memory.
        Returns mapping { file_name: [chunk, ...] }.
        """
        mapping = process_admin_pdf_files(directory)
        self.admin_pdf_chunks = mapping
        return mapping
    
    # --- Unchanged Original Methods (fully preserved) ---
    def set_ui_mode(self, mode):
        if mode not in ["default", "card", "bubble", "smx"]:
            raise ValueError("UI mode must be one of: 'default', 'card', 'bubble', 'smx'.")
        self.ui_mode = mode

    @staticmethod
    def list_ui_modes():
        return "default", "card", "bubble", "smx"
    
    @staticmethod
    def list_themes():
        return list(DEFAULT_THEMES.keys())
    
    def set_theme(self, theme_name, theme):
        if theme_name in DEFAULT_THEMES:
            self.theme = DEFAULT_THEMES[theme_name]
        elif isinstance(theme, dict):
            self.theme["custom"] = theme
            DEFAULT_THEMES[theme_name] = theme
        else:
            self.theme = DEFAULT_THEMES["light"]
            raise ValueError("Theme must be 'light', 'dark', or a custom dict.")
    
    def enable_theme_toggle(self):
        self.theme_toggle_enabled = True
    
    def disable_theme_toggle(self):
        self.theme_toggle_enabled = False
    
    def columns(self, components):
        col_html = "<div style='display:flex; gap:10px;'>"
        for comp in components:
            col_html += f"<div style='flex:1;'>{comp}</div>"
        col_html += "</div>"
        return col_html
    
    def set_site_icon(self, icon):
        self.site_icon = icon

    def set_site_title(self, title):
        self.site_title = title
    
    def set_site_logo(self, logo):
        self.site_logo = logo

    def set_project_title(self, project_title):
        self.project_title = project_title

    def set_user_icon(self, icon):
        self.user_icon = icon

    def set_bot_icon(self, icon):
        self.bot_icon = icon

    # Public API: Widget registration.
    def text_input(self, key, label, placeholder="Ask me anything"):
        if key not in self.widgets:
            self.widgets[key] = {"type": "text_input", "key": key, "label": label, "placeholder": placeholder}

    def get_text_input_value(self, key, default=""):
        return session.get(key, default)

    def clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True
    
    def button(self, key, label, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}

    def file_uploader(self, key, label, accept_multiple_files=False, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {
                "type": "file_upload",
                "key": key,               "label": label,
                "accept_multiple": accept_multiple_files,
               "callback": callback
        }

    def get_file_upload_value(self, key):
        return session.get(key, None)

    def get_chat_history(self):
        if has_request_context():
            return session.get("chat_history", [])
        else:
            return getattr(self, "_fallback_chat_history", [])

    def set_chat_history(self, history):
        if has_request_context():
            session["chat_history"] = history
            session.modified = True
        else:
            self._fallback_chat_history = history

    def clear_chat_history(self):
        if has_request_context():
            session["chat_history"] = []
            session.modified = True
        else:
            self._fallback_chat_history = []
    
    def write(self, content):
        self.bot_message(content)

    def markdown(self, md_text):
        try:
            import markdown
            html = markdown.markdown(md_text)
        except ImportError:
            html = md_text
        self.write(html)
    
    def latex(self, math_text):
        self.write(f"\\({math_text}\\)")

    def bot_message(self, content):
        history = self.get_chat_history()
        history.append(("Bot", content))
        self.set_chat_history(history)

    def plt_plot(self, fig):
        html = render_pyplot(fig)
        self.bot_message(html)

    def plotly_plot(self, fig):
        try:
            html = render_plotly(fig)
            self.bot_message(html)
        except Exception as e:
            self.error(f"Plotly rendering failed: {e}")

    def error(self, content):
        self.write(f'<div style="color:red; font-weight:bold;">{content}</div>')
    
    def warning(self, content):
        self.write(f'<div style="color:orange; font-weight:bold;">{content}</div>')
    
    def success(self, content):
        self.write(f'<div style="color:green; font-weight:bold;">{content}</div>')
    
    def info(self, content):
        self.write(f'<div style="color:blue;">{content}</div>')

    @staticmethod
    def generate_contextual_title(history):
        
        def get_generated_title(conversation: str, service_url: str = "https://syntaxmatrix-175860941374.europe-west2.run.app"):
            endpoint = f"{service_url}/api/title"
            payload = {"conversation": conversation}
            headers = {"Content-Type": "application/json"}

            response = requests.post(endpoint, json=payload, headers=headers)
                    
            if response.status_code == 200:
                data = response.json()
                return data.get("title", "No title returned")
            else:
                # Return a string error message instead of an Exception object
                return f"Error calling API: {response.status_code} - {response.text}"

        conversation = history
        title = get_generated_title(conversation)
        return title
    # --- End of Original Methods ---

    # --- Casual User Uploaded File Methods
    def get_session_id(self):
        """Return current chat’s UUID (so we can key uploaded chunks)."""
        return session.get("current_session", {}).get("id")

    def add_user_chunks(self, session_id, chunks):
        """Append these text‐chunks under that session’s key."""
        self.user_file_chunks.setdefault(session_id, []).extend(chunks)

    def get_user_chunks(self, session_id):
        """Get any chunks that this session has uploaded."""
        return self.user_file_chunks.get(session_id, [])

    def clear_user_chunks(self, session_id):
        """Remove all stored chunks for a session (on chat‑clear or delete)."""
        self.user_file_chunks.pop(session_id, None)
    
    

    def run(self):
        url = f"http://{self.host}:{self.port}/"
        webbrowser.open(url)
        self.app.run(host=self.host, port=self.port, debug=False)
    