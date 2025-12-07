from collections import defaultdict
from typing import Dict, List, Set
import numpy as np

# Funções auxiliares


def print_cabecalho(titulo):
    """Função auxiliar para imprimir títulos formatados."""
    titulo_upper = titulo.upper()
    separador = "=" * len(titulo_upper)
    print(f"\n{separador}")
    print(titulo_upper)
    print(f"{separador}\n")


class Indexador:
    def __init__(self):
        # Estrutura do Índice Invertido Posicional
        # { termo: { id_doc: [pos1, pos2, ...], id_doc2: [...] } }
        self.indice = defaultdict(lambda: defaultdict(list))

    # --- CONSTRUIR E ATUALIZAR ÍNDICE ---
    def atualizar_indice(self, docs_tokens_processados: Dict[str, List[str]]):

        print(
            "\n[INFO - Indexador] Acionando atualização do Índice Invertido Posicional...")
        self.indice.clear()  # Limpa o índice antigo

        for doc_id, tokens in docs_tokens_processados.items():
            for pos, termo in enumerate(tokens):
                # O índice armazena a posição (pos) de cada ocorrência do termo
                self.indice[termo][doc_id].append(pos)

        print("[INFO - Indexador] Índice Invertido Posicional atualizado com sucesso.")

    # --- EXIBIR ÍNDICE INVERTIDO ---
    def exibir_indice_invertido(self):

        print_cabecalho("6) ÍNDICE INVERTIDO COMPLETO (POSICIONAL)")

        indice_ordenado = dict(
            sorted(self.indice.items(), key=lambda item: item[0]))

        if not indice_ordenado:
            print("O índice está vazio. Adicione documentos primeiro.")
            return

        print(f"Termo (Total: {len(indice_ordenado)}): Documentos e Posições")
        print("-" * 70)

        # Exibe apenas os 50 primeiros termos para evitar uma saída excessivamente longa
        for i, (termo, docs) in enumerate(indice_ordenado.items()):
            if i >= 50:
                print("... (Exibindo apenas os primeiros 50 termos)...")
                break

            # Formato: D1: [2, 5], D3: [1]
            docs_formatados = ", ".join(
                [f"{doc}: {pos}" for doc, pos in docs.items()])
            print(f"{termo.ljust(20)} → {docs_formatados}")

        print(f"\nTotal de termos distintos indexados: {len(indice_ordenado)}")

    # --- BUSCA POR FRASE ---

    def buscar_por_frase(self, frase_processada: List[str]) -> Set[str]:

        if not frase_processada:
            return set()

        termo_inicial = frase_processada[0]

        if termo_inicial not in self.indice:
            return set()

        candidatos = set()
        docs_do_termo_inicial = self.indice[termo_inicial]

        # Iterar sobre cada documento que contém o termo inicial
        for doc_id, posicoes_iniciais in docs_do_termo_inicial.items():

            # Para cada posição inicial do primeiro termo no documento:
            for pos_inicio in posicoes_iniciais:
                match_completo = True

                # Verificar se os termos seguintes estão nas posições subsequentes
                for i, termo in enumerate(frase_processada):

                    posicao_esperada = pos_inicio + i

                    # 1. Verifica se o termo existe no índice E no documento atual
                    if termo not in self.indice or doc_id not in self.indice[termo]:
                        match_completo = False
                        break

                    # 2. Verifica se a posição esperada (pos_inicio + i) existe na lista
                    # O 'in' aqui é eficiente porque a lista de posições é pequena.
                    if posicao_esperada not in self.indice[termo][doc_id]:
                        match_completo = False
                        break

                if match_completo:
                    candidatos.add(doc_id)
                    # Se encontrou a frase uma vez no documento, já pode parar de checar
                    break

        return candidatos
