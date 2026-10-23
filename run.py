"""
Point d'entrée principal pour démarrer le serveur de développement local.

Usage :
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Démarre le serveur local de développement Flask
    app.run(debug=True, host="127.0.0.1", port=5000)
