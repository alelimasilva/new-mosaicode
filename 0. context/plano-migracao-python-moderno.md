# 📋 Plano de Migração - Mosaicode para Python Moderno

## 🎯 Objetivo
Modernizar a aplicação Mosaicode para usar as melhores práticas do Python moderno, incluindo type hints, dataclasses, pathlib, logging estruturado e outras funcionalidades do Python 3.9+.

## 📊 Visão Geral
- **Duração Total**: 14 semanas
- **Fases**: 8 fases principais
- **Python Target**: 3.9+
- **Principais Melhorias**: Type safety, performance, legibilidade, manutenibilidade
- **Migração de Dados**: Conversão de arquivos .py para .json onde apropriado

---

## 🚀 Fase 1: Preparação e Análise (Semana 1)

### 1.1 Análise Completa do Código
- [ ] Mapear todas as classes que herdam de `object`
- [ ] Identificar todos os `print()` statements
- [ ] Localizar todos os `except:` genéricos
- [ ] Mapear uso de `os.path` vs `pathlib`
- [ ] Identificar dependências desatualizadas

### 1.2 Configuração do Ambiente
- [ ] Criar ambiente virtual com Python 3.9+
- [ ] Atualizar `setup.py` com dependências modernas
- [ ] Configurar ferramentas de linting (mypy, black, flake8)
- [ ] Configurar testes automatizados

### 1.3 Inventário de Arquivos
- [ ] Listar todos os arquivos Python que precisam ser modernizados
- [ ] Priorizar arquivos por impacto e dependências
- [ ] Criar mapa de dependências entre módulos
- [ ] Identificar arquivos .py que podem ser convertidos para .json

**Como posso ajudar:**
- Analisar todos os arquivos Python para criar um inventário completo
- Identificar padrões de código que precisam ser modernizados
- Criar scripts de análise automatizada
- Identificar arquivos de configuração que podem ser migrados para JSON

---

## 🔧 Fase 2: Modernização Básica (Semanas 2-3)

### 2.1 Atualização de Sintaxe
- [ ] Remover herança de `object` em classes
- [ ] Converter `print()` para logging
- [ ] Substituir `os.path` por `pathlib`
- [ ] Implementar f-strings
- [ ] Usar context managers para arquivos

### 2.2 Melhoria de Imports
- [ ] Organizar imports (stdlib, third-party, local)
- [ ] Usar imports absolutos em vez de relativos
- [ ] Adicionar `__future__` imports quando necessário

### 2.3 Exemplos de Mudanças

#### Antes:
```python
class System(object):
    def __init__(self):
        self.instance = None
    
    def get_user_dir(self):
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, self.APP)
    
    def log(self, msg):
        print("Error: " + msg)
```

#### Depois:
```python
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class System:
    def __init__(self):
        self.instance = None
    
    def get_user_dir(self) -> Path:
        return Path.home() / self.APP
    
    def log(self, msg: str) -> None:
        logger.error(f"Error: {msg}")
```

**Como posso ajudar:**
- Criar scripts de refatoração automatizada
- Implementar as mudanças arquivo por arquivo
- Validar que as mudanças não quebram funcionalidade

---

## 📁 Fase 3: Migração de Dados (Semanas 4-5)

### 3.1 Migração de Arquivos .py para .json
- [ ] Identificar arquivos Python que contêm apenas dados de configuração
- [ ] Converter `mosaicode/model/preferences.py` para JSON
- [ ] Migrar constantes do `mosaicode/system.py` para JSON
- [ ] Converter configurações hardcoded em modelos para JSON
- [ ] Criar sistema de carregamento dinâmico de configurações

### 3.2 Migração XML para JSON
- [ ] Converter arquivos XML restantes para JSON
- [ ] Migrar templates de blocos de XML para JSON
- [ ] Converter code templates de XML para JSON
- [ ] Implementar sistema de validação para JSON

### 3.3 Exemplos de Migração .py → .json

#### Arquivo Python Original (`preferences.py`):
```python
class Preferences(object):
    def __init__(self):
        self.author = ""
        self.license = "GPL 3.0"
        self.version = System.VERSION
        self.recent_files = []
        self.grid = 10
        self.width = 900
        self.height = 500
```

