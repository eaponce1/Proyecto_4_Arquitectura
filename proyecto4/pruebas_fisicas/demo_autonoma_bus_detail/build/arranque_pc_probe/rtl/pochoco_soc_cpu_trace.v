// Independent monitor wrapper: original Espino/SoC and MMIO RTL are instantiated
// unchanged; hierarchy taps only observe commit, stall, PC and the data bus.
module pochoco_soc_cpu_trace #(
  parameter integer NumWords=128,
  parameter MemFile="proyecto4/alternativas/mmio_sma10/sw/trade.hex"
) (
  input wire i_Clk,
  input wire i_SPI_SCLK,i_SPI_MOSI,i_SPI_CS_n,
  output wire o_SPI_MISO,
  output wire dbg_reset_released,dbg_instr_req,
  output wire [31:0] dbg_instr_addr,
  output wire dbg_commit,dbg_core_stall,dbg_instr_valid,
  output wire dbg_lsu_busy,
  output wire [31:0] dbg_pc,dbg_pc_id,
  output wire [31:0] dbg_instr_id,
  output wire dbg_data_req,dbg_data_we,
  output wire [3:0] dbg_data_be,
  output wire [31:0] dbg_data_addr,dbg_data_wdata,dbg_data_rdata,
  output wire dbg_status_read,dbg_price_read,dbg_sum_read,dbg_ready_read,
  output wire dbg_decision_write,dbg_spi_byte_done,
  output wire [7:0] dbg_price,
  output wire [31:0] dbg_spi_rdata
);
  wire clk=i_Clk;
  reg [3:0] por_cnt=0;
  wire rst_ni=(por_cnt==4'hf);
  always @(posedge clk) if(por_cnt!=4'hf) por_cnt<=por_cnt+1'b1;
  assign dbg_reset_released=rst_ni;

  wire instr_req,data_req,data_we;
  wire core_commit,core_stall;
  wire [31:0] core_pc_id;
  wire [31:0] instr_addr,instr_rdata,data_addr,data_wdata,data_rdata;
  wire [3:0] data_be;
  espino_core_cpu_trace #(.BootAddr(32'h0)) u_core(
    .clk_i(clk),.rst_ni(rst_ni),.instr_req_o(instr_req),.instr_addr_o(instr_addr),
    .instr_rdata_i(instr_rdata),.data_req_o(data_req),.data_we_o(data_we),
    .data_be_o(data_be),.data_addr_o(data_addr),.data_wdata_o(data_wdata),
    .data_rdata_i(data_rdata),.dbg_commit_o(core_commit),
    .dbg_stall_o(core_stall),.dbg_instr_valid_o(dbg_instr_valid),
    .dbg_lsu_busy_o(dbg_lsu_busy),.dbg_instr_id_o(dbg_instr_id),.dbg_pc_id_o(core_pc_id)
  );
  assign dbg_instr_req=instr_req;
  assign dbg_instr_addr=instr_addr;
  assign dbg_commit=core_commit;
  assign dbg_core_stall=core_stall;
  assign dbg_pc=instr_addr;
  assign dbg_pc_id=core_pc_id;
  assign dbg_data_req=data_req;
  assign dbg_data_we=data_we;
  assign dbg_data_be=data_be;
  assign dbg_data_addr=data_addr;
  assign dbg_data_wdata=data_wdata;
  assign dbg_data_rdata=data_rdata;

  wire is_mmio=data_addr[31];
  wire per_sel=is_mmio & ~data_addr[16];
  wire spi_sel=is_mmio & data_addr[16];
  wire ram_b_req=data_req & ~is_mmio;
  wire spi_req=data_req & spi_sel;
  wire [31:0] ram_b_rdata,spi_rdata;
  reg rd_is_per=0,rd_is_spi=0;
  always @(posedge clk or negedge rst_ni) begin
    if(!rst_ni) begin rd_is_per<=0;rd_is_spi<=0;end
    else if(data_req & ~data_we) begin rd_is_per<=per_sel;rd_is_spi<=spi_sel;end
  end
  assign data_rdata=rd_is_per ? 32'b0 : rd_is_spi ? spi_rdata : ram_b_rdata;

  pochoco_ram #(.NumWords(NumWords),.MemFile(MemFile)) u_ram(
    .clk_i(clk),.a_req_i(instr_req),.a_addr_i(instr_addr),.a_rdata_o(instr_rdata),
    .b_req_i(ram_b_req),.b_we_i(data_we),.b_be_i(data_be),.b_addr_i(data_addr),
    .b_wdata_i(data_wdata),.b_rdata_o(ram_b_rdata)
  );
  wire [7:0] sma_price;
  wire sma_price_valid;
  wire [11:0] sma_sum;
  wire sma_ready;
  pochoco_spi_slave u_spi(
    .clk_i(clk),.rst_ni(rst_ni),.sel_i(spi_sel),.req_i(spi_req),.we_i(data_we),
    .addr_i(data_addr[7:0]),.wdata_i(data_wdata),.be_i(data_be),.rdata_o(spi_rdata),
    .spi_sclk_i(i_SPI_SCLK),.spi_mosi_i(i_SPI_MOSI),.spi_cs_n_i(i_SPI_CS_n),
    .spi_miso_o(o_SPI_MISO),.price_o(sma_price),.price_valid_o(sma_price_valid),
    .sma_sum_i(sma_sum),.sma_ready_i(sma_ready)
  );
  pochoco_sma10 u_sma10(.clk_i(clk),.rst_ni(rst_ni),.price_valid_i(sma_price_valid),
    .price_i(sma_price),.sum_o(sma_sum),.ready_o(sma_ready));
  assign dbg_spi_byte_done=sma_price_valid;
  assign dbg_price=sma_price;
  assign dbg_spi_rdata=spi_rdata;
  assign dbg_status_read=spi_req & ~data_we & (data_addr[7:2]==0);
  assign dbg_price_read=spi_req & ~data_we & (data_addr[7:2]==1);
  assign dbg_decision_write=spi_req & data_we & data_be[0] & (data_addr[7:2]==2);
  assign dbg_sum_read=spi_req & ~data_we & (data_addr[7:2]==3);
  assign dbg_ready_read=spi_req & ~data_we & (data_addr[7:2]==4);
endmodule
