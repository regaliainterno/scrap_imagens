import sys
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Adiciona o diretório 'src' ao PATH para que as importações funcionem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import QApplication, MainWindow

if __name__ == "__main__":
    # Verifica se a chave da API Gemini está configurada
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("⚠️  AVISO: Variável GEMINI_API_KEY não configurada!")
        print("   Por favor, crie um arquivo .env na raiz do projeto com sua chave API.")
        print("   Exemplo: copie .env.example para .env e adicione sua chave.")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
