from typing import Dict, List, Tuple
from Documento import Documento # Importa a classe Documento

class IndiceInvertido:
    """
    Gerenciar o Índice Invertico com as posições...
    """
    def __init__(self):
        # Estrutura do Índice Invertido
        self.indice: Dict[str, Dict[str, List[int]]] = {}

    def construir_indice(self, documentos: Dict[str, Documento]):
        """
        Construir ou atualizar o Índice Invertido a partir da coleção.
        """
        self.indice.clear()
        
        for doc_id, doc in documentos.items():
            # Itera sobre os termos processados (radicais) e suas posições (índices)
            for posicao, termo in enumerate(doc.termos_processados):
                if termo not in self.indice:
                    self.indice[termo] = {}
                
                if doc_id not in self.indice[termo]:
                    self.indice[termo][doc_id] = []
                    
                self.indice[termo][doc_id].append(posicao)

    def get_indice(self) -> Dict[str, Dict[str, List[int]]]:
          """Retorna o índice completo para uso em consultas."""
          return self.indice

    def exibir_indice(self):
        if not self.indice:
            print("[INFO] O Índice Invertido está vazio. Adicione documentos à coleção.")
            return

        print("\n--- Índice Invertido (Termo: {Doc_ID: [posições]}) ---")
        
        # Ordena por termo para exibição
        termos_ordenados = sorted(self.indice.keys())
        
        # Exibe no formato solicitado
        for termo in termos_ordenados:
            posting_list = self.indice[termo]
            posts_formatados = []
            
            # Ordena a posting list por Doc_ID
            doc_ids_ordenados = sorted(posting_list.keys())
            
            for doc_id in doc_ids_ordenados:
                posicoes = posting_list[doc_id]
                posts_formatados.append(f"{doc_id}: {posicoes}")
                
            print(f"'{termo}': {' | '.join(posts_formatados)}")
