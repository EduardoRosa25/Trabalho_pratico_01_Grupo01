#Alunos:
#  Bernardo Carvalho Trindade 12321BSI253 
#  Eduardo Antonio 12311BSI317
#  Eduardo Rosa 12311BSI275
#  Luiz Fellipe 12311BSI262 
#  Lucas Pinheiro Barbosa 12221BSI224

from Colecao import Colecao
import sys

# Função auxiliar para limpar a tela ou dar espaço (opcional, mas ajuda na visualização)
def espaco():
    print("\n" + "="*30 + "\n")

def print_menu():
    print('\n=== MENU PRINCIPAL ===')
    print('1) Adicionar um documento por vez (fila)')
    print('2) Adicionar TODOS os documentos (lote)')
    print('3) Remover documento por ID')
    print('4) Exibir Vocabulário')
    print('5) Exibir Matriz TF-IDF')
    print('6) Exibir Índice Invertido (Posicional)')
    print('7) Consulta Booleana (AND, OR, NOT)')
    print('8) Consulta por Similaridade (Ranking)')
    print('9) Consulta por Frase (Exata)')
    print('0) Sair')

def main():
    sistema = Colecao()
    arquivo_json = 'colecao - trabalho 01.json'

    # Carrega o JSON na memória
    sistema.carregar_dados_iniciais(arquivo_json)

    while True:
        print_menu()
        choice = input('Escolha uma opção: ').strip()

        try:
            if choice == '1':
                sistema.adicionar_proximo_da_fila()

            elif choice == '2':
                sistema.adicionar_todos_restantes()

            elif choice == '3':
                id_doc = input("Digite o ID do Documento (ex: D1): ").strip()
                sistema.remover_documento(id_doc)

            elif choice == '4':
                vocab = sistema.get_vocabulario()
                print(f"\nVocabulário ({len(vocab)} termos):")
                print(", ".join(vocab))

            elif choice == '5':
                sistema.get_matriz_handler().exibir_matriz_tfidf()

            elif choice == '6':
                sistema.get_indice_invertido_handler().exibir_indice()

            elif choice == '7':
                if not sistema.documentos:
                    print("[ERRO] Coleção vazia. Adicione documentos primeiro.")
                    continue
                print("\n--- Consulta Booleana ---")
                query = input("Termos da consulta: ")
                operador = input("Operador (AND, OR, NOT): ").strip()

                res = sistema.get_matriz_handler().buscar_booleana(query, operador)
                if res:
                    print(f"✅ Documentos encontrados ({operador}): {', '.join(res)}")
                else:
                    print(f"❌ Nenhum resultado para '{query}' com operador {operador}.")

            elif choice == '8':
                if not sistema.documentos:
                    print("[ERRO] Coleção vazia.")
                    continue
                print("\n--- Consulta por Similaridade (Cosseno) ---")
                query = input("Digite a consulta: ")

                indice = sistema.get_indice_invertido_handler().get_indice()
                ranking = sistema.get_matriz_handler().buscar_similaridade(query, indice)

                if ranking:
                    print(f"✅ Ranking de Relevância:")
                    for doc_id, score in ranking:
                        print(f"1. {doc_id} (Score: {score:.4f})")
                else:
                    print("❌ Nenhum documento relevante encontrado.")

            elif choice == '9':
                if not sistema.documentos:
                    print("[ERRO] Coleção vazia.")
                    continue
                print("\n--- Consulta por Frase ---")
                frase = input("Digite a frase exata: ").strip()

                frase_processada = sistema.processador.processar(frase)
                if not frase_processada:
                    print("[AVISO] Frase vazia ou só contém stopwords.")
                    continue

                res = sistema.get_indice_invertido_handler().buscar_por_frase(frase_processada)

                if res:
                    print(f"✅ Frase encontrada nos documentos: {', '.join(res)}")
                else:
                    print("❌ Frase não encontrada exatamente nessa ordem.")

            elif choice == '0':
                print("Encerrando sistema...")
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"[ERRO CRÍTICO] {e}")

if __name__ == '__main__':
    main()
