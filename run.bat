@echo off

set chroma_db_path="C:\Users\isaac\dev\ANOTHER-LM\data\chromadb"

cd /d "C:\Users\isaac\dev\ANOTHER-LM\src"
call "C:\Users\isaac\dev\ANOTHER-LM\venv\Scripts\activate.bat"
powershell -Command "chroma run --path %chroma_db_path%"