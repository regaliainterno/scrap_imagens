# 🎭 Anunnakis - Roteiros e Imagens

Aplicação desktop moderna para gerar roteiros sobre Anunnakis usando IA avançada e fazer web scraping de imagens relacionadas.

## ✨ Funcionalidades Principais

### 📝 Gerador de Roteiros Inteligente
- ✅ **Salvamento automático** no banco de dados após geração
- ✅ Geração automática de prompts sobre Anunnaki
- ✅ Botão "Sugestão Aleatória" para diversas temáticas  
- ✅ Múltiplos modos de visualização (com marcações, limpo, com tempos)
- ✅ Exportação individual para arquivo TXT
- ✅ Interface limpa e intuitiva com feedback visual

### 📚 Biblioteca de Roteiros
- ✅ **Acesso independente a todos os roteiros salvos**
- ✅ Visualização organizada em lista
- ✅ Seleção para leitura rápida
- ✅ Exclusão de roteiros
- ✅ Exportação individual para arquivo
- ✅ Atualização em tempo real

### 🖼️ Web Scraper de Imagens Avançado
- ✅ Busca inteligente de imagens
- ✅ Filtro de resolução (alta ou qualquer)
- ✅ Controle fino de quantidade
- ✅ Escolha de pasta de destino
- ✅ Detecção de duplicatas por hash SHA256
- ✅ Log em tempo real com progresso visual

## 🛠️ Estrutura do Projeto

```
anunnakis_roteiros/
├── src/
│   ├── db/                    # Banco de dados SQLite
│   ├── images/               # Pasta de imagens baixadas
│   ├── __init__.py
│   ├── main.py               # Interface PySide6 redesenhada
│   ├── db_manager.py         # Gerenciamento de dados
│   ├── gemini_generator.py   # IA com seleção automática de modelos
│   └── image_scraper.py      # Web scraping com hash detection
├── run.py                    # Ponto de entrada
├── requirements.txt          # Dependências Python
├── .env                      # Chave API (gitignored)
├── .env.example              # Exemplo de configuração
├── .gitignore               # Proteção de dados sensíveis
└── README.md                # Esta documentação
```

## 🚀 Quick Start

### 1️⃣ Obter Chave da API Gemini
- Acesse: https://ai.google.dev/
- Clique em "Get API Key"
- Crie uma chave gratuita

### 2️⃣ Clonar e Configurar
```bash
# Clonar repositório
git clone <seu_repo>
cd anunnakis_roteiros

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar API
cp .env.example .env
# Editar .env e adicionar sua chave:
# GEMINI_API_KEY=sua_chave_aqui
```

### 3️⃣ Executar Aplicação
```bash
python anunnakis_roteiros/run.py
```

## 📋 Dependências

```
pyside6            # Interface gráfica moderna
google-genai       # IA Gemini com fallback automático
requests           # HTTP para web scraping
beautifulsoup4     # Parsing HTML
Pillow             # Processamento de imagens
sqlite-utils       # Gerenciamento de banco de dados
python-dotenv      # Carregamento de variáveis de ambiente
```

## 🎨 Design e UX

A interface foi completamente redesenhada com:
- **Tema escuro moderno** com paleta de cores azul/teal
- **Organização clara** com seções bem definidas
- **Feedback visual** com ícones e status em tempo real
- **Layout responsivo** com abas bem separadas
- **Formulários intuitivos** com valores padrão sensatos

## 🧠 Tecnologia de IA

### Seleção Automática de Modelos
A aplicação detecta automaticamente os melhores modelos disponíveis na sua conta Gemini e os seleciona em ordem de preferência:

1. `gemini-2.0-flash` - Mais rápido e eficiente
2. `gemini-2.0-flash-lite` - Ultra rápido
3. `gemini-1.5-pro` - Maior capacidade
4. `gemini-1.5-flash` - Equilíbrio
5. E mais... com fallback automático

### Fallback Inteligente
Se um modelo está sobrecarregado (503 UNAVAILABLE), a aplicação tenta automaticamente o próximo modelo da lista até conseguir uma resposta.

## 💾 Banco de Dados

Usa SQLite para armazenar:
- ✅ Roteiros gerados (título, conteúdo, data)
- ✅ Hashes de imagens baixadas (para evitar duplicatas)
- ✅ Histórico de buscas

## 🔒 Segurança

- ✅ Chave API em arquivo `.env` (não commitado)
- ✅ `.gitignore` protege dados sensíveis
- ✅ Banco de dados local (sem upload)
- ✅ Hashes SHA256 para integridade de imagens

## 📸 Prints da Interface

### Aba Gerador de Roteiros
- Campo de entrada com placeholder
- Botões destacados: "Gerar Roteiro" e "Sugestão Aleatória"
- Área de visualização com opções de formatação
- Status em tempo real com emojis

### Aba Biblioteca de Roteiros
- Lista de roteiros salvos (lado esquerdo)
- Visualização do conteúdo (lado direito)
- Botões: Atualizar, Deletar, Exportar

### Aba Web Scraper
- Campo de busca
- Filtros: máximo de imagens, resolução
- Seleção de pasta de destino
- Barra de progresso
- Log em tempo real

## 🐛 Troubleshooting

### "API key not valid"
- Verifique se copiou a chave corretamente em `.env`
- Regenere a chave no site do Gemini

### "ModuleNotFoundError"
- Certifique-se que o ambiente virtual está ativado
- Execute: `pip install -r requirements.txt`

### Imagens não salvam
- Verifique a pasta escolhida tem permissão de escrita
- Tente "📁 Escolher Pasta" novamente

## 📝 Notas de Uso

1. **Roteiros são salvos automaticamente** - Não precisa clicar em salvar!
2. **Biblioteca é organizada** - Acesse todos os roteiros na aba "📚 Biblioteca"
3. **Fallback automático** - Não se preocupe se um modelo estiver lento
4. **Sem limite de tokens** - Use quantas vezes quiser com sua chave gratuita

## 🔄 Fluxo Típico

```
1. Abrir app → 2. Ir para "📝 Gerador"
3. Clicar "🎲 Sugestão Aleatória" (ou digitar prompt)
4. Esperar geração (está salvando automaticamente!)
5. Escolher modo de visualização
6. (Opcional) Exportar para arquivo
7. Ir para "📚 Biblioteca" para ver histórico
```

## 📞 Suporte

Para dúvidas ou issues:
- Verifique os logs no console
- Consulte a documentação do Gemini
- Verifique a conexão com internet

## 📄 Licença

Este projeto é open source e educacional.

---

**Desenvolvido com ❤️ para explorar a mitologia Anunnaki através da IA.**
