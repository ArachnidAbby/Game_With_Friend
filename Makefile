env/bin/activate: requirements.txt
	python3.11 -m venv env
	./env/bin/pip3.11 install -r requirements.txt

run: env/bin/activate
	./env/bin/python3.11 src/main.py

compile: env/bin/activate
	./env/bin/python3.11 -m nuitka --follow-imports --experimental=python3.11 src/main.py

profile_cpu: env/bin/activate
	./env/bin/python3.11 -m cProfile -o tests/random/program.prof src/main.py hmmmm
	./env/bin/snakeviz tests/random/program.prof

clean:
	rm -rf __pycache__
	rm -rf env
	rm -rf main.build/