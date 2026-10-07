.PHONY: test reproduce live docker
test: ; pytest -q
reproduce: ; python scripts/run_all.py
live: ; python -c "import sys;sys.path.insert(0,'src');from vonneumann.live import *;print(fetch_yahoo('AAPL'),fetch_btc(),fetch_fx())"
docker: ; docker compose up --build
