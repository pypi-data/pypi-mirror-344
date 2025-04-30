# Módulo download_utils

Este módulo contém funções para gerenciamento de downloads e tratamento de erros em automações Selenium.

## Classes

### DownloadErroException

Exceção personalizada para erros durante o processo de download.

```python
class DownloadErroException(Exception):
    def __init__(self, mensagem, seletor_erro=None, codigo_erro="DESCONHECIDO", elemento_visivel=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.seletor_erro = seletor_erro
        self.codigo_erro = codigo_erro
        self.elemento_visivel = elemento_visivel
```

**Atributos:**
- `mensagem`: Mensagem detalhada do erro
- `seletor_erro`: Seletor(es) que foram passados como parâmetro na função (pode ser uma lista)
- `codigo_erro`: Código do erro (ex: "ELEMENTO", "TIMEOUT")
- `elemento_visivel`: Seletor específico que estava visível (quando há múltiplos seletores)

## Funções Principais

### processar_download

```python
def processar_download(sb, dir_download, btn_download, nome_arquivo, seletor_carregamento=None,
seletores_erro=None):
```

Processa o download de um arquivo, incluindo clique no botão, aguardo do download e tratamento de erros.

**Parâmetros:**
- `sb`: Instância do SeleniumBase
- `dir_download`: Diretório onde o arquivo será baixado
- `btn_download`: Seletor CSS do botão de download
- `nome_arquivo`: Nome a ser dado ao arquivo
- `seletor_carregamento`: Seletor CSS para indicador de carregamento (opcional)
- `seletores_erro`: Seletor(es) CSS para mensagens de erro (string ou lista)

**Retorno:**
- Caminho completo para o arquivo baixado

### aguardar_download

```python
def aguardar_download(sb, dir_download, handler, observer, seletores_erro=None, tempo_max_espera=180, intervalo=1):
```

Aguarda o download de um arquivo ser concluído e retorna o caminho do arquivo.

**Parâmetros:**
- `sb`: Instância do SeleniumBase
- `dir_download`: Diretório onde o arquivo será baixado
- `handler`: Instância do manipulador de eventos de arquivo
- `observer`: Instância do observador de diretório
- `seletores_erro`: Seletor(es) CSS para mensagens de erro (string ou lista)
- `tempo_max_espera`: Tempo máximo de espera em segundos
- `intervalo`: Intervalo entre verificações em segundos

**Retorno:**
- Caminho completo para o arquivo baixado

**Exceções:**
- `DownloadErroException`: Quando ocorre um erro durante o download
- Exceções genéricas

### aguardar_carregamento

```python
def aguardar_carregamento(sb, seletor):
```

Aguarda até que um elemento de carregamento desapareça ou apareça.

**Parâmetros:**
- `sb`: Instância do SeleniumBase
- `seletor`: Seletor CSS do elemento de carregamento

### renomear_arquivo

```python
def renomear_arquivo(caminho_arquivo, novo_nome):
```

Renomeia um arquivo de forma segura, aguardando caso o arquivo esteja em uso.

**Parâmetros:**
- `caminho_arquivo`: Caminho do arquivo a ser renomeado
- `novo_nome`: Novo nome para o arquivo (sem extensão)

**Retorno:**
- Caminho do arquivo renomeado

## Funções Auxiliares

### is_file_in_use

```python
def is_file_in_use(filepath):
```

Verifica se um arquivo está em uso por outro processo.

**Parâmetros:**
- `filepath`: Caminho do arquivo a verificar

**Retorno:**
- `True` se o arquivo estiver em uso, `False` caso contrário

### wait_for_file_access

```python
def wait_for_file_access(filepath, max_retries=30, retry_interval=1):
```

Aguarda até que um arquivo esteja disponível para acesso.

**Parâmetros:**
- `filepath`: Caminho do arquivo a verificar
- `max_retries`: Número máximo de tentativas
- `retry_interval`: Intervalo entre tentativas em segundos

**Retorno:**
- `True` se o arquivo estiver disponível, `False` se o timeout for atingido

### limpar_nome_arquivo

```python
def limpar_nome_arquivo(nome):
```

Remove caracteres inválidos para nomes de arquivos.

**Parâmetros:**
- `nome`: Nome a ser limpo

**Retorno:**
- Nome limpo, sem caracteres inválidos

## Exemplos de Uso

### Exemplo Básico

```python
from automacao_utils import processar_download

def baixar_relatorio(sb):
    caminho_arquivo = processar_download(
        sb=sb,
        dir_download="C:/Downloads",
        btn_download="#botao_download",
        nome_arquivo="relatorio_mensal"
    )
    
    print(f"Arquivo baixado: {caminho_arquivo}")
    return caminho_arquivo
```

### Exemplo com Tratamento de Erros

```python
from automacao_utils import processar_download, DownloadErroException

def baixar_relatorio(sb):
    try:
        caminho_arquivo = processar_download(
            sb=sb,
            dir_download="C:/Downloads",
            btn_download="#botao_download",
            nome_arquivo="relatorio_mensal",
            seletor_carregamento="#loader",
            seletores_erro=["#mensagem_erro", "#outro_erro"]
        )
        
        print(f"Download concluído com sucesso: {caminho_arquivo}")
        return caminho_arquivo
        
    except DownloadErroException as e:
        if e.codigo_erro == "ELEMENTO":
            print(f"Erro: Elemento de erro detectado: {e.mensagem}")
            
            # Identifica qual elemento específico foi encontrado
            if e.elemento_visivel == "#mensagem_erro":
                print("Erro de validação detectado")
            elif e.elemento_visivel == "#outro_erro":
                print("Outro tipo de erro encontrado")
        else:
            print(f"Erro desconhecido: {e.mensagem}")
        
        return None
```
