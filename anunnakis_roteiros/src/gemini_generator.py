import os
from google import genai
import re

class GeminiGenerator:
    def __init__(self):
        """Inicializa o cliente Gemini com a chave da API do arquivo .env"""
        try:
            # Carrega a chave da API da variável de ambiente
            api_key = os.getenv('GEMINI_API_KEY')
            
            if not api_key:
                raise ValueError(
                    "GEMINI_API_KEY não configurada. "
                    "Crie um arquivo .env na raiz do projeto com sua chave API."
                )
            
            self.client = genai.Client(api_key=api_key)
            self.model = self._select_best_model()
            print(f"Modelo Gemini selecionado: {self.model}")
        except Exception as e:
            print(f"Erro ao inicializar o cliente Gemini: {e}")
            self.client = None
            self.model = None

    def _select_best_model(self):
        """Detecta os modelos disponíveis e seleciona o melhor para geração de texto."""
        # Lista de modelos em ordem de preferência
        preferred_models = [
            'gemini-2.0-flash',           # Últimas e melhores capacidades
            'gemini-2.0-flash-lite',      # Rápido e leve
            'gemini-1.5-pro',             # Pro com capacidades avançadas
            'gemini-1.5-flash',           # Flash rápido
            'gemini-1.5-flash-8b',        # Ultra rápido com 8B parâmetros
            'gemini-1.5-flash-001',       # Versão estável do Flash
            'gemini-exp-1209',             # Modelos experimentais
            'gemini-exp-1121',
            'text-embedding-004',          # Fallback para embedding
        ]
        
        try:
            # Obtém lista de modelos disponíveis
            available_models = self.client.models.list()
            available_model_names = [model.name.split('/')[-1] for model in available_models]
            
            print(f"Modelos disponíveis: {available_model_names[:5]}...")  # Mostra primeiros 5
            
            # Tenta encontrar o melhor modelo na lista de preferências
            for preferred_model in preferred_models:
                if preferred_model in available_model_names:
                    return preferred_model
            
            # Se nenhum modelo preferido foi encontrado, usa o primeiro disponível
            if available_model_names:
                return available_model_names[0]
            
            # Fallback padrão
            return 'gemini-2.0-flash'
            
        except Exception as e:
            print(f"Aviso ao listar modelos: {e}. Usando modelo padrão 'gemini-2.0-flash'")
            return 'gemini-2.0-flash'

    def generate(self, prompt):
        """Gera um roteiro de história sobre Anunnakis usando a API Gemini."""
        if not self.client:
            raise Exception("Cliente Gemini não inicializado. Verifique a configuração da sua chave API.")

        system_instruction = (
            "Você é um roteirista especializado em mitologia suméria e na teoria dos Antigos Astronautas, "
            "com foco nos Anunnakis. Sua tarefa é criar um roteiro de história detalhado e envolvente "
            "baseado no prompt do usuário. O roteiro deve ser estruturado em cenas e parágrafos. "
            "Inclua sugestões de tempo de leitura/duração para cada cena (ex: [Duração: 2 minutos]). "
            "O roteiro deve ser totalmente controlável pelo usuário, então use títulos de cena claros e "
            "parágrafos bem definidos. O tema principal é sempre relacionado aos Anunnakis."
        )
        
        full_prompt = f"Crie um roteiro de história sobre Anunnakis com o seguinte tema: '{prompt}'"

        # Lista de modelos em ordem de preferência (fallback)
        fallback_models = [
            self.model,
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-1.5-flash-8b',
        ]
        
        last_error = None
        
        # Tenta usar cada modelo até conseguir uma resposta bem-sucedida
        for model in fallback_models:
            try:
                print(f"Tentando com modelo: {model}")
                response = self.client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                print(f"Sucesso com modelo: {model}")
                return response.text
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # Se for erro de modelo não encontrado, tenta o próximo
                if 'not found' in error_msg or 'invalid' in error_msg or 'not available' in error_msg:
                    print(f"Modelo {model} não disponível, tentando próximo...")
                    continue
                
                # Se for erro de sobrecarga, também tenta o próximo
                if 'overload' in error_msg or 'unavailable' in error_msg or 'busy' in error_msg:
                    print(f"Modelo {model} sobrecarregado, tentando próximo...")
                    continue
                
                # Para outros erros, continua tentando
                print(f"Erro com {model}: {e}. Tentando próximo...")
                continue
        
        # Se todos os modelos falharam, lança a última exceção
        raise Exception(f"Erro na geração do roteiro com todos os modelos: {last_error}")

    def format_roteiro(self, roteiro_raw, mode):
        """Formata o roteiro bruto de acordo com o modo de visualização selecionado."""
        
        if mode == "Padrão (com marcações)":
            # Retorna o texto como veio, com todas as marcações (títulos, durações, etc.)
            return roteiro_raw
            
        elif mode == "Limpo (apenas parágrafos)":
            # Remove títulos de cena e marcações de duração
            # Assume que títulos de cena são linhas em MAIÚSCULAS ou com formatação específica (ex: #, ##)
            # e que marcações de duração estão entre colchetes.
            lines = roteiro_raw.split('\n')
            clean_lines = []
            for line in lines:
                # Remove marcações de duração (ex: [Duração: 2 minutos])
                line = re.sub(r'\[Duração:.*?\]', '', line).strip()
                
                # Tenta identificar e remover títulos (linhas curtas e em maiúsculas)
                if line and len(line) < 80 and line.isupper() and not line.endswith('.'):
                    continue
                
                if line:
                    clean_lines.append(line)
            
            return '\n\n'.join(clean_lines)
            
        elif mode == "Com Tempos (para leitura)":
            # Destaca apenas os parágrafos e os tempos de leitura
            lines = roteiro_raw.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                
                # Encontra a marcação de duração
                duration_match = re.search(r'(\[Duração:.*?\])', line)
                
                if duration_match:
                    # Se for uma linha de título com duração, destaca a duração
                    duration = duration_match.group(1)
                    line_without_duration = line.replace(duration, '').strip()
                    formatted_lines.append(f"--- {line_without_duration} --- {duration}\n")
                elif line:
                    # Se for um parágrafo, apenas adiciona
                    formatted_lines.append(line)
            
            return '\n'.join(formatted_lines)
            
        return roteiro_raw

if __name__ == '__main__':
    # Este bloco é apenas para teste e não será executado na aplicação GUI
    # O usuário precisará configurar a chave API para que isso funcione.
    print("Módulo GeminiGenerator pronto. Configure a variável de ambiente GEMINI_API_KEY para uso.")
