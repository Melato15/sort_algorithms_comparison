# Relatório Técnico - Algoritmos de Ordenação com OpenTelemetry

## Alunos
Filipe Luiz Orlamünder, Guilherme Melato e Lucas M. Venero

## Introdução
Este documento apresenta a implementação e análise de algoritmos de ordenação utilizando o padrão Strategy. Os algoritmos são avaliados em diferentes cenários, e os resultados são registrados utilizando OpenTelemetry para posterior análise.

## Estrutura do Código
O código foi organizado em três principais seções:
1. **Geração de dados** - Cria conjuntos de números aleatórios e os armazena em um arquivo.
2. **Implementação dos algoritmos** - Cada algoritmo segue a abordagem do padrão Strategy para modularidade.
3. **Execução e comparação** - Mede desempenho dos algoritmos, registrando logs detalhados.

## Uso do Padrão Strategy
O padrão Strategy foi aplicado para desacoplar os algoritmos de ordenação. Cada algoritmo é implementado em uma classe separada, permitindo que possam ser usados intercambiavelmente sem modificação no restante do código.

## Processo de Geração de Dados
- Foi implementada uma classe `RandomNumberGenerator` para criar listas de números aleatórios.
- Os tamanhos suportados são parametrizáveis (ex: 1.000, 10.000, 100.000 números).
- Os dados gerados são salvos em um arquivo `data.txt`.

## Algoritmos Implementados
Foram implementados os seguintes algoritmos:

### Algoritmos Básicos
- **Bubble Sort**
- **Bubble Sort Melhorado**
- **Insertion Sort**
- **Selection Sort**

### Algoritmos Avançados 
- **Quick Sort**
- **Merge Sort**
- **Tim Sort**

### Outros Algoritmos
- **Shell Sort**

## Métricas Coletadas
Para cada execução, foram registradas as seguintes métricas:
- Tempo de execução (milissegundos)
- Quantidade de comparações
- Quantidade de trocas/movimentações
- Logs detalhados com OpenTelemetry

Os experimentos foram repetidos várias vezes para obter valores médios confiáveis.

## Ferramenta Utilizada para Logs e Análise
Os logs foram registrados utilizando **OpenTelemetry**, com a ferramenta **Jaeger** para visualização. Cada algoritmo gera eventos de comparação e troca, permitindo uma análise detalhada do comportamento dos algoritmos.

### Observação
Como não foi possível utilizar o Docker no computador da faculdade, usamos o Jaeger pelo CMD baixado do repositório disponível no link:
[https://github.com/jaegertracing/jaeger/releases](https://github.com/jaegertracing/jaeger/releases)

## Resultados e Análise
### Comparativo de Desempenho
Foram gerados gráficos comparando os tempos de execução, quantidade de comparações e movimentações para diferentes tamanhos de entrada.

## Conclusão
O **Tim Sort** apresentou melhor desempenho na maioria dos cenários devido à combinação de Merge Sort e Insertion Sort para pequenas partições. O **Quick Sort** também teve desempenho excelente, mas pode degradar em certos casos. Algoritmos básicos como Bubble Sort e Selection Sort tiveram tempos de execução significativamente mais altos, tornando-se inviáveis para grandes conjuntos de dados.

### Vale a pena usar Dividir e Conquistar?
Sim, algoritmos baseados em **Dividir e Conquistar** (Quick Sort, Merge Sort, Tim Sort) são claramente mais eficientes e escaláveis para grandes volumes de dados. Por esse motivo, são amplamente utilizados na prática.

## Dependências
Para rodar o código:
```sh
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-exporter-jaeger
pip install opentelemetry-semantic-conventions
```

## Para executar o código

> - Inicie o executável 'jaeger-all-in-one.exe' pelo cmd 
> - Rode o arquivo app.py com o comanddo 'py app.py'
> - Abra a interface na url http://localhost:16686
> - No dropdown 'Service', selecione a opção 'sorting_algorithms'
> - E aperte o botão 'Find Traces'
