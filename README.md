# Scrap Imagens (Anunnakis Roteiros)

Aplicação de scraping de imagens (GUI + backend) para buscar, validar, evitar duplicatas e salvar imagens via Bing. Inclui geração de texto com Google Gemini.

## Sumário rápido
- **Entrada**: `run.py` — GUI (PySide6) com 3 abas: Gerador (AI), Biblioteca (viewer), Scraper (web).
- **Backend**: `anunnakis_roteiros/src/` — core scraping, BD, Gemini integration.
- **Dependências**: `anunnakis_roteiros/requirements.txt`.

## Requisitos
- Python 3.10+ (testado com 3.13). Recomenda-se virtualenv.
- Google Drive montado em Windows (opcional) — padrão: `G:\Meu Drive\CanaL Anunnaki`.
- Google Gemini API (opcional) — configure `GOOGLE_API_KEY` em `.env`.

## Instalação rápida (Windows / PowerShell)

1. Clone e entre na pasta:
```powershell
git clone https://github.com/regaliainterno/scrap_imagens.git
cd scrap_imagens
```

2. Criar e ativar virtualenv:
```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

3. Instalar dependências:
```powershell
pip install -r anunnakis_roteiros\requirements.txt
```

4. (Opcional) Configurar variáveis de ambiente:
```powershell
Copy-Item .env.example .env
# Edite .env com seus valores
```

## Executando

Na raiz do projeto:
```powershell
& .venv\Scripts\python.exe anunnakis_roteiros\run.py
```

A interface gráfica abrirá com três abas:
- **Gerador**: Gera texto usando Google Gemini.
- **Biblioteca**: Visualiza imagens salvas.
- **Scraper**: Busca e baixa imagens do Bing.

## Variáveis de ambiente

Configure no arquivo `.env` (copiar de `.env.example`):

| Variável | Descrição | Default |
|----------|-----------|---------|
| `GOOGLE_API_KEY` | Chave da API Google Gemini | (vazio) |
| `IMAGE_DIR` | Caminho de salvamento de imagens | `G:\Meu Drive\CanaL Anunnaki` |
| `DB_PATH` | Caminho do banco de dados SQLite | `anunnakis_roteiros/src/db/roteiros.db` |
| `MIN_IMAGE_SIZE` | Tamanho mínimo em bytes | `1000` |
| `HIGH_RES_MIN_DIMENSION` | Min px quando `high_res=True` | `1080` |
| `STANDARD_RES_MIN_DIMENSION` | Min px quando `high_res=False` | `480` |

## Configurações importantes

- **Diretório de imagens**: `G:\Meu Drive\CanaL Anunnaki` (fallback: `src/images` se indisponível).
- **Banco de dados**: `anunnakis_roteiros/src/db/roteiros.db` — armazena hashes MD5 para evitar duplicatas.
- **Filtro de resolução**: rejeita imagens com maior lado < `min_dimension`.
- **Multiplicador de requisições**: solicita até `max_images * 10` resultados ao Bing para compensar duplicatas (cap: 1000).

## Como evitar duplicatas

- A aplicação calcula MD5 do conteúdo e verifica no SQLite. Se existir, a imagem é ignorada.
- Para forçar download de duplicatas, modifique `is_hash_downloaded()` em `db_manager.py`.

## Estrutura do projeto

```
scrap_imagens/
├── anunnakis_roteiros/
│   ├── src/
│   │   ├── main.py              # GUI (PySide6)
│   │   ├── image_scraper.py     # Scraper (icrawler + Bing)
│   │   ├── db_manager.py        # Database (SQLite)
│   │   ├── gemini_generator.py  # AI text generation
│   │   └── db/
│   │       └── roteiros.db      # (gerado) SQLite DB
│   ├── run.py                   # Entry point
│   ├── requirements.txt         # Dependências
│   └── README.md
├── .github/workflows/ci.yml     # GitHub Actions CI
├── .env.example                 # Template env vars
├── .gitignore
├── README.md                    # Este arquivo
├── LICENSE                      # MIT
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## CI / Tests

Workflow GitHub Actions (`.github/workflows/ci.yml`) instala deps e executa `pytest` se houver testes.

## Contribuição

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines.

## Licença

MIT License — veja [LICENSE](LICENSE).

---

## FAQ

**P: Como forçar download de imagens duplicadas?**  
R: Modifique `is_hash_downloaded()` em `db_manager.py` para retornar `False`, ou adicione coluna `force` em `image_hashes`.

**P: Como alterar diretório de salvamento?**  
R: Configure `IMAGE_DIR` em `.env` ou use `ImageScraper.set_image_dir(path)`.

**P: Qual é o mínimo de imagens a baixar?**  
R: O sistema tenta até `max_images` únicas. Com muitas duplicatas, pode salvar menos.

**P: Como configurar Google Gemini?**  
R: Obtenha chave em https://aistudio.google.com/app/apikeys e configure `GOOGLE_API_KEY` em `.env`.

