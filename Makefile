ifeq ($(OS),Windows_NT)
    compile_command := g++ -fPIC --shared -static -o shared.dll shared.cpp
    run_command := python main.py
else
    compile_command := g++ -fPIC --shared -o shared.so shared.cpp
    run_command := python3 main.py
endif

install:
	pip install PyQt5
	$(compile_command)

compile:
	$(compile_command)

run:
	$(run_command)