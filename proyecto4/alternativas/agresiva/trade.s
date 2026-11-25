# Pochoco Trader: momentum 16/8, 100% objetivo, entrada directa.
# Fase 0 de cada bloque de 16: delta de precio contra revisi?n anterior.
# Compra estando plano con delta >= 8 y liquida con delta <= -8.
# x1=MMIO, x4=DECISION, x5=acciones, x6=liquidaci?n[4]/fase[3:0],
# x7=precio de revisi?n anterior, x15=caja. Inicialmente $10.000 y sin posici?n.
# La caja y las acciones se actualizan al precio de ejecuci?n del tick siguiente.
# La rutina com?n de cantidades no usa MUL, DIV, shifts ni RAM de trabajo.

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
    lw    x10, 12(x1)        # SUM10 disponible; esta regla usa momentum por revisi?n
    lw    x13, 16(x1)        # READY
    addi  x11, x0, 0         # pendiente de se?al fuera de las revisiones
    andi  x10, x6, 15
    bne   x10, x0, PROBAR_READY
    sub   x11, x3, x7        # diferencia contra el precio de la revisi?n anterior
    add   x7, x3, x0
PROBAR_READY:
    andi  x13, x13, 1
    beq   x13, x0, MANTENER
    bne   x5, x0, POSICION_ABIERTA

    andi  x6, x6, 15         # cartera plana: finalizar liquidaci?n
    addi  x10, x0, 8
    blt   x11, x10, MANTENER
    # Exposici?n 100%: la brecha de objetivo es caja/precio.
    # El presupuesto tras comisi?n domina la brecha e impide sobrecotizar.
    addi  x2, x15, -5
    addi  x9, x0, 63
    addi  x4, x0, 0
    jal   x0, RESOLVER_CANTIDAD
COMPRA_COTIZADA:
    beq   x8, x0, MANTENER
    addi  x4, x8, 64
    jal   x0, EMITIR

POSICION_ABIERTA:
    andi  x10, x6, 16
    bne   x10, x0, COTIZAR_VENTA
    addi  x10, x0, -8
    blt   x10, x11, MANTENER
    addi  x6, x6, 16         # conservar liquidaci?n si el precio de ejecuci?n impide vender
COTIZAR_VENTA:
    # Una ?nica compra mientras plano limita inventario a 63.
    # Si caja<5, basta sumar ingresos de hasta cinco acciones para decidir si
    # la venta completa cubre comisi?n al precio conocido.
    addi  x2, x15, -5
    bge   x2, x0, EMITIR_VENTA
    add   x10, x5, x0
CUBRIR_COMISION:
    add   x2, x2, x3
    bge   x2, x0, EMITIR_VENTA
    addi  x10, x10, -1
    bne   x10, x0, CUBRIR_COMISION
    jal   x0, MANTENER
EMITIR_VENTA:
    addi  x4, x5, 128
    jal   x0, EMITIR

MANTENER:
    addi  x4, x0, 0
EMITIR:
    sw    x4, 8(x1)
    addi  x6, x6, 1
    andi  x10, x6, 15
    bne   x10, x0, POLL_STATUS
    addi  x6, x6, -16        # reinicia fase m?dulo 16 preservando la bandera
    jal   x0, POLL_STATUS
