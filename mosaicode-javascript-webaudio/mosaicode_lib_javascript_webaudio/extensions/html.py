# -*- coding: utf-8 -*-
# [MOSAICODE PROJECT]
#
"""
This module contains the JavascriptTemplate class.
"""
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.GUI.fieldtypes import *

class Html(CodeTemplate):
    """
    This class contains methods related the JavascriptTemplate class.
    """
    # ----------------------------------------------------------------------

    def __init__(self):
        CodeTemplate.__init__(self)
        self.name = "webaudio"
        self.language = "javascript"
        self.command = "python -m webbrowser -t $dir_name$index.html\n"
        self.description = "Javascript / webaudio code template"

        self.code_parts = ["onload", "function", "declaration", "execution", "html"]
        self.properties = [{"name": "title",
                            "label": "Title",
                            "value": "Title",
                            "type": MOSAICODE_STRING
                            }
                           ]

        self.files["index.html"] = r"""
<html>
    <head>
        <meta http-equiv="Cache-Control" content="no-store" />
        <!-- $author$ $license$ -->
        <title>$prop[title]$</title>
        <link rel="stylesheet" type="text/css" href="theme.css">
        <script src="functions.js"></script>
        <script>
        $single_code[function]$
        function loadme(){
        $single_code[onload]$
        return;
        }
        var context = new (window.AudioContext || window.webkitAudioContext)();
        //declaration block
        $code[declaration]$

        //execution
        $code[execution]$

        //connections
        $connections$
        </script>
    </head>

    <body onload='loadme();'>
        $code[html]$
    </body>
</html>
"""

        self.files["theme.css"] = r"""
/*
Developed by: $author$
*/
html, body {
  background: #ffeead;
  color: #ff6f69;
}
h1, p {
  color: #ff6f69;
}
#navbar a {
  color: #ff6f69;
}
.item {
  background: #ffcc5c;
}
button {
  background: #ff6f69;
  color: #ffcc5c;
}
"""

        self.files["functions.js"] = r"""
/*
Developed by: $author$
*/
$single_code[function]$
"""
# -------------------------------------------------------------------------
