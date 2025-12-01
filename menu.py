from Colecao import Colecao
# Não precisa importar nltk, stopwords, e RSLPStemmer aqui, pois Colecao e ProcessadorTexto já cuidam disso.
# A linha "2" no seu original foi ignorada.

def print_menu():
    print('\n=== MENU PRINCIPAL ===')
    print('1) Adicionar um documento por vez à coleção')
    print('2) Adicionar todos os documentos da lista')
    print('3) Remover um documento da coleção pelo seu identificador')
    print('4) Exibir o vocabulário atualizado')
    print('5) Exibir a matriz TF-IDF atual')
    print('6) Exibir o índice invertido completo por posição de palavras')
    print('7) Realizar consultas booleanas')
    print('8) Realizar consultas por similaridade')
    print('9) Realizar consultas por frase')
    print('10) Outras operações (extensões do grupo)')
    print('0) Sair')


def main():

    sistema = Colecao()
    arquivo_json = 'colecao - trabalho 01.json'

    # Carrega os dados iniciais do JSON na memória (não adiciona à coleção, apenas prepara a fila)
    sistema.carregar_dados_iniciais(arquivo_json)

    while True:
        print_menu()
        choice = input('Escolha uma opção: ').strip()
        
        try:
            match choice:
                case '1':
                    sistema.adicionar_proximo_da_fila()
                case '2':
                    sistema.adicionar_todos_restantes()
                case '3':
                    id_doc = input("ID do Documento para remover: ")
                    sistema.remover_documento(id_doc)
                case '4':
                    print(f"\nVocabulário ({len(sistema.vocabulario)} termos):")
                    print(", ".join(sistema.vocabulario))
                
                case '5':
                    sistema.matriz_handler.exibir_matriz_tfidf()
                
                case '7':
                    print("\n--- Consulta Booleana (AND, OR, NOT) ---")
                    query = input("Digite a consulta (termos, ex: 'sol liberdade'): ")
                    operador = input("Digite o operador (AND, OR, NOT): ").strip()
                    
                    # Chama o método implementado em MatrizTFIDF
                    resultados = sistema.matriz_handler.buscar_booleana(query, operador)
                    
                    if resultados:
                        print(f"\n✅ Resultados para '{query}' ({operador.upper()}):")
                        print(f"Documentos encontrados: {', '.join(resultados)}")
                    else:
                        print(f"\n❌ Nenhum documento encontrado para a consulta '{query}' ({operador.upper()}).")

                case '6':
                    
                    print("Opção 6: Exibir Índice Invertido - Implementação Pendente.")
                case '8':
                    
                    print("Opção 8: Consultas por Similaridade - Implementação Pendente.")
                case '9':
                    
                    print("Opção 9: Consultas por Frase - Implementação Pendente. ")
                case '10':
                    print('Opção 10: Extensões do Grupo - Implementação Pendente.')
                case '0':
                    print('Saindo...')
                    return
                case _:
                    print('Opção inválida. Tente novamente.')
        
        except SyntaxError:
            # Caso a versão do Python seja antiga (antes do 3.10)
            print('Erro de sintaxe: sua versão do Python pode não suportar `match-case`.')
            print('Dica: Mude para uma estrutura `if/elif/else`.')
            return
        except Exception as e:
            print(f"[ERRO CRÍTICO] Ocorreu um erro no sistema: {e}")
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nPrograma interrompido pelo usuário.')