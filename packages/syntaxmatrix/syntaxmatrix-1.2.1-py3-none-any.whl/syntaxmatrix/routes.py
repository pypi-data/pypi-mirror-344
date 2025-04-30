import os
import time
import uuid
from flask import request, render_template_string, redirect, url_for, session, has_request_context, jsonify, send_from_directory, url_for

from . import db
from .themes import DEFAULT_THEMES
from openai import OpenAI 
import sqlite3
# from PyPDF2.errors import EmptyFileError

from .file_processor import process_admin_pdf_files, remove_admin_pdf_file, recursive_text_split
from . import core
from io import BytesIO
from PyPDF2 import PdfReader


def get_contrast_color(hex_color: str) -> str:
    """
    Returns a contrasting color (#000000 or #ffffff) based on the brightness of hex_color.
    """
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        r = int(hex_color[0]*2, 16)
        g = int(hex_color[1]*2, 16)
        b = int(hex_color[2]*2, 16)
    elif len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    else:
        return '#000000'
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return '#ffffff' if brightness < 0.5 else '#000000'

def render_chat_history(smx):
    messages = session.get("chat_history", [])
    chat_html = ""
    if not messages:
        chat_html += f"""
        <div id="deepseek-header" style="text-align:center; margin-top:10px; margin-bottom:5px;">
          <h2>{smx.bot_icon}{smx.project_title}.</h2>
          <p>How can I help you today?</p>
        </div>
        """
    for role, message in messages:
        timestamp = ""
        if smx.ui_mode == "card":
            timestamp = f"""<span style="float: right; font-size: 0.8em; color: {smx.theme['text_color']};">{time.strftime('%H:%M')}</span>"""
        chat_icon = smx.user_icon if role.lower() == "user" else smx.bot_icon
        chat_html += f"""
        <div class='chat-message {role.lower()}'>
          <span>{chat_icon}{timestamp}</span>
          <p>{message}</p>
        </div>
        """
    return chat_html

