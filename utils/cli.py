import sys
import time
from itertools import cycle
from datetime import datetime
from typing import Optional
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Spinner:
    def __init__(self):
        self.spinner = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.start_time = None
        
    def spin(self, message: str):
        sys.stdout.write(f"\r{next(self.spinner)} {message}")
        sys.stdout.flush()

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.WARNING}! {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.FAIL}✕ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def create_loading_bar(current: int, total: int, width: int = 40) -> str:
    filled = int(width * current / total)
    bar = '█' * filled + '▒' * (width - filled)
    percent = int(100 * current / total)
    return f"[{bar}] {percent}%"

def log_to_file(message: str, log_file: Optional[str] = "processing.log"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
