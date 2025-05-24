# AI Assistant with Supabase Authentication

A sophisticated Python desktop chatbot application with Supabase authentication that connects to OpenAI's API. This application provides a modern, elegant user interface using PyQt6 and integrates with the OpenAI Agents system.

## Features

- **Secure Authentication**: Email and password authentication through Supabase
- **Elegant Chat Interface**: Modern UI with message bubbles, typing indicators, and timestamps
- **OpenAI Integration**: Connects to OpenAI's API for intelligent responses
- **Session Management**: Maintains conversation context between messages
- **Chat History**: Preserves chat history for returning users
- **Multi-specialist System**: Routes questions to appropriate specialists (hospital equipment experts)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Supabase account
- OpenAI API key

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`:
   ```
   # Supabase configuration
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   
   # OpenAI API configuration
   OPENAI_API_KEY=your_openai_api_key
   ```
5. Create the assets directories:
   ```
   mkdir -p src/assets/icons src/assets/fonts src/assets/styles
   ```
6. Download the required fonts and icons (or replace with your own):
   - Download Inter font family to `src/assets/fonts/`
   - Add icons to `src/assets/icons/`:
     - app_icon.png
     - chat_logo.png
     - user.png
     - assistant.png
     - send.png

### Running the Application

```
python main.py
```

## Project Structure

```
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── src/
│   ├── assets/                # Application assets
│   │   ├── fonts/             # Fonts
│   │   ├── icons/             # Icons
│   │   └── styles/            # QSS stylesheets
│   ├── components/            # Reusable UI components
│   │   ├── message_bubble.py  # Chat message component
│   │   └── typing_indicator.py# Typing animation component
│   ├── utils/                 # Utility modules
│   │   ├── chat_history.py    # Message history management
│   │   ├── logger.py          # Application logging
│   │   ├── openai_handler.py  # OpenAI API integration
│   │   ├── styles.py          # Stylesheet utilities
│   │   └── supabase_client.py # Supabase authentication
│   └── windows/               # Application windows
│       ├── chat_window.py     # Main chat interface
│       └── login_window.py    # Login and registration UI
└── chat_history/              # Local storage for chat history
```

## Customization

- **Styling**: Modify the stylesheet in `src/assets/styles/app.qss` or through the `get_default_stylesheet()` function in `src/utils/styles.py`
- **Behavior**: Adjust the OpenAI integration in `src/utils/openai_handler.py`
- **UI Components**: Customize components in the `src/components/` directory

## License

MIT