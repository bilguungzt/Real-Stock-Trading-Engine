# Real-Stock-Trading-Engine
# Real-Time Stock Order Matching Simulation

## Overview
This project simulates a real-time stock trading environment, featuring functions to add stock orders (`Buy` or `Sell`) and match these orders efficiently. It's designed to handle concurrent transactions, mimicking the high-paced activity of stock exchanges.

## Features

- **Real-time Order Processing**: Orders are added and matched instantly based on market conditions.
- **Efficient Matching**: Utilizes heaps (priority queues) to quickly match buy and sell orders based on the best available prices.
- **Concurrent Execution**: Threads manage simultaneous operations safely, ensuring smooth and conflict-free transactions.
- **Simulation of Stock Transactions**: Randomly generates orders across 1,024 different stock tickers, representing active market scenarios.

## How It Works

### Adding Orders
The `addOrder` function takes the following parameters:
- `Order Type`: Buy or Sell
- `Ticker Symbol`: Represents one of 1,024 available stocks
- `Quantity`: Number of shares
- `Price`: Offered or asked price

Each order is placed into an efficient, sorted data structure specific to the stock ticker.

### Matching Orders
The `matchOrder` function automatically:
- Matches buy orders that are equal or higher than the lowest available sell price.
- Processes transactions immediately, ensuring fast-paced trading.
- Safely manages concurrent order modifications using threads, minimizing conflicts and race conditions.

## Technical Details

- **No external libraries for maps or dictionaries**: Entire logic built using basic language constructs (heaps, arrays, threads).
- **Thread Management**: Distinct threads manage subsets of tickers to ensure minimal contention and high performance.
- **Performance Optimization**: Designed for speed and real-time responsiveness, suitable for simulating real-world stock exchanges.

## Usage
Run the simulation to see real-time order additions and matching:
```bash
python stock.py
```

## Sample Output
```
Added Buy order for ticker 572: price=99.54, qty=8
Matched 27 units for ticker 138 at price 34.57
Simulation completed
```

## Contributions
Feel free to improve this simulation by submitting a pull request!

---

Enjoy exploring real-time stock trading simulation!


