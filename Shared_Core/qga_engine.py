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
