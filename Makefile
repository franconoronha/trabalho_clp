ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    target := shared.dll
else
    detected_OS := $(shell uname)  # same as "uname -s"
	ifeq (detected_OS, Darwin)
		target := shared.dylib
	else
		target := shared.so
	endif
endif

install:
	pip install PyQt5
	g++ -fPIC --shared -static -o shared.dll shared.cpp

compile:
	g++ -fPIC --shared -static -o shared.dll shared.cpp

run:
	python main.py

