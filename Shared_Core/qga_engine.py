import numpy as np
import pandas as pd
import yfinance as yf
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import random
import os
from datetime import datetime

# --- KALI INDIA DATA CONFIG ---
INDIAN_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS", 
    "TATAMOTORS.NS", "ITC.NS", "BAJFINANCE.NS", "SBIN.NS", "ADANIENT.NS"
]
BENCHMARK = "^NSEI" # NIFTY 50

def fetch_india_data(tickers=INDIAN_TICKERS):
    """
    Fetches historical data for Indian stocks. 
    Falls back to local CSV if live fetch fails.
    """
    try:
        data = yf.download(tickers + [BENCHMARK], period="1y")['Adj Close']
        if data.empty: raise ValueError("Empty data from yfinance")
        return data, "Live (NSE India)"
    except Exception as e:
        print(f"Live fetch failed ({e}), switching to local cache...")
        csv_path = "data/india_stocks_sample.csv"
        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            return data, "Offline Cache (Local)"
        else:
            # Last resort: Mock data if local cache is also missing
            mock_data = pd.DataFrame(
                np.random.rand(100, len(tickers) + 1) * 100, 
                columns=tickers + [BENCHMARK]
            )
            return mock_data, "Emergency Mock"

def calculate_metrics(data, tickers):
    """Calculates expected returns and risks for the given tickers."""
    returns_df = data[tickers].pct_change().dropna()
    avg_returns = returns_df.mean().values * 252 # Annualized
    risks = returns_df.std().values * np.sqrt(252) # Annualized Std Dev
    
    benchmark_returns = data[BENCHMARK].pct_change().dropna()
    benchmark_performance = benchmark_returns.mean() * 252
    
    return avg_returns, risks, benchmark_performance

# --- 1. Problem Formulation (Markowitz Portfolio Theory) ---
class PortfolioOptimizer:
    def __init__(self, n_assets: int, returns: np.ndarray, risks: np.ndarray):
        self.n_assets = n_assets
        self.returns = returns
        self.risks = risks

    def fitness(self, weights: np.ndarray, risk_aversion: float = 0.5) -> float:
        """
        Calculates fitness based on (Expected Return - Lambda * Risk).
        Weights are normalized to sum to 1.
        """
        # Normalize weights
        if np.sum(weights) == 0: return -1.0
        w = weights / np.sum(weights)
        expected_return = np.dot(w, self.returns)
        risk = np.sqrt(np.dot(w**2, self.risks**2))
        
        return expected_return - (risk_aversion * risk)

# --- 2. Quantum Genetic Algorithm (QGA) Implementation ---
class QGAEngine:
    def __init__(self, optimizer: PortfolioOptimizer, pop_size: int = 20, max_gen: int = 50):
        self.optimizer = optimizer
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.n = optimizer.n_assets
        
        # Quantum Population: Using theta to represent qubits (cos(theta), sin(theta))
        # Initialized to pi/4 for 50/50 probability
        self.theta = np.full((pop_size, self.n), np.pi/4)
        self.best_individual = None
        self.best_fitness = -float('inf')
        self.history = []

    def get_population(self):
        """Measures the qubits to get a binary population."""
        population = np.zeros((self.pop_size, self.n))
        for i in range(self.pop_size):
            for j in range(self.n):
                # Probability of being '1' is sin^2(theta)
                prob_one = np.sin(self.theta[i][j])**2
                population[i][j] = 1 if random.random() < prob_one else 0
        return population

    def update_theta(self, population, fitness_scores):
        """Update qubit phases based on the best individual."""
        local_best_idx = np.argmax(fitness_scores)
        local_best = population[local_best_idx]
        
        # If this generation's best is better than the global best, update global
        if fitness_scores[local_best_idx] > self.best_fitness:
            self.best_fitness = fitness_scores[local_best_idx]
            self.best_individual = local_best.copy()

        # Update each chromosome using rotation gate (delta_theta)
        for i in range(self.pop_size):
            for j in range(self.n):
                # Basic QGA rotation rule:
                # If pop[i][j] != best[j], rotate towards best[j]
                if population[i][j] != self.best_individual[j]:
                    delta = 0.05 * np.pi # Rotation step
                    if self.best_individual[j] == 1:
                        self.theta[i][j] += delta
                    else:
                        self.theta[i][j] -= delta
                
                # Boundary checks [0, pi/2]
                self.theta[i][j] = np.clip(self.theta[i][j], 0, np.pi/2)

    def run(self, risk_aversion: float = 0.5):
        for gen in range(self.max_gen):
            population = self.get_population()
            fitness_scores = [self.optimizer.fitness(ind, risk_aversion) for ind in population]
            
            self.update_theta(population, fitness_scores)
            self.history.append(self.best_fitness)
            
        return self.best_individual, self.best_fitness, self.history

