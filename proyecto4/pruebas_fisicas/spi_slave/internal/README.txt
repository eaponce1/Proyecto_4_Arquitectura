Prueba SPI modo internal
========================

El maestro y el SPI Slave están conectados por nets internas. No requiere jumpers.
El PCF deja PS7..PS10 como sondas opcionales: SCLK/MOSI/CS_n/MISO.

La prueba envía cinco patrones, verifica STATUS y PRICE para cuatro precios,
escribe cuatro decisiones y comprueba en los cinco bytes MISO el desfase de un tick.

LED0=PASS, LED1=FAIL, LED2=BUSY, LED3=DONE.
