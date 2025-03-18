class BubbleSort:
    def ordenar(self, dados):
        n = len(dados)
        for i in range(n):
            for j in range(0, n-i-1):
                if dados[j] > dados[j+1]:
                    dados[j], dados[j+1] = dados[j+1], dados[j]  # Troca os elementos
        return dados
