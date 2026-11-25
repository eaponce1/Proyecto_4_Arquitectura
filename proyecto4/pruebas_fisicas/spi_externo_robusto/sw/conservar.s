# Posición cero: atender cada precio y publicar MANTENER para el tick siguiente.
    lui   x1, 0x80010
POLL_STATUS:
    lw    x2, 0(x1)
    andi  x2, x2, 1
    beq   x2, x0, POLL_STATUS
    lw    x3, 4(x1)           # PRICE limpia new_price
    lw    x10, 12(x1)         # SUM10
    lw    x13, 16(x1)         # READY
    sw    x0, 8(x1)           # DECISION = 0x00
    jal   x0, POLL_STATUS
