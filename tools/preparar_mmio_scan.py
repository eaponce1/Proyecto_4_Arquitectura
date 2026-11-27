"""Alternativa MMIO con recálculo secuencial de ventana en una BRAM."""
from pathlib import Path
import hashlib,json,shutil
from preparar_codisenio_lento import ROOT,OUT,assemble
RTL='''// SMA10 alternativa: nueve lecturas de historia + precio entrante.
// Latencia de actualización: nueve ciclos; CPU consulta después del fin.
module pochoco_sma10 (
  input wire clk_i,rst_ni,price_valid_i,
  input wire [7:0] price_i,
  output wire [11:0] sum_o,
  output wire ready_o
);
  reg [3:0] pointer_q=0,count_q=0,scan_q=0,remaining_q=0;
  reg busy_q=0;
  reg [11:0] accumulator_q=0;
  wire [15:0] old_word;
  wire [3:0] next_pointer=(pointer_q==9)?0:pointer_q+1'b1;
  wire [3:0] first=(count_q<9)?0:next_pointer;
  wire [3:0] read_pointer=price_valid_i?first:scan_q;
  wire read_enable=(price_valid_i && count_q!=0) || (busy_q && remaining_q>1);
  assign sum_o=accumulator_q;
  assign ready_o=(count_q==10) && !busy_q;
  SB_RAM40_4K #(.READ_MODE(0),.WRITE_MODE(0),.INIT_0(256'h0)) history (
    .RDATA(old_word),.RADDR({7'b0,read_pointer}),.RCLK(clk_i),.RCLKE(read_enable),.RE(1'b1),
    .WDATA({8'b0,price_i}),.WADDR({7'b0,pointer_q}),.WCLK(clk_i),.WCLKE(1'b1),
    .WE(price_valid_i),.MASK(16'hff00)
  );
  always @(posedge clk_i or negedge rst_ni) begin
    if(!rst_ni) begin
      pointer_q<=0;count_q<=0;scan_q<=0;remaining_q<=0;busy_q<=0;accumulator_q<=0;
    end else if(price_valid_i) begin
      pointer_q<=next_pointer;
      if(count_q<10)count_q<=count_q+1'b1;
      scan_q<=(first==9)?0:first+1'b1;
      accumulator_q<={4'b0,price_i};remaining_q<=(count_q<9)?count_q:9;busy_q<=(count_q!=0);
    end else if(busy_q) begin
      accumulator_q<=accumulator_q+{4'b0,old_word[7:0]};
      remaining_q<=remaining_q-1'b1;
      scan_q<=(scan_q==9)?0:scan_q+1'b1;
      if(remaining_q==1)busy_q<=0;
    end
  end
endmodule
'''
def main():
    folder=OUT/'mmio_scan';rtl=folder/'rtl';rtl.mkdir(parents=True,exist_ok=True)
    text=(ROOT/'sw/trade.s').read_text(encoding='utf-8')
    old='    lw    x10, 12(x1)         # SUM10\n    lw    x13, 16(x1)         # READY'
    text=text.replace(old,'KERNEL_START:\n'+old+'\nKERNEL_END:')
    labels,words=assemble(text);assert len(words)==130
    (folder/'trade.s').write_text(text,encoding='utf-8');shutil.copyfile(ROOT/'sw/trade.hex',folder/'trade.hex')
    top=(ROOT/'rtl/trade_spi_externo.v').read_text().replace('sw/trade.hex',(folder/'trade.hex').relative_to(ROOT).as_posix())
    (rtl/'trade_spi_externo.v').write_text(top,encoding='utf-8')
    (rtl/'pochoco_sma10.v').write_text(RTL,encoding='utf-8')
    path=OUT/'variantes.json';meta=json.loads(path.read_text())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    meta['variantes']['mmio_scan']=dict(palabras=130,kernel_start=labels['KERNEL_START'],kernel_end=labels['KERNEL_END'],
        sha256_s=sha(folder/'trade.s'),sha256_hex=sha(folder/'trade.hex'),etiquetas=labels)
    path.write_text(json.dumps(meta,indent=2),encoding='utf-8');print('PASS alternativa MMIO scan de nueve ciclos')
if __name__=='__main__':main()
