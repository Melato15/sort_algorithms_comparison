class InsertionSort:
    def ordenar(self, dados):
        for i in range(1, len(dados)):
            chave = dados[i]
            j = i - 1
            while j >= 0 and chave < dados[j]:
                dados[j + 1] = dados[j]
                j -= 1
            dados[j + 1] = chave
        return dados
