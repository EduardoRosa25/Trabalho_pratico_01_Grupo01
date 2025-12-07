import json
from typing import Dict, List
from MatrizIDF import MatrizTFIDF
from Documento import Documento
from ProcessadorTexto import ProcessadorTexto
from IndiceInvertido import IndiceInvertido

class Colecao:
    def __init__(self):
        self.documentos: Dict[str, Documento] = {}
        self.vocabulario: List[str] = []

        self.fila_documentos: List[Dict[str, str]] = []
        self.lista_completa_backup: List[Dict[str, str]] = []

        self.matriz_handler = MatrizTFIDF()
        self.processador = ProcessadorTexto()
        self.indice_invertido_handler = IndiceInvertido()

    def carregar_dados_iniciais(self, caminho_arquivo: str):
        if self.lista_completa_backup:
            return

        print(f"[DEBUG] Lendo JSON: {caminho_arquivo}")
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            dados_normalizados = []
            if isinstance(dados, list):
                dados_normalizados = dados
            elif isinstance(dados, dict):
                dados_normalizados = [{"name": k, "content": v} for k, v in dados.items()]

            self.lista_completa_backup = list(dados_normalizados)
            self.fila_documentos = list(dados_normalizados)
            print(f"[SUCESSO] {len(self.lista_completa_backup)} documentos carregados.")

        except FileNotFoundError:
            print(f"[ERRO] Arquivo '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            print(f"[ERRO] Falha ao ler JSON: {e}")

    def adicionar_proximo_da_fila(self):
        if not self.fila_documentos:
            print("[AVISO] Fila vazia.")
            return

        item = self.fila_documentos.pop(0)
        d_id = item.get('name') or item.get('id')
        d_conteudo = item.get('content') or item.get('text')

        if d_id and d_conteudo:
            if d_id not in self.documentos:
                self._adicionar_documento_interno(d_id, d_conteudo)
                print(f"[SUCESSO] Documento {d_id} adicionado.")
            else:
                print(f"[INFO] Doc {d_id} já existe.")

    def adicionar_todos_restantes(self):
        if not self.lista_completa_backup:
            print("[ERRO] Carregue o JSON primeiro.")
            return

        print("Processando inserção em lote...")
        count = 0
        for item in self.lista_completa_backup:
            d_id = item.get('name') or item.get('id')
            d_conteudo = item.get('content') or item.get('text')

            if d_id and d_conteudo and d_id not in self.documentos:
                self._adicionar_documento_interno(d_id, d_conteudo, atualizar_agora=False)
                count += 1

        self.fila_documentos = []
        if count > 0:
            self._atualizar_sistema()
            print(f"[SUCESSO] {count} documentos adicionados.")
        else:
            print("[INFO] Todos os documentos já estavam presentes.")

    def remover_documento(self, doc_id: str):
        if doc_id in self.documentos:
            del self.documentos[doc_id]
            self._atualizar_sistema()
            print(f"[SUCESSO] Documento {doc_id} removido.")
        else:
            print("[ERRO] ID não encontrado.")

    def _adicionar_documento_interno(self, doc_id: str, texto: str, atualizar_agora=True):
        doc = Documento(doc_id, texto)
        doc.termos_processados = self.processador.processar(texto)
        self.documentos[doc_id] = doc

        if atualizar_agora:
            self._atualizar_sistema()

    def _atualizar_sistema(self):
        termos = set()
        for doc in self.documentos.values():
            termos.update(doc.termos_processados)
        self.vocabulario = sorted(list(termos))

        if self.documentos:
            self.matriz_handler.construir_matrizes(self.documentos)
            self.indice_invertido_handler.construir_indice(self.documentos)

    # --- GETTERS ---
    def get_indice_invertido_handler(self):
        return self.indice_invertido_handler

    def get_matriz_handler(self):
        return self.matriz_handler

    def get_vocabulario(self):
        # Aqui está o return que você procurava! Ele retorna a lista para quem pediu.
        return self.vocabulario
