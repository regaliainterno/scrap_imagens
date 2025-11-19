# 🚀 INÍCIO RÁPIDO - Anunnakis Roteiros

## ⚡ Em 3 Passos

### 1️⃣ Configurar API Key
Edite o arquivo `.env` na pasta do projeto:
```
GEMINI_API_KEY=sua_chave_aqui
```
**Obter chave gratuitamente**: https://ai.google.dev

### 2️⃣ Executar a Aplicação
```bash
python anunnakis_roteiros/run.py
```

### 3️⃣ Começar a Usar!

---

## 📝 Como Usar Cada Funcionalidade

### Aba 1: Gerador de Roteiros 📝

1. Escolha um tema da lista ou escreva seu próprio prompt
2. Clique em **[🎲 Gerar Prompt Aleatório]** (opcional)
3. Clique em **[📄 Gerar Roteiro]**
4. ✅ Roteiro é **auto-salvo** no banco de dados

**Temas pré-definidos:**
- Medo e Horror
- Mistério e Suspense
- Antigo Egito
- Anunnaki (civilização antiga)
- E mais...

---

### Aba 2: Biblioteca de Roteiros 📚

**Lista (esquerda):**
- Mostra todos os roteiros salvos
- Clique para visualizar

**Visualizador (direita):**
- Mostra conteúdo completo
- Botão **[📋 Copiar]** para copiar para clipboard
- Botão **[❌ Deletar]** para remover com confirmação

---

### Aba 3: Scraper de Imagens 🖼️

1. **Digite o termo**: Ex: "Anunnaki", "Egito Antigo", "Mistério"
2. **Máx de imagens**: Escolha entre 1-100 (padrão: 20)
3. **Qualidade**: 
   - ⭐ = 480p mínimo (padrão)
   - ⭐⭐⭐⭐⭐ = 1080p mínimo (máxima qualidade)
4. Clique em **[Baixar Imagens]**
5. ✅ Imagens aparecem em `src/images/`

**O que acontece:**
- Selenium abre Chrome (headless)
- Acessa Bing Images
- Faz scroll para carregar imagens
- Valida qualidade
- Impede duplicatas
- Faz download com validação

---

## 📁 Onde Estão os Dados?

### Roteiros (Banco de Dados)
```
G:\Meu Drive\SQL\roteiros\roteiros.db
```
(ou conforme configurado)

### Imagens Baixadas
```
anunnakis_roteiros\src\images\
```

### Arquivo de Configuração
```
anunnakis_roteiros\.env
```

---

## 🆘 Problemas Comuns

### "Erro: GEMINI_API_KEY not found"
→ Configure `.env` com sua chave de https://ai.google.dev

### "Selenium timeout esperando imagens"
→ Bing Images estava carregando lentamente, tente novamente

### "Nenhuma imagem encontrada para este termo"
→ Tente outro termo ou aumentar o número máximo de imagens

### "ChromeDriver failed to install"
→ Instale Chrome em sua máquina (webdriver-manager encontrará)

### "Database locked"
→ Feche a aplicação e reabra (SQLite thread-safe agora)

---

## 💡 Dicas e Truques

### 🎨 Temas para Prompts
```
- "Crie um roteiro sobre viajantes do espaço na era das pirâmides"
- "Escreva um mistério envolvendo artefatos antigos e tecnologia"
- "Narrative sobre contato extraterrestre na civilização Anunnaki"
- "Roteiro de horror baseado em lendas egípcias"
```

### 🖼️ Termos Úteis para Imagens
```
- "Egito Antigo Pirâmides"
- "Hieróglifos Egípcios"
- "Artefatos Antigos Mistério"
- "Noite Estrelada Cosmos"
- "Templo Ruínas Arqueologia"
```

### ⏱️ Tempos Estimados
- **Gerar Roteiro**: 2-5 segundos
- **Baixar 20 Imagens**: 30-60 segundos
- **Primeiro Scrape**: Mais lento (ChromeDriver inicia)

---

## 🎯 Exemplo de Uso Completo

```
1. Abrir aplicação
   → Interface clara com 3 abas

2. Ir para Gerador
   → Escolher tema ou escrever prompt
   → Clicar "Gerar Roteiro"
   → Roteiro aparece automaticamente salvo

3. Ir para Scraper
   → Buscar "Pirâmides Egito"
   → Selecionar 15 imagens
   → Qualidade máxima
   → Clicar "Baixar"

4. Ir para Biblioteca
   → Ver roteiro gerado na lista
   → Copiar ou deletar conforme necessário

5. Imagens estão em src/images/
   → Prontas para usar em apresentações, blogs, etc.
```

---

## 🔧 Configuração Avançada

### Alterar Diretório de Imagens
No código `src/main.py`, procure por:
```python
# No método scraper_worker:
self.scraper.set_image_dir("seu/caminho/aqui")
```

### Alterar Diretório de Banco de Dados
No arquivo `.env`, adicione:
```
DB_PATH=G:\Seu\Caminho\Customizado
```

### Usar Modelo Gemini Diferente
Em `src/gemini_generator.py`, modifique a lista de modelos:
```python
preferred_models = [
    "gemini-2.5-pro",  # Novo modelo
    "gemini-2.0-flash",
    # ...
]
```

---

## 📊 Requisitos do Sistema

- **Windows 10+** ✅
- **Python 3.13+** ✅
- **Chrome/Chromium instalado** ✅
- **Conexão com Internet** ✅
- **Espaço em disco**: ~2GB (para imagens)
- **RAM mínima**: 4GB recomendado

---

## 🚀 Para Iniciar

```bash
# Abrir terminal na pasta do projeto
cd C:\Users\jdfxop\PycharmProjects\anunnakis_roteiros

# Executar
python anunnakis_roteiros/run.py
```

Pronto! A aplicação deve abrir em segundos.

---

## 📚 Documentação Completa

Para detalhes técnicos, veja:
- `STATUS_FINAL.md` - Status completo do projeto
- `SCRAPER_INTEGRATION.md` - Detalhes do web scraper
- Código-fonte em `src/`

---

## ✨ Destaques

✅ **Tudo Automático**
- Auto-save de roteiros
- ChromeDriver auto-gerenciado
- Fallback automático de modelos IA

✅ **Validação Rigorosa**
- Limite EXATO de imagens
- Deduplicação via hash
- Validação de dimensões

✅ **Interface Profissional**
- Tema claro com azul #1976D2
- Responsiva e intuitiva
- Logging em tempo real

✅ **Production-Ready**
- Thread-safe
- Error handling completo
- Documentação completa

---

**Desenvolvido com ❤️ em Python + PySide6 + Selenium**

Aproveite! 🎉
