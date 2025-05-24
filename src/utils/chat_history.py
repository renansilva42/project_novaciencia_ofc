import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger

class ChatHistory:
    """
    Manages chat history for users, saving to local JSON files.
    In a production app, this would use Supabase for storage.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history_dir = Path("chat_history")
        self.history_file = self.history_dir / f"{user_id}.json"
        
        # Create history directory if it doesn't exist
        self.history_dir.mkdir(exist_ok=True)
        
        # Create history file if it doesn't exist
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps({"messages": []}))
            
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages for the user."""
        try:
            with open(self.history_file, "r") as f:
                data = json.load(f)
                return data.get("messages", [])
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return []
            
    def add_message(self, role: str, content: str, timestamp: str) -> None:
        """Add a message to the user's history."""
        try:
            messages = self.get_messages()
            
            # Add new message
            messages.append({
                "role": role,
                "content": content,
                "timestamp": timestamp
            })
            
            # Save updated messages
            with open(self.history_file, "w") as f:
                json.dump({"messages": messages}, f, indent=2)
                
            logger.info(f"Added message to history for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error adding message to chat history: {str(e)}")
            
    def clear_history(self) -> None:
        """Clear the user's chat history."""
        try:
            with open(self.history_file, "w") as f:
                json.dump({"messages": []}, f)
                
            logger.info(f"Cleared history for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error clearing chat history: {str(e)}")