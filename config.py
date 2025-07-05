import os
from dotenv import load_dotenv

load_dotenv()

# API keys and configuration for the Smart Video Study Assistant

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# Default model priority list
MODEL_PRIORITY = [
    "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "mistralai/Mixtral-8x7B-Instruct-v0.1"
]

# Other configuration options can be added here as needed
