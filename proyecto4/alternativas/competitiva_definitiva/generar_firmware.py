"""Genera Assembly RV32E de la política congelada, sin modificar versiones previas."""
from estrategia import *
import hashlib

def main():
    c=frozen()
    assert c.family in ('momentum','dual','breakout','trailing') and c.exposure==100 and c.neutral==0
    assert c.fast<=256 and c.slow<=256 and c.review==8
    legacy=(HERE.parent/'agresiva/trade.s').read_text(encoding='utf-8')
    # Reuse independently validated binary greedy division and fill reconciliation.
    prefix=legacy[legacy.index('    lui   x1,'):legacy.index('\nCARTERA_LISTA:')]
    prefix=prefix.replace('    addi  x7, x0, 0','    addi  x7, x0, 1')
    entry=f'''
# x6=tick, x7=regimen. RAM[256..511] = 256 precios, un entero por tick.
# No se lee una celda antes de recibir el precio que representa.
CARTERA_LISTA:
    lw x10, 12(x1)
    lw x13, 16(x1)
    add x13, x3, x0
    beq x5, x0, GUARDAR_PICO
    lw x13, 1000(x0)
    bge x13, x3, GUARDAR_PICO
    add x13, x3, x0
GUARDAR_PICO:
    sw x13, 1000(x0)
    addi x11, x0, 0
    addi x12, x0, 0
    andi x9, x6, 255
    add x9, x9, x9
    add x9, x9, x9
    addi x9, x9, 1024
    addi x10, x0, {c.fast}
    blt x6, x10, SIN_RAPIDA
    addi x10, x9, {-4*c.fast}
    addi x10, x10, -1024
    andi x10, x10, 1023
    addi x10, x10, 1024
    lw x11, 0(x10)
    sub x11, x3, x11
SIN_RAPIDA:
    addi x10, x0, {c.slow}
    blt x6, x10, SIN_LENTA
    addi x10, x9, {-4*c.slow}
    addi x10, x10, -1024
    andi x10, x10, 1023
    addi x10, x10, 1024
    lw x12, 0(x10)
    sub x12, x3, x12
SIN_LENTA:
    sw x3, 0(x9)
    andi x10, x6, 7
    bne x10, x0, OBJETIVO
    addi x10, x0, {c.fast}
    blt x6, x10, OBJETIVO
    addi x10, x0, {-c.exit}
    bge x10, x11, SALIR
'''
    if c.family=='dual':
        entry+=f'''    addi x10, x0, {c.slow}
    blt x6, x10, ENTRADA
    addi x10, x0, {-c.gradual}
    bge x10, x12, SALIR
'''
    if c.family=='trailing':
        entry+=f'''    lw x13, 1000(x0)
    sub x13, x13, x3
    addi x10, x0, {c.stop}
    bge x13, x10, SALIR
'''
    entry+=f'''ENTRADA:
    addi x10, x0, {c.entry}
    blt x11, x10, OBJETIVO
'''
    if c.family in ('dual','breakout'):
        entry+='    blt x12, x0, OBJETIVO\n'
    if c.family=='breakout':
        entry+=f'''    addi x8, x0, 0
    addi x10, x0, {c.fast}
MAXIMO:
    addi x9, x9, -4
    addi x13, x0, 1024
    bge x9, x13, PUNTERO_OK
    addi x9, x9, 1024
PUNTERO_OK:
    lw x13, 0(x9)
    bge x8, x13, MAXIMO_OK
    add x8, x13, x0
MAXIMO_OK:
    addi x10, x10, -1
    bne x10, x0, MAXIMO
    blt x3, x8, OBJETIVO
'''
    entry+='''    addi x7, x0, 1
    jal x0, OBJETIVO
SALIR:
    addi x7, x0, 0
OBJETIVO:
    beq x7, x0, VENDER
    addi x2, x15, -5
    addi x9, x0, 63
    addi x4, x0, 0
    jal x0, RESOLVER_CANTIDAD
COMPRA_COTIZADA:
    beq x8, x0, MANTENER
    addi x4, x8, 64
    jal x0, EMITIR
VENDER:
    beq x5, x0, MANTENER
    addi x8, x0, 63
    bge x5, x8, VENTA_LIMITADA
    add x8, x5, x0
VENTA_LIMITADA:
    addi x4, x8, 128
    jal x0, EMITIR
MANTENER:
    addi x4, x0, 0
EMITIR:
    sw x4, 8(x1)
    addi x6, x6, 1
    jal x0, POLL_STATUS
'''
    text='# Política congelada: '+json.dumps(asdict(c))+'\n# Caja x15; acciones x5; orden pendiente x4.\n'+prefix+entry
    (HERE/'trade.s').write_text(text,encoding='utf-8')
    print('Assembly generado',c)

if __name__=='__main__':main()
