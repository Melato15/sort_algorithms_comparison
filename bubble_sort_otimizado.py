class BubbleSortOtimizado:
    def ordenar(self, dados):
        n = len(dados)
        for i in range(n):
            trocou = False
            for j in range(0, n-i-1):
                if dados[j] > dados[j+1]:
                    dados[j], dados[j+1] = dados[j+1], dados[j]  # Troca os elementos
                    trocou = True
            # Se não houver trocas, a lista já está ordenada
            if not trocou:
                break
        return dados
