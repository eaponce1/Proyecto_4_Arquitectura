# SMA10 +/-4, evaluación cada 64 ticks, lote fijo de 3 y piso de $9.000.
# Reserva para comprar: 9000 + 3*255 + 5 de compra + 5 de salida = 9775.
# x4 = decisión pendiente, x5 = posición, x6 = tick mod 64, x15 = caja.
    lui   x1, 0x80010
    addi  x4, x0, 0
    addi  x5, x0, 0
    addi  x6, x0, 0
    lui   x14, 2
    addi  x14, x14, 1583     # 9.775
    lui   x15, 2
    addi  x15, x15, 1808     # 10.000

POLL_STATUS:
    lw    x2, 0(x1)
    andi  x2, x2, 1
    beq   x2, x0, POLL_STATUS
    lw    x3, 4(x1)
    beq   x4, x0, APLICADA

    add   x8, x3, x3
    add   x8, x8, x3         # valor del lote a precio de ejecución
    addi  x13, x0, 67        # 0x43: compra de 3
    beq   x4, x13, COMPRA_EJECUTADA

    add   x15, x15, x8
    addi  x15, x15, -5       # la venta puede reducir caja a precios muy bajos
    addi  x5, x0, 0
    jal   x0, APLICADA

COMPRA_EJECUTADA:
    sub   x15, x15, x8       # el peor coste ya fue reservado al emitir la compra
    addi  x15, x15, -5
    addi  x5, x0, 3

APLICADA:
    lw    x10, 12(x1)
    lw    x13, 16(x1)
    andi  x13, x13, 1
    beq   x13, x0, MANTENER
    bne   x6, x0, MANTENER

    add   x13, x3, x3
    add   x12, x13, x13
    add   x12, x12, x12
    add   x12, x12, x13      # 10 * precio con cuatro sumas
    bne   x5, x0, SENAL_VENTA
    addi  x13, x10, -40
    blt   x13, x12, MANTENER
    blt   x15, x14, MANTENER
    addi  x4, x0, 67
    jal   x0, EMITIR

SENAL_VENTA:
    addi  x13, x10, 40
    blt   x12, x13, MANTENER
    addi  x4, x0, 131        # 0x83: venta de 3
    jal   x0, EMITIR

MANTENER:
    addi  x4, x0, 0
EMITIR:
    sw    x4, 8(x1)
    addi  x6, x6, 1
    andi  x6, x6, 63
    jal   x0, POLL_STATUS
