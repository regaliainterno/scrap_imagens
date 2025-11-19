# Anunnakis Roteiros e Imagens

Esta é uma aplicação desktop em Python desenvolvida com **PySide6** (Qt for Python) para:
1. Gerar roteiros de histórias sobre os Anunnakis usando a **API Gemini**.
2. Realizar web scraping de imagens relacionadas a um termo de pesquisa, com controle de duplicidade por hash.

## Estrutura do Projeto

\`\`\`
anunnakis_roteiros/
├── src/
│   ├── db/
│   ├── images/
│   ├── ui/
│   ├── __init__.py
│   ├── main.py           # Lógica principal da GUI
│   ├── db_manager.py     # Gerenciamento do banco de dados SQLite
│   ├── gemini_generator.py # Integração com a API Gemini
│   └── image_scraper.py  # Lógica de Web Scraping
├── run.py                # Ponto de entrada da aplicação
├── requirements.txt      # Dependências do Python
└── README.md             # Este arquivo
\`\`\`

## Requisitos

Você precisará ter o **Python 3.10+** instalado em seu sistema.

## Configuração

### 1. Chave da API Gemini

Para que o gerador de roteiros funcione, você precisa de uma chave da API Gemini.

1. Obtenha sua chave em [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).
2. **Configure a chave como uma variável de ambiente** no seu sistema operacional. O nome da variável deve ser **\`GEMINI_API_KEY\`**.

**No PyCharm:** Você pode configurar a variável de ambiente diretamente na configuração de execução do seu projeto.

### 2. Instalação das Dependências

1. Abra o terminal (ou o terminal do PyCharm) na pasta raiz do projeto (\`anunnakis_roteiros\`).
2. **Recomendado:** Crie e ative um ambiente virtual:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # No Linux/macOS
   venv\Scripts\activate     # No Windows
   \`\`\`
3. Instale as dependências:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Execução da Aplicação

Após a configuração e instalação das dependências, execute o arquivo \`run.py\`:

\`\`\`bash
python run.py
\`\`\`

## Funcionalidades

### 1. Gerador de Roteiros (Aba "Gerador de Roteiros")

*   **Prompt:** Digite o tema do roteiro (ex: "A criação do homem por Enki e Enlil").
*   **Gerar Roteiro:** Usa a API Gemini para criar um roteiro detalhado.
*   **Modo de Visualização:** Permite alternar entre:
    *   **Padrão:** O texto original gerado, com marcações de cena e tempo.
    *   **Limpo:** Apenas os parágrafos de diálogo/ação, sem títulos ou tempos.
    *   **Com Tempos:** Destaca os tempos de leitura/duração para cada bloco de texto.
*   **Salvar/Carregar:** Os roteiros são salvos em um banco de dados SQLite (\`src/db/anunnakis_data.db\`) e podem ser carregados posteriormente.

### 2. Web Scraper de Imagens (Aba "Web Scraper de Imagens")

*   **Termo de Pesquisa:** Digite o termo para buscar imagens (ex: "Nibiru planet").
*   **Máx. Imagens:** Defina o número máximo de imagens a serem baixadas.
*   **Resolução:** Escolha entre "Alta Resolução" (tenta buscar imagens maiores) ou "Qualquer Resolução".
*   **Buscar e Baixar Imagens:**
    *   As imagens são baixadas para a pasta \`src/images/\`.
    *   Um **hash** de cada imagem é calculado e salvo no banco de dados.
    *   Se você tentar baixar a mesma imagem novamente, ela será ignorada, prevenindo duplicidade.
\`\`\`