def setup_routes(smx):
    # Prevent duplicate route registration.
    if "home" in smx.app.view_functions:
        return

    def head_html():
        # Determine a contrasting mobile text color based on the sidebar background.
        mobile_text_color = smx.theme["nav_text"]
        if smx.theme.get("sidebar_background", "").lower() in ["#eeeeee", "#ffffff"]:
            mobile_text_color = smx.theme.get("text_color", "#333")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <style>
            body {{
              font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
              margin: 0;
              padding: 0;
              background: {smx.theme["background"]};
              color: {smx.theme["text_color"]};
            }}
            /* Responsive typography using clamp */
            html {{
              font-size: clamp(14px, 1.5vw, 18px);
            }}
            /* Desktop Navbar */
            nav {{
              display: flex;
              justify-content: space-between;
              align-items: center;
              background: {smx.theme["nav_background"]};
              padding: 10px 20px;
              position: fixed;
              top: 0;
              left: 0;
              right: 0;
              z-index: 1000;
            }}
            .nav-left {{
              display: flex;
              align-items: center;
            }}
            .nav-left .logo {{
              font-size: clamp(1.3rem, 2vw, 1.5rem);
              font-weight: bold;
              color: {smx.theme["nav_text"]};
              margin-right: 20px;
            }}
            .nav-left .nav-links a {{
              font-size: clamp(1rem, 1.2vw, 1.2rem);
              color: {smx.theme["nav_text"]};
              text-decoration: none;
              margin-right: 15px;
            }}
            .nav-right a {{
              font-size: clamp(1rem, 1.2vw, 1.2rem);
              color: {smx.theme["nav_text"]};
              text-decoration: none;
            }}
            /* Hamburger button (hidden on desktop) */
            #hamburger-btn {{
              display: none;
              font-size: 2rem;
              background: none;
              border: none;
              color: {smx.theme["nav_text"]};
              cursor: pointer;
            }}
            /* Mobile nav menu */
            #mobile-nav {{
              position: fixed;
              top: 60px; 
              right: -260px; /* hidden off-screen by default */
              width: 170px;
              height: calc(100% - 60px);
              background: {smx.theme["sidebar_background"]};
              box-shadow: -2px 0 5px rgba(0,0,0,0.3);
              transition: right 0.3s ease;
              padding: 20px;
              display: flex;
              flex-direction: column;
              gap: 20px;
              z-index: 900;
              font-size: clamp(1.1rem, 2.5vw, 1.8rem);
              color: {mobile_text_color};
            }}
            #mobile-nav a {{
              font-size: inherit;
              color: {mobile_text_color};
              text-decoration: none;
            }}
            #mobile-nav.active {{
              right: 0;
            }}
            /* Responsive adjustments for mobile */
            @media (max-width: 768px) {{
              .nav-left .nav-links, .nav-right {{
                display: none;
              }}
              #hamburger-btn {{
                display: block;
              }}
            }}
            /* Sidebar styles */
            #sidebar {{
              position: fixed;
              top: 40px;
              left: -240px;
              width: 170px;
              height: calc(100% - 10px);
              background: {smx.theme["sidebar_background"]};
              overflow-y: auto;
              padding: 10px;
              box-shadow: 2px 0 5px rgba(0,0,0,0.3);
              transition: left 0.3s ease;
              z-index: 999;
              color: {get_contrast_color(smx.theme["sidebar_background"])};
            }}
            #sidebar a {{
              color: {get_contrast_color(smx.theme["sidebar_background"])};
              text-decoration: none;
            }}
            #sidebar.open {{
                left: 0;
            }}
            #sidebar-toggle-btn {{
              position: fixed;
              top: 42px;
              left: 0;
              z-index: 1000;
              background: {smx.theme["nav_text"]};
              color: {smx.theme["nav_text"]};
              padding: 4px;
              border-radius: 4px;
              cursor: pointer;
              transition: background-color 0.2s ease, transform 0.2s ease;
            }}
            #sidebar-toggle-btn:hover {{
              background-color: rgba(0, 0, 0, 0.05);
              transform: scale(1.2);
            }}
            #chat-history {{
              width: 100%;
              max-width: 850px;
              margin: 50px auto 10px auto;
              padding: 10px;
              background: {smx.theme["chat_background"]};
              border-radius: 8px;
              box-shadow: 0 2px 4px rgba(0,0,0,0.5);
              overflow-y: auto;
              min-height: 350px;
            }}
            #widget-container {{
              max-width: 850px;
              margin: 0 auto 40px auto;
            }}
            { _chat_css() }
            .closeable-div {{
              position: relative;
              padding: 20px;
              border: 1px solid #ccc;
              max-width: 70%;
              background-color: #fff;
            }}
            .close-btn {{
              position: absolute;
              top: 5px;
              right: 5px;
              cursor: pointer;
              font-size: 16px;
              padding: 2px 6px;
              color: #000;
            }}
            .close-btn:hover {{
              color: #ff0000;
            }}
          </style>
          <style>
            @keyframes spin {{
              0% {{ transform: rotate(0deg); }}
              100% {{ transform: rotate(360deg); }}
            }}
          </style>
          <style>
            .dropdown:hover .dropdown-content {{
                display: block;
            }}
          </style>
          <!-- Add MathJax -->
          <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
          <title>{smx.site_icon}{smx.site_title}{smx.page}</title>
        </head>
        <body>
          <script>
          // Toggle mobile nav menu on hamburger click
          document.addEventListener("DOMContentLoaded", function() {{
            var hamburger = document.getElementById("hamburger-btn");
            var mobileNav = document.getElementById("mobile-nav");
            hamburger.addEventListener("click", function() {{
              mobileNav.classList.toggle("active");
            }});
          }});
          </script>
        """
    
    def footer_html():
        # Returns a simple footer styled with theme variables.
        return f"""
        <footer style="width:100%; padding:10px; background:{smx.theme['nav_background']}; color:{smx.theme['nav_text']}; text-align:center; margin-top:20px;">
          <p style="margin:0; font-size: clamp(0.8rem, 1vw, 1rem);">
            &copy; {time.strftime('%Y')} {smx.site_title}. All rights reserved.
          </p>
        </footer>
        """

    def _chat_css():
        if smx.ui_mode == "bubble":
            return f"""
            .chat-message {{
              position: relative;
              max-width: 70%;
              margin: 10px 0;
              padding: 12px 18px;
              border-radius: 20px;
              animation: fadeIn 0.9s forwards;
              clear: both;
            }}
            .chat-message.user {{
              background: pink;
              float: right;
              margin-right: 15px;
              border-bottom-left-radius: 2px;
            }}
            .chat-message.user::before {{
              content: '';
              position: absolute;
              left: -8px;
              top: 12px;
              width: 0;
              height: 0;
              border: 8px solid transparent;
              border-right-color: pink;
              border-right: 0;
            }}
            .chat-message.bot {{
              background: #ffffff;
              float: left;
              margin-left: 15px;
              border-bottom-left-radius: 2px;
              border: 1px solid {smx.theme['chat_border']};
            }}
            .chat-message.bot::after {{
              content: '';
              position: absolute;
              right: -8px;
              top: 12px;
              width: 0;
              height: 0;
              border: 8px solid transparent;
              border-left-color: #ffffff;
              border-right: 0;
            }}
            .chat-message p {{
              margin: 0;
              padding: 0;
              word-wrap: break-word;
            }}
            """
        elif smx.ui_mode == "default":
            return f"""
            .chat-message {{
              display: block;
              width: 90%;
              margin: 15px auto;
              padding: 15px 20px;
              border-radius: 10px;
              background: linear-gradient(135deg, #ffffff, #f0f8ff);
              box-shadow: 0 2px 5px rgba(0,0,0,0.1);
              animation: fadeIn 0.9s forwards;
            }}
            .chat-message.user {{
              border: 1px solid {smx.theme['chat_border']};
              text-align: left;
            }}
            .chat-message.bot {{
              border: 1px solid {smx.theme['chat_border']};
              text-align: right;
            }}
            .chat-message p {{
              margin: 0;
              word-wrap: break-word;
            }}
            """
        elif smx.ui_mode == "card":
            return f"""
            .chat-message {{
              display: block;
              margin: 20px auto;
              padding: 20px 24px;
              border-radius: 16px;
              background: linear-gradient(135deg, #fff, #f7f7f7);
              box-shadow: 0 4px 12px rgba(0,0,0,0.15);
              max-width: 80%;
              animation: fadeIn 0.9s forwards;
              position: relative;
            }}
            .chat-message.user {{
              margin-left: auto;
              border: 2px solid {smx.theme['nav_background']};
            }}
            .chat-message.bot {{
              margin-right: auto;
              border: 2px solid {smx.theme['chat_border']};
            }}
            .chat-message p {{
              margin: 0;
              font-size: 1em;
              line-height: 1.2;
            }}
            .chat-message strong {{
              display: block;
              margin-bottom: 8px;
              color: {smx.theme['nav_background']};
              font-size: 0.9em;
            }}
            """
        elif smx.ui_mode == "smx":
            return f"""
            .chat-message {{
              display: block;
              margin: 15px auto;
              padding: 16px 22px;
              border-radius: 12px;
              animation: fadeIn 0.9s forwards;
              max-width: 85%;
              background: #ffffff;
              border: 2px solid {smx.theme['nav_background']};
              position: relative;
            }}
            .chat-message.user {{
              background: #f9f9f9;
              border-color: {smx.theme['chat_border']};
              text-align: left;
            }}
            .chat-message.bot {{
              background: #e9f7ff;
              border-color: {smx.theme['nav_background']};
              text-align: right;
            }}
            .chat-message p {{
              margin: 0;
              word-wrap: break-word;
              font-size: 1em;
            }}
            """
        else:
            return f"""
            .chat-message {{
              display: block;
              width: 90%;
              margin-bottom: 10px;
              padding: 12px 18px;
              border-radius: 8px;
              animation: fadeIn 0.9s forwards;
            }}
            .chat-message.user {{
              background: #e1f5fe;
              text-align: right;
              margin-left: auto;
              max-width: 50%;
            }}
            .chat-message.bot {{
              background: #ffffff;
              border: 1px solid {smx.theme["chat_border"]};
              text-align: left;
              max-width: 80%;
            }}
            """
    def _generate_nav():
        logo = f'<a href="/" style="color: inherit; text-decoration: none;">{smx.site_icon}{smx.site_logo}</a>'
        nav_links = ""
        for page in smx.pages:
            nav_links += f'<a href="/page/{page}">{page}</a>'
        # nav_links += '<a href="/admin">Admin</a>'
        theme_link = ''
        if smx.theme_toggle_enabled:
            theme_link = '<a href="/toggle_theme">Theme</a>'
        desktop_nav = f"""
        <div class="nav-left">
          <span class="logo">{logo}</span>
          <div class="nav-links">
            {nav_links}
          </div>
        </div>
        <div class="nav-right">
          {theme_link}
        </div>
        """
        hamburger_btn = '<button id="hamburger-btn">&#9776;</button>'
        mobile_nav = f"""
        <div id="mobile-nav">
          {nav_links}
          {theme_link}
        </div>
        """
        return f"""
        <nav>
          {desktop_nav}
          {hamburger_btn}
        </nav>
        {mobile_nav}
        """
    
    def _render_widgets():
        """
        Renders the default system widget (the user_query text area with inner icons)
        and then any additional developer-defined widgets.
        Developer file upload triggered by the paper clip now supports multiple files.
        """
        form_html = """
        <form id="chat-form" onsubmit="submitChat(event)"
              style="width:100%; max-width:800px; margin:100px auto 20px auto; padding:0 10px; box-sizing:border-box;">
          <input type="hidden" id="action-field" name="action" value="submit_query">
        """

        horizontal_buttons_html = ""

        for key, widget in smx.widgets.items():
            """<span class="icon-default" style="cursor:pointer; transition:transform 0.2s ease;" title="Attach"
                          onclick="document.getElementById('user-file-upload').click();">
                          📎
                    </span>"""
            # For the 'user_query' text input with injected icons and submit button.
            if widget["type"] == "text_input" and widget["key"] == "user_query":
                form_html += f"""
                <div style="position: relative; margin-bottom:15px; padding:10px 5px; width:100%; box-sizing:border-box;">
                  <textarea
                    id="user_query"
                    name="{key}"
                    rows="2"
                    placeholder="{widget.get('placeholder','')}"
                    style="
                      position: absolute;
                      bottom:0; left:0;
                      width:100%;
                      padding:12px 12px 50px 12px;
                      font-size:1em;
                      border:1px solid #ccc;
                      border-radius:8px;
                      box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                      overflow:hidden; resize:none; box-sizing:border-box;
                    "
                    oninput="this.style.height='auto'; this.style.height=(this.scrollHeight)+'px'; checkInput(this)"
                    autofocus
                  >{session.get(key, '')}</textarea>

                  <!-- Inline icons -->
                  <div style="position:absolute; bottom:12px; left:10px; display:flex; gap:15px;">
                    <!-- “+” opens the hidden PDF‐upload input -->
                    <span class="icon-default"
                          title="Upload PDF files for this chat"
                          style="cursor:pointer; transition:transform 0.2s ease;"
                          onclick="document.getElementById('user_pdfs').click()">
                      ➕
                    </span>
                    <!--
                    <span class="icon-default"
                          title="Internet"
                          style="cursor:pointer; transition:transform 0.2s ease;">
                      🌐
                    </span>
                    <span class="icon-default"
                          title="Search"
                          style="cursor:pointer; transition:transform 0.2s ease;">
                      🔍
                    </span> 
                    -->
                  </div>

                  <!-- Hidden file‐upload input bound to smx.file_uploader('user_pdfs',…) -->
                  <input
                    type="file"
                    id="user_pdfs"
                    name="user_pdfs"
                    multiple
                    style="display:none"
                    onchange="uploadUserFileAndProcess(this, 'user_pdfs')"
                  />

                  <!-- Send button -->
                  <button
                    type="submit"
                    id="submit-button"
                    name="submit_query"
                    value="clicked"
                    onclick="document.getElementById('action-field').value='submit_query'"
                    style="
                      position:absolute;
                      bottom:12px; right:10px;
                      width:36px; height:36px;
                      border-radius:50%; border:none;
                      opacity:0.5;
                      background:{smx.theme['nav_background']};
                      color:{smx.theme['nav_text']};
                      cursor:pointer; font-size:1.2em;
                      display:flex; align-items:center; justify-content:center;
                    "
                    disabled
                  >⬆</button>
                </div>
                """

            elif widget["type"] == "button" and widget["key"] == "submit_query":
                continue
            elif widget["type"] == "button":
                horizontal_buttons_html += f"""
                <button
                    type="submit"
                    name="{key}"
                    value="clicked"
                    onclick="document.getElementById('action-field').value='{key}'"
                    style="
                        padding:10px 20px;
                        border:none;
                        border-radius:30px;
                        background:{smx.theme['nav_background']};
                        color:{smx.theme['nav_text']};
                        cursor:pointer;
                        transition: background 0.3s;
                    "
                    onmouseover="this.style.backgroundColor='#e0e0e0';"
                    onmouseout="this.style.backgroundColor='{smx.theme['nav_background']}';"
                >
                    {widget['label']}
                </button>
                """
            elif widget["type"] == "text_input":
                form_html += f"""
                <div style="margin-bottom:15px;">
                  <label for="{key}" style="display:block; margin-bottom:5px;">{widget['label']}</label>
                  <input type="text" id="{key}" name="{key}" placeholder="{widget.get('placeholder','')}"
                        value="{session.get(key, '')}"
                        style="
                            width:calc(100% - 20px);
                            padding:12px; font-size:1em;
                            border:1px solid #ccc;
                            border-radius:8px;
                            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                            box-sizing:border-box;
                        "
                  >
                </div>
                """
            elif widget["type"] == "file_upload":
                uploaded = request.files.getlist(key)
                if uploaded:
                    sid = smx.get_session_id()
                    for f in uploaded:
                        raw = f.read()
                        reader = PdfReader(BytesIO(raw))
                        text = "".join(page.extract_text() or "" for page in reader.pages)
                        chunks = recursive_text_split(text)
                        smx.add_user_chunks(sid, chunks)
                    # invoke the one callback you registered
                    if widget.get("callback"):
                        widget["callback"]()

        if horizontal_buttons_html:
            form_html += f"""
            <div style="display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:15px;">
                {horizontal_buttons_html}
            </div>
            """
        
        form_html += "</form>"
        
        form_html += """
        <script>
          function checkInput(textarea) {
            var submitBtn = document.getElementById("submit-button");
            if (!submitBtn) return;
            if (textarea.value.trim() === "") {
              submitBtn.disabled = true;
              submitBtn.style.opacity = "0.5";
            } else {
              submitBtn.disabled = false;
              submitBtn.style.opacity = "1";
            }
          }
          // Animate icons on hover
          var icons = document.getElementsByClassName('icon-default');
          for (var i = 0; i < icons.length; i++) {
            icons[i].addEventListener('mouseover', function() {
              this.style.transform = "scale(1.2)";
            });
            icons[i].addEventListener('mouseout', function() {
              this.style.transform = "scale(1)";
            });
          }
          
          // AJAX function to upload multiple user files
          function uploadUserFile(inputElement) {
            if (inputElement.files.length > 0) {
              var formData = new FormData();
              for (var i = 0; i < inputElement.files.length; i++) {
                  formData.append("user_files", inputElement.files[i]);
              }
              fetch('/upload_user_file', {
                  method: "POST",
                  body: formData
              })
              .then(response => response.json())
              .then(data => {
                  if(data.error) {
                      alert("Error: " + data.error);
                  } else {
                      alert("Uploaded files: " + data.uploaded_files.join(", "));
                      // Optionally, store or display file paths returned by the server.
                  }
              })
              .catch(err => {
                  console.error(err);
                  alert("Upload failed.");
              });
            }
          }
        </script>
        <script>
          // When you pick files, stash the action to your widget key
          // then fire submitChat with submitter.id = that key.
          function uploadUserFileAndProcess(inputEl, actionKey) {
            if (!inputEl.files.length) return;
            // set action-field so process_chat knows which widget to invoke
            document.getElementById('action-field').value = actionKey;
            // pass submitter.id = actionKey so we don't override it below
            submitChat({ preventDefault(){}, submitter:{ id: actionKey } });
          }

          // Override only when clicking the “Send” button.
          async function submitChat(e) {
            e.preventDefault();
            document.getElementById('loading-spinner').style.display = 'block';

            // Only reset to 'submit_query' when it really came from the send‑button
            if (e.submitter && e.submitter.id === 'submit-button') {
              document.getElementById('action-field').value = 'submit_query';
            }

            const form = document.getElementById('chat-form');
            const formData = new FormData(form);
            const action = document.getElementById('action-field').value;
            if (!formData.has(action)) {
              formData.append(action, 'clicked');
            }

            try {
              const response = await fetch('/process_chat', {
                method: 'POST',
                body: formData
              });
              const data = await response.json();
              document.getElementById("chat-history").innerHTML = data.chat_html;

              let outputContainer = document.getElementById('system-output-container');
              if (outputContainer) {
                outputContainer.innerHTML = data.system_output_html;
              } else if (data.system_output_html.trim() !== "") {
                outputContainer = document.createElement('div');
                outputContainer.id = 'system-output-container';
                outputContainer.style = "max-width:850px; margin:20px auto; padding:10px; background:#fff; border:1px solid #ccc; border-radius:8px; margin-top:150px;";
                outputContainer.innerHTML = data.system_output_html;
                document.body.prepend(outputContainer);
              }

              // Clear the user query textarea only on a real “Send”
              if (document.getElementById('action-field').value === 'submit_query') {
                const ta = document.querySelector('textarea[name="user_query"]');
                ta.value = "";
                checkInput(ta);
              }

              const chatHistory = document.getElementById("chat-history");
              chatHistory.scrollTop = chatHistory.scrollHeight;
              window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            } catch (err) {
              console.error("Error processing chat:", err);
            } finally {
              document.getElementById('loading-spinner').style.display = 'none';
            }
          }

          // wire up Enter→Send
          document.addEventListener("DOMContentLoaded", () => {
            const ta = document.querySelector('textarea[name="user_query"]');
            if (ta) {
              ta.addEventListener("keydown", evt => {
                if (evt.key === "Enter" && !evt.shiftKey) {
                  document.getElementById('action-field').value = 'submit_query';
                  submitChat(evt);
                  evt.preventDefault();
                }
              });
            }
          });
        </script>
        """      
        return form_html

            
    def _render_session_sidebar():
        current = session.get("current_session", {"title": "Current"})
        current_display = current.get("title", "Current")
        past_sessions = session.get("past_sessions", [])
        sidebar_html = '<div id="sidebar">'
        sidebar_html += (
            '<div style="margin-bottom: 10px;">'
            '<button type="button" onclick="createNewChat()" style="width:100%; padding: 8px;">New Chat</button>'
            '</div>'
        )
        if current_display == "Current":
            sidebar_html += f'''
                <div class="session-item active" style="margin-bottom: 15px; color: {smx.theme["nav_text"]};">
                  <span class="session-title" style="cursor: default;">{current_display}</span>
                </div>
            '''
        if past_sessions:
            sidebar_html += f'''
                <hr style="margin:10px 0;">
                <div style="color: {smx.theme["nav_background"]};"><strong>Chats</strong></div>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
            '''
            for s in past_sessions:
                safe_title = s["title"]
                display_title = safe_title if len(safe_title) <= 15 else safe_title[:15] + "..."
                active_class = " active" if s["id"] == current.get("id") and current_display != "Current" else ""
                sidebar_html += f'''
                    <li class="session-item{active_class}" data-session-id="{s["id"]}">
                      <span class="session-title" title="{safe_title}" onclick="setSession('{s["id"]}', this)">{display_title}</span>
                      <span class="session-ellipsis" onclick="event.stopPropagation(); toggleSessionMenu('{s["id"]}')">&#8230;</span>
                      <div class="session-menu" id="menu-{s["id"]}">
                          <div class="menu-item" onclick="openRenameModal('{s["id"]}', '{safe_title}')"><span>&#9998;</span> Rename</div>
                          <div class="menu-item" onclick="openDeleteModal('{s["id"]}')"><span>&#128465;</span> Delete</div>
                      </div>
                    </li>
                '''
            sidebar_html += '</ul>'
        sidebar_html += '</div>'
        extra = f"""
        <style>
          .session-item {{
              position: relative;
              padding: 5px 10px;
              border-radius: 4px;
              cursor: pointer;
              display: flex;
              justify-content: space-between;
              align-items: center;
              transition: background 0.3s;
          }}
          .session-item:hover {{
              background-color: {smx.theme.get('sidebar_hover', '#cccccc')};
          }}
          .session-item.active {{
              background-color: {smx.theme.get('sidebar_active', '#aaaaaa')};
          }}
          .session-title {{
              flex-grow: 1;
          }}
          .session-ellipsis {{
              display: none;
              margin-left: 5px;
          }}
          .session-item:hover .session-ellipsis {{
              display: inline-block;
          }}
          .session-menu {{
              display: none;
              position: absolute;
              right: 0;
              top: 50%;
              transform: translateY(-50%);
              background: #fff;
              border: 1px solid #ccc;
              min-width: 100px;
              z-index: 10;
              padding: 5px;
          }}
          .menu-item {{
              padding: 3px 5px;
              cursor: pointer;
          }}
          .menu-item:hover {{
              background: #eee;
          }}
        </style>
        """
        return sidebar_html + extra

    new_chat_js = """
    <script>
      function createNewChat() {
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/";
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "action";
        input.value = "new_session";
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
      }
    </script>
    """
    
    def clear_chat_history():
        session["chat_history"] = []
        session.modified = True
    smx.clear_chat_history = clear_chat_history
    
    @smx.app.route("/", methods=["GET", "POST"])
    def home():
        smx.page = ""
        if session.get("app_token") != smx.app_token:
            current_history = session.get("chat_history", [])
            current_session = session.get("current_session", {"id": str(uuid.uuid4()), "title": "Current", "history": []})
            past_sessions = session.get("past_sessions", [])
            if current_history:
                exists = any(s["id"] == current_session["id"] for s in past_sessions)
                if not exists:
                    generated_title = core.SyntaxMUI.generate_contextual_title(current_history)
                    current_session["title"] = generated_title
                    current_session["history"] = current_history.copy()
                    past_sessions.insert(0, current_session)
                else:
                    for s in past_sessions:
                        if s["id"] == current_session["id"]:
                            s["history"] = current_history.copy()
                            break
                session["past_sessions"] = past_sessions
            session["current_session"] = {"id": str(uuid.uuid4()), "title": "Current", "history": []}
            session["chat_history"] = []
            session["app_token"] = smx.app_token
        if request.method == "POST":
            action = request.form.get("action")
            if action == "clear_chat":
                session["chat_history"] = []
            elif action == "new_session":
                current_history = session.get("chat_history", [])
                current_session = session.get("current_session", {"id": str(uuid.uuid4()), "title": "Current", "history": []})
                past_sessions = session.get("past_sessions", [])
                exists = any(s["id"] == current_session["id"] for s in past_sessions)
                if current_history:
                    if not exists:
                        generated_title = core.SyntaxMUI.generate_contextual_title(current_history)
                        current_session["title"] = generated_title
                        current_session["history"] = current_history.copy()
                        past_sessions.insert(0, current_session)
                    else:
                        for s in past_sessions:
                            if s["id"] == current_session["id"]:
                                s["history"] = current_history.copy()
                                break
                    session["past_sessions"] = past_sessions
                session["current_session"] = {"id": str(uuid.uuid4()), "title": "Current", "history": []}
                session["chat_history"] = []
            session["app_token"] = smx.app_token
        nav_html = _generate_nav()
        chat_html = render_chat_history(smx)
        widget_html = _render_widgets()
        sidebar_html = _render_session_sidebar()
        
        scroll_and_toggle_js = """
        <script>
          async function submitChat(e) {
            e.preventDefault();
            e.preventDefault();
            document.getElementById('loading-spinner').style.display = 'block';
            // If the event came from a button click and the clicked button is the default submit button,
            // or if it came from a keydown event (where event.submitter is undefined), reset the action field.
            if ((e.submitter && e.submitter.id === "submit-button") || !e.submitter) {
              document.getElementById("action-field").value = "submit_query";
            }

            const form = document.getElementById('chat-form');
            const formData = new FormData(form);
            const action = document.getElementById('action-field').value;
            if (!formData.has(action)) {
              formData.append(action, 'clicked');
            }
            try {
              const response = await fetch('/process_chat', {
                method: 'POST',
                body: formData
              });
              const data = await response.json();
              document.getElementById("chat-history").innerHTML = data.chat_html;
              let outputContainer = document.getElementById('system-output-container');
              if (outputContainer) {
                outputContainer.innerHTML = data.system_output_html;
              } else if(data.system_output_html.trim() !== "") {
                outputContainer = document.createElement('div');
                outputContainer.id = 'system-output-container';
                outputContainer.style = "max-width:850px; margin:20px auto; padding:10px; background:#fff; border:1px solid #ccc; border-radius:8px; margin-top:150px;";
                outputContainer.innerHTML = data.system_output_html;
                document.body.prepend(outputContainer);
              }
              if (action === 'submit_query') {
                const userQuery = document.querySelector('textarea[name="user_query"]');
                userQuery.value = "";
                checkInput(userQuery);
              }
              const chatHistory = document.getElementById("chat-history");
              chatHistory.scrollTop = chatHistory.scrollHeight;
              window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            } catch (error) {
              console.error("Error processing chat:", error);
            } finally {
              document.getElementById('loading-spinner').style.display = 'none';
            }
          }

          document.addEventListener("DOMContentLoaded", function(){
            const textArea = document.querySelector('textarea[name="user_query"]');
            if(textArea) {
              textArea.addEventListener("keydown", function(event) {
                // When Enter is pressed without the Shift key, set the action-field to 'submit_query'
                if(event.key === "Enter" && !event.shiftKey){
                  event.preventDefault();
                  document.getElementById("action-field").value = "submit_query";
                  submitChat(event);
                }
              });
            }
          });
        </script>
        
        """
        page_html = f"""<!DOCTYPE html>
        <html>
        <head>
          {head_html()}
        </head>
        <body>
          {nav_html}
          <button
            id="sidebar-toggle-btn"
            data-icon-open="{url_for('static', filename='icons/svg_497526.svg')}"
            data-icon-close="{url_for('static', filename='icons/svg_497528.svg')}"
          >
            <img
              id="sidebar-toggle-icon"
              src="{url_for('static', filename='icons/svg_497526.svg')}"
              alt="Toggle Sidebar"
              style="width:24px; height:24px;"
            />
          </button>



          <div id="sidebar-container">{sidebar_html}</div>         
          <div id="loading-spinner" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000;">
              <div class="spinner" style="border: 8px solid #f3f3f3; border-top: 8px solid {smx.theme['nav_background']}; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
          </div>
          <div id="chat-history">{chat_html}</div>
          <div id="widget-container">{widget_html}</div>
          {scroll_and_toggle_js}
          {new_chat_js}
+         <script src="{ url_for('static', filename='js/sidebar.js') }"></script>
        </body>
        </html>"""
        return render_template_string(page_html)
    
    @smx.app.route("/system_output")
    def system_output():
        return session.get("system_output", "")
    
    # Serve the raw media files
    @smx.app.route('/uploads/media/<path:filename>')
    def serve_media(filename):
        media_dir = os.path.join(os.getcwd(), 'uploads', 'media')
        return send_from_directory(media_dir, filename)

    # Override the generic page renderer to inject a gallery on the "service" page
    @smx.app.route('/page/<page_name>')
    def view_page(page_name):
        smx.page = '-' + page_name.lower()
        nav_html = _generate_nav()
        content = smx.pages.get(page_name, f"No content found for page '{page_name}'.")
        
        # only on the service page, build a gallery
        media_html = ''
        if page_name.lower() == 'service':
            media_folder = os.path.join(os.getcwd(), 'uploads', 'media')
            if os.path.isdir(media_folder):
                files = sorted(os.listdir(media_folder))
                # wrap each file in an <img> tag (you can special‑case videos if you like)
                thumbs = []
                for fn in files:
                    src = url_for('serve_media', filename=fn)
                    thumbs.append(f'<img src="{src}" alt="{fn}" style="max-width:150px; margin:5px;"/>')
                if thumbs:
                    media_html = f'''
                      <section id="media-gallery" style="margin-top:20px;">
                        <h3>Media Gallery</h3>
                        <div style="display:flex; flex-wrap:wrap; gap:10px;">
                          {''.join(thumbs)}
                        </div>
                      </section>
                    '''

        page_html = f"""
        <!DOCTYPE html>
        <html>
        <head>{head_html()}</head>
        <body>
          {nav_html}
          <div style="margin-top:20px; width:100%; padding:10px; box-sizing:border-box;">
            <div style="text-align:center; margin-top:20px; border:1px solid #ccc; padding:10px; 
                        border-radius:8px; background-color:#f9f9f9;">
              <h2>{page_name}</h2>
              <div>{content}</div>
              {media_html}
              <a class="button" href="/">Return to Home</a>
            </div>
          </div>
          {footer_html()}
        </body>
        </html>
        """
        return render_template_string(page_html)
    
    @smx.app.route("/admin", methods=["GET", "POST"])
    def admin_panel():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "upload_files":
                files = request.files.getlist("upload_files")
                upload_folder = os.path.join(os.getcwd(), "uploads", "sys")
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                saved_count = 0

                for file in files:
                    if file and file.filename.lower().endswith(".pdf"):
                        filepath = os.path.join(upload_folder, file.filename)
                        file.save(filepath)
                        saved_count += 1
                # Now process all PDFs there and cache into smx.admin_pdf_chunks
                mapping = process_admin_pdf_files(upload_folder)
                smx.admin_pdf_chunks = mapping

                total_chunks = sum(len(chunks) for chunks in mapping.values())
                session["upload_msg"] = (
                    f"Uploaded {saved_count} PDF(s); "
                    f"Processed {len(mapping)} files into {total_chunks} chunks."
                )

            elif action == "delete_sys_file":
              file_name = request.form.get("sys_file", "").strip()
              if file_name:
                  # where our system PDFs live
                  sys_dir = os.path.join(os.getcwd(), "uploads", "sys")
                  remove_admin_pdf_file(sys_dir, file_name)
                  smx.admin_pdf_chunks.pop(file_name, None)
                  session["upload_msg"] = f"Deleted {file_name} and its chunks."

            elif action == "add_page":
                page_name = request.form.get("page_name", "").strip()
                page_content = request.form.get("page_content", "").strip()
                if page_name and page_name not in smx.pages:
                    db.add_page(page_name, page_content)

            elif action == "delete_page":
                del_page = request.form.get("delete_page", "").strip()
                if del_page in smx.pages:
                    db.delete_page(del_page)

            return redirect(url_for("admin_panel"))
        
        smx.pages = db.get_pages()
        upload_msg = session.pop("upload_msg", "")
        alert_script = f"<script>alert('{upload_msg}');</script>" if upload_msg else ""
        # Generate individual page cards for the Manage Pages section.
        page_cards = ""
        for p in smx.pages:
            page_cards += f"""
                <div style="border: 1px solid #ddd; border-radius: 4px; padding:10px; margin-bottom:10px;">
                    <strong>{p}</strong>
                    <div style="text-align: right; margin-top: 10px;">
                        <a class="button" href="/admin/edit/{p}">Edit</a>
                        <form method="post" style="display:inline;">
                            <input type="hidden" name="delete_page" value="{p}">
                            <button type="submit" name="action" value="delete_page" style="margin-left:5px;">X</button>
                        </form>
                    </div>
                </div>
            """
        # scan for system PDFs
        sys_dir = os.path.join(os.getcwd(), "uploads", "sys")
        sys_files = []
        if os.path.isdir(sys_dir):
            sys_files = [f for f in os.listdir(sys_dir) if f.lower().endswith(".pdf")]

        # build HTML for the Manage System PDFs card
        sys_files_html = ""
        for f in sys_files:
            sys_files_html += f"""
              <li style="margin-bottom:8px;">
                {f}
                <form method="post" style="display:inline; margin-left:10px;">
                  <input type="hidden" name="sys_file" value="{f}">
                  <button type="submit" name="action" value="delete_sys_file">X</button>
                </form>
              </li>"""
        sys_files_card = f"""
        <div class="card">
          <h3>Manage System PDFs</h3>
          <div class="scrollable-list">
            <ul style="list-style:none; padding-left:0; margin:0;">
              {sys_files_html or "<li>No PDFs found.</li>"}
            </ul>
          </div>
        </div>
        """

        # Render the dashboard layout.
        return render_template_string(f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>{smx.site_icon}{smx.site_title} Admin Dashboard</title>
          <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #f4f7f9;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .card {{
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}
            .grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .grid > .card {{
                flex: 1 1 calc(33.333% - 20px);
                min-width: 280px;
            }}
            input, textarea, select {{
                padding: 10px;
                font-size: 1em;
                margin: 5px 0 15px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            button {{
                padding: 10px 20px;
                font-size: 1em;
                background: #007acc;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{
                background: #005fa3;
            }}
            a.button {{
                display: inline-block;
                padding: 10px 20px;
                background: #007acc;
                color: #fff;
                border-radius: 4px;
                text-decoration: none;
                margin-right: 10px;
            }}
            a.button:hover {{
                background: #005fa3;
            }}
            .scrollable-list {{
              max-height: 125px;      /* or however tall you want the card to be */
              overflow-y: auto;       /* turn on a vertical scrollbar */
              padding-right: 10px;    /* leave some room for the scrollbar */
              margin-top: 10px;       /* space out the heading from the list */
            }}
            /* Striped backgrounds for the SYSTEM PDF list */
            .scrollable-list ul {{
              list-style: none;
              padding-left: 0;
              margin: 0;
            }}
            .scrollable-list ul li:nth-child(odd) {{
              background-color: #bde6f7;
            }}
            .scrollable-list ul li:nth-child(even) {{
              background-color: #d1d6d8;
            }}
            .scrollable-list ul li {{
              padding: 3px;
            }}

            /* Striped backgrounds for the PAGES list */
            .scrollable-pages > div:nth-child(odd) {{
              background-color: #f9f9f9;
            }}
            .scrollable-pages > div:nth-child(even) {{
              background-color: #ffffff;
            }}
            .scrollable-pages > div {{
              padding: 8px;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <h1>Admin Dashboard</h1>
            {alert_script}
            <div class="grid">
                <!-- Upload PDF Card -->
                <div class="card">
                  <h3>Upload PDF Files</h3>
                  <form method="post" enctype="multipart/form-data">
                        <input type="file" name="upload_files" accept=".pdf" multiple>
                        <div style="text-align:right;">
                            <button type="submit" name="action" value="upload_files">Upload</button>
                        </div>
                  </form>
                </div>
                <!--
                <form method="post" enctype="multipart/form-data">
                    <label for="pdf_path">PDF Files Directory:</label>
                    <input type="text" name="pdf_path" value="uploads/sys" placeholder="Enter directory path">
                    <button type="submit" name="action" value="process_pdfs">Process PDFs</button>
                </form>
                -->
                <div class="card">
                  {sys_files_card}
                </div>
                <!-- Add New Page Card -->
                <div class="card">
                  <h3>Add New Page</h3>
                  <form method="post">
                        <input type="text" name="page_name" placeholder="Page Name" required>
                        <textarea name="page_content" placeholder="Page Content"></textarea>
                        <div style="text-align:right;">
                            <button type="submit" name="action" value="add_page">Add Page</button>
                        </div>
                  </form>
                </div>

                <!-- Manage Pages Card -->
                <div class="card">
                  <h3>Manage Pages</h3>
                  <div class="scrollable-list">
                        {page_cards}
                  </div>
                </div>

                <!-- Media Files Card -->
                <div class="card">
                  <h3>Upload Media Files</h3>
                  <form id="media-upload-form" method="post" enctype="multipart/form-data" action="/admin/upload_media">
                      <input type="file" name="media_files" accept="image/*,video/*" multiple>
                      <div style="text-align:right;">
                          <button type="submit">Upload Media</button>
                      </div>
                  </form>
                  <div id="media-upload-result"></div>
                </div>
                <!-- Theme Toggle Card -->
            </div>
            <div style="text-align: center; margin-top:20px;">
              <a class="button" href="/">Return to Home</a>
            </div>
          </div>
          <script>
            document.getElementById("media-upload-form").addEventListener("submit", function(e) {{
                e.preventDefault();
                var formData = new FormData(this);
                fetch("/admin/upload_media", {{ method: "POST", body: formData }})
                  .then(response => response.json())
                  .then(data => {{
                      var resultDiv = document.getElementById("media-upload-result");
                      if (data.file_paths && data.file_paths.length > 0) {{
                          resultDiv.innerHTML = "<p>Uploaded Media Files:</p><ul>" + 
                              data.file_paths.map(path => `<li>${{path}}</li>`).join("") + "</ul><p>Copy the path you need and insert it into your HTML.</p>";
                      }} else {{
                          resultDiv.innerHTML = "<p>No files were uploaded.</p>";
                      }}
                  }})
                  .catch(err => {{
                      console.error("Error uploading media:", err);
                      document.getElementById("media-upload-result").innerHTML = "<p>Error uploading files.</p>";
                  }});
            }});
          </script>
        </body>
        </html>
        """)
    # In syntaxmatrix/routes.py

    @smx.app.route("/admin/chunks", methods=["GET"])
    def list_chunks():
        # Retrieve all chunks from the database
        chunks = db.get_all_pdf_chunks()
        # Render them in a simple HTML table (for demo purposes)
        html = "<h2>PDF Chunk Records</h2><table border='1'><tr><th>ID</th><th>Source File</th><th>Index</th><th>Text Snippet</th><th>Actions</th></tr>"
        for chunk in chunks:
            snippet = chunk['chunk_text'][:100] + "..."
            html += f"<tr><td>{chunk.get('id', 'N/A')}</td><td>{chunk['source_file']}</td><td>{chunk['chunk_index']}</td>"
            html += f"<td>{snippet}</td>"
            html += f"<td><a href='/admin/chunks/edit/{chunk.get('id')}'>Edit</a> "
            html += f"<a href='/admin/chunks/delete/{chunk.get('id')}'>Delete</a></td></tr>"
        html += "</table>"
        return html

    @smx.app.route("/admin/chunks/edit/<int:chunk_id>", methods=["GET", "POST"])
    def edit_chunk(chunk_id):
        if request.method == "POST":
            new_text = request.form.get("chunk_text")
            db.update_pdf_chunk(chunk_id, new_text)
            return redirect(url_for("list_chunks"))
        # For GET, load the specific chunk and render an edit form.
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, source_file, chunk_index, chunk_text FROM pdf_chunks WHERE id = ?", (chunk_id,))
        chunk = cursor.fetchone()
        conn.close()
        if not chunk:
            return "Chunk not found", 404
        # Render a simple HTML form
        html = f"""
        <h2>Edit Chunk {chunk[0]} (from {chunk[1]}, index {chunk[2]})</h2>
        <form method="post">
            <textarea name="chunk_text" rows="10" cols="80">{chunk[3]}</textarea><br>
            <button type="submit">Save Changes</button>
        </form>
        """
        return html

    @smx.app.route("/admin/chunks/delete/<int:chunk_id>", methods=["GET"])
    def delete_chunk(chunk_id):
        db.delete_pdf_chunk(chunk_id)
        return redirect(url_for("list_chunks"))

    @smx.app.route("/admin/edit/<page_name>", methods=["GET", "POST"])
    def edit_page(page_name):
        if request.method == "POST":
            new_page_name = request.form.get("page_name", "").strip()
            new_content = request.form.get("page_content", "").strip()
            if page_name in smx.pages and new_page_name:
                db.update_page(page_name, new_page_name, new_content)
                return redirect(url_for("admin_panel"))
        # Load the full content for the page to be edited.
        content = smx.pages.get(page_name, "")
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Edit Page - {{ page_name }}</title>
          <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #f4f7f9;
                padding: 20px;
            }
            .editor {
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            input, textarea {
                width: 100%;
                margin: 10px 0;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                padding: 10px 20px;
                background: #007acc;
                border: none;
                color: #fff;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #005fa3;
            }
            a.button {
                padding: 10px 20px;
                background: #aaa;
                border: none;
                color: #fff;
                border-radius: 4px;
                text-decoration: none;
            }
            a.button:hover {
                background: #888;
            }
          </style>
        </head>
        <body>
          <div class="editor">
            <h1>Edit Page - {{ page_name }}</h1>
            <form method="post">
                <input type="text" name="page_name" value="{{ page_name }}" required>
                <textarea name="page_content" rows="20">{{ content }}</textarea>
                <div style="margin-top:15px;">
                  <button type="submit">Update Page</button>
                  <a class="button" href="{{ url_for('admin_panel') }}">Cancel</a>
                </div>
            </form>
          </div>
        </body>
        </html>
        """, page_name=page_name, content=content)
    
    @smx.app.route("/admin/upload_media", methods=["POST"])
    def upload_media():
        import os
        from flask import jsonify
        # Define the media folder.
        media_folder = os.path.join(os.getcwd(), "uploads", "media")
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)
        
        # Retrieve uploaded media files (images, videos, etc.).
        uploaded_files = request.files.getlist("media_files")
        file_paths = []
        for file in uploaded_files:
            if file.filename:
                filepath = os.path.join(media_folder, file.filename)
                file.save(filepath)
                # This path can be copied by the developer. Adjust if you have a web server serving these files.
                file_paths.append(f"/uploads/media/{file.filename}")
        return jsonify({"file_paths": file_paths})
    

    @smx.app.route("/toggle_theme", methods=["GET"])
    def toggle_theme():
        current = session.get("theme", "light")
        themes_list = list(DEFAULT_THEMES.keys())
        try:
            current_index = themes_list.index(current)
        except ValueError:
            current_index = 0
        new_index = (current_index + 1) % len(themes_list)
        new_theme = themes_list[new_index]
        session["theme"] = new_theme
        smx.set_theme(new_theme, DEFAULT_THEMES[new_theme])
        return redirect(url_for("home"))
    
    @smx.app.route("/rename_session", methods=["POST"])
    def rename_session():
        sess_id    = request.form.get("session_id")
        new_title  = request.form.get("new_title","").strip()
        if not sess_id or not new_title:
            return "Invalid request", 400

        if session.get("current_session",{}).get("id") == sess_id:
            session["current_session"]["title"] = new_title

        past = session.get("past_sessions", [])
        for s in past:
            if s["id"] == sess_id:
                s["title"] = new_title
        session["past_sessions"] = past
        session.modified = True

        return jsonify({ "new_title": new_title }), 200
    
    @smx.app.route("/delete_session", methods=["POST"])
    def delete_session():
        sess_id = request.form.get("session_id")
        if not sess_id:
            return "Invalid request", 400

        past = session.get("past_sessions", [])
        past = [s for s in past if s["id"] != sess_id]
        session["past_sessions"] = past

        # if they deleted the session we were in, spin up a fresh “Current”:
        if session.get("current_session",{}).get("id") == sess_id:
            session["current_session"] = { "id": str(uuid.uuid4()), "title": "Current", "history": [] }
            session["chat_history"]   = []

        session.modified = True

        # send back just the new chat-history HTML
        chat_html = render_chat_history(smx)
        return jsonify({ "chat_html": chat_html }), 200

    @smx.app.route("/process_chat", methods=["POST"])
    def process_chat():
        # 1) Handle any registered widgets, including file_uploads:
        for key, widget in smx.widgets.items():
            if widget["type"] == "text_input":
                session[key] = request.form.get(key, widget.get("placeholder", ""))

            elif widget["type"] == "file_upload":
                # if the user attached files under this widget…
                uploaded = request.files.getlist(key)
                if not uploaded:
                    continue

                sid = smx.get_session_id()
                for f in uploaded:
                    try:
                        raw = f.read()
                        # skip zero‑length reads
                        if not raw:
                            continue

                        reader = PdfReader(BytesIO(raw))
                        text = "".join(page.extract_text() or "" for page in reader.pages)
                        chunks = recursive_text_split(text)
                        smx.add_user_chunks(sid, chunks)

                    # except EmptyFileError:
                    #     # this was an empty file, skip it
                    #     continue
                    except Exception as e:
                        # log it but don’t interrupt /process_chat
                        smx.warning(f"Could not process uploaded PDF '{getattr(f, 'filename', '')}': {e}")

            elif widget["type"] == "button":
                if key in request.form and widget.get("callback"):
                    widget["callback"]()

        action = request.form.get("action")
        if action == "clear_chat":
            session["chat_history"] = []
            # also drop any file‑chunks
            sid = smx.get_session_id()
            smx.clear_user_chunks(sid)
            
        # Update the current session's history with any modifications.
        # 2) Persist session → past_sessions
        if "current_session" in session:
            session["current_session"]["history"] = session.get("chat_history", [])
            past_sessions = session.get("past_sessions", [])
            for s in past_sessions:
                if s["id"] == session["current_session"]["id"]:
                    s["history"] = session["chat_history"]
            session["past_sessions"] = past_sessions
        session.modified = True

        # 3) Now build the combined chat + system_output
        system_output_html = smx.system_output_buffer.strip()
        chat_html = render_chat_history(smx)

        return {"chat_html": chat_html, "system_output_html": system_output_html}
    
    
    @smx.app.route("/load_session", methods=["POST"])
    def load_session():
        # --- Execute "Ending Chat" for the current session ---
        current_history = session.get("chat_history", [])
        current_session = session.get(
            "current_session",
            {"id": str(uuid.uuid4()), "title": "Current", "history": []}
        )
        past_sessions = session.get("past_sessions", [])
        exists = any(s["id"] == current_session["id"] for s in past_sessions)

        if current_history:
            from .core import SyntaxMUI
            if not exists:
                generated_title = SyntaxMUI.generate_contextual_title(current_history)
                current_session["title"] = generated_title
                current_session["history"] = current_history.copy()
                past_sessions.insert(0, current_session)
            else:
                for s in past_sessions:
                    if s["id"] == current_session["id"]:
                        s["history"] = current_history.copy()
                        break
            session["past_sessions"] = past_sessions

        # --- Load the target session (the clicked chat) ---
        sess_id = request.form.get("session_id")
        target = next((s for s in past_sessions if s["id"] == sess_id), None)
        if target:
            session["current_session"] = target
            session["chat_history"]   = target["history"]
            session.modified = True

        # Return both refreshed panes
        chat_html    = render_chat_history(smx)
        sidebar_html = _render_session_sidebar()
        return jsonify({
            "chat_html":    chat_html,
            "sidebar_html": sidebar_html
        })
    
    @smx.app.route("/upload_user_file", methods=["POST"])
    def upload_user_file():
        import uuid
        from flask import jsonify
        # Define the upload folder for user files.
        upload_folder = os.path.join(os.getcwd(), "uploads", "user")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        # Retrieve list of files uploaded.
        uploaded_files = request.files.getlist("user_files")
        if not uploaded_files:
            return jsonify({"error": "No files provided"}), 400
        
        saved_files = []
        for file in uploaded_files:
            if file.filename == "":
                continue  # Skip files with empty filenames.
            # Create a unique filename.
            unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
            filepath = os.path.join(upload_folder, unique_filename)
            try:
                file.save(filepath)
                saved_files.append(unique_filename)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        if not saved_files:
            return jsonify({"error": "No valid files uploaded"}), 400
        
        return jsonify({"message": "Files uploaded successfully", "uploaded_files": saved_files})
