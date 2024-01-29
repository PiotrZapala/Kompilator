# Kompilator

Projekt realizowany na potrzebę kursu Języki Formalne i Techniki Translacji

Autor: Piotr Zapała

Wykorzystane narzędzia: Python 3.11.6, PLY 3.11

Wymagania: pip3 install ply

Uruchamianie:
python3 Kompilator.py plik_wejściowy.imp plik_wyjściowy.mr

Pliki wchodzące w skład projektu:

- Parser.py : parsowanie

- Lexer.py : tworzenie tokenów

- Node.py : definicje węzłów drzewa AST

- AbstractSyntaxTree.py : pobieranie informacji z drzewa AST

- Debugger.py : sprawdzanie błędów w programach

- BasicBlocks.py : tworzenie bloków bazowych programu

- AssemblyCode.py : tworzenie kodu wynikowego
