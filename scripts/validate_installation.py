#!/usr/bin/env python3
"""
Script de validação para instalação do Mosaicode.
Executa testes básicos para garantir que a instalação foi bem-sucedida.
"""
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """Executa um comando e retorna o resultado."""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0:
            return True, f"[OK] {description}: OK"
        else:
            return False, f"[ERRO] {description}: FALHOU\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"[TIMEOUT] {description}: TIMEOUT"
    except Exception as e:
        return False, f"[ERRO] {description}: ERRO - {e}"


def validate_python_imports() -> List[Tuple[bool, str]]:
    """Valida se os módulos principais podem ser importados."""
    results = []
    
    modules_to_test = [
        ("mosaicode.system", "Importação do módulo System"),
        ("mosaicode.model.blockmodel", "Importação do modelo BlockModel"),
        ("mosaicode.model.port", "Importação do modelo Port"),
        ("mosaicode.utils.config_loader", "Importação do ConfigLoader"),
        ("mosaicode.utils.logger", "Importação do sistema de logging"),
    ]
    
    for module, description in modules_to_test:
        try:
            __import__(module)
            results.append((True, f"[OK] {description}: OK"))
        except ImportError as e:
            results.append((False, f"[ERRO] {description}: FALHOU - {e}"))
        except Exception as e:
            results.append((False, f"[ERRO] {description}: ERRO - {e}"))
    
    return results


def validate_config_files() -> List[Tuple[bool, str]]:
    """Valida se os arquivos de configuração estão corretos."""
    results = []
    
    try:
        from mosaicode.utils.pydantic_schemas import PydanticValidator
        from mosaicode.utils.config_loader import ConfigLoader
        
        # Obter o diretório do projeto
        project_dir = Path(__file__).parent.parent
        config_dir = project_dir / "mosaicode" / "config"
        
        # Validar configurações principais
        configs_to_test = ["system", "preferences"]
        
        for config_name in configs_to_test:
            try:
                config_data = ConfigLoader.load_config(config_name, config_dir=config_dir)
                if not config_data:
                    results.append((False, f"[ERRO] {config_name}.json: ARQUIVO NÃO ENCONTRADO OU VAZIO"))
                    continue
                
                if config_name == "system":
                    result = PydanticValidator.validate_system_config(config_data)
                elif config_name == "preferences":
                    result = PydanticValidator.validate_preferences(config_data)
                else:
                    continue
                
                if result.success:
                    results.append((True, f"[OK] Validação de {config_name}.json: OK"))
                else:
                    results.append((False, f"[ERRO] Validação de {config_name}.json: FALHOU - {', '.join(result.errors)}"))
            except Exception as e:
                results.append((False, f"[ERRO] Validação de {config_name}.json: ERRO - {e}"))
        
        # Validar templates
        templates_dir = project_dir / "mosaicode" / "templates"
        templates_to_test = [("defaults", "blocks"), ("defaults", "ports")]
        
        for template_name, template_type in templates_to_test:
            try:
                # Mock temporário do System.get_user_dir para usar o diretório do projeto
                import mosaicode.system
                original_get_user_dir = mosaicode.system.System.get_user_dir
                
                def mock_get_user_dir():
                    return project_dir
                
                mosaicode.system.System.get_user_dir = mock_get_user_dir
                
                try:
                    template_data = ConfigLoader.load_template(template_name, template_type)
                    if not template_data:
                        results.append((False, f"[ERRO] Template {template_type}: ARQUIVO NÃO ENCONTRADO OU VAZIO"))
                        continue
                    
                    if template_type == "blocks":
                        result = PydanticValidator.validate_block_defaults(template_data)
                    elif template_type == "ports":
                        result = PydanticValidator.validate_port_defaults(template_data)
                    else:
                        continue
                    
                    if result.success:
                        results.append((True, f"[OK] Validação de template {template_type}: OK"))
                    else:
                        results.append((False, f"[ERRO] Validação de template {template_type}: FALHOU - {', '.join(result.errors)}"))
                finally:
                    mosaicode.system.System.get_user_dir = original_get_user_dir
                    
            except Exception as e:
                results.append((False, f"[ERRO] Validação de template {template_type}: ERRO - {e}"))
        
    except Exception as e:
        results.append((False, f"[ERRO] Validação de configurações: ERRO GERAL - {e}"))
    
    return results


def run_basic_tests() -> List[Tuple[bool, str]]:
    """Executa testes básicos de funcionalidade."""
    results = []
    
    # Teste de logger
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_logger.py", "-v", "--tb=short"],
        "Teste do sistema de logging"
    ))
    
    # Teste de fileutils
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_fileutils.py", "-v", "--tb=short"],
        "Teste de utilitários de arquivo"
    ))
    
    # Teste do sistema
    results.append(run_command(
        [sys.executable, "-m", "pytest", "tests/test_system.py", "-v", "--tb=short"],
        "Teste do módulo System"
    ))
    
    return results


def main():
    """Função principal de validação."""
    print("Iniciando validação da instalação do Mosaicode...")
    print("=" * 60)
    
    all_results = []
    
    # 1. Validar imports
    print("\nValidando importações de módulos...")
    import_results = validate_python_imports()
    all_results.extend(import_results)
    for success, message in import_results:
        print(f"  {message}")
    
    # 2. Validar arquivos de configuração
    print("\nValidando arquivos de configuração...")
    config_results = validate_config_files()
    all_results.extend(config_results)
    for success, message in config_results:
        print(f"  {message}")
    
    # 3. Executar testes básicos
    print("\nExecutando testes básicos...")
    test_results = run_basic_tests()
    all_results.extend(test_results)
    for success, message in test_results:
        print(f"  {message}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA VALIDAÇÃO:")
    
    total_tests = len(all_results)
    passed_tests = sum(1 for success, _ in all_results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"  Total de verificações: {total_tests}")
    print(f"  [OK] Passaram: {passed_tests}")
    print(f"  [ERRO] Falharam: {failed_tests}")
    
    if failed_tests == 0:
        print("\nVALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("O Mosaicode foi instalado corretamente.")
        return 0
    else:
        print("\nVALIDAÇÃO CONCLUÍDA COM PROBLEMAS!")
        print("Alguns testes falharam. Verifique os erros acima.")
        print("\nDicas para resolver problemas:")
        print("  - Verifique se todas as dependências estão instaladas")
        print("  - Execute 'make test_validation' para mais detalhes")
        print("  - Consulte a documentação de instalação")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 