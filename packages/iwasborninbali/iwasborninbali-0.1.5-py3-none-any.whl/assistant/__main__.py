import sys
import os

# Добавляем корень проекта в sys.path, чтобы можно было найти модуль assistant
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from assistant.cli import main

if __name__ == "__main__":
    main()
