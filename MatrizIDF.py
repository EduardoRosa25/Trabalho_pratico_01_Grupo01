import pandas as pd
import numpy as np

from typing import List, Dict, Union

# MOCK TEMPORÁRIO para que MatrizTFIDF funcione sozinha, até Colecao.py ser finalizado
class DocumentoMock:
    def __init__(self, id, termos):
        self.id = id
        self.termos_processados = termos

class MatrizTFIDF:
    """
    Gerencia o Vocabulário e a Matriz TF-IDF.
    Responsável por calcular e manter as matrizes TF, IDF e TF-IDF.
    """
    def __init__(self):
        self.vocabulario: List[str] = []
        self.matriz_tf: pd.DataFrame = pd.DataFrame()
        self.vetor_idf: pd.Series = pd.Series()
        self.matriz_tfidf: pd.DataFrame = pd.DataFrame()
        
    # --- MÉTODOS DE CÁLCULO  ---
    
    def calcular_tf(self, docs_processados: List[List[str]], nomes_docs: List[str]) -> pd.DataFrame:
        """
        Calcula o Log do TF (frequência do termo no documento) na base 2: 1 + log2(f).
        """
        # Reconstruir o vocabulário: essencial para atualizações dinâmicas
        self.vocabulario = sorted(set([t for doc in docs_processados for t in doc]))
        
        matriz_tf = pd.DataFrame(0.0, index=self.vocabulario, columns=nomes_docs)
        
        for nome, termos in zip(nomes_docs, docs_processados):
            for termo in termos:
                if termo in matriz_tf.index:
                    matriz_tf.loc[termo, nome] += 1
        
        # Aplica log2 apenas onde TF > 0
        matriz_tf = matriz_tf.map(lambda x: 1 + np.log2(x) if x > 0 else 0)
        return matriz_tf

    def calcular_idf(self, matriz_tf: pd.DataFrame) -> pd.Series:
        """
        Calcula o Vetor de IDF: log2(N / ni).
        """
        N = matriz_tf.shape[1]  # Número total de documentos
        ni = (matriz_tf > 0).sum(axis=1) # Document frequency
        idf = np.log2(N / ni)
        return pd.Series(idf, index=matriz_tf.index, name="IDF")

    def calcular_tfidf(self, matriz_tf: pd.DataFrame, idf: pd.Series) -> pd.DataFrame:
        """
        Calcula a Matriz TF-IDF: TF * IDF.
        """
        matriz_tfidf = matriz_tf.mul(idf, axis=0)
        return matriz_tfidf

    # --- MÉTODO ORQUESTRADOR (Para ser chamado pela Colecao) ---
    
    def construir_matrizes(self, documentos: Dict[str, DocumentoMock]):
        """
        Orquestra o cálculo completo do TF, IDF e TF-IDF.
        """
        if not documentos:
            self.__limpar_matrizes()
            return

        nomes_docs = list(documentos.keys())
        # Extrai os termos processados de cada Documento (Mock ou real)
        docs_processados = [doc.termos_processados for doc in documentos.values()]
        
        # 1. Calcula TF (e atualiza o vocabulário interno)
        self.matriz_tf = self.calcular_tf(docs_processados, nomes_docs)
        
        # 2. Calcula IDF
        self.vetor_idf = self.calcular_idf(self.matriz_tf)
        
        # 3. Calcula TF-IDF
        self.matriz_tfidf = self.calcular_tfidf(self.matriz_tf, self.vetor_idf)

    def exibir_matriz_tfidf(self):
        """Exibe a Matriz TF-IDF atual (Requisito de Menu)."""
        if self.matriz_tfidf.empty:
            print("A Matriz TF-IDF está vazia. Adicione documentos primeiro.")
        else:
            print("\n--- Matriz TF-IDF (Term Frequency-Inverse Document Frequency) ---")
            print(self.matriz_tfidf.round(4)) # Formatação para 4 casas decimais

    def __limpar_matrizes(self):
        """Método auxiliar para limpar todas as estruturas internas."""
        self.vocabulario = []
        self.matriz_tf = pd.DataFrame()
        self.vetor_idf = pd.Series()
        self.matriz_tfidf = pd.DataFrame()

    # --- MÉTODO DE BUSCA BOLEANA (Próxima Fase) ---
 