from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt

class TypingIndicator(QFrame):
    """
    A typing indicator widget that shows "Assistant is typing..." with animated dots.
    """
    
    def __init__(self):
        super().__init__()
        self.setProperty("class", "typing-indicator")
        
        # Initialize state
        self.dot_count = 0
        self.max_dots = 3
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Create label
        self.label = QLabel("Assistant is typing")
        self.label.setProperty("class", "typing-text")
        
        # Add label to layout
        layout.addWidget(self.label)
        layout.addStretch()
        
        # Start animation timer
        self.timer.start(500)  # Update every 500ms
        
    def update_dots(self):
        """Update the animated dots."""
        self.dot_count = (self.dot_count + 1) % (self.max_dots + 1)
        dots = "." * self.dot_count
        self.label.setText(f"Assistant is typing{dots}")
        
    def showEvent(self, event):
        """Start the animation when shown."""
        super().showEvent(event)
        self.timer.start(500)
        
    def hideEvent(self, event):
        """Stop the animation when hidden."""
        super().hideEvent(event)
        self.timer.stop()