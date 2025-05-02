# ai_snake/interpreter.py

import sys
from ai_snake.parser import parse_code
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# Store variables here
variables = {}
models = {}

def evaluate_expression(expr):
    """
    Evaluates a simple expression (supports +, -, *, / and variables)
    """
    tokens = expr.split()
    result = 0
    current_op = None

    def get_value(token):
        if token.isdigit():
            return int(token)
        elif token in variables:
            return variables[token]
        else:
            raise ValueError(f"Unknown variable or value: {token}")

    for token in tokens:
        if token in ['+', '-', '*', '/']:
            current_op = token
        else:
            value = get_value(token)
            if current_op is None:
                result = value
            else:
                if current_op == '+':
                    result += value
                elif current_op == '-':
                    result -= value
                elif current_op == '*':
                    result *= value
                elif current_op == '/':
                    result /= value
                current_op = None
    return result

def parse_list(list_str):
    """
    Converts '[1,2,3]' into [1,2,3]
    """
    list_str = list_str.strip()
    if list_str.startswith('[') and list_str.endswith(']'):
        items = list_str[1:-1].split(',')
        return [int(item.strip()) for item in items]
    else:
        raise ValueError(f"Invalid list format: {list_str}")

def execute(parsed_code):
    for line in parsed_code:
        execute_line(line)

def execute_line(line):
    line = line.strip()
    if line.startswith('let '):
        parts = line[4:].split('=')
        var_name = parts[0].strip()
        expr = parts[1].strip()
        value = evaluate_expression(expr)
        variables[var_name] = value

    elif line.startswith('print '):
        expr = line[6:].strip()
        value = evaluate_expression(expr)
        print(value)

    elif line.startswith('ai_model '):
        parts = line.split()
        model_name = parts[1]
        model_type = parts[2]

        if model_type == 'linear_regression':
            models[model_name] = LinearRegression()
            print(f"[INFO] Created Linear Regression model '{model_name}'")
        else:
            print(f"[ERROR] Unknown model type: {model_type}")

    elif line.startswith('ai_train '):
        parts = line.split(' ', 3)
        model_name = parts[1]
        X_list = parse_list(parts[2])
        Y_list = parse_list(parts[3])

        X = np.array(X_list).reshape(-1, 1)
        Y = np.array(Y_list)

        model = models.get(model_name)
        if model:
            model.fit(X, Y)
            print(f"[INFO] Trained model '{model_name}'")
        else:
            print(f"[ERROR] Model '{model_name}' not found")

    elif line.startswith('ai_predict '):
        parts = line.split(' ', 2)
        model_name = parts[1]
        X_list = parse_list(parts[2])
        X = np.array(X_list).reshape(-1, 1)

        model = models.get(model_name)
        if model:
            prediction = model.predict(X)
            print(f"[PREDICT] {prediction.tolist()}")
        else:
            print(f"[ERROR] Model '{model_name}' not found")

    elif line.startswith('ai_save '):
        parts = line.split(' ', 2)
        model_name = parts[1]
        file_path = parts[2].strip().strip('"')

        model = models.get(model_name)
        if model:
            joblib.dump(model, file_path)
            print(f"[INFO] Saved model '{model_name}' to '{file_path}'")
        else:
            print(f"[ERROR] Model '{model_name}' not found")

    elif line.startswith('ai_load '):
        parts = line.split(' ', 2)
        model_name = parts[1]
        file_path = parts[2].strip().strip('"')

        model = joblib.load(file_path)
        models[model_name] = model
        print(f"[INFO] Loaded model into '{model_name}' from '{file_path}'")

    elif line == '':
        return  # skip empty lines

    else:
        print(f"[ERROR] Unknown command: {line}")

def start_repl():
    print("Ai Snake REPL — Type 'exit' to quit")
    while True:
        try:
            line = input(">> ")
            if line.strip() == 'exit':
                print("Exiting REPL.")
                break
            execute_line(line)
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    if len(sys.argv) == 1:
        # No file → start REPL
        start_repl()

    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            code = file.read()

        parsed_code = parse_code(code)
        execute(parsed_code)

    else:
        print("Usage:")
        print("  python -m ai_snake.interpreter            # Start REPL")
        print("  python -m ai_snake.interpreter file.aisnake  # Run file")
        sys.exit(1)

if __name__ == "__main__":
    main()