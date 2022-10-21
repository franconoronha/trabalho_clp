ifeq ($(OS),Windows_NT)
    compile_command := g++ -fPIC --shared -static -o shared.dll shared.cpp
    run_command := python main.py
	install_command := pip install PyQt5
else
    compile_command := g++ -fPIC --shared -o shared.so shared.cpp
    run_command := python3 main.py
	install_command := sudo apt install python3-pyqt5
endif

install:
	$(install_command)
	$(compile_command)

compile:
	$(compile_command)

run:
	$(run_command)