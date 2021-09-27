from utils import *
import time
from collections import deque


def bfs():
    env = Environment()
    start_time = time.time()
    counter = 1
    initial_state = env.state
    frontiers = deque()
    frontiers.append(Transaction(0, initial_state, None, None))
    visited_state = {initial_state}
    while True:
        if not len(frontiers):
            print('failure')
            return
        current_transaction = frontiers.popleft()
        env.set_state(current_transaction.state)

        # add neighbors to frontier
        for action in Actions.ACTION_LIST:
            frontier_state = env.take_action(action)
            if frontier_state:
                if frontier_state not in visited_state:
                    frontier_transaction = Transaction(current_transaction.cost + 1, frontier_state, current_transaction,
                                                       action)
                    if frontier_state.is_idle():
                        end_time = time.time()
                        print(f'done in {end_time - start_time} seconds')
                        print(f'Cost: {frontier_transaction.cost}')
                        print(f'Counter: {counter}')
                        print(f'States: {len(visited_state)}')
                        frontier_transaction.print_route()
                        return
                    frontiers.append(frontier_transaction)
                    visited_state.add(frontier_state)
                    counter += 1


if __name__ == "__main__":
    bfs()
