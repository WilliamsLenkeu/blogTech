@echo off
echo ========================================
echo    Configuration du Blog Django
echo ========================================
echo.

echo Installation des dependances...
pip install -r requirements.txt

echo.
echo Configuration complete du blog...
python setup_blog.py

echo.
echo Demarrage du serveur...
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
python manage.py runserver

pause
