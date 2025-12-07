from typing import List

class Documento:
    def __init__(self, doc_id: str, texto_original: str):
        self.id = doc_id
        self.texto_original = texto_original
        self.termos_processados: List[str] = []
