#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o carregamento de portas no Mosaicode.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, os.getcwd())

def test_port_loading():
    """Testa o carregamento de portas no sistema."""
    try:
        from mosaicode.system import System
        
        # Inicializar o sistema
        system = System()
        
        # Carregar extensões
        system._System__Singleton__load_extensions(system.instance)
        
        # Obter portas carregadas
        ports = system.get_ports()
        
        print(f"\n=== TESTE DE CARREGAMENTO DE PORTAS ===")
        print(f"Total de portas carregadas: {len(ports)}")
        
        if len(ports) == 0:
            print("ERRO: Nenhuma porta foi carregada!")
            return False
        
        print(f"\nPortas carregadas:")
        for i, (port_type, port) in enumerate(ports.items()):
            print(f"  {i+1}. Tipo: {port_type}")
            print(f"     Hint: {port.hint}")
            print(f"     Color: {port.color}")
            print(f"     Language: {port.language}")
            print()
        
        # Verificar se as portas da extensão javascript-webaudio estão presentes
        webaudio_ports = [p for p in ports.keys() if 'mosaicode_lib_javascript_webaudio' in p]
        print(f"Portas da extensão javascript-webaudio: {len(webaudio_ports)}")
        for port in webaudio_ports:
            print(f"  - {port}")
        
        return True
        
    except Exception as e:
        print(f"ERRO ao testar carregamento de portas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_port_loading()
    sys.exit(0 if success else 1) 