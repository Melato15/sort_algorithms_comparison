class QuickSort:
    def ordenar(self, dados):
        if len(dados) <= 1:
            return dados
        else:
            pivo = dados[0]
            menores = [x for x in dados[1:] if x <= pivo]
            maiores = [x for x in dados[1:] if x > pivo]
            return self.ordenar(menores) + [pivo] + self.ordenar(maiores)
