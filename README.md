# Scrap Imagens (Anunnakis Roteiros)

Este repositório contém a aplicação de scraping de imagens (GUI + backend) usada para buscar imagens via Bing, validar, evitar duplicatas e salvar em uma pasta (por padrão: Google Drive local montado).

## Sumário rápido
- Entrada: `run.py` — inicia a aplicação GUI (PySide6)
- Código principal: `anunnakis_roteiros/src`
- Configuração de dependências: `anunnakis_roteiros/requirements.txt`

## Requisitos
- Python 3.10/3.11+ (teste com 3.13). Recomenda-se usar um virtualenv.
- Google Drive deve estar montado em Windows (opcional). O caminho padrão usado pela aplicação é `G:\\Meu Drive\\CanaL Anunnaki`.

## Instalação (Windows / PowerShell)
1. Criar e ativar virtualenv:
```powershell
python -m venv .venv
& .venv\\Scripts\\Activate.ps1
```
2. Instalar dependências:
```powershell
pip install -r anunnakis_roteiros\\requirements.txt
```

## Executando
Na raiz do projeto:
```powershell
& .venv\\Scripts\\python.exe anunnakis_roteiros\\run.py
```

## Configurações importantes
- Diretório de imagens padrão: `G:\\Meu Drive\\CanaL Anunnaki` — se não existir, a aplicação cria uma pasta local `src/images` como fallback.
- Banco de dados (SQLite): `anunnakis_roteiros/src/db/roteiros.db` — armazena hashes das imagens baixadas para evitar duplicatas.
- Filtro de resolução: ao ativar `high_res` a aplicação rejeita imagens com o maior lado menor que 1080px (padrão 480px quando `high_res=False`).

## Como evitar baixar duplicatas (comportamento atual)
- A aplicação calcula MD5 do conteúdo e verifica no DB. Se já existir, a imagem é ignorada.
- Para obter mais resultados quando muitas duplicatas existem, o scraper solicita mais resultados ao Bing (multiplicador padrão 10x). Você pode escolher buscar termos mais específicos.

## CI / Tests
Incluí um workflow GitHub Actions básico (`.github/workflows/ci.yml`) que instala dependências e executa `pytest` caso existam testes no repositório.

## Contribuição
- Faça fork do repositório, crie uma branch e abra um PR.

## Licença
Sem licença especificada. Adicione um arquivo `LICENSE` se desejar tornar o projeto público com termos claros.

---
Se quiser, eu posso adicionar instruções mais detalhadas (ex.: variáveis de ambiente, como ajustar `image_dir`, ou integração com APIs externas).
