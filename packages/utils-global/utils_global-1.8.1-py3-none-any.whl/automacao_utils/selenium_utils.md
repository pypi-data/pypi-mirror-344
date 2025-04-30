# Módulo selenium_utils

Este módulo fornece utilitários adicionais para trabalhar com SeleniumBase, estendendo suas funcionalidades para casos de uso específicos em automações.

## Funções Disponíveis

### `garantir_iframe(self, iframe)`

Garante que o script está no iframe correto, primeiro retornando para o conteúdo padrão da página e então mudando para o iframe especificado.

**Parâmetros:**
- `self`: Instância do SeleniumBase.
- `iframe`: Elemento ou seletor CSS do iframe.

**Comportamento:**
1. Retorna para o conteúdo padrão da página
2. Aguarda 0,5 segundos para garantir a transição
3. Muda para o iframe especificado

**Exemplo:**
```python
from seleniumbase import BaseCase
from automacao_utils.utils_selenium import garantir_iframe

class MinhaAutomacao(BaseCase):
    def test_exemplo(self):
        self.open("https://exemplo.com.br")
        
        # Garantir que estamos no iframe correto
        garantir_iframe(self, "#meu_iframe")
        
        # Agora podemos interagir com elementos dentro do iframe
        self.click("#botao_dentro_do_iframe")
```

## Notas de Uso

- Esta função é especialmente útil em páginas com múltiplos iframes, onde é comum perder a referência do iframe atual.
- A função trata exceções e fornece mensagens de erro detalhadas para facilitar o diagnóstico de problemas.
- É recomendável usar esta função sempre que precisar interagir com elementos dentro de iframes, especialmente em páginas complexas.
