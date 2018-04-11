# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import csv
import numpy


class Dado(object):
    def __init__(self,hora, idade, sexo, cidade, tipo=None, arma=None):
        super(Dado, self).__init__()
        self.hora = hora
        self.idade = idade
        self.sexo = sexo
        self.cidade = cidade
        self.tipo = tipo
        self.arma = arma

    def __iter__(self):
        return iter([self.hora,self.idade, self.sexo, self.cidade])

    def __sub__(self, other):
        return numpy.linalg.norm(numpy.array(list(self)) - numpy.array(list(other)))


class Dados(object):
    def __init__(self):
        super(Dados, self).__init__()

    def get_dados_regiao(self, regiao):

        CVLI = csv.DictReader(open('CVLI-Absoluto.csv'))

        abslt = []

        for row in CVLI:
            abslt.append(int(row[regiao]))

        # for i in abslt:
        # print("Sua Regiao: %s" % i)

        return abslt

    def get_dados_pe(self):
        CVLI = csv.DictReader(open('CVLI-Absoluto.csv'))
        peabs = []
        for row in CVLI:
            peabs.append(int(row["Pernambuco"]))

        # for i in peabs:
        # print("Pernambuco: %s" % i)

        return peabs


def plot_by_year(lista, regiao, dadospe):

    texto = '''
Nos gráficos você observa a quantidade absoluta de mortes por
Crimes Violentos Letais Intencionais (CVLI) de Pernambuco e da sua
região nos ultimos 10 anos.'''

    print(texto)
    plt.figure(1)

    plt.xlabel("Ano")
    plt.ylabel("Vitimas em regiao " + regiao)
    plt.title("CVLI em regiao %s" % (regiao))

    plt.plot([2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016], lista)

    plt.grid(True)

    plt.figure(2)

    plt.xlabel("Ano")
    plt.ylabel("Vitimas em Pernambuco")
    plt.title("CVLI em Pernambuco")

    plt.plot([2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016], dadospe)

    plt.grid(True)
    plt.show()


def menu():
    nome = raw_input('Qual o seu nome?\n')
    idade = raw_input(nome + ', qual a sua idade?\n')
    sexo = raw_input('Sexo(M/F):\n')

    while sexo != 'M' and sexo != 'm' and sexo != 'F' and sexo != 'f':
        sexo = raw_input('Sexo(M/F):\n')

    banner = '''
    1 -> Metropolitana
    2 -> Mata Norte
    3 -> Mata Sul
    4 -> Agreste Central
    5 -> Agreste Meridional
    6 -> Agreste Sententrional
    7 -> Sertão Central
    8 -> Sertão de Itaparica
    9 -> Sertão do Araripe
    10 -> Sertão do São Francisco
    11 -> Sertão do Moxotó
    12 -> Sertão do Pajeú
    '''
    print(banner)
    regiaoint = int(input(nome + ', em qual região você mora?\n'))

    while regiaoint >= 13 or regiaoint == 0:
        regiaoint = int(input(nome + ', em qual região você mora?\n'))

    regiao = ""
    if regiaoint == 1:
        regiao = "Metropolitana"
    elif regiaoint == 2:
        regiao = "Mata Norte"
    elif regiaoint == 3:
        regiao = "Mata Sul"
    elif regiaoint == 4:
        regiao = "Agreste Central"
    elif regiaoint == 5:
        regiao = "Agreste Meridional"
    elif regiaoint == 6:
        regiao = "Agreste Sententrional"
    elif regiaoint == 7:
        regiao = "Sertão Central"
    elif regiaoint == 8:
        regiao = "Sertão de Itaparica"
    elif regiaoint == 9:
        regiao = "Sertão do Araripe"
    elif regiaoint == 10:
        regiao = "Sertão do São Francisco"
    elif regiaoint == 11:
        regiao = "Sertão do Moxotó"
    elif regiaoint == 12:
        regiao = "Sertão do Pajeú"

    l = [regiao, nome, idade, sexo]

    return l


def knn(horauser,idadeuser, sexouser):
    dados = []

    with open('dados-al.csv') as f:
        read = f.read()
        read = read.split('\n')
        counter = 0
        for line in read:
            counter += 1
            if counter == 1:
                pass
            else:
                col = line.split(',')
                dados.append(
                    {"HORA": col[0], "IDADE": col[1], "SEXO": col[2], "TIPO": col[3], "ARMA": col[4], "CIDADE": col[5]})

    sexo = set()
    cidade = set()
    hora = set()
    for a in dados:
        sexo.add(a["SEXO"])
        cidade.add(a["CIDADE"])
        hora.add(a["HORA"])

    matriz = []

    sexo = list(sexo)
    cidade = list(cidade)

    matriz = []

    for i in dados:

        matriz.append(
            Dado(
                int(i["HORA"]) / 23,
                int(i["IDADE"]) / 100,
                sexo.index(i["SEXO"]),
                cidade.index(i["CIDADE"]) / (len(cidade) - 1),
                i["TIPO"],
                i["ARMA"]
            )
        )

    cara1 = Dado(horauser,idadeuser / 100, sexouser, 0.4375)

    distancias = []

    for i in matriz:
        distancias.append(i - cara1)

    distsort = [e for e in distancias]
    distsort.sort()

    # k=11

    k = []

    for a in range(1):
        k.append(distsort[a])

    arma = []
    tipo = []

    for b in k:
        indexk = distancias.index(b)
        matrizk = matriz[indexk]
        # print(matrizk.arma)
        arma.append(matrizk.arma)
        tipo.append(matrizk.tipo)

    if arma[0] == 'PAF':
        arma[0] = 'arma de fogo'
    if arma[0] == 'BRANCA':
        arma[0] = 'arma branca'

    return ('\nDe acordo com os dados da SDS, há bastante possibilidade de você morrer por %s por uma %s.' % (tipo[0], arma[0]))


def main():
    x = menu()
    regiao = x[0]
    nome = x[1]
    idade = x[2]
    sexo = x[3]
    dados = Dados()

    regional = dados.get_dados_regiao(regiao)
    dadospe = dados.get_dados_pe()

    if sexo == 'M' or sexo == 'm':
        sexo = 1
    elif sexo == 'F' or sexo == 'f':
        sexo = 0

    hora = int(input("\nQual hora você normalmente sai de casa? "))

    print(knn(hora,int(idade), sexo))

    plot_by_year(regional, regiao, dadospe)


if __name__ == '__main__':
    main()
