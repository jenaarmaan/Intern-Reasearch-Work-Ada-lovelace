import numpy as np
import pandas as pd
import yfinance as yf
import random
import os
from datetime import datetime

# --- KALI INDIA DATA CONFIG ---
# 15 Specific NSE Tickers for the BEE Dashboard
INDIAN_STOCK_MAP = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "WIPRO.NS": "Wipro",
    "TATAMOTORS.NS": "Tata Motors",
    "ITC.NS": "ITC Limited",
    "BAJFINANCE.NS": "Bajaj Finance",
    "SBIN.NS": "State Bank of India",
    "ADANIENT.NS": "Adani Enterprises",
    "MARUTI.NS": "Maruti Suzuki",
    "SUNPHARMA.NS": "Sun Pharma",
    "AXISBANK.NS": "Axis Bank",
    "LTIM.NS": "LTIMindtree",
    "NESTLEIND.NS": "Nestle India"
}

INDIAN_TICKERS = list(INDIAN_STOCK_MAP.keys())
BENCHMARK = "^NSEI" # NIFTY 50

# Sector mapping for the Sector Breakdown chart
SECTOR_MAP = {
    "RELIANCE.NS": "Energy",
    "TCS.NS": "IT",
    "INFY.NS": "IT",
    "HDFCBANK.NS": "Banking",
    "WIPRO.NS": "IT",
    "TATAMOTORS.NS": "Auto",
    "ITC.NS": "FMCG",
    "BAJFINANCE.NS": "Finance",
    "SBIN.NS": "Banking",
    "ADANIENT.NS": "Energy/Conglomerate",
    "MARUTI.NS": "Auto",
    "SUNPHARMA.NS": "Pharma",
    "AXISBANK.NS": "Banking",
    "LTIM.NS": "IT",
    "NESTLEIND.NS": "FMCG"
}

def fetch_india_data(tickers=INDIAN_TICKERS):
    """
    Fetches historical data for Indian stocks. 
    Falls back to local CSV if live fetch fails.
    """
    try:
        data = yf.download(tickers + [BENCHMARK], period="1y")['Adj Close']
        if data.empty: raise ValueError("Empty data from yfinance")
        # Save a local cache copy whenever fetch succeeds
        if not os.path.exists("data"): os.makedirs("data")
        data.to_csv("data/india_stocks_1yr.csv")
        return data, "Live (NSE India)"
    except Exception as e:
        print(f"Live fetch failed ({e}), switching to local cache...")
        csv_path = "data/india_stocks_1yr.csv"
        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            return data, "Offline Cache (Local)"
        else:
            # Last resort: Mock data if local cache is also missing
            mock_data = pd.DataFrame(
                np.random.rand(252, len(tickers) + 1) * 100, 
                columns=tickers + [BENCHMARK],
                index=pd.date_range(end=datetime.now(), periods=252)
            )
            return mock_data, "Emergency Mock"

def calculate_advanced_metrics(weights, returns_df):
    """
    Calculates Sharpe, Sortino, and Max Drawdown for the portfolio.
    Returns are in INR.
    """
    if np.sum(weights) == 0: return 0, 0, 0
    w = weights / np.sum(weights)
    
    # Portfolio Returns
    portfolio_daily_returns = (returns_df * w).sum(axis=1)
    
    # Sharpe Ratio (Rf = 0 for simplicity)
    ann_return = portfolio_daily_returns.mean() * 252
    ann_vol = portfolio_daily_returns.std() * np.sqrt(252)
    sharpe = ann_return / ann_vol if ann_vol != 0 else 0
    
    # Sortino Ratio (Downside deviation)
    downside_returns = portfolio_daily_returns[portfolio_daily_returns < 0]
    ann_downside_vol = downside_returns.std() * np.sqrt(252)
    sortino = ann_return / ann_downside_vol if ann_downside_vol != 0 else 0
    
    # Max Drawdown
    cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    max_dd = drawdown.min()
    
    return round(sharpe, 2), round(sortino, 2), round(max_dd * 100, 2)

def calculate_metrics(data, tickers):
    """Compatibility alias for Assignment 1 Technical Report."""
    returns_df = data[tickers].pct_change().dropna()
    avg_returns = returns_df.mean().values * 252
    risks = returns_df.std().values * np.sqrt(252)
    benchmark_returns = data[BENCHMARK].pct_change().dropna()
    benchmark_performance = benchmark_returns.mean() * 252
    return avg_returns, risks, benchmark_performance

