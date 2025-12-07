from typing import Dict, List, Set
from Documento import Documento

class IndiceInvertido:
    def __init__(self):
        # Estrutura: { termo: { id_doc: [pos1, pos2, ...], ... } }
        self.indice: Dict[str, Dict[str, List[int]]] = {}

    def construir_indice(self, documentos: Dict[str, Documento]):
        """Constroi o índice com as posições dos termos."""
        self.indice.clear()
        for doc_id, doc in documentos.items():
            for posicao, termo in enumerate(doc.termos_processados):
                if termo not in self.indice:
                    self.indice[termo] = {}
                if doc_id not in self.indice[termo]:
                    self.indice[termo][doc_id] = []
                self.indice[termo][doc_id].append(posicao)

    def get_indice(self) -> Dict[str, Dict[str, List[int]]]:
        return self.indice

    def exibir_indice(self):
        if not self.indice:
            print("[INFO] O Índice Invertido está vazio.")
            return
        print("\n--- Índice Invertido (Termo: {Doc_ID: [posições]}) ---")
        termos_ordenados = sorted(self.indice.keys())
        for termo in termos_ordenados:
            posting = self.indice[termo]
            # Formata a saída: D1: [1, 5] | D2: [3]
            formatado = " | ".join([f"{did}: {posting[did]}" for did in sorted(posting.keys())])
            print(f"'{termo}': {formatado}")

    # --- MÉTODOS DE BUSCA (Incorporado do Indexador.py) ---

    def buscar_por_frase(self, frase_processada: List[str]) -> Set[str]:
        """
        Retorna os IDs dos documentos que contêm a frase exata.
        """
        if not frase_processada:
            return set()

        termo_inicial = frase_processada[0]

        # Se o primeiro termo nem existe no índice, a frase não existe
        if termo_inicial not in self.indice:
            return set()

        candidatos = set()
        docs_do_termo_inicial = self.indice[termo_inicial]

        # Verifica cada documento que tem a primeira palavra
        for doc_id, posicoes_iniciais in docs_do_termo_inicial.items():
            # Para cada ocorrência da primeira palavra...
            for pos_inicio in posicoes_iniciais:
                match_completo = True

                # Verifica se as palavras seguintes estão nas posições seguintes (pos_inicio + i)
                for i in range(1, len(frase_processada)):
                    termo_seguinte = frase_processada[i]
                    posicao_esperada = pos_inicio + i

                    # Checa se o termo existe no índice, no doc, e na posição exata
                    if (termo_seguinte not in self.indice or
                        doc_id not in self.indice[termo_seguinte] or
                        posicao_esperada not in self.indice[termo_seguinte][doc_id]):
                        match_completo = False
                        break

                if match_completo:
                    candidatos.add(doc_id)
                    break # Se achou uma vez no doc, já serve

        return candidatos
