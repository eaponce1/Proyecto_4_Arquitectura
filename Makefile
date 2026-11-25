# Proyecto activo: Pochoco Trader, Go Board HX1K/VQ100.
# El Makefile del juego anterior se conserva en respaldos/antes_integracion_competitiva_20261125/.
PYTHON ?= python
.PHONY: all prog test verify
all:
	$(PYTHON) -B tools/trader.py build
verify:
	$(PYTHON) -B tools/trader.py verify
test:
	$(PYTHON) -B tools/trader.py test
prog: all
	$(PYTHON) -B tools/trader.py verify
	iceprog competition.bin
	iceprog -c competition.bin
