import numpy as np

def simmulated_annealing(func, T, n_restarts = 5, min_T=1e-4):
    overall_best_x, overall_best_val, overall_best_history = None, -np.inf, []
    for _ in range(n_restarts):
        scale = np.sqrt(T)
        x = np.random.uniform(-1, 1)
        curr = func(x)
        best_val = curr
        best_x = x
        best_history = [x]
        history = [x]
        t = T

        for i in range(1000):
            prop = x + np.random.normal() * scale
            if prop > 1 or prop < -1:
                prop = x
            else:
                delta = func(prop) - curr
                if delta < 0 and np.log(np.random.rand()) > delta / t:
                    prop = x
            x = prop
            curr = func(x)
            t = 0.9 * t
            scale = np.sqrt(t)
            history.append(x)
            if curr > best_val:
                best_val = curr
                best_x = x
                best_history = history[:]
            if t < min_T:
                break
            if best_val > overall_best_val:
                overall_best_val = best_val
                overall_best_x = best_x
                overall_best_history = best_history
    return overall_best_x, overall_best_val, overall_best_history