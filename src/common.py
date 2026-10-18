"""Общие пути и выбор компилятора для скриптов сборки."""
import os, shutil, tempfile
SRC = os.path.dirname(os.path.abspath(__file__))   # src/
ROOT = os.path.dirname(SRC)                         # корень платформы (то, что раздаёт server.py)
TMP = os.path.join(tempfile.gettempdir(), 'pvk-gen')
os.makedirs(TMP, exist_ok=True)
CXX = os.environ.get('CXX') or next((c for c in ('clang++', 'g++', 'c++') if shutil.which(c)), 'c++')
