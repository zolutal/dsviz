# Credit: https://stackoverflow.com/questions/60044441/context-menus-for-nodes-and-edges-for-dot-graphs-using-python

from dsviz.util import read_module_file
import webview
import os

context_js = read_module_file('graph_context.js')
context_css = read_module_file('graph_context.css')

class GraphServer:
    def __init__(self, graph, row_menu):
        self.graph = graph
        self.row_menu = row_menu

    def make_menu(self, menu_info, menu_type):
        lis = '\n'.join(f'<li class="menu-option" onclick="menuClick(\'{menu_type}\', \'{name}\')">{name}</li>' for name in menu_info)
        return f"""
        <div class="menu" id="{menu_type}_context_menu">
          <ul class="menu-options">
            {lis}
          </ul>
        </div>
        """

    def get_content(self):
        svg = self.graph.draw()

        html = f"""<!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8"/>
                        <style>
                            {context_css}
                        </style>
                    </head>
                    <body>
                        <div id="graph">{svg}</div>
                        {self.make_menu(self.row_menu, 'row')}
                        <script>{context_js}</script>
                    </body>
                    </html>
                    """
        return html

    def start_graph_server(self):
        row_menu = self.row_menu
        class Api:
            def menu_item_clicked(self, menu_type, selected, item):
                if menu_type == "row":
                    callback = row_menu[item]
                    callback(selected)
                return {}

        html = self.get_content()

        self.window = webview.create_window(
            "Graph Viewer",
            html=html,
            js_api=Api()
        )
        webview.start(args=self.window, debug=False)

    def restart(self):
        if not hasattr(self, 'window'):
            self.start_graph_server()
        html = self.get_content()
        self.window.load_html(html)
