# Proyecto 4 SPI smoke test, not an investment algorithm.
# Poll STATUS, read each PRICE, then publish a fixed BUY-1 byte (0x41).
# This exercises CPU MMIO access and the one-transaction MISO response delay.
lui   x1, 0x80010          # SPI base from RTL decode: 0x80010000
addi  x4, x0, 65           # DECISION = buy one share
LOOP:
    lw    x2, 0(x1)        # STATUS
    andi  x2, x2, 1
    beq   x2, x0, LOOP
    lw    x3, 4(x1)        # PRICE; clears new_price
    sw    x4, 8(x1)        # DECISION
    jal   x0, LOOP