#### Arquivo JSON Resultante (`preferences.json`):
```json
{
  "author": "",
  "license": "GPL 3.0",
  "version": "0.0.1",
  "recent_files": [],
  "grid": 10,
  "width": 900,
  "height": 500,
  "default_directory": "~/mosaicode/code-gen",
  "default_filename": "%n",
  "connection": "Curve"
}
```

#### Sistema de Carregamento:
```python
from pathlib import Path
import json
from typing import Dict, Any

class ConfigLoader:
    @staticmethod
    def load_config(config_name: str) -> Dict[str, Any]:
        config_path = Path.home() / "mosaicode" / f"{config_name}.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
```

**Como posso ajudar:**
- Identificar e converter arquivos .py para .json
- Criar scripts de migração automatizada
- Implementar sistema de configuração robusto
- Migrar dados XML para JSON

---

## 🎯 Fase 4: Type Hints (Semanas 6-7)

### 4.1 Implementação Gradual
- [ ] Adicionar type hints em modelos de dados
- [ ] Tipar métodos de persistência
- [ ] Tipar controladores
- [ ] Tipar componentes GUI

### 4.2 Configuração de Ferramentas
- [ ] Configurar mypy
- [ ] Adicionar stubs para bibliotecas externas
- [ ] Criar configuração de type checking

### 4.3 Exemplos de Type Hints

#### Antes:
```python
def get_blocks(self):
    return copy(self.__blocks)

def load_block(self, file_name):
    block = BlockModel()
    return block
```

#### Depois:
```python
from typing import Dict, Optional
from copy import copy

def get_blocks(self) -> Dict[str, BlockModel]:
    return copy(self.__blocks)

def load_block(self, file_name: str) -> Optional[BlockModel]:
    block = BlockModel()
    return block
```

**Como posso ajudar:**
- Analisar cada classe para determinar tipos corretos
- Implementar type hints de forma incremental
- Criar stubs para bibliotecas que não têm type hints

---

## 📦 Fase 5: Dataclasses e Estruturas Modernas (Semanas 8-9)

### 5.1 Conversão de Modelos
- [ ] Converter `Preferences` para dataclass
- [ ] Converter `BlockModel` para dataclass
- [ ] Converter `Port` para dataclass
- [ ] Converter `CodeTemplate` para dataclass

### 5.2 Enums e Constantes
- [ ] Criar enums para valores constantes
- [ ] Substituir constantes por enums
- [ ] Implementar configurações baseadas em dataclasses

### 5.3 Exemplos de Dataclasses

#### Antes:
```python
class Preferences(object):
    def __init__(self):
        self.author = ""
        self.license = "GPL 3.0"
        self.version = System.VERSION
        self.recent_files = []
        self.grid = 10
        self.width = 900
        self.height = 500
```

#### Depois:
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Preferences:
    author: str = ""
    license: str = "GPL 3.0"
    version: str = field(default_factory=lambda: System.VERSION)
    recent_files: List[str] = field(default_factory=list)
    grid: int = 10
    width: int = 900
    height: int = 500
```

**Como posso ajudar:**
- Analisar cada modelo para determinar estrutura ideal
- Implementar dataclasses com validação
- Criar enums apropriados para cada contexto

---

## 🛡️ Fase 6: Tratamento de Erros Moderno (Semana 10)

### 6.1 Exceptions Específicas
- [ ] Criar hierarquia de exceptions customizadas
- [ ] Substituir `except:` por exceptions específicas
- [ ] Implementar logging estruturado

### 6.2 Logging Adequado
- [ ] Configurar logging centralizado
- [ ] Implementar diferentes níveis de log
- [ ] Adicionar contexto aos logs

### 6.3 Exemplos de Exceptions Customizadas

```python
class MosaicodeError(Exception):
    """Base exception for Mosaicode application."""
    pass

class BlockLoadError(MosaicodeError):
    """Raised when a block fails to load."""
    pass

class ConfigurationError(MosaicodeError):
    """Raised when configuration is invalid."""
    pass
