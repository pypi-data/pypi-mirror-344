from setuptools import setup, find_packages

setup(
    name='AiSnake',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
        'joblib',
    ],
    entry_points={
        'console_scripts': [
            'ai_snake = ai_snake.interpreter:main',
        ],
    },
    description='A beginner-friendly programming language focused on AI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='K. Mohammed Imran',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/AiSnake',
)