# Trajetória Covid-19 - cidades do Brasil
Acompanhamento da trajetória dos casos do Covid-19 por cidade brasileira individual usando a metodologia de Aatish Bhatia (https://aatishb.com/covidtrends/)

O site não mostra os casos no Brasil por estado, muito menos por cidade. Tive a ideia inicial de fazer para o estado de São Paulo usando um repositório oficial de dados - o projeto ainda está no ar em: https://github.com/rafaelmmoreira/Trajet-ria-do-Covid-19---S-o-Paulo
Mas após encontrar os dados excelentes do https://brasil.io/home/ resolvi expandir a ideia original.

## Sobre a metodologia:
É difícil visualizar tendências de desaceleração quando estamos no meio da curva exponencial. Portanto, o método proposto utiliza um gráfico relacionando o número total de casos x número de casos novos. Os casos novos são agrupados por semana para desprezar ruídos de variação diária e tornar o gráfico mais nítido, e os eixos são logarítmicos.

Durante o período de crescimento exponencial, o gráfico aproxima-se bastante de uma reta crescente. Conforme a doença desacelera, mesmo que seja uma tendência sutil de achatamento na curva exponencial original, este gráfico vai mostrar a reta curvando-se para a horizontal, e quando os casos começarem a cair, a reta tornará-se decrescente. Vale à pena ver os gráficos de alguns países diferentes no site original para entender melhor o gráfico. Também recomendo muito assistir o vídeo do canal minutephysics a respeito (https://www.youtube.com/watch?v=54XLXg4fYsc).

<p align="center"><img src="brasil.png"><br>Gráfico agrupando dados do Brasil todo<br><br></p>

<p align="center"><img src="sp.png"><br>Gráfico agrupando dados do Estado de São Paulo<br><br></p>

<p align="center"><img src="saopaulo.png"><br>Gráfico da cidade de São Paulo<br><br></p>

É importante notar que temos algumas limitações:

* 1) Gráficos logarítmicos distorcem os dados: uma pequena oscilação na taxa de crescimento da curva exponencial (aquela que aparece nas notícias) causará uma grande variação neste gráfico. Portanto, este gráfico é útil para mostrar tendências, não quantidades absolutas.

* 2) Em cidades onde o monitoramento começou recentemente, há poucos pontos no gráfico (afinal, conseguimos 1 ponto novo a cada semana), o que compromete bastante a visualização da tendência. Veja abaixo o gráfico de uma cidade do interior (Cachoeira Paulista - SP) com aproximadamente 1 caso novo reportado por semana nas últimas 2 semanas.

* 3) O programa usa dados oficiais para gerar o gráfico. É sabido que há uma grande quantidade de subnotificação de casos por falta de testes (https://drive.google.com/file/d/1_whlqZnGgvqHuWCG4-JyiL2X9WXpZAe3/view, https://covid19br.github.io/informacoes.html).

<p align="center"><img src="cachoeira.png"><br>Gráfico da cidade de Cachoeira Paulista-SP<br><br></p>

Em suma, esse programa é apenas (mais) uma ferramenta para visualizar as tendências dos dados oficiais em SP.

Se você é pesquisador, sinta-se à vontade para se modificar ou se inspirar nesse código para fazer outras análises ou estudar outras regiões.

Se você não é pesquisador, evite tirar e espalhar as suas próprias conclusões e confie nos pesquisadores! :)
