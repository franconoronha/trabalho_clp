compile:
	echo $(OS)
	g++ -fPIC --shared -o shared.dll shared.cpp
run:
	python main.py