import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from typing import List

class ProcessadorTexto:
    def __init__(self):
        self._configurar_nltk()
        self.stemmer = RSLPStemmer()
        self.stopwords_pt = set(stopwords.words('portuguese'))

    def _configurar_nltk(self):
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('stemmers/rslp')
        except LookupError:
            print("[DEBUG] Baixando recursos do NLTK...")
            nltk.download('stopwords')
            nltk.download('rslp')

    def processar(self, texto: str) -> List[str]:
        """
        Recebe um texto bruto e retorna a lista de tokens (radicais).
        """
        texto = texto.lower()
        texto = re.sub(r'[^a-zà-úÀ-Ú\s]', '', texto)
        
        tokens = texto.split()
        
        tokens_processados = [
            self.stemmer.stem(t) 
            for t in tokens 
            if t not in self.stopwords_pt and len(t) > 1
        ]
        
        return tokens_processados