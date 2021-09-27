from utils import *
import time
from collections import deque


def ids():
    env = Environment()
    start_time = time.time()
    initial_state = env.state
    counter = 1
    limit = 0
    while True:
        limit += 1
        frontiers = deque()
        frontiers.append(Transaction(0, initial_state, None, None))
        visited_state = {}
        while True:
            if not len(frontiers):
                break
            current_transaction = frontiers.pop()

            visited_state[current_transaction.state] = current_transaction.cost
            env.set_state(current_transaction.state)
            counter += 1

            # add neighbors to frontier
            if current_transaction.cost < limit:
                for action in Actions.ACTION_LIST:
                    frontier_state = env.take_action(action)
                    if frontier_state:
                        frontier_transaction = Transaction(current_transaction.cost + 1, frontier_state,
                                                           current_transaction,
                                                           action)
                        if frontier_state.is_idle():
                            end_time = time.time()
                            print(f'done in {end_time - start_time} seconds')
                            print(f'Cost: {frontier_transaction.cost}')
                            print(f'Counter: {counter}')
                            print(f'States: {len(visited_state)}')
                            frontier_transaction.print_route()
                            return

                        if frontier_state not in visited_state:
                            frontiers.append(frontier_transaction)
                        elif frontier_transaction.cost < visited_state[frontier_state]:
                            frontiers.append(frontier_transaction)
                            visited_state[frontier_state] = frontier_transaction.cost


if __name__ == "__main__":
    ids()
