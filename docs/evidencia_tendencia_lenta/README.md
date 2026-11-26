# Evidencia activa: tendencia lenta

`validacion_integral.json` identifica BIN, HEX, fuentes y alcance. `trazas_rtl/` contiene los ocho CSV de 20.000 ticks comprimidos con gzip, cotejados contra el modelo y el HEX. Se pueden descomprimir con Python o 7-Zip. No son mediciones de placa.

```powershell
python -B tools/auditar_lenta.py
```

Esta auditoría verifica firmas, contabilidad por tick, MISO/DECISION, dos bancos oficiales 4/4, integración de 396 ticks a 1 y 10 ms y las pruebas de netlist/BIN con CS de 20/40/1000 ns. Los 160.000 ticks completos corresponden a 100 µs. El retardo uniforme de 1 ns de la reconstrucción del BIN es funcional; nextpnr aporta el timing.

Los logs activos están listados en los JSON de `build/trader/`; los demás logs de versiones previas son históricos. La imagen anterior y su prueba física se conservan por separado. El grupo confirmó la reprogramación de la imagen lenta; su registro es independiente de las cifras financieras del testbench. La campaña ampliada está en `docs/evidencia_todas_acciones/`.
