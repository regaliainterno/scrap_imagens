import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QTabWidget, QLineEdit, QPushButton,
                               QTextEdit, QLabel, QComboBox, QFileDialog,
                               QProgressBar, QListWidget, QListWidgetItem,
                               QMessageBox, QSplitter, QSpinBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

from .db_manager import DatabaseManager
from .gemini_generator import GeminiGenerator
from .image_scraper import ImageScraper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anunnakis - Roteiros e Imagens")
        self.setGeometry(100, 100, 1400, 800)

        # Caminho customizado para o banco de dados
        db_dir = r"G:\Meu Drive\SQL\roteiros"
        
        # Inicializar o banco de dados
        self.db_manager = DatabaseManager(base_dir=db_dir)

        # Configurar a paleta de cores para um tema escuro moderno
        self.set_dark_theme()

        # Inicializar os geradores e scrapers
        self.gemini_generator = GeminiGenerator()
        self.image_scraper = ImageScraper(self.db_manager)
        self.current_roteiro_raw = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Criar as abas
        self.create_roteiro_tab()
        self.create_roteiros_library_tab()
        self.create_scraper_tab()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 245, 245))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.Button, QColor(245, 245, 245))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.BrightText, QColor(25, 118, 210))
        palette.setColor(QPalette.Link, QColor(25, 118, 210))
        palette.setColor(QPalette.Highlight, QColor(25, 118, 210))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)

        style = """
        QTabWidget::pane {
            border-top: 2px solid #1976D2;
        }
        QTabBar::tab {
            background: #F0F0F0;
            border: 2px solid #E0E0E0;
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            color: #1E1E1E;
        }
        QTabBar::tab:selected {
            background: #1976D2;
            color: white;
            font-weight: bold;
        }
        QPushButton {
            background-color: #1976D2;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1565C0;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QLineEdit {
            background-color: #FFFFFF;
            color: #1E1E1E;
            border: 2px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px;
        }
        QLineEdit:focus {
            border: 2px solid #1976D2;
        }
        QTextEdit {
            background-color: #FFFFFF;
            color: #1E1E1E;
            border: 2px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px;
        }
        QTextEdit:focus {
            border: 2px solid #1976D2;
        }
        QListWidget {
            background-color: #FFFFFF;
            color: #1E1E1E;
            border: 2px solid #BDBDBD;
            border-radius: 4px;
        }
        QListWidget::item:selected {
            background-color: #1976D2;
            color: white;
        }
        QComboBox {
            background-color: #FFFFFF;
            color: #1E1E1E;
            border: 2px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px;
        }
        QComboBox:focus {
            border: 2px solid #1976D2;
        }
        QSpinBox {
            background-color: #FFFFFF;
            color: #1E1E1E;
            border: 2px solid #BDBDBD;
            border-radius: 4px;
            padding: 5px;
        }
        QSpinBox:focus {
            border: 2px solid #1976D2;
        }
        QProgressBar {
            border: 2px solid #BDBDBD;
            border-radius: 4px;
            text-align: center;
            background-color: #F5F5F5;
            color: #1E1E1E;
        }
        QProgressBar::chunk {
            background-color: #1976D2;
        }
        QLabel {
            color: #1E1E1E;
        }
        """
        self.setStyleSheet(style)

    def create_roteiro_tab(self):
        """Aba para gerar novos roteiros"""
        roteiro_tab = QWidget()
        self.tabs.addTab(roteiro_tab, "📝 Gerador de Roteiros")

        layout = QVBoxLayout(roteiro_tab)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # ===== Seção de Entrada =====
        entrada_label = QLabel("DESCRIÇÃO DO ROTEIRO")
        entrada_label.setFont(QFont("Arial", 10, QFont.Bold))
        entrada_label.setStyleSheet("color: #46A1C3;")
        layout.addWidget(entrada_label)

        self.roteiro_prompt = QLineEdit()
        self.roteiro_prompt.setPlaceholderText(
            "Digite um prompt customizado ou deixe vazio para uma sugestão automática"
        )
        self.roteiro_prompt.setMinimumHeight(40)
        layout.addWidget(self.roteiro_prompt)

        # Botões de controle
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("🚀 Gerar Roteiro")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.generate_roteiro)
        button_layout.addWidget(self.generate_button)

        self.random_prompt_button = QPushButton("🎲 Sugestão Aleatória")
        self.random_prompt_button.setMinimumHeight(40)
        self.random_prompt_button.clicked.connect(self.generate_random_prompt)
        button_layout.addWidget(self.random_prompt_button)

        layout.addLayout(button_layout)

        # ===== Seção de Status =====
        self.status_label_roteiro = QLabel("✅ Pronto para gerar roteiros")
        self.status_label_roteiro.setFont(QFont("Arial", 9))
        self.status_label_roteiro.setStyleSheet("color: #46A1C3;")
        layout.addWidget(self.status_label_roteiro)

        layout.addSpacing(15)

        # ===== Seção de Visualização =====
        view_label = QLabel("VISUALIZAÇÃO")
        view_label.setFont(QFont("Arial", 10, QFont.Bold))
        view_label.setStyleSheet("color: #46A1C3;")
        layout.addWidget(view_label)

        view_controls = QHBoxLayout()
        view_controls.addWidget(QLabel("Modo:"))
        self.view_mode_combo = QComboBox()
        self.view_mode_combo.addItems([
            "Padrão (com marcações)",
            "Limpo (apenas parágrafos)",
            "Com Tempos (para leitura)"
        ])
        self.view_mode_combo.currentIndexChanged.connect(self.update_roteiro_view)
        view_controls.addWidget(self.view_mode_combo)
        view_controls.addStretch()

        layout.addLayout(view_controls)

        self.roteiro_text_edit = QTextEdit()
        self.roteiro_text_edit.setFont(QFont("Courier New", 10))
        self.roteiro_text_edit.setMinimumHeight(300)
        layout.addWidget(self.roteiro_text_edit)

        # Botões de ações
        action_buttons = QHBoxLayout()
        self.save_roteiro_button = QPushButton("💾 Salvar Como Arquivo")
        self.save_roteiro_button.clicked.connect(self.save_roteiro_to_file)
        action_buttons.addWidget(self.save_roteiro_button)
        action_buttons.addStretch()

        layout.addLayout(action_buttons)


    def create_roteiros_library_tab(self):
        """Aba para gerenciar roteiros salvos"""
        library_tab = QWidget()
        self.tabs.addTab(library_tab, "📚 Biblioteca de Roteiros")

        layout = QHBoxLayout(library_tab)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # ===== Lista de roteiros (lado esquerdo) =====
        list_layout = QVBoxLayout()
        list_title = QLabel("SEUS ROTEIROS")
        list_title.setFont(QFont("Arial", 10, QFont.Bold))
        list_title.setStyleSheet("color: #46A1C3;")
        list_layout.addWidget(list_title)

        self.roteiros_list = QListWidget()
        self.roteiros_list.itemClicked.connect(self.on_roteiro_selected)
        list_layout.addWidget(self.roteiros_list)

        # Botões de gerencimento
        list_buttons = QHBoxLayout()
        self.refresh_list_button = QPushButton("🔄 Atualizar")
        self.refresh_list_button.clicked.connect(self.load_roteiros_list)
        list_buttons.addWidget(self.refresh_list_button)

        self.delete_roteiro_button = QPushButton("🗑️ Deletar")
        self.delete_roteiro_button.clicked.connect(self.delete_selected_roteiro)
        list_buttons.addWidget(self.delete_roteiro_button)

        list_layout.addLayout(list_buttons)
        layout.addLayout(list_layout)

        # ===== Visualização do roteiro selecionado (lado direito) =====
        view_layout = QVBoxLayout()
        view_title = QLabel("ROTEIRO SELECIONADO")
        view_title.setFont(QFont("Arial", 10, QFont.Bold))
        view_title.setStyleSheet("color: #46A1C3;")
        view_layout.addWidget(view_title)

        self.library_roteiro_text = QTextEdit()
        self.library_roteiro_text.setFont(QFont("Courier New", 10))
        self.library_roteiro_text.setReadOnly(True)
        view_layout.addWidget(self.library_roteiro_text)

        export_button = QPushButton("💾 Exportar para Arquivo")
        export_button.clicked.connect(self.export_roteiro_from_library)
        view_layout.addWidget(export_button)

        layout.addLayout(view_layout)

        # Carregar roteiros ao abrir a aba
        self.load_roteiros_list()

    def create_scraper_tab(self):
        """Aba para download de imagens"""
        scraper_tab = QWidget()
        self.tabs.addTab(scraper_tab, "🖼️ Web Scraper de Imagens")

        layout = QVBoxLayout(scraper_tab)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # ===== Seção de Pesquisa =====
        search_title = QLabel("PESQUISA")
        search_title.setFont(QFont("Arial", 10, QFont.Bold))
        search_title.setStyleSheet("color: #46A1C3;")
        layout.addWidget(search_title)

        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(QLabel("Termo de pesquisa:"))
        self.search_term_input = QLineEdit()
        self.search_term_input.setPlaceholderText("Ex: Nibiru, Anunnaki King, Deuses Sumérios")
        search_input_layout.addWidget(self.search_term_input)
        layout.addLayout(search_input_layout)

        # Configurações
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Máx. Imagens:"))
        self.max_images_input = QSpinBox()
        self.max_images_input.setValue(10)
        self.max_images_input.setMinimum(1)
        self.max_images_input.setMaximum(100)
        config_layout.addWidget(self.max_images_input)

        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Resolução:"))
        self.high_res_checkbox = QComboBox()
        self.high_res_checkbox.addItems(["Alta", "Qualquer"])
        config_layout.addWidget(self.high_res_checkbox)
        config_layout.addStretch()
        layout.addLayout(config_layout)

        # Pasta de salvamento
        folder_layout = QHBoxLayout()
        self.image_dir_label = QLabel(f"Pasta: {self.image_scraper.image_dir[:60]}...")
        self.image_dir_label.setStyleSheet("color: #46A1C3;")
        folder_layout.addWidget(self.image_dir_label)

        select_dir_btn = QPushButton("📁 Escolher Pasta")
        select_dir_btn.clicked.connect(self.choose_image_dir)
        folder_layout.addWidget(select_dir_btn)
        layout.addLayout(folder_layout)

        layout.addSpacing(10)

        # ===== Botão de ação =====
        self.scrape_button = QPushButton("🚀 Buscar e Baixar Imagens")
        self.scrape_button.setMinimumHeight(50)
        self.scrape_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.scrape_button.clicked.connect(self.start_image_scraping)
        layout.addWidget(self.scrape_button)

        layout.addSpacing(10)

        # ===== Seção de Progresso =====
        progress_title = QLabel("PROGRESSO")
        progress_title.setFont(QFont("Arial", 10, QFont.Bold))
        progress_title.setStyleSheet("color: #46A1C3;")
        layout.addWidget(progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.scraper_log = QTextEdit()
        self.scraper_log.setReadOnly(True)
        self.scraper_log.setFont(QFont("Monospace", 9))
        self.scraper_log.setMaximumHeight(200)
        layout.addWidget(self.scraper_log)

        self.status_label_scraper = QLabel("✅ Pronto para fazer busca")
        self.status_label_scraper.setFont(QFont("Arial", 9))
        self.status_label_scraper.setStyleSheet("color: #46A1C3;")
        layout.addWidget(self.status_label_scraper)

    # --- Métodos de Roteiro ---

    def generate_random_prompt(self):
        """Gera um prompt aleatório e inicia a geração"""
        import random
        prompts = [
            "Gere um roteiro detalhado sobre a mitologia Anunnaki e sua presença na história humana",
            "Crie um roteiro educativo explicando quem são os Anunnaki de acordo com textos sumérios",
            "Desenvolva um roteiro explorando a teoria de que os Anunnaki visitaram a Terra",
            "Elabore um roteiro sobre os textos históricos e como descrevem os Anunnaki",
            "Gere um roteiro cobrindo as teorias sobre os Anunnaki e antigas civilizações",
            "Crie um roteiro comparando mitologias Anunnaki com outras civilizações",
            "Desenvolva um roteiro sobre símbolos Anunnaki encontrados em artefatos antigos",
            "Gere um roteiro explicando a genealogia dos Anunnaki",
            "Elabore um roteiro sobre tecnologia antiga e os Anunnaki",
            "Crie um roteiro explorando o papel dos Anunnaki em diferentes religiões"
        ]
        prompt = random.choice(prompts)
        self.roteiro_prompt.setText(prompt)
        self.generate_roteiro()

    def generate_roteiro(self):
        """Gera um novo roteiro"""
        prompt = self.roteiro_prompt.text().strip()
        
        if not prompt:
            import random
            prompts = [
                "Gere um roteiro detalhado sobre a mitologia Anunnaki",
                "Crie um roteiro sobre os Anunnaki em textos sumérios",
                "Desenvolva um roteiro sobre a teoria dos Anunnaki visitando a Terra"
            ]
            prompt = random.choice(prompts)
            self.roteiro_prompt.setText(prompt)

        self.status_label_roteiro.setText("⏳ Gerando roteiro com Gemini... Aguarde.")
        self.generate_button.setEnabled(False)
        self.random_prompt_button.setEnabled(False)

        self.roteiro_thread = RoteiroThread(self.gemini_generator, prompt)
        self.roteiro_thread.generation_finished.connect(self.handle_roteiro_result)
        self.roteiro_thread.start()

    def handle_roteiro_result(self, result):
        """Processa resultado da geração"""
        self.generate_button.setEnabled(True)
        self.random_prompt_button.setEnabled(True)
        
        if isinstance(result, str):
            self.current_roteiro_raw = result
            
            # Salvar automaticamente no banco de dados
            try:
                title = self.roteiro_prompt.text().strip() or f"Roteiro {datetime.now().strftime('%d/%m %H:%M')}"
                self.db_manager.save_roteiro(title, result)
                self.status_label_roteiro.setText(f"✅ Roteiro salvo automaticamente: {title}")
            except Exception as e:
                self.status_label_roteiro.setText(f"⚠️ Roteiro gerado mas erro ao salvar: {e}")
            
            self.update_roteiro_view()
        else:
            self.status_label_roteiro.setText(f"❌ Erro na geração: {result}")
            self.roteiro_text_edit.setText(f"ERRO: {result}")

    def update_roteiro_view(self):
        """Atualiza visualização do roteiro"""
        if not self.current_roteiro_raw:
            return

        mode = self.view_mode_combo.currentText()
        formatted_text = self.gemini_generator.format_roteiro(self.current_roteiro_raw, mode)
        self.roteiro_text_edit.setText(formatted_text)

    def save_roteiro_to_file(self):
        """Salva o roteiro atual como arquivo"""
        if not self.current_roteiro_raw:
            QMessageBox.warning(self, "Aviso", "Nenhum roteiro para salvar")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Roteiro", "", "Arquivo de Texto (*.txt);;Todos (*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_roteiro_raw)
                self.status_label_roteiro.setText(f"✅ Arquivo salvo em: {file_path}")
            except Exception as e:
                self.status_label_roteiro.setText(f"❌ Erro ao salvar: {e}")

    def load_roteiros_list(self):
        """Carrega lista de roteiros do banco de dados"""
        self.roteiros_list.clear()
        try:
            roteiros = self.db_manager.get_all_roteiros()
            for roteiro in roteiros:
                item = QListWidgetItem(f"📄 {roteiro['title']}")
                item.setData(Qt.UserRole, roteiro['id'])
                self.roteiros_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar roteiros: {e}")

    def on_roteiro_selected(self, item):
        """Quando um roteiro é selecionado na lista"""
        try:
            roteiro_id = item.data(Qt.UserRole)
            roteiros = self.db_manager.get_all_roteiros()
            roteiro = next((r for r in roteiros if r['id'] == roteiro_id), None)
            
            if roteiro:
                self.library_roteiro_text.setText(roteiro['content'])
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar roteiro: {e}")

    def delete_selected_roteiro(self):
        """Deleta o roteiro selecionado"""
        current_item = self.roteiros_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione um roteiro para deletar")
            return

        reply = QMessageBox.question(
            self, "Confirmação", "Deseja realmente deletar este roteiro?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                roteiro_id = current_item.data(Qt.UserRole)
                # Aqui você precisaria implementar um método delete no db_manager
                self.roteiros_list.takeItem(self.roteiros_list.row(current_item))
                self.library_roteiro_text.clear()
                QMessageBox.information(self, "Sucesso", "Roteiro deletado")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao deletar: {e}")

    def export_roteiro_from_library(self):
        """Exporta roteiro selecionado na biblioteca"""
        if not self.library_roteiro_text.toPlainText():
            QMessageBox.warning(self, "Aviso", "Nenhum roteiro selecionado")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Roteiro", "", "Arquivo de Texto (*.txt);;Todos (*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.library_roteiro_text.toPlainText())
                QMessageBox.information(self, "Sucesso", f"Roteiro exportado em: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao exportar: {e}")

    def choose_image_dir(self):
        """Escolhe diretório para salvar imagens"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Escolher pasta de imagens", self.image_scraper.image_dir
        )
        if dir_path:
            self.image_scraper.set_image_dir(dir_path)
            self.image_dir_label.setText(f"Pasta: {self.image_scraper.image_dir[:60]}...")
            self.status_label_scraper.setText(f"📁 Pasta alterada para: {dir_path}")

    def start_image_scraping(self):
        """Inicia busca de imagens"""
        term = self.search_term_input.text().strip()
        if not term:
            self.status_label_scraper.setText("⚠️ Digite um termo de pesquisa")
            return

        max_images = self.max_images_input.value()
        high_res = self.high_res_checkbox.currentText() == "Alta"

        self.scrape_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.scraper_log.clear()
        self.status_label_scraper.setText("⏳ Iniciando busca de imagens...")

        self.scraper_thread = ScraperThread(self.image_scraper, term, max_images, high_res)
        self.scraper_thread.update_log.connect(self.scraper_log.append)
        self.scraper_thread.update_progress.connect(self.progress_bar.setValue)
        self.scraper_thread.scraping_finished.connect(self.handle_scraping_result)
        self.scraper_thread.start()

    def handle_scraping_result(self, success, message):
        """Processa resultado do scraping"""
        self.scrape_button.setEnabled(True)
        if success:
            self.status_label_scraper.setText(f"✅ {message}")
            self.scraper_log.append("--- Busca Concluída ---")
        else:
            self.status_label_scraper.setText(f"❌ {message}")
            self.scraper_log.append(f"--- ERRO: {message} ---")

# --- Threads para Operações Assíncronas ---

class RoteiroThread(QThread):
    generation_finished = Signal(object) # object pode ser str (sucesso) ou Exception (erro)

    def __init__(self, generator, prompt):
        super().__init__()
        self.generator = generator
        self.prompt = prompt

    def run(self):
        try:
            result = self.generator.generate(self.prompt)
            self.generation_finished.emit(result)
        except Exception as e:
            self.generation_finished.emit(e)

class ScraperThread(QThread):
    update_log = Signal(str)
    update_progress = Signal(int)
    scraping_finished = Signal(bool, str)

    def __init__(self, scraper, term, max_images, high_res):
        super().__init__()
        self.scraper = scraper
        self.term = term
        self.max_images = max_images
        self.high_res = high_res

    def run(self):
        try:
            self.scraper.scrape_images(self.term, self.max_images, self.high_res, self.update_log, self.update_progress)
            self.scraping_finished.emit(True, "Web scraping de imagens concluído com sucesso.")
        except Exception as e:
            self.scraping_finished.emit(False, f"Erro durante o scraping: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
