# Módulo notificacao_utils

Este módulo fornece utilitários para envio de notificações para o Microsoft Teams por meio de webhooks.

## Funções Disponíveis

### `layout_msg_teams(titulo, mensagem)`

Gera o corpo de um Adaptive Card para ser enviado ao Microsoft Teams.

**Parâmetros:**
- `titulo` (str): O título principal da mensagem.
- `mensagem` (str): A mensagem principal.

**Retorno:**
- `dict`: Estrutura JSON do Adaptive Card formatado para o Teams.

**Exemplo:**
```python
from automacao_utils.notificacao_utils import layout_msg_teams

corpo = layout_msg_teams(
    titulo="Alerta de Processamento", 
    mensagem="O processamento foi concluído com sucesso."
)
```

### `enviar_msg_teams(webhook_url, titulo, mensagem)`

Envia uma mensagem para o Microsoft Teams usando um webhook.

**Parâmetros:**
- `webhook_url` (str): URL do webhook do Teams.
- `titulo` (str): O título principal da mensagem.
- `mensagem` (str): A mensagem principal.

**Exemplo:**
```python
from automacao_utils.notificacao_utils import enviar_msg_teams

enviar_msg_teams(
    webhook_url="https://outlook.office.com/webhook/...",
    titulo="Automação Concluída",
    mensagem="O processo de extração foi finalizado com sucesso."
)
```

## Notas de Uso

- É necessário ter uma URL de webhook válida do Microsoft Teams para usar estas funções.
- As mensagens são formatadas usando Adaptive Cards, que permitem uma apresentação rica no Teams.
- A data e hora do envio são automaticamente incluídas na mensagem.