# --- Problem Formulation (Markowitz Portfolio Theory) ---
class PortfolioOptimizer:
    def __init__(self, n_assets: int, returns: np.ndarray, risks: np.ndarray):
        self.n_assets = n_assets
        self.returns = returns
        self.risks = risks

    def fitness(self, weights: np.ndarray, risk_aversion: float = 0.5) -> float:
        if np.sum(weights) == 0: return -1.0
        w = weights / np.sum(weights)
        expected_return = np.dot(w, self.returns)
        risk = np.sqrt(np.dot(w**2, self.risks**2))
        return expected_return - (risk_aversion * risk)

# --- Quantum Genetic Algorithm (QGA) Implementation ---
class QGAEngine:
    def __init__(self, optimizer: PortfolioOptimizer, pop_size: int = 20, max_gen: int = 50):
        self.optimizer = optimizer
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.n = optimizer.n_assets
        self.theta = np.full((pop_size, self.n), np.pi/4)
        self.best_individual = None
        self.best_fitness = -float('inf')
        self.history = []

    def get_population(self):
        population = np.zeros((self.pop_size, self.n))
        for i in range(self.pop_size):
            for j in range(self.n):
                prob_one = np.sin(self.theta[i][j])**2
                population[i][j] = 1 if random.random() < prob_one else 0
        return population

    def update_theta(self, population, fitness_scores):
        local_best_idx = np.argmax(fitness_scores)
        local_best = population[local_best_idx]
        if fitness_scores[local_best_idx] > self.best_fitness:
            self.best_fitness = fitness_scores[local_best_idx]
            self.best_individual = local_best.copy()

        for i in range(self.pop_size):
            for j in range(self.n):
                if population[i][j] != self.best_individual[j]:
                    delta = 0.05 * np.pi
                    if self.best_individual[j] == 1:
                        self.theta[i][j] += delta
                    else:
                        self.theta[i][j] -= delta
                self.theta[i][j] = np.clip(self.theta[i][j], 0, np.pi/2)

    def run(self, risk_aversion: float = 0.5):
        for gen in range(self.max_gen):
            population = self.get_population()
            fitness_scores = [self.optimizer.fitness(ind, risk_aversion) for ind in population]
            self.update_theta(population, fitness_scores)
            self.history.append(self.best_fitness)
        return self.best_individual, self.best_fitness, self.history

# --- Classical Benchmarks (GA, PSO, DE) for technical reports ---

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
            new_pop = []
            for _ in range(self.pop_size):
                parent1 = population[random.randint(0, self.pop_size-1)]
                parent2 = population[random.randint(0, self.pop_size-1)]
                pivot = self.n // 2
                child = np.concatenate([parent1[:pivot], parent2[pivot:]])
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
        positions = np.random.rand(self.pop_size, self.n)
        velocities = np.random.rand(self.pop_size, self.n) * 0.1
        p_best = positions.copy()
        p_best_fit = np.array([self.optimizer.fitness(p > 0.5, risk_aversion) for p in positions])
        g_best_idx = np.argmax(p_best_fit)
        g_best = p_best[g_best_idx].copy()
        g_best_fit = p_best_fit[g_best_idx]
        w, c1, c2 = 0.7, 1.5, 1.5
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
        F, CR = 0.8, 0.9
        for gen in range(self.max_gen):
            for i in range(self.pop_size):
                idxs = [idx for idx in range(self.pop_size) if idx != i]
                a, b, c = population[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + F*(b - c), 0, 1)
                cross_points = np.random.rand(self.n) < CR
                if not np.any(cross_points): 
                    cross_points[np.random.randint(0, self.n)] = True
                trial = np.where(cross_points, mutant, population[i])
                trial_fit = self.optimizer.fitness(trial > 0.5, risk_aversion)
                if trial_fit > fitness_scores[i]:
                    population[i] = trial
                    fitness_scores[i] = trial_fit
                    if trial_fit > best_fit:
                        best_fit = trial_fit
                        best_ind = trial.copy()
            self.history.append(best_fit)
        return (best_ind > 0.5).astype(int), best_fit, self.history
