clean:
	rm -rfv *.pyc *.py,cache __pycache__ None *.mscd *.txt

	rm -rfv mosaicode/*.pyc mosaicode/*.py,cache mosaicode/__pycache__ mosaicode/None mosaicode/*.mscd

		rm -rfv mosaicode/control/*.pyc mosaicode/control/*.py,cache mosaicode/control/__pycache__ mosaicode/control/None mosaicode/control/*.mscd

		rm -rfv mosaicode/persistence/*.pyc mosaicode/persistence/*.py,cache mosaicode/persistence/__pycache__

		rm -rfv mosaicode/utils/*.pyc mosaicode/utils/*.py,cache mosaicode/utils/__pycache__

		rm -rfv mosaicode/GUI/*.pyc mosaicode/GUI/*.py,cache mosaicode/GUI/__pycache__

			rm -rfv mosaicode/GUI/fields/*.pyc mosaicode/GUI/fields/*.py,cache mosaicode/GUI/fields/__pycache__

		rm -rfv mosaicode/model/*.pyc mosaicode/model/*.py,cache mosaicode/model/__pycache__

		rm -rfv mosaicode/plugins/*.pyc mosaicode/plugins/*.py,cache mosaicode/plugins/__pycache__

			rm -rfv mosaicode/plugins/extensionsmanager/*.pyc mosaicode/plugins/extensionsmanager/*.py,cache mosaicode/plugins/extensionsmanager/__pycache__

		rm -rfv mosaicode/config/*.pyc mosaicode/config/*.py,cache mosaicode/config/__pycache__

		rm -rfv mosaicode/data/*.pyc mosaicode/data/*.py,cache mosaicode/data/__pycache__

	rm -rfv mosaicode-javascript-webaudio/*.pyc mosaicode-javascript-webaudio/*.py,cache mosaicode-javascript-webaudio/__pycache__

		rm -rfv mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/*.pyc mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/*.py,cache mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/__pycache__

			rm -rfv mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/*.pyc mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/*.py,cache mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/__pycache__

				rm -rfv mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/blocks/*.pyc mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/blocks/*.py,cache mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/blocks/__pycache__

				rm -rfv mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/ports/*.pyc mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/ports/*.py,cache mosaicode-javascript-webaudio/mosaicode_lib_javascript_webaudio/extensions/ports/__pycache__

	rm -rfv *.egg-info
	sudo rm -rfv build dist 2>/dev/null || true
	clear

coverage:
	coverage run --source=mosaicode -m pytest
	coverage report -m
	coverage html

clean_coverage:
	rm -rfv htmlcov
	clear

test_normal:
	python -m pytest

# =============================================================================
# INSTALAÇÃO E DEPENDÊNCIAS
# =============================================================================

# Instalar dependências do sistema (Ubuntu/Debian)
install_system_deps:
	@echo "Instalando dependências do sistema..."
	sudo apt-get update
	sudo apt-get install -y \
		python3-gi \
		python3-cairo \
		python3-gi-cairo \
		gir1.2-gtk-3.0 \
		libgirepository1.0-dev \
		python3-dev \
		build-essential \
		pkg-config \
		python3-pip \
		python3-venv
	@echo "Dependências do sistema instaladas!"

# Instalar dependências Python
install_python_deps:
	@echo "Instalando dependências Python..."
	pip3 install --user --break-system-packages \
		pycairo>=1.20.0 \
		PyGObject>=3.40.0 \
		pgi \
		setuptools>=61.0 \
		wheel
	@echo "Dependências Python instaladas!"

# Verificar se as dependências estão instaladas
check_deps:
	@echo "Verificando dependências..."
	@python3 -c "import gi; print('✓ PyGObject: OK')" || echo "✗ PyGObject: FALHOU"
	@python3 -c "import cairo; print('✓ PyCairo: OK')" || echo "✗ PyCairo: FALHOU"
	@python3 -c "import pgi; print('✓ PGI: OK')" || echo "✗ PGI: FALHOU"
	@echo "Verificação concluída!"

# Instalação completa (dependências + mosaicode)
install_full: install_system_deps install_python_deps install
	@echo "Instalação completa concluída!"
	@echo "Execute 'make check_deps' para verificar se tudo está funcionando."

# Instalação completa global (dependências + mosaicode global)
install_full_global: install_system_deps install_python_deps install_global
	@echo "Instalação completa global concluída!"
	@echo "Execute 'make check_deps' para verificar se tudo está funcionando."

# Instalar mosaicode (usuário)
install:
	pip3 install --user --break-system-packages -e .

# Instalar mosaicode (global)
install_global:
	sudo pip3 install -e .

# Desinstalar mosaicode (usuário)
uninstall:
	pip3 uninstall mosaicode

# Desinstalar mosaicode (global)
uninstall_global:
	sudo pip3 uninstall mosaicode

# =============================================================================
# DESENVOLVIMENTO E TESTES
# =============================================================================

# Criar ambiente virtual
venv:
	python3 -m venv venv
	@echo "Ambiente virtual criado. Ative com: source venv/bin/activate"

# Instalar em ambiente virtual
install_venv: venv
	@echo "Ativando ambiente virtual e instalando..."
	. venv/bin/activate && pip install -e .
	@echo "Instalação no ambiente virtual concluída!"

# Executar mosaicode (desenvolvimento)
run:
	PYTHONPATH=. python3 launcher/mosaicode

# Executar mosaicode (instalado)
run_installed:
	mosaicode

# =============================================================================
# UTILITÁRIOS
# =============================================================================

# Mostrar ajuda
help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "INSTALAÇÃO:"
	@echo "  install_system_deps    - Instalar dependências do sistema"
	@echo "  install_python_deps    - Instalar dependências Python"
	@echo "  install_full          - Instalação completa (usuário)"
	@echo "  install_full_global   - Instalação completa (global)"
	@echo "  install               - Instalar mosaicode (usuário)"
	@echo "  install_global        - Instalar mosaicode (global)"
	@echo "  install_venv          - Instalar em ambiente virtual"
	@echo ""
	@echo "VERIFICAÇÃO:"
	@echo "  check_deps            - Verificar se dependências estão OK"
	@echo ""
	@echo "EXECUÇÃO:"
	@echo "  run                   - Executar mosaicode (desenvolvimento)"
	@echo "  run_installed         - Executar mosaicode (instalado)"
	@echo ""
	@echo "LIMPEZA:"
	@echo "  clean                 - Limpar arquivos temporários"
	@echo "  clean_coverage        - Limpar relatórios de coverage"
	@echo "  uninstall             - Desinstalar mosaicode (usuário)"
	@echo "  uninstall_global      - Desinstalar mosaicode (global)"
	@echo ""
	@echo "TESTES:"
	@echo "  test_normal           - Executar testes"
	@echo "  coverage              - Executar testes com coverage"
