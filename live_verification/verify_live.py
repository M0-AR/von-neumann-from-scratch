"""Live verification entrypoint (imports tested live.py)."""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from vonneumann.live import fetch_yahoo, fetch_btc, fetch_fx
if __name__=="__main__":
    print("AAPL:",fetch_yahoo("AAPL")); print("BTC:",fetch_btc()); print("FX:",fetch_fx())
