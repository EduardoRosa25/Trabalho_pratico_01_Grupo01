import pandas as pd
import numpy as np
from typing import List, Dict, Union, Any

# Importa a classe do colega para poder processar as queries de busca
# Assumimos que ProcessadorTexto e Documento estão em arquivos .py separados e acessíveis
from ProcessadorTexto import ProcessadorTexto 
from Documento import Documento

# Usamos a classe Documento real para type hinting, assumindo que ela será importada
# A classe Colecao passa os objetos Documento (que têm termos_processados) para este método.

class MatrizTFIDF:
    """
    Gerencia o Vocabulário e a Matriz TF-IDF, e realiza a Consulta Booleana.
    Responsável por calcular e manter as matrizes TF, IDF e TF-IDF.
    """
    def __init__(self):
        self.vocabulario: List[str] = []
        self.matriz_tf: pd.DataFrame = pd.DataFrame()
        self.vetor_idf: pd.Series = pd.Series()
        self.matriz_tfidf: pd.DataFrame = pd.DataFrame()
        # Instancia o ProcessadorTexto para uso interno, especialmente para processar queries
        self.processador = ProcessadorTexto()

    # --- MÉTODOS DE CÁLCULO (Seu código original adaptado) ---
    
    def calcular_tf(self, docs_processados: List[List[str]], nomes_docs: List[str]) -> pd.DataFrame:
        """Calcula o Log do TF (1 + log2(f))."""
        self.vocabulario = sorted(set([t for doc in docs_processados for t in doc]))
        matriz_tf = pd.DataFrame(0.0, index=self.vocabulario, columns=nomes_docs)
        
        for nome, termos in zip(nomes_docs, docs_processados):
            for termo in termos:
                if termo in matriz_tf.index:
                    matriz_tf.loc[termo, nome] += 1
        
        matriz_tf = matriz_tf.map(lambda x: 1 + np.log2(x) if x > 0 else 0)
        return matriz_tf

    def calcular_idf(self, matriz_tf: pd.DataFrame) -> pd.Series:
        """Calcula o Vetor de IDF (log2(N / ni))."""
        N = matriz_tf.shape[1]
        ni = (matriz_tf > 0).sum(axis=1)
        idf = np.log2(N / ni)
        return pd.Series(idf, index=matriz_tf.index, name="IDF")

    def calcular_tfidf(self, matriz_tf: pd.DataFrame, idf: pd.Series) -> pd.DataFrame:
        """Calcula a Matriz TF-IDF (TF * IDF)."""
        return matriz_tf.mul(idf, axis=0)

    # --- ORQUESTRADOR E EXIBIÇÃO ---
    
    def construir_matrizes(self, documentos: Dict[str, Documento]):
        """Orquestra o cálculo completo do TF, IDF e TF-IDF."""
        if not documentos:
            self.__limpar_matrizes()
            return

        nomes_docs = list(documentos.keys())
        # Usa o atributo termos_processados do objeto Documento do colega
        docs_processados = [doc.termos_processados for doc in documentos.values()]
        
        self.matriz_tf = self.calcular_tf(docs_processados, nomes_docs)
        self.vetor_idf = self.calcular_idf(self.matriz_tf)
        self.matriz_tfidf = self.calcular_tfidf(self.matriz_tf, self.vetor_idf)

    def exibir_matriz_tfidf(self):
        """Opção 5 do Menu."""
        if self.matriz_tfidf.empty:
            print("[INFO] A Matriz TF-IDF está vazia. Adicione documentos à coleção.")
        else:
            print("\n--- Matriz TF-IDF (Term Frequency-Inverse Document Frequency) ---")
            print(self.matriz_tfidf.round(4))

    def __limpar_matrizes(self):
        """Método auxiliar para limpar todas as estruturas internas."""
        self.vocabulario = []
        self.matriz_tf = pd.DataFrame()
        self.vetor_idf = pd.Series()
        self.matriz_tfidf = pd.DataFrame()

    # --- CONSULTA BOLEANA (REQUISITO FUNCIONAL 7) ---
    
    def buscar_booleana(self, query: str, operador: str) -> List[str]:
        """
        Implementa a busca booleana (AND, OR, NOT) usando a Matriz TF-IDF (presença > 0).
        """
        if self.matriz_tfidf.empty:
            print("[ERRO] A Matriz TF-IDF está vazia. Impossível buscar.")
            return []

        # 1. Pré-processamento da Query (usa ProcessadorTexto)
        query_processada = self.processador.processar(query)

        if not query_processada:
            print("[AVISO] A consulta não contém termos válidos após processamento (stopwords/radicais).")
            return []

        # Filtrar a Matriz: Apenas termos da query que existem no vocabulário
        termos_existentes = self.matriz_tfidf.index.intersection(query_processada)
        if termos_existentes.empty:
            print(f"[AVISO] Nenhum termo da consulta ('{query_processada}') existe no vocabulário da coleção.")
            return []
            
        # Matriz de Presença: 1 se TF-IDF > 0 (o termo existe no documento), 0 caso contrário
        matriz_presenca = (self.matriz_tfidf.loc[termos_existentes] > 0).astype(int)
        
        operador = operador.upper()
        documentos_disponiveis = self.matriz_tfidf.columns.tolist()
        resultados = []

        if operador == 'AND':
            # AND: A soma das presenças deve ser igual ao número de termos existentes
            soma_presencas = matriz_presenca.sum(axis=0)
            documentos_candidatos = soma_presencas[soma_presencas == len(termos_existentes)].index.tolist()
            resultados = [doc_id for doc_id in documentos_candidatos if doc_id in documentos_disponiveis]

        elif operador == 'OR':
            # OR: A soma das presenças deve ser maior que zero (pelo menos um termo presente)
            soma_presencas = matriz_presenca.sum(axis=0)
            documentos_candidatos = soma_presencas[soma_presencas > 0].index.tolist()
            resultados = [doc_id for doc_id in documentos_candidatos if doc_id in documentos_disponiveis]

        elif operador == 'NOT':
            # NOT: Documentos que NÃO contêm NENHUM dos termos da query.
            # Documentos que contêm pelo menos um dos termos da query
            docs_com_termo = matriz_presenca.columns[matriz_presenca.sum(axis=0) > 0].tolist()
            
            # Todos os documentos menos aqueles que contêm o termo
            todos_documentos = set(documentos_disponiveis)
            resultados = list(todos_documentos - set(docs_com_termo))
            
        else:
            print(f"[ERRO] Operador booleano '{operador}' não suportado. Use AND, OR, ou NOT.")
            
        return resultados
