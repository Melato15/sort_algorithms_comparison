class ShellSort:
    def ordenar(self, dados):
        n = len(dados)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = dados[i]
                j = i
                while j >= gap and dados[j - gap] > temp:
                    dados[j] = dados[j - gap]
                    j -= gap
                dados[j] = temp
            gap //= 2
        return dados
