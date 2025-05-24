import os
import uuid
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QScrollArea, 
    QFrame, QSplitter, QSizePolicy, QMenu
)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QAction

from loguru import logger

from src.utils.supabase_client import SupabaseClient
from src.components.message_bubble import MessageBubble
from src.components.typing_indicator import TypingIndicator
from src.utils.styles import apply_stylesheet, get_icon_path
from src.utils.openai_handler import OpenAIHandler
from src.utils.chat_history import ChatHistory

class ChatWorker(QThread):
    """Worker thread for handling chat message processing."""
    message_received = pyqtSignal(str)
    typing_started = pyqtSignal()
    typing_stopped = pyqtSignal()
    
    def __init__(self, openai_handler, user_message, user_id):
        super().__init__()
        self.openai_handler = openai_handler
        self.user_message = user_message
        self.user_id = user_id
        
    def run(self):
        """Process the message and emit the response."""
        try:
            logger.debug(f"ChatWorker started processing message for user_id={self.user_id}: {self.user_message}")
            self.typing_started.emit()
            response = self.openai_handler.process_message(self.user_id, self.user_message)
            self.typing_stopped.emit()
            self.message_received.emit(response)
            logger.debug(f"ChatWorker finished processing message for user_id={self.user_id}")
        except Exception as e:
            self.typing_stopped.emit()
            self.message_received.emit(f"Error: {str(e)}")
            logger.error(f"ChatWorker error for user_id={self.user_id}: {e}")