```

**Como posso ajudar:**
- Criar hierarquia de exceptions apropriada
- Implementar sistema de logging robusto
- Adicionar tratamento de erro específico

---

## ⚙️ Fase 7: Validação e Configuração Avançada (Semana 11)

### 7.1 Validação de Dados
- [ ] Implementar Pydantic para validação
- [ ] Criar schemas para todos os modelos
- [ ] Adicionar validação em tempo de execução

### 7.2 Exemplo de Configuração com Pydantic

```python
from pydantic import BaseModel, Field
from typing import Dict, List

class SystemConfig(BaseModel):
    app_name: str = "mosaicode"
    version: str = "0.0.1"
    zoom_levels: Dict[str, int] = Field(default_factory=lambda: {
        "original": 1,
        "in": 2,
        "out": 3
    })

class Preferences(BaseModel):
    author: str = ""
    license: str = "GPL 3.0"
    grid: int = Field(ge=1, le=100)
    width: int = Field(ge=100, le=3000)
    height: int = Field(ge=100, le=3000)
```

**Como posso ajudar:**
- Criar schemas Pydantic para todos os modelos
- Implementar sistema de configuração robusto
- Adicionar validação em tempo de execução

---

## ⚡ Fase 8: Otimizações e Performance (Semanas 12-13)

### 8.1 Caching e Performance
- [ ] Implementar `@cached_property`
- [ ] Usar `@lru_cache` para funções custosas
- [ ] Otimizar carregamento de extensões

### 8.2 Async/Await (Opcional)
- [ ] Identificar operações I/O que podem ser async
- [ ] Implementar async para operações de arquivo
- [ ] Adicionar suporte a async em controladores

### 8.3 Exemplos de Otimizações

```python
from functools import cached_property, lru_cache

class System:
    @cached_property
    def blocks(self) -> Dict[str, BlockModel]:
        return self._load_blocks()
    
    @lru_cache(maxsize=128)
    def get_user_dir(self) -> Path:
        return Path.home() / self.APP
```

**Como posso ajudar:**
- Identificar gargalos de performance
- Implementar otimizações apropriadas
- Criar versões async quando necessário

---

## 🧪 Fase 9: Testes e Documentação (Semana 14)

### 9.1 Testes Modernos
- [ ] Atualizar testes para usar fixtures modernas
- [ ] Adicionar testes de type checking
- [ ] Implementar testes de integração

### 9.2 Documentação
- [ ] Atualizar docstrings com type hints
- [ ] Criar documentação de migração
- [ ] Documentar novas funcionalidades

### 9.3 Exemplo de Teste Moderno

```python
import pytest
from pathlib import Path
from typing import Dict

@pytest.fixture
def sample_blocks() -> Dict[str, BlockModel]:
    return {
        "test_block": BlockModel(
            type="test",
            label="Test Block",
            color="#FF0000"
        )
    }

def test_block_loading(sample_blocks: Dict[str, BlockModel]):
    assert len(sample_blocks) == 1
    assert sample_blocks["test_block"].label == "Test Block"
```

**Como posso ajudar:**
- Atualizar testes existentes
- Criar novos testes para funcionalidades modernas
- Gerar documentação atualizada

---

## 🛠️ Ferramentas e Configurações

### Ferramentas de Desenvolvimento
- **mypy**: Type checking
- **black**: Formatação de código
- **flake8**: Linting
- **pytest**: Testes
- **pre-commit**: Hooks de qualidade

### Configuração de mypy
```ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### Configuração de black
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
```

---

## 📊 Métricas de Progresso

### Indicadores de Sucesso
- [ ] 0 classes herdando de `object`
- [ ] 0 `print()` statements
- [ ] 0 `except:` genéricos
- [ ] 100% type coverage
- [ ] 0 warnings do mypy
- [ ] 0 warnings do flake8
- [ ] Configurações migradas para JSON
- [ ] 0 arquivos XML restantes (todos migrados para JSON)

### Ferramentas de Validação
- mypy para type checking
- black para formatação
- flake8 para linting
- pytest para testes

---

## 🚀 Como Posso Ajudar

### Ferramentas Disponíveis
1. **Análise de Código:**
   - Busca semântica no codebase
   - Busca por padrões específicos
   - Leitura e análise de arquivos

2. **Refatoração Automatizada:**
   - Edição de arquivos
   - Substituições em massa
   - Execução de scripts

3. **Validação:**
   - Execução de testes
   - Análise de erros de linting
   - Verificação de type hints

### Exemplo de Ajuda na Fase 2
```python
# Script para modernizar sintaxe básica
def modernize_basic_syntax():
    # 1. Remover herança de object
    # 2. Converter print para logging
    # 3. Substituir os.path por pathlib
    # 4. Implementar f-strings
    pass
