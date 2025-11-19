import sqlite_utils
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="anunnakis_data.db", base_dir=None):
        # Se base_dir não for fornecido, usa a pasta 'db' local
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), "db")
        
        # Cria o caminho completo para o banco de dados
        self.db_file = os.path.join(base_dir, db_path)
        self.base_dir = base_dir  # Armazenar base_dir para criar novas instâncias
        os.makedirs(base_dir, exist_ok=True)
        self.db = sqlite_utils.Database(self.db_file)
        self._setup_database()

    def _setup_database(self):
        # Tabela para armazenar os roteiros
        self.db["roteiros"].create({
            "id": int,
            "title": str,
            "content": str,
            "created_at": str
        }, pk="id", if_not_exists=True)

        # Tabela para armazenar os hashes das imagens baixadas
        self.db["image_hashes"].create({
            "hash": str,
            "term": str,
            "downloaded_at": str
        }, pk="hash", if_not_exists=True)

    # --- Métodos para Roteiros ---

    def save_roteiro(self, title, content):
        """Salva um novo roteiro no banco de dados."""
        self.db["roteiros"].insert({
            "title": title,
            "content": content,
            "created_at": datetime.now().isoformat()
        })

    def get_all_roteiros(self):
        """Retorna todos os roteiros salvos."""
        return list(self.db["roteiros"].rows)

    # --- Métodos para Hashes de Imagens ---

    def is_hash_downloaded(self, image_hash):
        """Verifica se um hash de imagem já foi baixado."""
        try:
            return self.db["image_hashes"].get(image_hash) is not None
        except Exception as e:
            # sqlite-utils raises a NotFoundError when a primary key is not present.
            # Handle that case as 'not downloaded' instead of letting the exception propagate.
            if e.__class__.__name__ == 'NotFoundError':
                return False
            raise

    def add_downloaded_hash(self, image_hash, term):
        """Adiciona um novo hash de imagem baixada ao banco de dados."""
        self.db["image_hashes"].insert({
            "hash": image_hash,
            "term": term,
            "downloaded_at": datetime.now().isoformat()
        }, pk="hash", replace=True)

if __name__ == '__main__':
    # Exemplo de uso
    db_manager = DatabaseManager()
    print("Banco de dados configurado.")

    # Teste de roteiro
    db_manager.save_roteiro("Teste de Roteiro", "Este é o conteúdo do roteiro de teste.")
    roteiros = db_manager.get_all_roteiros()
    print(f"Roteiros salvos: {len(roteiros)}")

    # Teste de hash
    test_hash = "a1b2c3d4e5f6"
    db_manager.add_downloaded_hash(test_hash, "Anunnaki")
    print(f"Hash {test_hash} já baixado? {db_manager.is_hash_downloaded(test_hash)}")
    print(f"Hash 'naoexiste' já baixado? {db_manager.is_hash_downloaded('naoexiste')}")