class ChatWindow(QMainWindow):
    """Main chat window for the application."""
    
    def __init__(self, user):
        super().__init__()
        logger.info(f"Initializing ChatWindow for user: {user.email} (id={user.id})")
        self.user = user
        self.supabase = SupabaseClient()
        self.openai_handler = OpenAIHandler()
        self.chat_history = ChatHistory(self.user.id)
        
        # Window setup
        self.setWindowTitle("AI Assistant")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(get_icon_path("app_icon.png")))
        
        # Apply stylesheet
        apply_stylesheet(self)
        
        # Set up the UI
        self.init_ui()
        
        # Load chat history
        self.load_chat_history()
        
    def init_ui(self):
        """Initialize the user interface components."""
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)
        
        # Header
        header = QFrame()
        header.setProperty("class", "chat-header")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)
        
        # Logo and title
        logo_label = QLabel()
        logo_pixmap = QIcon(get_icon_path("chat_logo.png")).pixmap(QSize(32, 32))
        logo_label.setPixmap(logo_pixmap)
        
        title_label = QLabel("AI Assistant")
        title_label.setProperty("class", "chat-title")
        
        # User info and settings
        user_button = QPushButton()
        user_button.setIcon(QIcon(get_icon_path("user.png")))
        user_button.setIconSize(QSize(24, 24))
        user_button.setProperty("class", "icon-button")
        user_button.setToolTip(f"Signed in as {self.user.email}")
        user_button.clicked.connect(self.show_user_menu)
        
        # Add widgets to header layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(user_button)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        
        # Chat container
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        # Chat messages area
        self.messages_scroll_area = QScrollArea()
        self.messages_scroll_area.setWidgetResizable(True)
        self.messages_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.messages_scroll_area.setProperty("class", "messages-area")
        
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(16, 16, 16, 16)
        self.messages_layout.setSpacing(16)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.messages_scroll_area.setWidget(self.messages_container)
        
        # Welcome message
        welcome_message = MessageBubble(
            "Welcome to AI Assistant! How can I help you today?",
            "assistant",
            datetime.now()
        )
        self.messages_layout.addWidget(welcome_message)
        
        # Add typing indicator (hidden initially)
        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        self.messages_layout.addWidget(self.typing_indicator)
        
        # Add stretch to push messages to the top
        self.messages_layout.addStretch()
        
        # Message input area
        input_container = QFrame()
        input_container.setProperty("class", "input-container")
        input_container.setFixedHeight(80)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(16, 16, 16, 16)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setProperty("class", "message-input")
        self.message_input.returnPressed.connect(self.send_message)
        
        send_button = QPushButton()
        send_button.setIcon(QIcon(get_icon_path("send.png")))
        send_button.setIconSize(QSize(24, 24))
        send_button.setProperty("class", "send-button")
        send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(send_button)
        
        # Add components to chat layout
        chat_layout.addWidget(self.messages_scroll_area)
        chat_layout.addWidget(input_container)
        
        # Add chat container to splitter
        splitter.addWidget(chat_container)
        
        # Add header and splitter to main layout
        main_layout.addWidget(header)
        main_layout.addWidget(splitter)
        
    def load_chat_history(self):
        """Load chat history from the database."""
        messages = self.chat_history.get_messages()
        logger.info(f"Loaded {len(messages)} messages from chat history for user_id={self.user.id}")
        
        # Clear existing messages except welcome message
        for i in reversed(range(self.messages_layout.count() - 2)):  # -2 to keep typing indicator and stretch
            widget = self.messages_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Add messages from history
        for message in messages:
            message_bubble = MessageBubble(
                message['content'],
                message['role'],
                datetime.fromisoformat(message['timestamp'])
            )
            # Insert before the typing indicator and stretch
            self.messages_layout.insertWidget(self.messages_layout.count() - 2, message_bubble)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def send_message(self):
        """Send a user message and process the response."""
        message_text = self.message_input.text().strip()
        if not message_text:
            return
            
        logger.info(f"User {self.user.id} sent message: {message_text}")
        
        # Clear input field
        self.message_input.clear()
        
        # Add user message to UI
        timestamp = datetime.now()
        user_bubble = MessageBubble(message_text, "user", timestamp)
        self.messages_layout.insertWidget(self.messages_layout.count() - 2, user_bubble)
        
        # Save message to history
        self.chat_history.add_message("user", message_text, timestamp.isoformat())
        
        # Scroll to bottom
        self.scroll_to_bottom()
        
        # Process message in background thread
        self.chat_worker = ChatWorker(self.openai_handler, message_text, self.user.id)
        self.chat_worker.typing_started.connect(self.show_typing_indicator)
        self.chat_worker.typing_stopped.connect(self.hide_typing_indicator)
        self.chat_worker.message_received.connect(self.handle_response)
        self.chat_worker.start()
        
    def handle_response(self, response):
        """Handle the response from the AI."""
        logger.info(f"Received response for user {self.user.id}: {response}")
        
        # Add assistant message to UI
        timestamp = datetime.now()
        assistant_bubble = MessageBubble(response, "assistant", timestamp)
        self.messages_layout.insertWidget(self.messages_layout.count() - 2, assistant_bubble)
        
        # Save message to history
        self.chat_history.add_message("assistant", response, timestamp.isoformat())
        
        # Scroll to bottom
        self.scroll_to_bottom()
        
    def show_typing_indicator(self):
        """Show the typing indicator."""
        self.typing_indicator.show()
        self.scroll_to_bottom()
        
    def hide_typing_indicator(self):
        """Hide the typing indicator."""
        self.typing_indicator.hide()
        
    def scroll_to_bottom(self):
        """Scroll the messages area to the bottom."""
        self.messages_scroll_area.verticalScrollBar().setValue(
            self.messages_scroll_area.verticalScrollBar().maximum()
        )
        
    def show_user_menu(self):
        """Show the user menu."""
        menu = QMenu(self)
        
        # Add user email display (non-clickable)
        user_label = QAction(f"Signed in as {self.user.email}", self)
        user_label.setEnabled(False)
        menu.addAction(user_label)
        
        menu.addSeparator()
        
        # Add sign out action
        sign_out_action = QAction("Sign Out", self)
        sign_out_action.triggered.connect(self.sign_out)
        menu.addAction(sign_out_action)
        
        # Show the menu
        button = self.sender()
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
        
    def sign_out(self):
        """Sign out the user and return to login screen."""
        logger.info(f"User {self.user.id} signing out")
        self.supabase.sign_out()
        
        # Import here to avoid circular imports
        from src.windows.login_window import LoginWindow
        
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
