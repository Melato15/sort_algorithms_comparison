class SelectionSort:
    def ordenar(self, dados):
        n = len(dados)
        for i in range(n):
            menor_idx = i
            for j in range(i+1, n):
                if dados[j] < dados[menor_idx]:
                    menor_idx = j
            dados[i], dados[menor_idx] = dados[menor_idx], dados[i]
        return dados
