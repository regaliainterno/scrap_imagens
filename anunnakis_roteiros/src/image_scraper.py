import os
import hashlib
from PIL import Image
from io import BytesIO
import time
import shutil
from icrawler.builtin import BingImageCrawler

# Importar módulo local
from .db_manager import DatabaseManager


class ImageScraper:
    def __init__(self, db_manager: DatabaseManager, image_dir: str = None):
        self.db_path = db_manager.db_file
        self.db_base_dir = db_manager.base_dir
        
        # Se nao especificar diretorio, usar G:\Meu Drive\CanaL Anunnaki
        if image_dir:
            self.image_dir = image_dir
        else:
            self.image_dir = r"G:\Meu Drive\CanaL Anunnaki"
        
        # Criar diretorio se nao existir
        try:
            os.makedirs(self.image_dir, exist_ok=True)
        except Exception as e:
            # Se G:\ nao existir, usar pasta local como fallback
            self.image_dir = os.path.join(os.path.dirname(__file__), "images")
            os.makedirs(self.image_dir, exist_ok=True)

    def set_image_dir(self, path: str):
        """Permite alterar dinamicamente o diretório onde as imagens serão salvas."""
        if not path:
            return
        self.image_dir = path
        os.makedirs(self.image_dir, exist_ok=True)

    def _calculate_hash(self, image_data):
        """Calcula hash MD5 dos dados da imagem."""
        return hashlib.md5(image_data).hexdigest()

    def scrape_images(self, term, max_images, high_res, log_signal, progress_signal):
        """Realiza web scraping usando icrawler BingImageCrawler."""
        log_signal.emit(f"Iniciando busca por: '{term}' (Maximo: {max_images})")
        progress_signal.emit(10)
        
        try:
            # Criar nova conexao com BD
            db_manager = DatabaseManager(
                os.path.basename(self.db_path),
                base_dir=self.db_base_dir
            )
            
            # Diretorio temporario para download
            temp_dir = os.path.join(self.image_dir, "temp_bing")
            os.makedirs(temp_dir, exist_ok=True)
            
            log_signal.emit(f"[BUSCA] Buscando '{term}' no Bing Images...")
            progress_signal.emit(20)
            
            # Usar BingImageCrawler do icrawler
            # Aplicar filtros para evitar miniaturas e thumbnails de vídeo quando possível
            # Observação: Bing nem sempre respeita todos filtros, mas reduz ruído.
            filters = None
            if high_res:
                filters = {'size': 'large', 'type': 'photo'}
            else:
                filters = {'size': 'medium', 'type': 'photo'}

            try:
                log_signal.emit(f"[INFO] Aplicando filtros de busca: {filters}")
            except:
                pass

            bing_crawler = BingImageCrawler(
                storage={'root_dir': temp_dir}
            )
            
            log_signal.emit("[DOWNLOAD] Fazendo download das imagens...")
            progress_signal.emit(30)
            
            # Fazer download
            try:
                # Se houver muitas duplicatas, solicitar mais resultados ao icrawler
                # Multiplicador padrão (10x) para aumentar a chance de conseguir
                # max_images únicas. Capamos para evitar downloads excessivos.
                multiplier = 10
                if max_images <= 0:
                    num_to_fetch = 100
                else:
                    num_to_fetch = max_images * multiplier
                num_to_fetch = min(num_to_fetch, 1000)  # cap em 1000

                log_signal.emit(f"[INFO] Solicitando até {num_to_fetch} resultados para compensar duplicatas...")
                bing_crawler.crawl(
                    keyword=term,
                    filters=None,
                    offset=0,
                    max_num=num_to_fetch
                )
                # Aguardar conclusao do icrawler com timeout
                log_signal.emit("[INFO] Aguardando conclusao do download...")
                time.sleep(10)  # Aumentar tempo de espera significativamente
            except Exception as e:
                log_signal.emit(f"[AVISO] Erro no download: {str(e)[:50]}")
            
            progress_signal.emit(50)
            
            # Processar imagens baixadas
            # O icrawler cria uma subpasta com o nome do termo e coloca as imagens lá dentro
            search_folder = os.path.join(temp_dir, term)
            
            if not os.path.exists(search_folder):
                try:
                    log_signal.emit(f"[AVISO] Pasta esperada nao encontrada: {search_folder}")
                except:
                    pass
                # Tentar usar temp_dir diretamente
                search_folder = temp_dir
                if not os.path.exists(search_folder):
                    log_signal.emit("[ERRO] Pasta temporaria nao encontrada")
                    progress_signal.emit(100)
                    return
            
            downloaded_count = 0
            processed_count = 0
            
            # Listar arquivos diretamente em temp_dir (icrawler nao cria subpastas)
            image_files = []
            try:
                all_files = os.listdir(search_folder)
                log_signal.emit(f"[DEBUG] Arquivos em temp_dir: {len(all_files)}")
                log_signal.emit(f"[DEBUG] Listando arquivos: {all_files[:5]}...")  # DEBUG
                for f in all_files:
                    full_path = os.path.join(search_folder, f)
                    # Verificar se arquivo existe e é imagem
                    if os.path.isfile(full_path):
                        try:
                            log_signal.emit(f"[DEBUG] Arquivo encontrado: {f}")  # DEBUG
                        except:
                            pass
                        if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp', '.gif', '.bmp')):
                            image_files.append(full_path)
                        else:
                            try:
                                log_signal.emit(f"[DEBUG] Arquivo ignorado (sem extensao): {f}")  # DEBUG
                            except:
                                pass
            except Exception as list_err:
                log_signal.emit(f"[ERRO] Ao listar pasta: {str(list_err)[:50]}")
                return
            
            log_signal.emit(f"[INFO] Encontradas {len(image_files)} imagens. Processando...")
            progress_signal.emit(55)
            
            min_dimension = 1080 if high_res else 480
            
            for filepath in image_files:
                if downloaded_count >= max_images:
                    try:
                        log_signal.emit(f"[OK] Limite de {max_images} imagens atingido!")
                    except:
                        pass
                    break
                
                processed_count += 1
                filename = os.path.basename(filepath)
                
                try:
                    log_signal.emit(f"Processando {processed_count}/{len(image_files)}: {filename}")
                except:
                    pass
                
                try:
                    # Verificar se arquivo existe ANTES de tentar abrir
                    if not os.path.exists(filepath):
                        try:
                            log_signal.emit(f"  [AVISO] Arquivo desapareceu: {filename}")
                        except:
                            pass
                        continue
                    
                    try:
                        log_signal.emit(f"  [DEBUG] Caminho completo: {filepath}")  # DEBUG
                    except:
                        pass
                    
                    # Ler arquivo
                    with open(filepath, 'rb') as f:
                        image_data = f.read()
                    
                    log_signal.emit(f"  [DEBUG] Arquivo lido, tamanho: {len(image_data)} bytes")
                    
                    # Validar tamanho minimo (1KB)
                    if len(image_data) < 1000:
                        try:
                            log_signal.emit(f"  Ignorado: tamanho pequeno ({len(image_data)} bytes)")
                        except:
                            pass
                        continue
                    
                    # Calcular hash
                    file_hash = self._calculate_hash(image_data)
                    
                    # Verificar duplicidade
                    if db_manager.is_hash_downloaded(file_hash):
                        try:
                            log_signal.emit(f"  Ignorado: imagem JA BAIXADA (duplicada)")
                        except:
                            pass
                        continue
                    
                    # Validar imagem
                    try:
                        img = Image.open(BytesIO(image_data))
                        width, height = img.size
                        largest_side = max(width, height)
                        
                        # Log de dimensoes
                        try:
                            log_signal.emit(f"  Dimensoes: {width}x{height} (maior: {largest_side}px)")
                        except:
                            pass
                        
                        if largest_side < min_dimension:
                            try:
                                log_signal.emit(f"  Ignorado: muito pequena (minimo: {min_dimension}px)")
                            except:
                                pass
                            continue
                        
                        ext = img.format.lower() if img.format else 'jpg'
                        if ext == 'jpeg':
                            ext = 'jpg'
                        elif ext not in ['png', 'webp', 'gif', 'bmp', 'jpg']:
                            ext = 'jpg'
                    except Exception as img_err:
                        try:
                            log_signal.emit(f"  Ignorado: nao e imagem valida ({type(img_err).__name__}: {str(img_err)[:30]})")
                        except:
                            pass
                        continue
                    
                    # Salvar no diretorio final
                    final_filename = f"{term.replace(' ', '_')}_{file_hash[:8]}_{int(time.time())}.{ext}"
                    final_filepath = os.path.join(self.image_dir, final_filename)
                    
                    with open(final_filepath, 'wb') as f:
                        f.write(image_data)
                    
                    # Registrar no DB
                    db_manager.add_downloaded_hash(file_hash, term)
                    downloaded_count += 1
                    try:
                        log_signal.emit(f"  [SALVA] Imagem {downloaded_count}/{max_images} ({width}x{height})")
                    except:
                        pass
                
                except Exception as e:
                    try:
                        log_signal.emit(f"  [ERRO] {type(e).__name__}: {str(e)[:50]}")
                    except:
                        pass
                    continue
                
                # Progresso
                progress = 55 + int((downloaded_count / max_images) * 40) if max_images > 0 else 55
                progress_signal.emit(min(progress, 95))
                time.sleep(0.1)
            
            # Limpar pasta temporaria APOS terminar de processar
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            
            progress_signal.emit(100)
            
            if downloaded_count == max_images:
                try:
                    log_signal.emit(f"[OK] SUCESSO! {downloaded_count}/{max_images} imagens salvas em {self.image_dir}")
                except:
                    pass
            elif downloaded_count > 0:
                try:
                    log_signal.emit(f"[AVISO] Parcial: {downloaded_count}/{max_images} imagens salvas em {self.image_dir}")
                except:
                    pass
            else:
                try:
                    log_signal.emit("[ERRO] Nenhuma imagem valida foi salva.")
                except:
                    pass
        
        except Exception as e:
            log_signal.emit(f"[ERRO] {str(e)[:100]}")
            progress_signal.emit(100)
