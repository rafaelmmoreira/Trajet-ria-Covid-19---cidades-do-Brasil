import matplotlib.pyplot as plt
import requests
import tkinter as tk
from time import sleep

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class App(tk.Tk):

    def __init__(self):
        self.baixaDados()
        super().__init__()
        self.title('Evolução Covid-19 no Brasil')
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side=tk.LEFT)
        self.frame2 = tk.Frame(self)
        self.frame2.pack(side=tk.LEFT)
        
        self.estados = [e for e in self.dados]
        self.estados.sort()
        self.estado = tk.StringVar()
        self.cidade = tk.StringVar()
        self.estado.set(self.estados[0])

        self.estadosOptionMenu = tk.OptionMenu(self.frame2, self.estado,
                                                    *self.estados,
            command=lambda x:self.interfaceAtualizaCidades())
        self.estadosOptionMenu.grid(row = 0, column = 1, sticky = tk.N)

        self.scrollbar = tk.Scrollbar(self.frame2)
        self.scrollbar.grid(row = 1, column = 2, sticky = tk.N + tk.S)

        self.fig = Figure(figsize=(10, 6), dpi=100)
        
        self.cidadesListbox = tk.Listbox(self.frame2)

        self.interfaceAtualizaCidades()
        self.cidadesListbox.grid(row = 1, column = 1, sticky = tk.N + tk.S)
        self.cidadesListbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.cidadesListbox.yview)   

        self.optVar = tk.IntVar()
        self.optVar.set(1)
        self.optCasos = tk.Radiobutton(self.frame2, text='Casos confirmados', 
                variable=self.optVar, value=1)
        self.optCasos.grid(row=27, column=1, sticky=tk.W)
        self.optObitos = tk.Radiobutton(self.frame2, text='Óbitos confirmados',
                variable=self.optVar, value=2)        
        self.optObitos.grid(row=28, column=1, sticky=tk.W)
        self.optAmbos = tk.Radiobutton(self.frame2, text='Ambos',
                variable=self.optVar, value=3)
        self.optAmbos.grid(row=29, column=1, sticky=tk.W)

        self.botaoC = tk.Button(self.frame2, text = 'Gerar gráfico da cidade',
                command = lambda: self.desenhaGrafico())
        self.botaoC.grid(row=30, column=1)

        self.botaoE = tk.Button(self.frame2, text = 'Gerar gráfico do estado',
                command = lambda: self.desenhaGrafico(True))
        self.botaoE.grid(row=31, column=1)

        self.botaoP = tk.Button(self.frame2, text = 'Gerar gráfico do Brasil',
                command = lambda: self.desenhaGrafico(False, True))
        self.botaoP.grid(row=32, column=1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.mainloop()
    
    def desenhaGrafico(self, porEstado=False, porPais=False, limpa=True):
        if self.optVar.get() == 1:
            opcao = 'casos'
            cor = 'blue'
        elif self.optVar.get() == 2:
            opcao = 'obitos'
            cor = 'red'
        else:
            self.optVar.set(1)
            self.desenhaGrafico(porEstado, porPais, True)
            self.optVar.set(2)
            self.desenhaGrafico(porEstado, porPais, False)
            self.optVar.set(3)
            return

        if porPais:
            casosBrasil = {}
            for e in self.dados:
                for c in self.dados[e]:
                    for i in range(len(self.dados[e][c]['datas'])):
                        if self.dados[e][c]['datas'][i] in casosBrasil:
                            casosBrasil[self.dados[e][c]['datas'][i]] += self.dados[e][c][opcao][i]
                        else:
                            casosBrasil[self.dados[e][c]['datas'][i]] = self.dados[e][c][opcao][i]

            tdatas = list(casosBrasil.keys())
            tdatas.sort()
            tcasos = []

            for d in tdatas:
                tcasos.append(casosBrasil[d])
                
        elif porEstado:
            casosEstado = {}
            for c in self.dados[self.estado.get()]:
                for i in range(len(self.dados[self.estado.get()][c]['datas'])):
                    if self.dados[self.estado.get()][c]['datas'][i] in casosEstado:
                        casosEstado[self.dados[self.estado.get()][c]['datas'][i]] += self.dados[self.estado.get()][c][opcao][i]
                    else:
                        casosEstado[self.dados[self.estado.get()][c]['datas'][i]] = self.dados[self.estado.get()][c][opcao][i]
       
            tdatas = list(casosEstado.keys())
            tdatas.sort()
            tcasos = []

            for d in tdatas:
                tcasos.append(casosEstado[d])
            
        else:
            tdatas = [x for x in self.dados[self.estado.get()][self.cidadesListbox.get(self.cidadesListbox.curselection())]['datas']]
            tcasos = [x for x in self.dados[self.estado.get()][self.cidadesListbox.get(self.cidadesListbox.curselection())][opcao]]
            tdatas.reverse()
            tcasos.reverse()
        tnovos = [0]

        if opcao == 'obitos':
            opcao = 'óbitos'

        if len(tcasos) > 2:
        # é possível estar faltando data... neste caso, a data é = 0
        # em casos assim, vamos considerar o número de casos do dia
        # anterior
            for i in range(1, len(tcasos)):
                if tcasos[i] < tcasos[i-1]:
                    tcasos[i] = tcasos[i-1]
        
        for i in range(1,len(tcasos)):
            tnovos.append(tcasos[i] - tcasos[i-1])

        while (len(tnovos)) <= 7:
            tcasos.insert(0, 0)
            tnovos.insert(0, 0)
            tdatas.insert(0, '')

        novossem = [0 for x in range(7)]
        
        for i in range(7, len(tcasos)):
            n = 0
            for j in range(7):
                n += tnovos[i-j]
            novossem.append(n)

        if limpa:
            self.fig.clf()
        else:
            opcao = 'casos/óbitos'
        ax = self.fig.add_subplot(111)
        ax.set_xlabel('Total de {} confirmados (até {})'.format(opcao, tdatas[-1]))
        ax.set_ylabel('Total de novos {} (por semana)'.format(opcao))
        if porPais:
            ax.set_title('Trajetória dos {} de COVID-19 no Brasil'.format(opcao))        
        elif porEstado:
            ax.set_title('Trajetória dos {} de COVID-19 em '.format(opcao) + self.estado.get())
        else:
            ax.set_title('Trajetória dos {} de COVID-19 em '.format(opcao) + self.cidadesListbox.get(self.cidadesListbox.curselection()))
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.grid(True)
        ax.plot([0]+tcasos, [0]+novossem, 'o-', color=cor, markersize=2)
        if not limpa:
            self.fig.legend(labels=['casos', 'óbitos'])
        self.canvas.draw()

    def baixaDados(self):
        req = requests.get('https://brasil.io/api/dataset/covid19/caso/data/?page_size=10000')
        self.dados = dict()
        pag = 1
        prox = True
        while prox:
            print('Buscando página ' + str(pag) + '...')
            if req.status_code == 200:
                req = req.json()
                for ocorrencia in req['results']:
                    estado = ocorrencia['state']
                    cidade = ocorrencia['city']
                    if estado != None and cidade != None:
                    
                        if estado not in self.dados:
                            self.dados[estado] = {}

                        if cidade not in self.dados[estado]:
                            self.dados[estado][cidade] = {
                                'casos':[],
                                'datas':[],
                                'obitos':[]
                                }
        
                        self.dados[estado][cidade]['casos'].append(ocorrencia['confirmed'])
                        self.dados[estado][cidade]['datas'].append(ocorrencia['date'])
                        self.dados[estado][cidade]['obitos'].append(ocorrencia['deaths'])
                        

                if req['next'] == None:
                    prox = False
                else:
                    url = req['next']
                    req = requests.get(url)
                    pag += 1
            elif req.status_code == 429:
                    # se estourou quantidade máxima de requests,
                    # dá uma folguinha pra API
                    sleep(10)
                    req = requests.get(url)
            else:
                print('Erro', req.status_code)
                break

    def interfaceAtualizaCidades(self):
        cidades = [c for c in self.dados[self.estado.get()]]
        cidades.sort()
        self.cidadesListbox.delete(0, tk.END)
        for c in cidades:
            self.cidadesListbox.insert(tk.END, c)
        self.cidade.set(cidades[0])

        
App()
