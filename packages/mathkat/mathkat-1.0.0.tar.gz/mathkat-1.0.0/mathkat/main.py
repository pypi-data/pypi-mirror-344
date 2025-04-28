import numpy as np
from rich.table import Table
from rich.console import Console
import functools
from dataclasses import dataclass, field

console = Console()

def imprimir_tabla(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        resultado = func(self, *args, **kwargs)
        if hasattr(self, 'data'):
            nombre_func = func.__name__

            match nombre_func:
                case "simple":
                    headers = ["Iteración", "x", "Norma"]
                case "momentum":
                    headers = ["Iteración", "x", "Norma", "velocidad"]
                case "nesterov":
                    headers = ["Iteración", "x", "Norma", "velocidad"]
            table = Table(title=f"[bold magenta]Resultados de {nombre_func.capitalize()}[/bold magenta]", show_lines=True)
            for header in headers:
                table.add_column(header.upper(), justify="center", style="yellow", no_wrap=True)
            for row in self.data:
                table.add_row(*[str(x) for x in row])
            console.print(table)
        return resultado
    return wrapper

@dataclass
class Gradiente:
    """
    Clase que representa una función objetivo y sus métodos de optimización mediante descenso de gradiente.
    Permite aplicar diferentes variantes del descenso de gradiente y visualizar los resultados en tablas.
    """

    f : callable
    grad_f : callable
    x_0 : np.ndarray
    v_0 : np.ndarray
    alpha : float
    iteraciones : int
    epsilon : float
    eta : float
    x_historico : list = field(default_factory=list, init=False)
    data : list = field(default_factory=list, init=False)

    

    @imprimir_tabla
    def simple(self):
        """
        Realiza el descenso de gradiente estándar para minimizar la función objetivo.
        En cada iteración, actualiza la posición usando el gradiente y almacena el historial de posiciones y normas.
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        lr = self.alpha
        max_iters = self.iteraciones
        epsilon = self.epsilon
        self.x_historico = [x0]
        
        for i in range(max_iters):
            f_i = f(*x0)
            grad_f_i = grad_f(*x0)
            nomra_grad = np.linalg.norm(grad_f_i)
            if nomra_grad < epsilon: 
                break
            xi = x0 - lr * grad_f_i
            x0 = xi.copy()
            self.x_historico.append(x0)
            self.data.append((i+1, x0.tolist(), nomra_grad))
        return self.x_historico


    @imprimir_tabla
    def momentum(self):
        """
        Aplica el método de descenso de gradiente con momentum para minimizar la función objetivo.
        Utiliza un término de velocidad para acelerar la convergencia y almacena el historial de posiciones, normas y velocidades.
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        v0 = self.v_0
        lr = self.alpha
        eta = self.eta
        max_iters = self.iteraciones
        epsilon = self.epsilon
        self.x_historico = [x0]
        
        for i in range(max_iters):
            f_i = f(*x0)
            grad_f_i = grad_f(*x0)
            nomra_grad = np.linalg.norm(grad_f_i)
            if nomra_grad < epsilon: # Criterio de paro 
                break
            vi = eta * v0 + lr * grad_f_i
            xi = x0 - vi
            x0 = xi.copy()
            v0 = vi.copy()
            self.x_historico.append(x0)
            self.data.append((i+1, x0.tolist(), nomra_grad, vi.tolist()))
        return self.x_historico
    
    
    @imprimir_tabla
    def nesterov(self):
        """
        Aplica el método de descenso de gradiente con Nesterov para minimizar la función objetivo.
        Utiliza un término de velocidad y calcula el gradiente en la posición adelantada (lookahead).
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        v0 = self.v_0
        lr = self.alpha
        eta = self.eta
        max_iters = self.iteraciones
        epsilon = self.epsilon
        x_historico = [x0]
        data_grad_nesterov = []
        
        for i in range(max_iters):
            lookahead = x0 - eta * v0
            grad_f_i = grad_f(*lookahead)
            norm_grad = np.linalg.norm(grad_f_i)
            if norm_grad < epsilon:
                break
            vi = eta * v0 + lr * grad_f_i
            xi = x0 - vi
            x0 = xi.copy()
            v0 = vi.copy()
            x_historico.append(x0)
            data_grad_nesterov.append((i+1, x0.tolist(), norm_grad, vi.tolist()))
        return x_historico