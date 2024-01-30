# Kompilator

## O Projekcie

Projekt "Kompilator" został zrealizowany na potrzeby kursu _Języki Formalne i Techniki Translacji_.  
Jest to kompilator stworzony do obsługi prostego języka imperatywnego.

## Autor

#Piotr Zapała

## Technologie

- **Język programowania:** Python 3.11.6
- **Biblioteka:** PLY 3.11

## Wymagania

Aby korzystać z kompilatora, należy zainstalować wymagane pakiety za pomocą polecenia:

pip3 install ply

## Uruchamianie

Kompilator jest uruchamiany z linii komend. Poniżej znajduje się przykład użycia:

python3 Kompilator.py plik_wejściowy.imp plik_wyjściowy.mr

## Struktura Projektu

Projekt składa się z następujących plików:

- `Parser.py` - Odpowiedzialny za parsowanie.
- `Lexer.py` - Tworzenie tokenów.
- `Node.py` - Definicje węzłów drzewa AST (Abstract Syntax Tree).
- `AbstractSyntaxTree.py` - Pobieranie informacji z drzewa AST.
- `Debugger.py` - Sprawdzanie błędów w programach.
- `BasicBlocks.py` - Tworzenie bloków bazowych programu.
- `AssemblyCode.py` - Tworzenie kodu wynikowego.
