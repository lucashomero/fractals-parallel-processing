import matplotlib.pyplot as plt
import numpy as np
import random
import os
import threading
import time

# Função para gerar fractais usando um Sistema de Funções Iteradas (IFS)
def gerar_fractal(transformacoes, probabilidades, iteracoes=100000):
    if not abs(sum(probabilidades) - 1.0) < 1e-6:
        raise ValueError("As probabilidades devem somar 1.")

    x, y = 0.0, 0.0
    pontos = []

    for _ in range(iteracoes):
        r = random.random()
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                transformacao = transformacoes[i]
                break

        x, y = transformacao(x, y)
        pontos.append((x, y))

    return pontos

# Fractais (sem alteração)
def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    probabilidades = [1/3, 1/3, 1/3]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    plt.figure()
    plt.scatter(x_vals, y_vals, s=0.1, color='black', marker='.')
    plt.title("Triângulo de Sierpinski")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "sierpinski.png"), bbox_inches='tight', dpi=300)
    plt.close()

def samambaia_barnsley():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    probabilidades = [0.01, 0.85, 0.07, 0.07]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    plt.figure()
    plt.scatter(x_vals, y_vals, s=0.1, color='green', marker='.')
    plt.title("Samambaia de Barnsley")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "samambaia_barnsley.png"), bbox_inches='tight', dpi=300)
    plt.close()

# Outras funções de fractais (Mandelbrot, Julia, etc.) continuam iguais
# ...

# Lista com nome e função de cada fractal
fractais = [
    ("Triângulo de Sierpinski", sierpinski),
    ("Samambaia de Barnsley", samambaia_barnsley),
    ("Conjunto de Mandelbrot", mandelbrot),
    ("Conjunto de Julia", julia),
    ("Curva de Koch", koch_curve),
    ("Árvore Fractal", fractal_tree),
    ("Tapete de Sierpinski", sierpinski_carpet),
    ("Esponja de Menger", menger_sponge)
]

# Função que será executada em cada thread
def gerar_fractal_em_thread(nome, funcao):
    print(f"Iniciando: {nome}")
    funcao()
    print(f"Finalizado: {nome}")

# Função principal que cria threads e gera os fractais
def gerar_fractais_em_threads():
    threads = []
    inicio = time.time()

    # Criar uma thread para cada fractal
    for nome, funcao in fractais:
        t = threading.Thread(target=gerar_fractal_em_thread, args=(nome, funcao))
        t.start()
        threads.append(t)

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

    fim = time.time()
    print(f"Todos os fractais foram gerados em {fim - inicio:.2f} segundos.")

# Executa o programa
if __name__ == "__main__":
    gerar_fractais_em_threads()
