import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap

from src.utils.supabase_client import SupabaseClient
from src.windows.chat_window import ChatWindow
from src.utils.styles import apply_stylesheet, get_icon_path

class LoginWindow(QMainWindow):
    """Login window for user authentication with Supabase."""
    
    def __init__(self):
        super().__init__()
        self.supabase = SupabaseClient()
        
        # Window setup
        self.setWindowTitle("AI Assistant - Login")
        self.setMinimumSize(400, 500)
        self.setWindowIcon(QIcon(get_icon_path("app_icon.png")))
        
        # Apply stylesheet
        apply_stylesheet(self)
        
        # Set up the UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface components."""
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_widget.setLayout(main_layout)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap(get_icon_path("chat_logo.png"))
        logo_label.setPixmap(logo_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_layout.addWidget(logo_label)
        
        main_layout.addLayout(logo_layout)
        
        # Title
        title_label = QLabel("AI Assistant")
        title_label.setProperty("class", "login-title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Sign in to continue")
        subtitle_label.setProperty("class", "login-subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Add some spacing
        main_layout.addSpacing(20)
        
        # Form container
        form_container = QFrame()
        form_container.setProperty("class", "login-form-container")
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(16)
        
        # Email field
        email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setProperty("class", "login-input")
        
        # Password field
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setProperty("class", "login-input")
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setProperty("class", "primary-button")
        self.login_button.clicked.connect(self.handle_login)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        register_label = QLabel("Don't have an account?")
        self.register_button = QPushButton("Sign Up")
        self.register_button.setProperty("class", "text-button")
        self.register_button.clicked.connect(self.show_register_view)
        
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        
        # Add widgets to form layout
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addLayout(register_layout)
        
        # Add form container to main layout
        main_layout.addWidget(form_container)
        
        # Set up "register" view widgets but hide them initially
        self.setup_register_view()
        self.toggle_view(is_login=True)
        
    def setup_register_view(self):
        """Set up the registration view components."""
        # Form container for registration
        self.register_container = QFrame()
        self.register_container.setProperty("class", "login-form-container")
        register_layout = QVBoxLayout(self.register_container)
        register_layout.setContentsMargins(20, 20, 20, 20)
        register_layout.setSpacing(16)
        
        # Email field
        reg_email_label = QLabel("Email")
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Enter your email")
        self.reg_email_input.setProperty("class", "login-input")
        
        # Password field
        reg_password_label = QLabel("Password")
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Create a password")
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password_input.setProperty("class", "login-input")
        
        # Confirm password field
        confirm_password_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setProperty("class", "login-input")
        
        # Register button
        self.register_submit_button = QPushButton("Sign Up")
        self.register_submit_button.setProperty("class", "primary-button")
        self.register_submit_button.clicked.connect(self.handle_register)
        
        # Back to login link
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        back_label = QLabel("Already have an account?")
        self.back_button = QPushButton("Sign In")
        self.back_button.setProperty("class", "text-button")
        self.back_button.clicked.connect(self.show_login_view)
        
        back_layout.addWidget(back_label)
        back_layout.addWidget(self.back_button)
        
        # Add widgets to registration layout
        register_layout.addWidget(reg_email_label)
        register_layout.addWidget(self.reg_email_input)
        register_layout.addWidget(reg_password_label)
        register_layout.addWidget(self.reg_password_input)
        register_layout.addWidget(confirm_password_label)
        register_layout.addWidget(self.confirm_password_input)
        register_layout.addWidget(self.register_submit_button)
        register_layout.addLayout(back_layout)
        
        # Add register container to central widget but hide it initially
        self.centralWidget().layout().addWidget(self.register_container)
        self.register_container.hide()
        
    def toggle_view(self, is_login=True):
        """Toggle between login and registration views."""
        form_container = self.findChild(QFrame, "")  # Get the first QFrame (login form)
        
        if is_login:
            form_container.show()
            self.register_container.hide()
            self.setWindowTitle("AI Assistant - Login")
        else:
            form_container.hide()
            self.register_container.show()
            self.setWindowTitle("AI Assistant - Register")
            
    def show_login_view(self):
        """Show the login view."""
        self.toggle_view(is_login=True)
        
    def show_register_view(self):
        """Show the registration view."""
        self.toggle_view(is_login=False)
        
    def handle_login(self):
        """Handle the login process with Supabase."""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
            return
            
        # Attempt to login with Supabase
        try:
            user = self.supabase.sign_in(email, password)
            if user:
                self.open_chat_window(user)
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        except Exception as e:
            QMessageBox.critical(self, "Login Error", f"An error occurred: {str(e)}")
            
    def handle_register(self):
        """Handle the registration process with Supabase."""
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not email or not password or not confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Please fill out all fields.")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match.")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Registration Failed", "Password must be at least 6 characters.")
            return
            
        # Attempt to register with Supabase
        try:
            user = self.supabase.sign_up(email, password)
            if user:
                QMessageBox.information(self, "Registration Successful", 
                                       "Your account has been created successfully. You can now log in.")
                self.show_login_view()
                self.email_input.setText(email)
                self.password_input.clear()
            else:
                QMessageBox.warning(self, "Registration Failed", "Could not create account.")
        except Exception as e:
            QMessageBox.critical(self, "Registration Error", f"An error occurred: {str(e)}")
            
    def open_chat_window(self, user):
        """Open the chat window and close the login window."""
        self.chat_window = ChatWindow(user)
        self.chat_window.show()
        self.close()