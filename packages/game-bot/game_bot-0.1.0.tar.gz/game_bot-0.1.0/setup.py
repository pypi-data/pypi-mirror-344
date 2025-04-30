from setuptools import setup, find_packages

setup(
    name='game_bot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pywin32>=305',
        'opencv-python>=4.8.0',
        'pytesseract>=0.3.10',
        'numpy>=1.24.0',
        'mss>=10.0.0'
    ],
    entry_points={
        'console_scripts': [
            'game-bot=src.python.picker:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ],
    platforms=['Windows'],
)