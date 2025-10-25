class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet, transitions, initial_state, accept_states, tape_input=""):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.reset(tape_input)

    def reset(self, tape_input=""):
        self.tape = list(tape_input) if tape_input else ['_']
        self.head = 0
        self.current_state = self.initial_state
        self.halted = False

    def step(self):
        if self.halted:
            return "Máquina detenida"

        symbol = self.tape[self.head]
        key = (self.current_state, symbol)

        if key not in self.transitions:
            self.halted = True
            return f"No hay transición para ({self.current_state}, {symbol})"

        new_state, write_symbol, move = self.transitions[key]
        self.tape[self.head] = write_symbol
        self.current_state = new_state

        if move == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append('_')
        elif move == 'L':
            if self.head > 0:
                self.head -= 1
            else:
                self.tape.insert(0, '_')
        else:
            pass

        if self.current_state in self.accept_states:
            self.halted = True
            return "Cadena aceptada ✅"

        return f"Estado: {self.current_state}, Cinta: {''.join(self.tape)}, Cabezal: {self.head}"