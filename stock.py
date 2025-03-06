import threading
import heapq
import random
import time
import queue

# Order class to hold price and quantity


class Order:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

# OrderBook class with heaps and a lock


class OrderBook:
    def __init__(self):
        self.buy_orders = []  # Max-heap (negated prices)
        self.sell_orders = []  # Min-heap
        self.lock = threading.Lock()


# Initialize 1,024 order books
orderBooks = [OrderBook() for _ in range(1024)]
order_queues = [queue.Queue()
                for _ in range(1024)]  # Queues for matching signals

# Add an order to the order book


def addOrder(order_type, ticker, quantity, price):
    if not (0 <= ticker < 1024):
        raise ValueError("Ticker must be between 0 and 1023")
    if quantity <= 0 or price < 0:
        raise ValueError("Quantity must be positive, price non-negative")
    if order_type not in ["Buy", "Sell"]:
        raise ValueError("Order type must be 'Buy' or 'Sell'")

    order_book = orderBooks[ticker]
    with order_book.lock:
        new_order = Order(price, quantity)
        if order_type == "Buy":
            heapq.heappush(order_book.buy_orders, (-price, new_order))
        else:
            heapq.heappush(order_book.sell_orders, (price, new_order))
        print(
            f"Added {order_type} order for ticker {ticker}: price={price}, qty={quantity}")
    order_queues[ticker].put(1)  # Signal matching thread

# Match orders for a ticker


def matchOrder(ticker):
    order_book = orderBooks[ticker]
    with order_book.lock:
        while (order_book.buy_orders and order_book.sell_orders and
               -order_book.buy_orders[0][0] >= order_book.sell_orders[0][0]):
            buy_price, buy_order = order_book.buy_orders[0]
            sell_price, sell_order = order_book.sell_orders[0]
            matched_quantity = min(buy_order.quantity, sell_order.quantity)
            buy_order.quantity -= matched_quantity
            sell_order.quantity -= matched_quantity
            print(
                f"Matched {matched_quantity} units for ticker {ticker} at price {sell_price}")
            if buy_order.quantity == 0:
                heapq.heappop(order_book.buy_orders)
            if sell_order.quantity == 0:
                heapq.heappop(order_book.sell_orders)

# Matching worker thread


def matching_worker(tickers):
    while True:
        for ticker in tickers:
            if not order_queues[ticker].empty():
                order_queues[ticker].get()  # Consume signal
                matchOrder(ticker)

# Trading simulation thread


def simulate_trading(tickers, max_orders=100):
    orders_added = 0
    while orders_added < max_orders:
        ticker = random.choice(tickers)
        order_type = random.choice(["Buy", "Sell"])
        quantity = random.randint(1, 50)  # Smaller quantities to reduce load
        price = round(random.uniform(10.0, 100.0), 2)
        addOrder(order_type, ticker, quantity, price)
        orders_added += 1
        time.sleep(0.001)  # Minimal delay to prevent overwhelming


# Main execution
if __name__ == "__main__":
    num_threads = 10
    tickers_per_thread = 1024 // num_threads

    # Start matching threads
    matching_threads = []
    for i in range(num_threads):
        start_ticker = i * tickers_per_thread
        end_ticker = start_ticker + tickers_per_thread
        tickers = list(range(start_ticker, end_ticker))
        t = threading.Thread(target=matching_worker, args=(tickers,))
        t.daemon = True
        t.start()
        matching_threads.append(t)

    # Start trading threads
    trading_threads = []
    for i in range(num_threads):
        start_ticker = i * tickers_per_thread
        end_ticker = start_ticker + tickers_per_thread
        tickers = list(range(start_ticker, end_ticker))
        t = threading.Thread(target=simulate_trading,
                             args=(tickers, 50))  # Fewer orders
        t.start()
        trading_threads.append(t)

    # Wait for trading to complete
    for t in trading_threads:
        t.join()

    print("Simulation completed")
