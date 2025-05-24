import os
from pathlib import Path
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QFile, QTextStream

def get_icon_path(icon_name):
    """Get the path to an icon in the assets directory."""
    # For development, create assets directory if it doesn't exist
    assets_dir = Path("src/assets/icons")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    return str(assets_dir / icon_name)

def apply_stylesheet(widget: QWidget):
    """Apply the application stylesheet to a widget."""
    # Create and get the stylesheet path
    stylesheet_dir = Path("src/assets/styles")
    stylesheet_dir.mkdir(parents=True, exist_ok=True)
    stylesheet_path = stylesheet_dir / "app.qss"
    
    # Create stylesheet if it doesn't exist
    if not stylesheet_path.exists():
        with open(stylesheet_path, "w") as f:
            f.write(get_default_stylesheet())
    
    # Read and apply stylesheet
    file = QFile(str(stylesheet_path))
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        widget.setStyleSheet(stream.readAll())
        file.close()

def get_default_stylesheet():
    """Get the default application stylesheet."""
    return """
/* Main Window */
QMainWindow {
    background-color: #F9FAFB;
}

/* Login Window */
.login-title {
    font-size: 24px;
    font-weight: bold;
    color: #2563EB;
}

.login-subtitle {
    font-size: 16px;
    color: #64748B;
}

.login-form-container {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
}

.login-input {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    background-color: #F8FAFC;
    selection-background-color: #BFDBFE;
    min-height: 36px;
}

.login-input:focus {
    border: 1px solid #2563EB;
}

.primary-button {
    background-color: #2563EB;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-height: 40px;
}

.primary-button:hover {
    background-color: #1D4ED8;
}

.primary-button:pressed {
    background-color: #1E40AF;
}

.text-button {
    background-color: transparent;
    color: #2563EB;
    border: none;
    padding: 4px 8px;
    font-weight: bold;
}

.text-button:hover {
    color: #1D4ED8;
    text-decoration: underline;
}

/* Chat Window */
.chat-header {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
}

.chat-title {
    font-size: 18px;
    font-weight: bold;
    color: #1E293B;
}

.icon-button {
    background-color: transparent;
    border: none;
    padding: 4px;
    border-radius: 4px;
}

.icon-button:hover {
    background-color: #F1F5F9;
}

.messages-area {
    background-color: #F9FAFB;
    border: none;
}

.user-message {
    background-color: #EFF6FF;
    border-radius: 12px 12px 2px 12px;
    max-width: 80%;
    align-self: flex-end;
    margin-left: 20%;
}

.assistant-message {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px 12px 12px 2px;
    max-width: 80%;
    align-self: flex-start;
    margin-right: 20%;
}

.message-sender {
    font-weight: bold;
    color: #334155;
    font-size: 13px;
}

.message-timestamp {
    color: #94A3B8;
    font-size: 12px;
}

.message-content {
    color: #1E293B;
}

.input-container {
    background-color: #FFFFFF;
    border-top: 1px solid #E2E8F0;
}

.message-input {
    border: 1px solid #CBD5E1;
    border-radius: 20px;
    padding: 8px 16px;
    background-color: #F8FAFC;
    selection-background-color: #BFDBFE;
    min-height: 40px;
}

.message-input:focus {
    border: 1px solid #2563EB;
}

.send-button {
    background-color: #2563EB;
    color: white;
    border-radius: 20px;
    padding: 8px;
    min-width: 40px;
    min-height: 40px;
}

.send-button:hover {
    background-color: #1D4ED8;
}

.send-button:pressed {
    background-color: #1E40AF;
}

.typing-indicator {
    background-color: #F1F5F9;
    border-radius: 12px;
    max-width: 80%;
    align-self: flex-start;
    margin-right: 20%;
}

.typing-text {
    color: #64748B;
    font-size: 13px;
}

/* Scrollbar styling */
QScrollBar:vertical {
    border: none;
    background-color: #F1F5F9;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* Menu styling */
QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 4px 0px;
}

QMenu::item {
    padding: 6px 16px;
}

QMenu::item:selected {
    background-color: #EFF6FF;
}

QMenu::separator {
    height: 1px;
    background-color: #E2E8F0;
    margin: 4px 0px;
}
"""