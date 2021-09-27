class Actions:
    RIGHT_MOVE = 0
    LEFT_MOVE = 1
    UP_MOVE = 2
    DOWN_MOVE = 3

    ACTION_LIST = [DOWN_MOVE, RIGHT_MOVE, LEFT_MOVE, UP_MOVE]


class Transaction:
    def __init__(self, cost, state, parent, action):
        self.cost = cost
        self.parent = parent
        self.state = state
        self.action = action

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def print_route(self):
        if self.parent:
            self.parent.print_route()
        if self.action == Actions.RIGHT_MOVE:
            print('right')
        elif self.action == Actions.LEFT_MOVE:
            print('left')
        elif self.action == Actions.UP_MOVE:
            print('up')
        elif self.action == Actions.DOWN_MOVE:
            print('down')


class State:
    def __init__(self, ambulance_pos, patient_positions, hospitals):
        self.hospitals = hospitals
        self.ambulance_pos = ambulance_pos
        self.patient_positions = patient_positions

    def is_idle(self):
        return len(self.patient_positions) == 0

    def copy(self):
        return State(self.ambulance_pos, self.patient_positions.copy(), self.hospitals.copy())

    def __key(self):
        return tuple(self.hospitals), self.ambulance_pos, tuple(self.patient_positions)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    @property
    def heuristic1(self):
        h = 0
        for patient_pos in self.patient_positions:
            min_distance = 100
            for hospital in self.hospitals:
                hos_pos = hospital[0]
                distance = 0
                distance += abs(hos_pos[0] - patient_pos[0])
                distance += abs(hos_pos[1] - patient_pos[1])
                if distance < min_distance:
                    min_distance = distance
            h += min_distance

        for patient_pos in self.patient_positions:
            h += abs(patient_pos[0] - self.ambulance_pos[0])
            h += abs(patient_pos[1] - self.ambulance_pos[1])
        return h

    @property
    def heuristic2(self):
        h = 0
        for hospital in self.hospitals:
            hos_pos = hospital[0]
            for patient_pos in self.patient_positions:
                h += abs(hos_pos[0] - patient_pos[0])
                h += abs(hos_pos[1] - patient_pos[1])

        for patient_pos in self.patient_positions:
            h += abs(patient_pos[0] - self.ambulance_pos[0])
            h += abs(patient_pos[1] - self.ambulance_pos[1])
        return h

    @property
    def heuristic3(self):
        return len(self.patient_positions)


class Environment:
    def __init__(self):
        ambulance_pos = None
        patient_positions = []
        hospitals = []

        file_name = input('enter testcase file name: ')
        with open(f'../testcases/{file_name}') as f:
            lines = [l[:-1] for l in f.readlines()]

        self.world = []
        for line_num in range(len(lines)):
            line = lines[line_num]        
            row = list(line)
            for row_num in range(len(row)):
                item = row[row_num]
                position = (row_num, line_num)
                if item == 'P':
                    patient_positions.append(position)
                elif item == 'A':
                    ambulance_pos = position
                    row[row_num] = ' '
                elif item != '#' and item != ' ':
                    hospitals.append((position, int(item)))
            self.world.append(row)
            line_num += 1
        self.state = State(ambulance_pos, patient_positions, hospitals)

    def take_action(self, action):
        next_state = self.state.copy()
        amb_pos = self.state.ambulance_pos        
        if action == Actions.RIGHT_MOVE:
            next_pos = (amb_pos[0] + 1, amb_pos[1])
            patient_next_pos = (amb_pos[0] + 2, amb_pos[1])
        if action == Actions.LEFT_MOVE:
            next_pos = (amb_pos[0] - 1, amb_pos[1])
            patient_next_pos = (amb_pos[0] - 2, amb_pos[1])
        if action == Actions.UP_MOVE:
            next_pos = (amb_pos[0], amb_pos[1] - 1)
            patient_next_pos = (amb_pos[0], amb_pos[1] - 2)
        if action == Actions.DOWN_MOVE:
            next_pos = (amb_pos[0], amb_pos[1] + 1)
            patient_next_pos = (amb_pos[0], amb_pos[1] + 2)

        item = self._get_item_in_pos(next_pos)
        if item == '#':
            return None
        elif item == 'P':
            item = self._get_item_in_pos(patient_next_pos)
            if item == ' ':
                next_state.ambulance_pos = next_pos
                next_state.patient_positions.remove(next_pos)
                next_state.patient_positions.append(patient_next_pos)
            elif item == '#' or item == 'P':
                return None
            else:
                cap = int(item)
                next_state.ambulance_pos = next_pos
                next_state.patient_positions.remove(next_pos)
                next_state.hospitals.remove((patient_next_pos, cap))
                if cap > 1:
                    next_state.hospitals.append((patient_next_pos, cap-1))
        else:
            next_state.ambulance_pos = next_pos

        return next_state

    def set_state(self, state):
        for hospital in self.state.hospitals:
            self._set_item_in_pos(hospital[0], ' ')
        for hospital in state.hospitals:
            self._set_item_in_pos(hospital[0], str(hospital[1]))

        for pos in self.state.patient_positions:
            self._set_item_in_pos(pos, ' ')
        for pos in state.patient_positions:
            self._set_item_in_pos(pos, 'P')

        self.state = state
        
    def _set_item_in_pos(self, pos, item):
        self.world[pos[1]][pos[0]] = item
    
    def _get_item_in_pos(self, pos):
        return self.world[pos[1]][pos[0]]
