import logging
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

from server.indexxocore import Indexxo


class IndexxoServer:
    """TODO"""

    def __init__(self, indexxo: Indexxo):
        """TODO"""
        self.app = Flask(__name__)
        CORS(self.app)
        self.indexxo = indexxo
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/folder", "folder", self.get_folder_info)
        self.app.add_url_rule("/search", "search", self.search_files)

    def run_server(self):
        """TODO"""
        self.app.run(host="localhost", debug=False)

    @staticmethod
    def index():
        """
        Page that can be used for pinging.
        """
        return "<p>Welcome to Indexxo!</p>"

    def get_folder_info(self):
        """
        See: indexxo.get_spaces if no path is provided.
        See: indexxo.get_content if path is provided.
        """
        path = request.args.get("path")
        if path is None or path == "":
            return jsonify({
                "content": [s.to_json() for s in self.indexxo.get_spaces()]
            })

        try:
            content, parent = self.indexxo.get_content(Path(path))

            return jsonify({
                "content": [c.to_json() for c in content],
                "parent": parent.to_json() if parent else None
            })
        except Exception as e:
            logging.error(e)
            return jsonify({
                "error": f"{path} is not found in index"
            }), 404

    def search_files(self):
        """
        See: indexxo.find_files
        """
        query = request.args.get("query")
        if (query is None) or (query == ""):
            return jsonify({
                "error": "Please provide query argument"
            }), 400
        result = self.indexxo.find_files(query)
        return jsonify({
            "result": [r.to_json() for r in result]
        })
