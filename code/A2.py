from utils import *
from utils import Transaction as OldTransaction
import time
from heapq import *


class Transaction(OldTransaction):

    @property
    def f(self):
        return self.cost + self.state.heuristic2

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.f == other.f

    def __le__(self, other):
        return self.f <= other.f

    def __ge__(self, other):
        return self.f >= other.f

    def __gt__(self, other):
        return self.f > other.f


def A1():
    env = Environment()
    start_time = time.time()
    counter = 1
    initial_state = env.state
    frontiers = []
    heappush(frontiers, Transaction(0, initial_state, None, None))
    visited_state = {initial_state: 0}

    while True:
        if not len(frontiers):
            print('failure')
            return
        current_transaction = heappop(frontiers)

        if current_transaction.state.is_idle():
            end_time = time.time()
            print(f'done in {end_time - start_time} seconds')
            print(f'Cost: {current_transaction.cost}')
            print(f'Counter: {counter}')
            print(f'States: {len(visited_state)}')
            current_transaction.print_route()
            return

        env.set_state(current_transaction.state)

        # add neighbors to frontier
        for action in Actions.ACTION_LIST:
            frontier_state = env.take_action(action)
            if frontier_state:
                counter += 1
                frontier_transaction = Transaction(current_transaction.cost + 1, frontier_state, current_transaction,
                                                   action)
                if frontier_state not in visited_state:
                    heappush(frontiers, frontier_transaction)
                    visited_state[frontier_state] = frontier_transaction.cost
                else:
                    prev_cost = visited_state[frontier_state]
                    if frontier_transaction.cost < prev_cost:
                        heappush(frontiers, frontier_transaction)
                        visited_state[frontier_state] = frontier_transaction.cost


if __name__ == "__main__":
    A1()