# --- 3. Classical Benchmarks (GA, PSO, DE) ---
# Full benchmark implementations for comparison

class ClassicalGA:
    def __init__(self, optimizer: PortfolioOptimizer, pop_size: int = 20, max_gen: int = 50):
        self.optimizer = optimizer
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.n = optimizer.n_assets
        self.history = []

    def run(self, risk_aversion: float = 0.5):
        population = np.random.randint(2, size=(self.pop_size, self.n))
        best_fit = -float('inf')
        best_ind = None

        for gen in range(self.max_gen):
            fitness_scores = np.array([self.optimizer.fitness(ind, risk_aversion) for ind in population])
            
            idx = np.argmax(fitness_scores)
            if fitness_scores[idx] > best_fit:
                best_fit = fitness_scores[idx]
                best_ind = population[idx].copy()
            
            # Simple Selection, Crossover & Mutation
            new_pop = []
            for _ in range(self.pop_size):
                parent1 = population[random.randint(0, self.pop_size-1)]
                parent2 = population[random.randint(0, self.pop_size-1)]
                # One-point crossover
                pivot = self.n // 2
                child = np.concatenate([parent1[:pivot], parent2[pivot:]])
                # Mutation
                if random.random() < 0.1:
                    m_idx = random.randint(0, self.n-1)
                    child[m_idx] = 1 - child[m_idx]
                new_pop.append(child)
            
            population = np.array(new_pop)
            self.history.append(best_fit)
            
        return best_ind, best_fit, self.history

class ClassicalPSO:
    def __init__(self, optimizer: PortfolioOptimizer, pop_size: int = 20, max_gen: int = 50):
        self.optimizer = optimizer
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.n = optimizer.n_assets
        self.history = []

    def run(self, risk_aversion: float = 0.5):
        # PSO uses continuous positions [0, 1] then thresholds
        positions = np.random.rand(self.pop_size, self.n)
        velocities = np.random.rand(self.pop_size, self.n) * 0.1
        p_best = positions.copy()
        p_best_fit = np.array([self.optimizer.fitness(p > 0.5, risk_aversion) for p in positions])
        
        g_best_idx = np.argmax(p_best_fit)
        g_best = p_best[g_best_idx].copy()
        g_best_fit = p_best_fit[g_best_idx]

        w, c1, c2 = 0.7, 1.5, 1.5 # PSO Hyperparameters

        for gen in range(self.max_gen):
            for i in range(self.pop_size):
                r1, r2 = random.random(), random.random()
                velocities[i] = w*velocities[i] + c1*r1*(p_best[i] - positions[i]) + c2*r2*(g_best - positions[i])
                positions[i] = np.clip(positions[i] + velocities[i], 0, 1)
                
                current_fit = self.optimizer.fitness(positions[i] > 0.5, risk_aversion)
                if current_fit > p_best_fit[i]:
                    p_best_fit[i] = current_fit
                    p_best[i] = positions[i].copy()
                    if current_fit > g_best_fit:
                        g_best_fit = current_fit
                        g_best = positions[i].copy()
            
            self.history.append(g_best_fit)
            
        return (g_best > 0.5).astype(int), g_best_fit, self.history

class ClassicalDE:
    def __init__(self, optimizer: PortfolioOptimizer, pop_size: int = 20, max_gen: int = 50):
        self.optimizer = optimizer
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.n = optimizer.n_assets
        self.history = []

    def run(self, risk_aversion: float = 0.5):
        population = np.random.rand(self.pop_size, self.n)
        fitness_scores = np.array([self.optimizer.fitness(ind > 0.5, risk_aversion) for ind in population])
        
        best_idx = np.argmax(fitness_scores)
        best_fit = fitness_scores[best_idx]
        best_ind = population[best_idx].copy()

        F, CR = 0.8, 0.9 # DE Hyperparameters

        for gen in range(self.max_gen):
            for i in range(self.pop_size):
                # Mutation: x_new = a + F*(b - c)
                idxs = [idx for idx in range(self.pop_size) if idx != i]
                a, b, c = population[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + F*(b - c), 0, 1)
                
                # Crossover
                cross_points = np.random.rand(self.n) < CR
                if not np.any(cross_points): 
                    cross_points[np.random.randint(0, self.n)] = True
                trial = np.where(cross_points, mutant, population[i])
                
                # Selection
                trial_fit = self.optimizer.fitness(trial > 0.5, risk_aversion)
                if trial_fit > fitness_scores[i]:
                    population[i] = trial
                    fitness_scores[i] = trial_fit
                    if trial_fit > best_fit:
                        best_fit = trial_fit
                        best_ind = trial.copy()
            
            self.history.append(best_fit)
            
        return (best_ind > 0.5).astype(int), best_fit, self.history
