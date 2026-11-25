# Pochoco Trader: tendencia de 128 ticks confirmada por SMA10.
# x1 MMIO, x4 orden pendiente (reutilizado al resolver un fill), x5 inventario,
# x6 tick mod 128, x7 precio de la última revisión, x15 caja.
# x2, x3 y x8–x14 son temporales. No hay MUL, DIV ni shifts.
    lui   x1, 0x80010
    addi  x4, x0, 0
    addi  x5, x0, 0
    addi  x6, x0, 0
    addi  x7, x0, 0
    lui   x15, 2
    addi  x15, x15, 1808

POLL_STATUS:
    lw    x2, 0(x1)
    andi  x2, x2, 1
    beq   x2, x0, POLL_STATUS
    lw    x3, 4(x1)
    andi  x9, x4, 63
    beq   x9, x0, CARTERA_LISTA
    andi  x4, x4, 192
    addi  x10, x0, 64
    beq   x4, x10, APLICAR_COMPRA
    addi  x10, x0, 128
    bne   x4, x10, CARTERA_LISTA

    # La maestra recorta la venta al inventario disponible.
    bge   x5, x9, PRESUPUESTO_VENTA
    add   x9, x5, x0
PRESUPUESTO_VENTA:
    lui   x2, 4               # 16.384 cubre 63 * 255
    jal   x0, RESOLVER_CANTIDAD

APLICAR_COMPRA:
    addi  x2, x15, -5
    jal   x0, RESOLVER_CANTIDAD

# Greedy binario: mayor cantidad <= x9 que cabe en x2, a precio x3.
# x4: 64 para compra ejecutada, 128 para venta ejecutada, 0 para cotizar.
# x8 devuelve la cantidad y x2 queda con el presupuesto no utilizado.
RESOLVER_CANTIDAD:
    addi  x8, x0, 0
    add   x10, x3, x3
    add   x11, x10, x10
    add   x12, x11, x11
    add   x13, x12, x12
    add   x14, x13, x13

    addi  x9, x9, -32
    blt   x9, x0, DESHACER_32
    blt   x2, x14, DESHACER_32
    sub   x2, x2, x14
    addi  x8, x8, 32
    jal   x0, PROBAR_16
DESHACER_32:
    addi  x9, x9, 32
PROBAR_16:

    addi  x9, x9, -16
    blt   x9, x0, DESHACER_16
    blt   x2, x13, DESHACER_16
    sub   x2, x2, x13
    addi  x8, x8, 16
    jal   x0, PROBAR_8
DESHACER_16:
    addi  x9, x9, 16
PROBAR_8:

    addi  x9, x9, -8
    blt   x9, x0, DESHACER_8
    blt   x2, x12, DESHACER_8
    sub   x2, x2, x12
    addi  x8, x8, 8
    jal   x0, PROBAR_4
DESHACER_8:
    addi  x9, x9, 8
PROBAR_4:

    addi  x9, x9, -4
    blt   x9, x0, DESHACER_4
    blt   x2, x11, DESHACER_4
    sub   x2, x2, x11
    addi  x8, x8, 4
    jal   x0, PROBAR_2
DESHACER_4:
    addi  x9, x9, 4
PROBAR_2:

    addi  x9, x9, -2
    blt   x9, x0, DESHACER_2
    blt   x2, x10, DESHACER_2
    sub   x2, x2, x10
    addi  x8, x8, 2
    jal   x0, PROBAR_1
DESHACER_2:
    addi  x9, x9, 2
PROBAR_1:

    addi  x9, x9, -1
    blt   x9, x0, DESHACER_1
    blt   x2, x3, DESHACER_1
    sub   x2, x2, x3
    addi  x8, x8, 1
    jal   x0, CANTIDAD_LISTA
DESHACER_1:
    addi  x9, x9, 1

CANTIDAD_LISTA:
    beq   x4, x0, COMPRA_COTIZADA
    beq   x8, x0, CARTERA_LISTA
    addi  x10, x0, 64
    bne   x4, x10, LIQUIDAR
    add   x15, x2, x0
    add   x5, x5, x8
    jal   x0, CARTERA_LISTA
LIQUIDAR:
    lui   x10, 4
    sub   x10, x10, x2        # cantidad ejecutada * precio
    add   x10, x15, x10
    addi  x10, x10, -5
    blt   x10, x0, CARTERA_LISTA
    add   x15, x10, x0
    sub   x5, x5, x8

CARTERA_LISTA:
    lw    x10, 12(x1)        # SUM10 incluye PRICE actual
    lw    x13, 16(x1)        # READY
    bne   x6, x0, MANTENER
    sub   x8, x3, x7         # delta del precio contra la revisión anterior
    add   x7, x3, x0
    andi  x13, x13, 1
    beq   x13, x0, MANTENER

    add   x13, x3, x3
    add   x12, x13, x13
    add   x12, x12, x12
    add   x12, x12, x13
    sub   x12, x12, x10      # confirmación: 10 * precio - SUM10
    bne   x5, x0, EVALUAR_VENTA
    addi  x13, x0, 8
    blt   x8, x13, MANTENER
    blt   x12, x0, MANTENER
    addi  x9, x0, 32
    addi  x13, x0, 16
    blt   x8, x13, COTIZAR
    addi  x9, x0, 63
COTIZAR:
    # Reserva de $500 y $10 para ambas comisiones, aun si el siguiente precio es 255.
    addi  x2, x15, -510
    addi  x3, x0, 255
    addi  x4, x0, 0
    jal   x0, RESOLVER_CANTIDAD
COMPRA_COTIZADA:
    beq   x8, x0, MANTENER
    addi  x4, x8, 64
    jal   x0, EMITIR

EVALUAR_VENTA:
    addi  x13, x0, -8
    bge   x13, x8, EMITIR_VENTA
    bge   x8, x0, MANTENER
    blt   x0, x12, MANTENER
EMITIR_VENTA:
    # Una posición nace de una única compra y nunca supera 63 acciones.
    addi  x4, x5, 128
    jal   x0, EMITIR
MANTENER:
    addi  x4, x0, 0
EMITIR:
    sw    x4, 8(x1)
    addi  x6, x6, 1
    andi  x6, x6, 127
    jal   x0, POLL_STATUS

