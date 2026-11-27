# Pochoco Trader: tendencia 128/5 % sobre SUM10, lote maximo.
# Cada 128 ticks compara SUM10 (periferico MMIO) con el de la revision anterior:
#   20*(SUM10-ancla) >= ancla -> dentro ; 20*(ancla-SUM10) >= ancla -> fuera.
# Dentro: compra todo lo que alcance (max 63 por orden, completar solo si >= 8).
# Fuera: vende min(63, acciones) hasta quedar en cero.
# x1=MMIO, x3=precio, x4=DECISION, x5=acciones, x6=dentro[7]/fase[6:0],
# x7=ancla (SUM10 de la revision anterior, 0 = sin ancla), x15=caja.
# La caja y las acciones se actualizan al precio de ejecucion del tick siguiente.
# Sin MUL, DIV, shifts ni RAM de trabajo: 20x = 16x + 4x con ADD.

    lui   x1, 0x80010
    addi  x4, x0, 0
    addi  x5, x0, 0
    addi  x6, x0, 0
    addi  x7, x0, 0
    lui   x15, 2
    addi  x15, x15, 1808      # caja = 10.000

POLL_STATUS:
    lw    x2, 0(x1)
    andi  x2, x2, 1
    beq   x2, x0, POLL_STATUS
    lw    x3, 4(x1)           # PRICE; la lectura limpia new_price

# Aplicar a la cartera local la orden que la maestra acaba de ejecutar al precio x3.
    andi  x9, x4, 63
    beq   x9, x0, CARTERA_LISTA
    andi  x4, x4, 192
    addi  x10, x0, 64
    beq   x4, x10, APLICAR_COMPRA
    addi  x10, x0, 128
    bne   x4, x10, CARTERA_LISTA
    bge   x5, x9, PRESUPUESTO_VENTA   # la maestra recorta la venta al inventario
    add   x9, x5, x0
PRESUPUESTO_VENTA:
    lui   x2, 4               # 16.384 cubre 63 * 255
    jal   x0, RESOLVER_CANTIDAD

APLICAR_COMPRA:
    addi  x2, x15, -5
    jal   x0, RESOLVER_CANTIDAD

# Greedy binario: mayor cantidad <= x9 que cabe en x2 al precio x3.
# x4: 64 compra ejecutada, 128 venta ejecutada, 0 cotizacion.
# x8 devuelve la cantidad y x2 el presupuesto no utilizado.
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
    blt   x9, x0, CANTIDAD_LISTA
    blt   x2, x3, CANTIDAD_LISTA
    sub   x2, x2, x3
    addi  x8, x8, 1

CANTIDAD_LISTA:
    beq   x4, x0, COMPRA_COTIZADA
    beq   x8, x0, CARTERA_LISTA
    addi  x10, x0, 64
    bne   x4, x10, LIQUIDAR
    add   x15, x2, x0         # compra: caja = presupuesto restante
    add   x5, x5, x8
    jal   x0, CARTERA_LISTA
LIQUIDAR:
    lui   x10, 4
    sub   x10, x10, x2        # cantidad ejecutada * precio
    add   x10, x15, x10
    addi  x10, x10, -5
    blt   x10, x0, CARTERA_LISTA  # la maestra no vende si no cubre la comision
    add   x15, x10, x0
    sub   x5, x5, x8

CARTERA_LISTA:
KERNEL_START:
    lw    x10, 12(x1)         # SUM10
    lw    x13, 16(x1)         # READY
KERNEL_END:
    andi  x11, x6, 127
    bne   x11, x0, DECIDIR    # solo se revisa en fase 0
    andi  x13, x13, 1
    beq   x13, x0, DECIDIR    # ventana de 10 precios incompleta
    beq   x7, x0, FIJAR_ANCLA
    sub   x11, x10, x7        # delta = SUM10 - ancla
    addi  x14, x0, 128        # signo: 128 = sube (dentro), 0 = baja (fuera)
    bge   x11, x0, DELTA_ABS
    sub   x11, x0, x11
    addi  x14, x0, 0
DELTA_ABS:
    add   x12, x11, x11       # 2
    add   x12, x12, x12       # 4
    add   x13, x12, x12       # 8
    add   x13, x13, x13       # 16
    add   x12, x12, x13       # 20*|delta|
    blt   x12, x7, FIJAR_ANCLA   # movimiento menor a 5 %: conservar modo
    andi  x6, x6, 127
    add   x6, x6, x14
FIJAR_ANCLA:
    add   x7, x10, x0

DECIDIR:
    andi  x11, x6, 128
    beq   x11, x0, FUERA
    addi  x2, x15, -5         # dentro: cotizar la compra maxima
    addi  x9, x0, 63
    addi  x4, x0, 0
    jal   x0, RESOLVER_CANTIDAD
COMPRA_COTIZADA:
    beq   x8, x0, MANTENER
    beq   x5, x0, EMITIR_COMPRA
    addi  x10, x0, 8
    blt   x8, x10, MANTENER   # no pagar comision por completar con menos de 8
EMITIR_COMPRA:
    addi  x4, x8, 64
    jal   x0, EMITIR

FUERA:
    beq   x5, x0, MANTENER
    addi  x4, x0, 63
    bge   x5, x4, EMITIR_VENTA
    add   x4, x5, x0
EMITIR_VENTA:
    addi  x4, x4, 128
    jal   x0, EMITIR

MANTENER:
    addi  x4, x0, 0
EMITIR:
    sw    x4, 8(x1)
    addi  x6, x6, 1
    andi  x10, x6, 127
    bne   x10, x0, POLL_STATUS
    addi  x6, x6, -128        # fase modulo 128 preservando el bit de modo
    jal   x0, POLL_STATUS
