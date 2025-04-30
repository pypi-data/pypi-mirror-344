# Módulo mover_arquivo_utils

Este módulo fornece uma função para mover arquivos entre diretórios com opções avançadas de controle, incluindo substituição, renomeação automática e limitação de quantidade.

## Funções Disponíveis

### `mover_arquivo(diretorio_origem, diretorio_destino, nome_arquivo=None, substituir=True, max_arquivos=10)`

Move um ou mais arquivos de uma origem para um destino, verificando existência, cuidando de substituições e controlando a quantidade.

**Parâmetros:**
- `diretorio_origem`: Caminho completo do arquivo a ser movido ou diretório de origem.
- `diretorio_destino`: Caminho do diretório de destino.
- `nome_arquivo`: Nome específico do arquivo a ser movido (opcional).
  - Se None e diretorio_origem for um arquivo, usa o nome do arquivo no caminho.
  - Se None e diretorio_origem for um diretório, move todos os arquivos do diretório.
- `substituir`: Se True (padrão), substitui o arquivo de destino caso já exista um com o mesmo nome.
  - Se False, adiciona um contador no nome do arquivo caso já exista.
- `max_arquivos`: Número máximo de arquivos que podem ser movidos em uma única operação (padrão: 10).
  - Se for mover mais arquivos que este limite, será solicitada uma confirmação.

**Retorno:**
- Lista de caminhos dos arquivos no diretório de destino.

**Comportamento:**
1. Verifica se a origem é um arquivo ou diretório
2. Identifica os arquivos a serem movidos
3. Verifica se o destino já possui arquivos com os mesmos nomes e trata conforme parâmetro `substituir`
4. Confirma com o usuário caso a quantidade de arquivos exceda o limite
5. Cria o diretório de destino se não existir
6. Copia os arquivos para o destino e remove os originais
7. Retorna a lista de caminhos dos arquivos movidos

**Exemplo:**
```python
from automacao_utils.mover_arquivo_utils import mover_arquivo

# Mover um arquivo específico
arquivos_movidos = mover_arquivo(
    diretorio_origem="C:/Downloads/documento.pdf",
    diretorio_destino="C:/Documentos/Importantes"
)

# Mover todos os arquivos de um diretório (com renomeação automática se já existirem)
arquivos_movidos = mover_arquivo(
    diretorio_origem="C:/Downloads/Relatórios",
    diretorio_destino="C:/Trabalho/Relatórios",
    substituir=False
)

# Mover um arquivo específico de um diretório com novo nome
arquivos_movidos = mover_arquivo(
    diretorio_origem="C:/Downloads",
    diretorio_destino="C:/Documentos",
    nome_arquivo="relatório.xlsx"
)
```

## Notas de Uso

- A função trata exceções e fornece mensagens de erro detalhadas para facilitar o diagnóstico de problemas.
- O parâmetro `max_arquivos` é uma proteção para evitar mover inadvertidamente grandes quantidades de arquivos.
- A função preserva os metadados dos arquivos (como data de modificação) ao movê-los.
- **Se o diretório de destino não existir, ele será criado automaticamente.**

## Exceções

- `FileNotFoundError`: Se o arquivo de origem não existir.
- `PermissionError`: Se não houver permissão para mover o arquivo.
- `IOError`: Se houver um erro ao mover o arquivo.
