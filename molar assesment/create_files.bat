@echo off

rem Create directories
mkdir backend
mkdir app

rem Create files
type nul > backend\schema.sql
type nul > backend\load_data.py
type nul > backend\simple_nl2sql.py
type nul > backend\db.py
type nul > backend\server.py

type nul > app\streamlit_app.py

type nul > README.md

echo All files created successfully!
pause
