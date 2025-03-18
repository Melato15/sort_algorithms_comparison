class MergeSort:
    def ordenar(self, dados):
        if len(dados) > 1:
            meio = len(dados) // 2
            esquerda = dados[:meio]
            direita = dados[meio:]

            esquerda = self.ordenar(esquerda)
            direita = self.ordenar(direita)

            return self.merge(esquerda, direita)
        else:
            return dados

    def merge(self, esquerda, direita):
        dados_ordenados = []
        while esquerda and direita:
            if esquerda[0] < direita[0]:
                dados_ordenados.append(esquerda.pop(0))
            else:
                dados_ordenados.append(direita.pop(0))
        dados_ordenados.extend(esquerda)
        dados_ordenados.extend(direita)
        return dados_ordenados
