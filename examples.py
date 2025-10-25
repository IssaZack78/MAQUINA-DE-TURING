# examples.py

from turing_machine import TuringMachine

def get_unary_increment_machine():
    """
    Máquina de Turing que incrementa un número en unario.
    Ejemplo: '111' -> '1111'
    Alfabeto: {1}
    """
    states = {"q0", "q1", "q2", "q_accept"}
    input_alphabet = {"1"}
    tape_alphabet = {"1", "_"}
    start_state = "q0"
    accept_states = {"q_accept"}

    transitions = {
        # Mover a la derecha hasta encontrar el blanco
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "_"): ("q1", "1", "L"),

        # Retroceder a la última posición
        ("q1", "1"): ("q2", "1", "R"),

        # Aceptar
        ("q2", "1"): ("q_accept", "1", "N"),
        ("q2", "_"): ("q_accept", "_", "N"),
    }

    return TuringMachine(
        states,
        input_alphabet,
        tape_alphabet,
        transitions,
        start_state,
        accept_states
    )


def get_binary_palindrome_checker():
    """
    Verifica si una cadena binaria es palíndromo
    Ej: 101 -> Acepta | 110 -> Rechaza
    """
    states = {"q0", "q1", "q2", "q3", "q4", "q_accept"}
    input_alphabet = {"0", "1"}
    tape_alphabet = {"0", "1", "X", "_"}
    start_state = "q0"
    accept_states = {"q_accept"}

    transitions = {
        # Buscar el inicio y marcar
        ("q0", "0"): ("q1", "X", "R"),
        ("q0", "1"): ("q2", "X", "R"),
        ("q0", "X"): ("q_accept", "X", "N"),

        # Buscar último 0
        ("q1", "0"): ("q1", "0", "R"),
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q3", "_", "L"),
        ("q3", "0"): ("q0", "X", "L"),

        # Buscar último 1
        ("q2", "0"): ("q2", "0", "R"),
        ("q2", "1"): ("q2", "1", "R"),
        ("q2", "_"): ("q4", "_", "L"),
        ("q4", "1"): ("q0", "X", "L"),
    }

    return TuringMachine(
        states,
        input_alphabet,
        tape_alphabet,
        transitions,
        start_state,
        accept_states
    )


# Diccionario de ejemplos accesibles desde main.py
EXAMPLES = {
    "Unary Incrementador": get_unary_increment_machine,
    "Palíndromo binario": get_binary_palindrome_checker
}