```

### Exemplo de Ajuda na Fase 4
```python
# Análise e adição de type hints
def add_type_hints_to_file(file_path: str):
    # 1. Analisar estrutura da classe
    # 2. Determinar tipos apropriados
    # 3. Implementar type hints
    # 4. Validar com mypy
    pass
```

---

## 📅 Cronograma Detalhado

| Semana | Fase | Principais Tarefas | Entregáveis |
|--------|------|-------------------|-------------|
| 1 | Preparação | Análise, configuração | Inventário completo |
| 2-3 | Modernização Básica | Sintaxe, imports | Código modernizado |
| 4-5 | Migração de Dados | .py → .json, XML → JSON | Dados estruturados |
| 6-7 | Type Hints | Tipagem gradual | Type safety |
| 8-9 | Dataclasses | Estruturas modernas | Modelos otimizados |
| 10 | Tratamento de Erros | Exceptions, logging | Sistema robusto |
| 11 | Validação | Pydantic, schemas | Validação robusta |
| 12-13 | Performance | Caching, async | Otimizações |
| 14 | Testes | Validação, docs | Qualidade garantida |

---

## 🎯 Próximos Passos Imediatos

1. **Análise completa do código atual**
2. **Criação de scripts de refatoração**
3. **Implementação da Fase 1**
4. **Configuração de ferramentas de desenvolvimento**

---

## 📁 Arquivos que Podem Ser Convertidos de .py para .json

### Arquivos de Configuração
- **`mosaicode/model/preferences.py`** → `config/preferences.json`
  - Contém configurações padrão do usuário
  - Valores hardcoded que podem ser externalizados

- **Constantes do `mosaicode/system.py`** → `config/system.json`
  - `VERSION`, `APP`, `ZOOM_ORIGINAL`, `ZOOM_IN`, `ZOOM_OUT`
  - Configurações do sistema que não mudam frequentemente

### Arquivos de Dados Estáticos
- **`mosaicode/model/blockmodel.py` (valores padrão)** → `templates/blocks/defaults.json`
  - Valores padrão de blocos (cores, grupos, etc.)
  - Configurações que podem ser customizadas

- **`mosaicode/model/port.py` (configurações)** → `templates/ports/defaults.json`
  - Configurações padrão de portas
  - Tipos de conexão disponíveis

### Arquivos de Templates
- **Templates de código hardcoded** → `templates/code/`
  - Códigos de exemplo
  - Templates de geração de código

### Vantagens da Conversão
1. **Flexibilidade**: Mudanças sem recompilação
2. **Manutenibilidade**: Configurações centralizadas
3. **Legibilidade**: JSON é mais fácil de ler
4. **Separação**: Dados separados da lógica
5. **Internacionalização**: Textos externalizados

### Estrutura de Diretórios Proposta
```
mosaicode/
├── config/
│   ├── preferences.json
│   ├── system.json
│   └── defaults.json
├── templates/
│   ├── blocks/
│   ├── ports/
│   └── code/
└── data/
    ├── blocks/
    ├── ports/
    └── codetemplates/
```

## 📝 Notas Importantes

- Cada fase deve ser testada antes de prosseguir
- Manter compatibilidade com funcionalidades existentes
- Documentar todas as mudanças
- Criar rollback plan para cada fase
- Manter comunicação com a equipe sobre progresso
- **Migração gradual**: Converter um arquivo por vez e testar
- **Backup**: Manter versões Python como fallback
- **Validação**: Usar Pydantic para validar JSONs

---

*Este plano foi criado para modernizar a aplicação Mosaicode seguindo as melhores práticas do Python moderno, garantindo type safety, performance e manutenibilidade.* 