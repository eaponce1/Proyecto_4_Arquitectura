"""Publica en el workspace el mismo BIN del proyecto activo, tras verificarlo."""
from pathlib import Path
import argparse
import hashlib
import shutil
import trader

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verificar',action='store_true');args=parser.parse_args()
    meta=trader.verify();workspace=trader.ROOT.parent;target=workspace/'competition.bin'
    if not args.verificar:
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=meta['sha256_bin']:
            backup=trader.ROOT/'respaldos'/('workspace_competition_'+hashlib.sha256(target.read_bytes()).hexdigest()+'.bin')
            if not backup.exists():shutil.copy2(target,backup)
        shutil.copy2(trader.ROOT/'competition.bin',target)
        shutil.copy2(trader.ROOT/'competition.sha256',workspace/'competition.sha256')
    assert hashlib.sha256(target.read_bytes()).hexdigest()==meta['sha256_bin']
    print('PASS imagen activa en',target)

if __name__=='__main__':main()
