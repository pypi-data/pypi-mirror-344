import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statistics import NormalDist

def between_prob(mu, sigma, greaterthan, lessthan):
    plt.figure(figsize=(10, 6))
    x= np.linspace(mu-4*sigma, mu+4*sigma, 100)
    plt.plot(x, stats.norm.pdf(x,mu,sigma), 'r')
    section=np.linspace(greaterthan,lessthan,100)
    plt.fill_between(section, stats.norm.pdf(section,mu,sigma))
    prob_ = NormalDist(mu=mu, sigma=sigma).cdf(lessthan) - NormalDist(mu=mu, sigma=sigma).cdf(greaterthan)
    print(f"Probability for x ≥ {greaterthan} and x ≤ {lessthan}: {prob_:.5f}")
    z1 = (greaterthan-mu)/sigma
    z2 = (lessthan-mu)/sigma
    print(f"Z-Score for {greaterthan}: {z1:.4f}")
    print(f"Z-Score for {lessthan}: {z2:.4f}")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Normal Distribution')
    plt.grid(True)
    plt.show()
    
def left_tail(mu, sigma, lessthan):
    plt.figure(figsize=(10, 6))
    x= np.linspace(mu-4*sigma, mu+4*sigma, 100)
    plt.plot(x, stats.norm.pdf(x,mu,sigma), 'r')
    section=np.linspace(min(x),lessthan,100)
    plt.fill_between(section, stats.norm.pdf(section,mu,sigma))
    prob_ = NormalDist(mu=mu, sigma=sigma).cdf(lessthan)
    print(f"Probability for x ≤ {lessthan}: {prob_:.5f}")
    z = (lessthan-mu)/sigma
    print(f"Z-Score for {lessthan}: {z:.4f}")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Normal Distribution')
    plt.grid(True)
    plt.show()

def right_tail(mu, sigma, greaterthan):
    plt.figure(figsize=(10, 6))
    x= np.linspace(mu-4*sigma, mu+4*sigma, 100)
    plt.plot(x, stats.norm.pdf(x,mu,sigma), 'r')
    section=np.linspace(greaterthan,max(x),100)
    plt.fill_between(section, stats.norm.pdf(section,mu,sigma))
    prob_ = 1 - NormalDist(mu=mu, sigma=sigma).cdf(greaterthan)
    print(f"Probability for x ≥ {greaterthan}: {prob_:.5f}")
    z = (greaterthan-mu)/sigma
    print(f"Z-Score for {greaterthan}: {z:.4f}")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Normal Distribution')
    plt.grid(True)
    plt.show()

def both_tails(mu, sigma, lessthan, greaterthan):
    plt.figure(figsize=(10, 6))
    x= np.linspace(mu-4*sigma, mu+4*sigma, 100)
    plt.plot(x, stats.norm.pdf(x,mu,sigma), 'r')
    section1=np.linspace(min(x),lessthan,100)
    section2=np.linspace(greaterthan,max(x),100)
    plt.fill_between(section1, stats.norm.pdf(section1,mu,sigma))
    plt.fill_between(section2, stats.norm.pdf(section2,mu,sigma), color='tab:blue')
    prob_l = NormalDist(mu=mu, sigma=sigma).cdf(lessthan)
    prob_r = 1 - NormalDist(mu=mu, sigma=sigma).cdf(greaterthan)
    prob_ = prob_l + prob_r
    print(f"Probability for x ≤ {lessthan} and x ≥ {greaterthan}: {prob_:.5f}")
    z1 = (lessthan-mu)/sigma
    z2 = (greaterthan-mu)/sigma
    print(f"Z-Score for {lessthan}: {z1:.4f}")
    print(f"Z-Score for {greaterthan}: {z2:.4f}")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Normal Distribution')
    plt.grid(True)
    plt.show()