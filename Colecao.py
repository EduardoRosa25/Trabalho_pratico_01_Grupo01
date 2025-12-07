import json
from typing import Dict, List, Any
from MatrizIDF import MatrizTFIDF
from Documento import Documento
from ProcessadorTexto import ProcessadorTexto
from IndiceInvertido import IndiceInvertido

class Colecao:
    def __init__(self):
        self.documentos: Dict[str, Documento] = {}
        self.vocabulario: List[str] = []
        
        # Fila para Opção 1 (consome itens)
        self.fila_documentos: List[Dict[str, str]] = []
        # Lista Mestra para Opção 2 (referência completa)
        self.lista_completa_backup: List[Dict[str, str]] = []
        
        self.matriz_handler = MatrizTFIDF()
        self.processador = ProcessadorTexto()

        self.indice_invertido_handler = IndiceInvertido()

    def carregar_dados_iniciais(self, caminho_arquivo: str):
        """
        Lê o JSON e prepara tanto a fila quanto o backup completo.
        """
        if self.lista_completa_backup:
            print("[AVISO] O arquivo já foi carregado na memória.")
            return

        print(f"[DEBUG] Lendo JSON: {caminho_arquivo}")
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Normaliza para lista de objetos
            dados_normalizados = []
            if isinstance(dados, list):
                dados_normalizados = dados
            elif isinstance(dados, dict):
                dados_normalizados = [{"name": k, "content": v} for k, v in dados.items()]
            
            # Salva nas duas estruturas
            self.lista_completa_backup = list(dados_normalizados) # Cópia Mestra
            self.fila_documentos = list(dados_normalizados)       # Cópia para consumo (Opção 1)
            
            print(f"[SUCESSO] {len(self.lista_completa_backup)} documentos carregados na memória.")
            
        except FileNotFoundError:
            print(f"[ERRO] Arquivo '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha ao ler JSON: {e}")

    def adicionar_proximo_da_fila(self):
        """
        Opção 1: Adiciona estritamente o próximo da fila de espera.
        """
        if not self.fila_documentos:
            print("[AVISO] A fila de inserção manual acabou.")
            print("Dica: Se quiser re-adicionar documentos removidos, use a Opção 2.")
            return

        # Pega o primeiro da fila
        item = self.fila_documentos.pop(0)
        
        d_id = item.get('name') or item.get('id')
        d_conteudo = item.get('content') or item.get('text')
        
        if d_id and d_conteudo:
            # Verifica se já existe (caso tenha sido adicionado via Opção 2 antes)
            if d_id in self.documentos:
                print(f"[INFO] Documento {d_id} já existe na coleção. Pulando...")
            else:
                self._adicionar_documento_interno(d_id, d_conteudo)
                print(f"[SUCESSO] Documento {d_id} adicionado.")
                print(f"Restam {len(self.fila_documentos)} na fila de inserção manual.")
        else:
            print(f"[ERRO] Item inválido na fila: {item}")

    def adicionar_todos_restantes(self):
        """
        Opção 2: Garante que TODOS os documentos do JSON estejam na coleção.
        Se faltar algum (seja porque nunca entrou ou porque foi removido), ele adiciona.
        """
        if not self.lista_completa_backup:
            print("[ERRO] Nenhum dado carregado. Verifique o arquivo JSON.")
            return

        print("Verificando consistência da coleção completa...")
        adicionados_agora = 0
        
        for item in self.lista_completa_backup:
            d_id = item.get('name') or item.get('id')
            d_conteudo = item.get('content') or item.get('text')
            
            if d_id and d_conteudo:
                # LÓGICA CORRIGIDA: Checa se está na coleção ativa. Se não estiver, adiciona.
                if d_id not in self.documentos:
                    self._adicionar_documento_interno(d_id, d_conteudo, atualizar_agora=False)
                    adicionados_agora += 1
        
        # Limpa a fila manual, pois agora tudo foi adicionado
        self.fila_documentos = []
        
        if adicionados_agora > 0:
            self._atualizar_sistema()
            print(f"[SUCESSO] {adicionados_agora} documentos faltantes foram adicionados/restaurados.")
        else:
            print("[INFO] Todos os documentos do arquivo já estão na coleção.")

    def _adicionar_documento_interno(self, doc_id: str, texto: str, atualizar_agora=True):
        doc = Documento(doc_id, texto)
        doc.termos_processados = self.processador.processar(texto)
        self.documentos[doc_id] = doc
        
        if atualizar_agora:
            self._atualizar_sistema()

    def remover_documento(self, doc_id: str):
        if doc_id in self.documentos:
            del self.documentos[doc_id]
            self._atualizar_sistema()
            print(f"[SUCESSO] Documento {doc_id} removido da coleção ativa.")
        else:
            print("[ERRO] Documento não encontrado na coleção ativa.")

    def _atualizar_sistema(self):
        # 1. Atualiza Vocabulário
        termos_unicos = set()
        for doc in self.documentos.values():
            termos_unicos.update(doc.termos_processados)
        self.vocabulario = sorted(list(termos_unicos))
        
        # 2. Chama o Integrante 2 (MatrizIDF)
        if self.documentos:
            self.matriz_handler.construir_matrizes(self.documentos)

        # 3. Atualiza Índice Invertido (com posições)
        if self.documentos:
            self.indice_invertido_handler.construir_indice(self.documentos)
            
    def get_vocabulario(self):
        return self.vocabulario

    def get_indice_invertido_handler(self):
        return self.indice_invertido_handler

    def get_matriz_handler(self):
        return self.matriz_handler
