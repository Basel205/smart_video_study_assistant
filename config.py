import os
from dotenv import load_dotenv

load_dotenv()

# API keys and configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "") # <-- ADD THIS

# Default model priority list (Old, for Together AI)
MODEL_PRIORITY = [
    "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "mistralai/Mixtral-8x7B-Instruct-v0.1"
]

# New Gemini Model
# You can change this to other models like "gemini-pro"
GEMINI_MODEL = "gemini-1.5-flash" # <-- ADD THIS

# Other configuration options can be added here as needed
