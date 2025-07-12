# 📊 Relatório de Análise - Modernização Mosaicode

**Arquivos analisados**: 87

## 🏗️ Classes que Herdam de `object`
**Total**: 9

- `mosaicode/system.py`
  - Linha 22: `class System(object):`
- `mosaicode/model/authormodel.py`
  - Linha 3: `class AuthorModel(object):`
- `mosaicode/model/codetemplate.py`
  - Linha 4: `class CodeTemplate(object):`
- `mosaicode/model/connectionmodel.py`
  - Linha 5: `class ConnectionModel(object):`
- `mosaicode/model/port.py`
  - Linha 4: `class Port(object):`
- `mosaicode/model/blockmodel.py`
  - Linha 4: `class BlockModel(object):`
- `mosaicode/model/preferences.py`
  - Linha 5: `class Preferences(object):`
- `mosaicode/model/commentmodel.py`
  - Linha 6: `class CommentModel(object):`
- `mosaicode/model/diagrammodel.py`
  - Linha 3: `class DiagramModel(object):`

## 🖨️ Statements `print()`
**Total**: 3

- `0. context/analise-automatizada.py`
  - Linha 38: `print(f"Erro ao ler {file_path}: {e}")`
  - Linha 93: `print("🔍 Iniciando análise do projeto...")`
  - Linha 97: `print(f"📁 Encontrados {len(python_files)} arquivos Python")`
  - Linha 154: `report.append("## 🖨️ Statements `print()`")`
  - Linha 194: `print("🚀 Iniciando análise automatizada do Mosaicode...")`
  - Linha 209: `print("✅ Análise concluída!")`
  - Linha 210: `print(f"📊 Arquivos analisados: {results['files_analyzed']}")`
  - Linha 211: `print(f"🏗️ Classes object: {len(results['classes_object'])}")`
  - Linha 212: `print(f"🖨️ Print statements: {len(results['print_statements'])}")`
  - Linha 213: `print(f"⚠️ Exceptions genéricas: {len(results['generic_exceptions'])}")`
  - Linha 214: `print(f"📂 Usos de os.path: {len(results['os_path_usage'])}")`
  - Linha 215: `print("📄 Relatórios salvos em '0. context/'")`
- `mosaicode/system.py`
  - Linha 207: `print("Error in loading block " + key)`
  - Linha 284: `print("Could not set logger")`
  - Linha 293: `print(msg)`
- `mosaicode/persistence/codetemplatepersistence.py`
  - Linha 68: `print(e)`

## ⚠️ Exceptions Genéricas (`except:`)
**Total**: 12

- `0. context/analise-automatizada.py`
  - Linha 164: `report.append("## ⚠️ Exceptions Genéricas (`except:`)")`
- `mosaicode/system.py`
  - Linha 77: `except:`
  - Linha 206: `except:`
  - Linha 283: `except:`
  - Linha 292: `except:`
- `mosaicode/persistence/persistence.py`
  - Linha 32: `except:`
- `mosaicode/persistence/preferencespersistence.py`
  - Linha 63: `except:`
- `mosaicode/persistence/blockpersistence.py`
  - Linha 67: `except:`
- `mosaicode/persistence/portpersistence.py`
  - Linha 55: `except:`
- `mosaicode/plugins/extensionsmanager/codetemplatecodeeditor.py`
  - Linha 202: `except:`
  - Linha 210: `except:`
- `mosaicode/plugins/extensionsmanager/blockcodeeditor.py`
  - Linha 211: `except:`
  - Linha 219: `except:`
- `mosaicode/plugins/extensionsmanager/propertyeditor.py`
  - Linha 171: `except:`
- `mosaicode/plugins/extensionsmanager/blockporteditor.py`
  - Linha 183: `except:`
- `mosaicode/GUI/fields/floatfield.py`
  - Linha 45: `except:`
- `mosaicode/GUI/fields/colorfield.py`
  - Linha 70: `except:`

## 📂 Uso de `os.path`
**Total**: 17

- `mosaicode/system.py`
  - Linha 54: `path = os.path.join(System.get_user_dir(), name)`
  - Linha 55: `if not os.path.isdir(path):`
  - Linha 97: `extension_path = os.path.join(System.get_user_dir(),"extensions")`
  - Linha 99: `path = os.path.join(extension_path, language)`
  - Linha 100: `path = os.path.join(path, "examples")`
  - Linha 102: `file_path = os.path.join(path, filename)`
  - Linha 159: `if not os.path.exists(data_dir):`
  - Linha 163: `lang_path = os.path.join(data_dir, languages)`
  - Linha 166: `for file_name in os.listdir(os.path.join(lang_path, "codetemplates")):`
  - Linha 169: `file_path = os.path.join(lang_path,"codetemplates")`
  - Linha 170: `file_path = os.path.join(file_path, file_name)`
  - Linha 177: `for file_name in os.listdir(os.path.join(lang_path,"ports")):`
  - Linha 180: `file_path = os.path.join(lang_path,"ports")`
  - Linha 181: `file_path = os.path.join(file_path, file_name)`
  - Linha 188: `for extension_name in os.listdir(os.path.join(lang_path,"blocks")):`
  - Linha 189: `extension_path = os.path.join(lang_path, "blocks")`
  - Linha 190: `extension_path = os.path.join(extension_path, extension_name)`
  - Linha 192: `group_path = os.path.join(extension_path, group_name)`
  - Linha 196: `file_path = os.path.join(group_path, file_name)`
  - Linha 298: `home_dir = os.path.expanduser("~")`
  - Linha 299: `return os.path.join(home_dir, System.APP)`
