from datetime import datetime
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from src.utils.styles import get_icon_path

class MessageBubble(QFrame):
    """
    A chat message bubble that displays the message content, sender, and timestamp.
    """
    
    def __init__(self, content, role, timestamp):
        super().__init__()
        self.content = content
        self.role = role  # "user" or "assistant"
        self.timestamp = timestamp
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        # Set frame properties based on role
        if self.role == "user":
            self.setProperty("class", "user-message")
        else:
            self.setProperty("class", "assistant-message")
            
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header with role icon and timestamp
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Icon based on role
        icon_path = get_icon_path("user.png" if self.role == "user" else "assistant.png")
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(16, 16)))
        
        # Sender name
        sender_label = QLabel("You" if self.role == "user" else "Assistant")
        sender_label.setProperty("class", "message-sender")
        
        # Timestamp
        time_format = "%H:%M"
        timestamp_label = QLabel(self.timestamp.strftime(time_format))
        timestamp_label.setProperty("class", "message-timestamp")
        
        # Add widgets to header layout
        header_layout.addWidget(icon_label)
        header_layout.addWidget(sender_label)
        header_layout.addStretch()
        header_layout.addWidget(timestamp_label)
        
        # Message content
        content_label = QLabel(self.content)
        content_label.setWordWrap(True)
        content_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | 
            Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        content_label.setProperty("class", "message-content")
        
        # Add widgets to main layout
        layout.addLayout(header_layout)
        layout.addWidget(content_label)