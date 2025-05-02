# Ai Snake Programming Language

Ai Snake is a beginner-friendly programming language for creating AI models easily.

## Installation

To install Ai Snake, simply run:

```bash
pip install AiSnake
```

## Usage

After installation, you can run Ai Snake scripts or start an interactive REPL:

### Create and train an AI model:

```plaintext
ai_model m1 linear_regression
ai_train m1 [1, 2, 3, 4, 5] [2, 4, 6, 8, 10]
ai_predict m1 [6]
```

### Start REPL (Interactive Mode):

```bash
python -m ai_snake.interpreter
```

### Save and Load Models:

```plaintext
ai_save m1 "model1.joblib"
ai_load m2 "model1.joblib"
```

## Features
- Simple print statement support
- Easy project structure to extend further

## Project Structure

```
AiSnakeLanguage/
├── ai_snake/
├── examples/
└── tests/
```

## Run Example

```bash
python -m ai_snake.interpreter examples/hello_world.aisnake
```

## Output

```
Hello, Ai Snake!
```

## License

Ai Snake is open-source, released under the MIT license.