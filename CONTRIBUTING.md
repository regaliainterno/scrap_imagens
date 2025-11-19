# Contributing to Scrap Imagens

Obrigado por seu interesse em contribuir para este projeto! Aqui estão as diretrizes.

## Como contribuir

1. **Fork o repositório** — clique em "Fork" no GitHub.
2. **Clone seu fork localmente**:
   ```powershell
   git clone https://github.com/seu-usuario/scrap_imagens.git
   cd scrap_imagens
   ```
3. **Crie uma branch com um nome descritivo**:
   ```powershell
   git checkout -b feature/sua-feature
   # ou
   git checkout -b fix/seu-bug
   ```
4. **Faça seus commits** com mensagens claras:
   ```powershell
   git commit -m "Add [feature]: descrição do que foi feito"
   ```
5. **Push para seu fork**:
   ```powershell
   git push origin feature/sua-feature
   ```
6. **Abra um Pull Request (PR)** no repositório principal, descrevendo suas mudanças.

## Estilo de código

- **Python**: seguir PEP 8. Use `flake8` para verificação:
  ```powershell
  flake8 anunnakis_roteiros
  ```
- **Commits**: use mensagens descritivas, ex:
  - `Add feature: xy` — nova funcionalidade
  - `Fix: xy` — corrige bug
  - `Refactor: xy` — melhora código existente
  - `Docs: xy` — atualização de documentação

## Testes

Se você adicionar novas funcionalidades, por favor adicione testes:
```powershell
# Na pasta test/
pytest
```

## Reportar bugs

Use a seção "Issues" do GitHub. Inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. observado
- Versão do Python, SO, e arquivo `.env` (sem senha!)

## Perguntas ou dúvidas

Abra uma Issue com tag `question` ou `discussion`.

---

Obrigado por contribuir! 🙏
