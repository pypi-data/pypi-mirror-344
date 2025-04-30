from .core import SyntaxMUI

_app_instance = SyntaxMUI()

_app_instance.enable_theme_toggle()

run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
file_uploader = _app_instance.file_uploader
set_ui_mode = _app_instance.set_ui_mode
set_theme = _app_instance.set_theme
enable_theme_toggle = _app_instance.enable_theme_toggle
disable_theme_toggle = _app_instance.disable_theme_toggle
get_text_input_value = _app_instance.get_text_input_value
clear_text_input_value = _app_instance.clear_text_input_value
get_file_upload_value = _app_instance.get_file_upload_value
get_chat_history = _app_instance.get_chat_history
set_chat_history = _app_instance.set_chat_history
clear_chat_history = _app_instance.clear_chat_history
write = _app_instance.write
markdown = _app_instance.markdown
latex = _app_instance.latex
error = _app_instance.error
success = _app_instance.success
info = _app_instance.info
warning = _app_instance.warning
plt_plot = _app_instance.plt_plot
plotly_plot = _app_instance.plotly_plot

set_user_icon = _app_instance.set_user_icon
set_bot_icon = _app_instance.set_bot_icon
set_site_icon = _app_instance.set_site_icon
set_project_title = _app_instance.set_project_title
set_site_title = _app_instance.set_site_title
set_site_logo = _app_instance.set_site_logo
list_ui_modes = _app_instance.list_ui_modes
load_pdf_chunks = _app_instance.load_pdf_chunks
# delete_pdf_chunks = _app_instance.delete_pdf_chunks

get_session_id = _app_instance.get_session_id
add_user_chunks = _app_instance.add_user_chunks
get_user_chunks = _app_instance.get_user_chunks
clear_user_chunks = _app_instance.clear_user_chunks


# Expose the plotting submodule.
from . import plottings

