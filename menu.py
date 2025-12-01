from Colecao import Colecao
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
2
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

    sistema.carregar_dados_iniciais(arquivo_json)

    while True:
        print_menu()
        choice = input('Escolha uma opção: ').strip()
        # Usando match-case para comportamento de switch/case 
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
                    ()
                case '6':
                    ()
                case '7':
                    ()
                case '8':
                    ()
                case '9':
                    ()
                case '10':
                   ()
                case '0':
                    print('Saindo...')
                    return
                case _:
                    print('Opção inválida. Tente novamente.')
        except SyntaxError:
            # Caso a versão do Python não suporte match-case
            print('Erro de sintaxe: sua versão do Python pode não suportar `match-case`.')
            return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nPrograma interrompido pelo usuário.')
