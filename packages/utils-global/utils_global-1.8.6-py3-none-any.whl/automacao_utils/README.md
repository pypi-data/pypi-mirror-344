# Pacote automacao_utils

Este pacote contém módulos utilitários para automações baseadas em Selenium, facilitando operações comuns como downloads de arquivos, verificação de arquivos em uso, e detecção de erros.

## Módulos Disponíveis

- [download_utils](./download_utils.md): Funções para gerenciamento de downloads e tratamento de erros
- [version_check](./version_check.md): Sistema de verificação de versões da biblioteca
- [selenium_utils](./selenium_utils.md): Utilitários para interação com iframes no Selenium
- [notificacao_utils](./notificacao_utils.md): Envio de notificações para o Microsoft Teams

## Importação

```python
# Importação básica
from automacao_utils import processar_download, DownloadErroException

# Importação específica
from automacao_utils.download_utils import renomear_arquivo, limpar_nome_arquivo
from automacao_utils.version_check import mostrar_ultima_versao
from automacao_utils.selenium_utils import garantir_iframe
from automacao_utils.notificacao_utils import enviar_msg_teams
```