- `docs/source/conf.py`
  - Linha 20: `# documentation root, use os.path.abspath to make it absolute, like shown here.`
  - Linha 21: `sys.path.insert(0, os.path.abspath('../..'))`
- `docs/source/_themes/sphinx_rtd_theme/__init__.py`
  - Linha 14: `cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))`
- `mosaicode/persistence/persistence.py`
  - Linha 26: `if os.path.isdir(path):`
- `mosaicode/persistence/preferencespersistence.py`
  - Linha 28: `file_name = os.path.expanduser(file_name)`
  - Linha 29: `if os.path.exists(file_name) is False:`
  - Linha 34: `if os.path.exists(file_name) is False:`
- `mosaicode/persistence/diagrampersistence.py`
  - Linha 32: `if os.path.exists(diagram.file_name) is False:`
- `mosaicode/persistence/blockpersistence.py`
  - Linha 30: `if os.path.exists(file_name) is False:`
  - Linha 129: `path = os.path.join(path, file_name + '.json')`
- `mosaicode/persistence/portpersistence.py`
  - Linha 31: `if os.path.exists(file_name) is False:`
  - Linha 89: `data_file = open(os.path.join(path, port.type + '.json'), 'w')`
- `mosaicode/persistence/codetemplatepersistence.py`
  - Linha 32: `if os.path.exists(file_name) is False:`
  - Linha 34: `if os.path and os.path.isdir(file_name):`
  - Linha 113: `data_file = open(os.path.join(path, file_name + '.json'), 'w')`
- `mosaicode/utils/FileUtils.py`
  - Linha 11: `directory = os.path.dirname(os.path.realpath('__file__'))`
  - Linha 12: `filename = os.path.join(directory, filename)`
  - Linha 13: `filename = os.path.abspath(os.path.realpath(filename))`
- `mosaicode/control/blockcontrol.py`
  - Linha 88: `path = os.path.join(System.get_user_dir(),"extensions")`
  - Linha 89: `path = os.path.join(path, block.language)`
  - Linha 90: `path = os.path.join(path, "blocks")`
  - Linha 91: `path = os.path.join(path, block.extension)`
  - Linha 92: `path = os.path.join(path, block.group)`
- `mosaicode/control/codetemplatecontrol.py`
  - Linha 36: `path = os.path.join(System.get_user_dir(), "extensions")`
  - Linha 37: `path = os.path.join(path, code_template.language)`
  - Linha 38: `path = os.path.join(path, "codetemplates")`
- `mosaicode/control/diagramcontrol.py`
  - Linha 303: `if not os.path.exists(self.diagram.file_name):`
- `mosaicode/control/maincontrol.py`
  - Linha 139: `if os.path.exists(name) is True:`
  - Linha 186: `if name is not None and os.path.exists(name) is True:`
  - Linha 662: `path = os.path.join(path, folder, ports[key].language, 'ports')`
  - Linha 669: `path = os.path.join(path,`
  - Linha 681: `path = os.path.join(path,`
  - Linha 689: `path = os.path.join(path, "extensions")`
  - Linha 692: `relpath = os.path.relpath(example, path)`
  - Linha 694: `path = os.path.join(path, folder, relpath)`
  - Linha 695: `os.makedirs(os.path.dirname(path), exist_ok=True)`
  - Linha 700: `path = os.path.join(path, folder+".zip")`
  - Linha 704: `path = os.path.join(path, folder)`
  - Linha 708: `filePath = os.path.join(folderName, filename)`
  - Linha 711: `zip_file.write(filePath, os.path.relpath(filePath, path))`
  - Linha 715: `path = os.path.join(path, folder)`
  - Linha 721: `path = os.path.join(path, filename)`
  - Linha 747: `file_path = os.path.join(System.get_user_dir(), file_name)`
  - Linha 751: `destination = os.path.join(System.get_user_dir(), "extensions")`
- `mosaicode/control/portcontrol.py`
  - Linha 42: `path = os.path.join(System.get_user_dir(), "extensions")`
  - Linha 43: `path = os.path.join(path, port.language, "ports")`
- `mosaicode/model/preferences.py`
  - Linha 22: `self.default_directory = os.path.join(System.get_user_dir(), "code-gen")`
- `mosaicode/GUI/fields/openfilefield.py`
  - Linha 65: `if os.path.isdir(self.field.get_text()):`
  - Linha 68: `current_dir = os.path.dirname(self.field.get_text())`
