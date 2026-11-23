# Proyecto 4: reversión a la media SMA10, compatible con Espino RV32E.
#
# MMIO derivado de rtl/pochoco_spi_slave.v:
#   x1+0 STATUS, bit 0 = new_price; x1+4 PRICE; x1+8 DECISION.
# Periferico: SUM10 en +12 y READY en +16 dentro de la ventana SPI.
#
# Estrategia Python equivalente:
#   sumar los últimos diez precios; comparar 10*precio con suma +/- 10.
#   Si holdings==0 y 10*p <= suma-10: pedir comprar 16.
#   Si holdings>0 y 10*p >= suma+10: pedir vender min(16, holdings).
#   En otro caso: mantener.
# No se calcula division ni se usan MUL o shifts: 10*p = 8*p + 2*p.
# Cada decision se calcula despues de leer el precio y se ejecuta en el tick
# siguiente. x4 conserva el byte pendiente y x5 es la posicion ya ejecutada.

    lui   x1, 0x80010
    addi  x4, x0, 0            # DECISION pendiente inicial = mantener
    addi  x5, x0, 0            # acciones actuales
    lui   x15, 2
    addi  x15, x15, 1808       # caja local inicial = 10.000

POLL_STATUS:
    lw    x2, 0(x1)
    andi  x2, x2, 1
    beq   x2, x0, POLL_STATUS
    lw    x3, 4(x1)            # PRICE; la lectura limpia new_price

# Aplicar a la cartera local el byte transmitido en la transaccion actual.
# La FPGA maestra ya ejecuto esa decision al precio x3.
    addi  x13, x0, 80          # 0x50 = comprar 16
    beq   x4, x13, APLICAR_COMPRA
    andi  x13, x4, 192         # aislar accion [7:6]
    addi  x12, x0, 128         # 0x80 = vender
    bne   x13, x12, PENDIENTE_APLICADA
    andi  x11, x4, 63          # cantidad solicitada por la venta pendiente
    beq   x11, x0, PENDIENTE_APLICADA
    add   x9, x11, x0          # multiplicacion q*p por sumas repetidas
    addi  x13, x0, 0
CALCULAR_INGRESO:
    beq   x9, x0, REVISAR_COMISION_VENTA
    add   x13, x13, x3
    addi  x9, x9, -1
    jal   x0, CALCULAR_INGRESO
REVISAR_COMISION_VENTA:
    add   x13, x13, x15        # caja + q*precio
    addi  x12, x0, 5
    bge   x13, x12, APLICAR_VENTA
    jal   x0, PENDIENTE_APLICADA # la maestra no ejecuta si no cubre comision
APLICAR_VENTA:
    addi  x13, x13, -5
    add   x15, x13, x0         # actualizar caja despues de vender
    sub   x5, x5, x11          # actualizar acciones ejecutadas
    jal   x0, PENDIENTE_APLICADA

APLICAR_COMPRA:
    addi  x13, x15, -5        # presupuesto tras reservar comision
    addi  x9, x0, 0           # cantidad asequible calculada
    addi  x11, x0, 16         # maximo solicitado por SMA10
COMPRA_ASEQUIBLE_LOOP:
    bge   x13, x3, COMPRAR_UNA
    jal   x0, COMPRA_ASEQUIBLE_FIN
COMPRAR_UNA:
    sub   x13, x13, x3
    addi  x9, x9, 1
    addi  x11, x11, -1
    bne   x11, x0, COMPRA_ASEQUIBLE_LOOP
COMPRA_ASEQUIBLE_FIN:
    beq   x9, x0, PENDIENTE_APLICADA # sin fill no se cobra comision
    add   x15, x13, x0         # remaining cash = caja - fee - q*precio
    add   x5, x9, x0           # holdings exactos, incluso si hubo fill parcial

PENDIENTE_APLICADA:
# El perif?rico captur? el byte SPI al finalizar la transacci?n.
    lw    x10, 12(x1)          # SUM10, address 0x8001000C
    lw    x13, 16(x1)          # READY, address 0x80010010
    andi  x13, x13, 1
    beq   x13, x0, HISTORIAL_INCOMPLETO

# x12 = 10*precio, usando cuatro ADD: 2p, 4p, 8p, 10p.
    add   x13, x3, x3
    add   x12, x13, x13
    add   x12, x12, x12
    add   x12, x12, x13

# Aplicar condiciones exactas de estrategia_reversion_media.
    bne   x5, x0, REVISAR_SENAL_VENTA
    addi  x13, x10, -10
    bge   x13, x12, EMITIR_COMPRA  # sum10 - 10 >= 10*p
    addi  x4, x0, 0
    sw    x4, 8(x1)
    jal   x0, POLL_STATUS

REVISAR_SENAL_VENTA:
    addi  x13, x10, 10
    bge   x12, x13, EMITIR_VENTA  # 10*p >= sum10 + 10
    addi  x4, x0, 0
    sw    x4, 8(x1)
    jal   x0, POLL_STATUS

EMITIR_COMPRA:
    addi  x4, x0, 80           # 01 acción, cantidad 16 => 0x50
    sw    x4, 8(x1)
    jal   x0, POLL_STATUS

EMITIR_VENTA:
    addi  x4, x0, 128
    add   x4, x4, x5           # 10 acción, cantidad min(16, holdings)
    sw    x4, 8(x1)
    jal   x0, POLL_STATUS

HISTORIAL_INCOMPLETO:
    addi  x4, x0, 0
    sw    x4, 8(x1)
    jal   x0, POLL_STATUS
