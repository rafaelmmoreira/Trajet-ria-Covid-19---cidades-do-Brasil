import copy
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class App:

    def __init__(self):
        self.baixaDados()

        self.janela = tkinter.Tk()

        self.janela.title('Evolução Covid-19 no Brasil')
        self.frame1 = tkinter.Frame()
        self.frame1.pack(side=tkinter.LEFT)
        self.frame2 = tkinter.Frame()
        self.frame2.pack(side=tkinter.LEFT)
        
        self.estados = [e for e in self.dados]
        self.estados.sort()
        self.estado = tkinter.StringVar()
        self.cidade = tkinter.StringVar()
        self.estado.set(self.estados[0])

        self.estadosOptionMenu = tkinter.OptionMenu(self.frame2, self.estado,
                                                    *self.estados,
            command=lambda x:self.interfaceAtualizaCidades())
        self.estadosOptionMenu.grid(row = 0, column = 1, sticky = tkinter.N)

        self.scrollbar = tkinter.Scrollbar(self.frame2)
        self.scrollbar.grid(row = 1, column = 2, sticky = tkinter.N+tkinter.S)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.cidadesListbox = tkinter.Listbox(self.frame2)

        self.interfaceAtualizaCidades()
        self.cidadesListbox.grid(row = 1, column = 1, sticky = tkinter.N+tkinter.S)
        self.cidadesListbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.cidadesListbox.yview)   

        self.botaoC = tkinter.Button(self.frame2, text = 'Gerar gráfico da cidade',
                command = lambda: self.desenhaGrafico())
        self.botaoC.grid(row=30, column=1)

        self.botaoE = tkinter.Button(self.frame2, text = 'Gerar gráfico do estado',
                command = lambda: self.desenhaGrafico(True))
        self.botaoE.grid(row=31, column=1)

        self.botaoP = tkinter.Button(self.frame2, text = 'Gerar gráfico do Brasil',
                command = lambda: self.desenhaGrafico(False, True))
        self.botaoP.grid(row=32, column=1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame1)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.janela.mainloop()
    
    def desenhaGrafico(self, porEstado=False, porPais=False):
        if porPais:
            casosBrasil = {}
            for e in self.dados:
                for c in self.dados[e]:
                    for i in range(len(self.dados[e][c]['datas'])):
                        if self.dados[e][c]['datas'][i] in casosBrasil:
                            casosBrasil[self.dados[e][c]['datas'][i]] += self.dados[e][c]['casos'][i]
                        else:
                            casosBrasil[self.dados[e][c]['datas'][i]] = self.dados[e][c]['casos'][i]
       
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
                        casosEstado[self.dados[self.estado.get()][c]['datas'][i]] += self.dados[self.estado.get()][c]['casos'][i]
                    else:
                        casosEstado[self.dados[self.estado.get()][c]['datas'][i]] = self.dados[self.estado.get()][c]['casos'][i]
       
            tdatas = list(casosEstado.keys())
            tdatas.sort()
            tcasos = []

            for d in tdatas:
                tcasos.append(casosEstado[d])
        else:
            tdatas = copy.deepcopy(self.dados[self.estado.get()][self.cidadesListbox.get(self.cidadesListbox.curselection())]['datas'])
            tcasos = copy.deepcopy(self.dados[self.estado.get()][self.cidadesListbox.get(self.cidadesListbox.curselection())]['casos'])
            tdatas.reverse()
            tcasos.reverse()
        tnovos = [0]
        
        for i in range(1,len(tcasos)):
            tnovos.append(tcasos[i] - tcasos[i-1])

        while (len(tcasos)) % 7 != 0:
            tcasos.insert(0, 0)
            tnovos.insert(0, 0)
            tdatas.insert(0, '')
        tcasos.insert(0, 0)
        tnovos.insert(0, 0)
        tdatas.insert(0, '')

        totaissem = []
        novossem = []
        ultimadata = ''
        n = 0
        
        for i in range(len(tcasos)):
            if i % 7 == 0:
                ultimadata = tdatas[i]
                totaissem.append(tcasos[i])
                novossem.append(n)
                n = 0
            n += tnovos[i]

        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.set_xlabel('Total de casos confirmados (até {})'.format(ultimadata))
        ax.set_ylabel('Total de novos casos (por semana)')
        if porPais:
            ax.set_title('Trajetória dos casos de COVID-19 no Brasil')
        
        elif porEstado:
            ax.set_title('Trajetória dos casos de COVID-19 em ' + self.estado.get())
        else:
            ax.set_title('Trajetória dos casos de COVID-19 em ' + self.cidadesListbox.get(self.cidadesListbox.curselection()))
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.grid(True)
        ax.plot(totaissem, novossem, 'ro-')
        self.canvas.draw()

    def baixaDados(self):
        req = requests.get('https://brasil.io/api/dataset/covid19/caso/data/')
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
                                'datas':[]
                                }
        
                        self.dados[estado][cidade]['casos'].append(ocorrencia['confirmed'])
                        self.dados[estado][cidade]['datas'].append(ocorrencia['date'])
                        

                if req['next'] == None:
                    prox = False
                else:
                    url = req['next']
                    req = requests.get(url)
                    pag += 1
            else:
                print('Erro', req.status_code)
                break

    def interfaceAtualizaCidades(self):
        cidades = [c for c in self.dados[self.estado.get()]]
        cidades.sort()
        self.cidadesListbox.delete(0, tkinter.END)
        for c in cidades:
            self.cidadesListbox.insert(tkinter.END, c)
        self.cidade.set(cidades[0])

        
app = App()
