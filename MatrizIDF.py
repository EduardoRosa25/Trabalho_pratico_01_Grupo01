import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from ProcessadorTexto import ProcessadorTexto
from Documento import Documento

class MatrizTFIDF:
    def __init__(self):
        self.vocabulario: List[str] = []
        self.matriz_tf: pd.DataFrame = pd.DataFrame()
        self.vetor_idf: pd.Series = pd.Series()
        self.matriz_tfidf: pd.DataFrame = pd.DataFrame()
        self.normas_doc: Dict[str, float] = {}
        self.processador = ProcessadorTexto()

    def construir_matrizes(self, documentos: Dict[str, Documento]):
        if not documentos:
            return

        nomes_docs = list(documentos.keys())
        docs_processados = [doc.termos_processados for doc in documentos.values()]

        # 1. Vocabulário Global
        self.vocabulario = sorted(set([t for doc in docs_processados for t in doc]))

        # 2. Matriz TF (1 + log2(f))
        # Cria dataframe vazio e preenche
        self.matriz_tf = pd.DataFrame(0.0, index=self.vocabulario, columns=nomes_docs)
        for nome, termos in zip(nomes_docs, docs_processados):
            for termo in termos:
                self.matriz_tf.loc[termo, nome] += 1

        # Aplica log apenas onde > 0
        self.matriz_tf = self.matriz_tf.map(lambda x: 1 + np.log2(x) if x > 0 else 0)

        # 3. Vetor IDF (log2(N / ni))
        N = len(nomes_docs)
        ni = (self.matriz_tf > 0).sum(axis=1)
        # Evita divisão por zero
        idf_vals = np.log2(N / ni.replace(0, 1))
        self.vetor_idf = pd.Series(idf_vals, index=self.vocabulario)

        # 4. TF-IDF
        self.matriz_tfidf = self.matriz_tf.mul(self.vetor_idf, axis=0)

        # 5. Normas (para cosseno)
        self.normas_doc = np.sqrt((self.matriz_tfidf**2).sum(axis=0)).to_dict()

    def exibir_matriz_tfidf(self):
        if self.matriz_tfidf.empty:
            print("[INFO] Matriz vazia.")
        else:
            print(self.matriz_tfidf.round(4))

    def buscar_booleana(self, query: str, operador: str) -> List[str]:
        if self.matriz_tfidf.empty: return []

        termos_query = self.processador.processar(query)
        # Filtra apenas termos que existem no vocabulário
        termos_validos = [t for t in termos_query if t in self.matriz_tfidf.index]

        if not termos_validos: return []

        # Matriz de presença (0 ou 1)
        presenca = (self.matriz_tfidf.loc[termos_validos] > 0).astype(int)
        operador = operador.upper()

        if operador == 'AND':
            # Soma das presenças tem que ser igual à qtde de termos
            match = presenca.sum(axis=0) == len(termos_validos)
            return match[match].index.tolist()

        elif operador == 'OR':
            # Soma > 0
            match = presenca.sum(axis=0) > 0
            return match[match].index.tolist()

        elif operador == 'NOT':
            # Docs que contêm os termos
            match_pos = presenca.sum(axis=0) > 0
            docs_com_termo = match_pos[match_pos].index.tolist()
            # Retorna quem NÃO está na lista acima
            todos = self.matriz_tfidf.columns.tolist()
            return list(set(todos) - set(docs_com_termo))

        return []

    def buscar_similaridade(self, query: str, indice: Dict) -> List[Tuple[str, float]]:
        if self.matriz_tfidf.empty: return []

        q_termos = self.processador.processar(query)
        # TF da Query
        q_tf = pd.Series([q_termos.count(t) for t in self.vocabulario], index=self.vocabulario)
        q_tf = q_tf.map(lambda x: 1 + np.log2(x) if x > 0 else 0)

        # TF-IDF da Query (apenas termos validos)
        q_vec = q_tf * self.vetor_idf
        q_norm = np.sqrt((q_vec**2).sum())

        if q_norm == 0: return []

        # Candidatos via índice invertido (otimização)
        candidatos = set()
        for t in q_termos:
            if t in indice:
                candidatos.update(indice[t].keys())

        resultados = []
        for doc_id in candidatos:
            # Produto Escalar
            doc_vec = self.matriz_tfidf[doc_id]
            dot = (q_vec * doc_vec).sum()
            d_norm = self.normas_doc.get(doc_id, 0)

            if d_norm > 0:
                score = dot / (q_norm * d_norm)
                if score > 0:
                    resultados.append((doc_id, score))

        return sorted(resultados, key=lambda x: x[1], reverse=True)
