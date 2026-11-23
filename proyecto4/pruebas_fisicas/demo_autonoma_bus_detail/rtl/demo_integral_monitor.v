module demo_integral_monitor #(parameter TIMEOUT_DIAG=0)(
  input wire clk,rst,byte_done,first_commit,status_valid,
  input wire [3:0] access,frame_index,
  input wire transport_timeout,frame_start,response_ok,
  input wire [7:0] price,decision,
  input wire response_valid,master_done,
  input wire [3:0] timeout_code,
  output wire debug_in_tick,debug_price_read,debug_decision_written,
  output reg [3:0] led=0,
  output reg error=0,
  output wire final_complete, first_byte_seen
);
  reg [7:0] prices[0:15], decisions[0:15];
  initial begin
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/prices.hex",prices);
    $readmemh("proyecto4/pruebas_fisicas/demo_autonoma_bus_detail/data/expected_writes.hex",decisions);
  end
  reg [3:0] previous_access=0;
  wire [3:0] events=access & ~previous_access;
  wire price_read=events[0],sum_read=events[1],ready_read=events[2],write_decision=events[3];
  // One shared tick index plus sticky per-tick events encodes the six
  // saturating counts. Each new tick requires every previous event.
  reg in_tick=0;
  wire [4:0] n_price={1'b0,frame_index}+in_tick;
  reg [4:0] tick_seen=0;
  wire [4:0] tick_events={response_valid,events[3:0]};
  wire [4:0] prior_ticks={1'b0,frame_index};
  wire [4:0] n_read=prior_ticks+tick_seen[0], n_sum=prior_ticks+tick_seen[1],
             n_ready=prior_ticks+tick_seen[2], n_write=prior_ticks+tick_seen[3],
             n_response=prior_ticks+tick_seen[4];


  reg [9:0] hits=0;
  assign first_byte_seen=hits[0];
  wire [9:0] reached;
  assign reached[0]=hits[0];
  genvar i;
  generate for(i=1;i<10;i=i+1) begin : milestones
    assign reached[i]=reached[i-1] && hits[i];
  end endgenerate
  wire [3:0] stage={
    reached[7],
    reached[3] && !reached[7],
    (reached[1] && !reached[3]) || (reached[5] && !reached[7]) || reached[9],
    (reached[0] && !reached[1]) || (reached[2] && !reached[3]) ||
    (reached[4] && !reached[5]) || (reached[6] && !reached[7]) ||
    (reached[8] && !reached[9])
  };
  wire [4:0] tick_next=tick_seen | tick_events;
  assign debug_in_tick=in_tick;
  assign debug_price_read=tick_next[0];
  assign debug_decision_written=tick_next[3];
  // Include valid events on the current edge so completion wins at the limit.
  assign final_complete=in_tick && (&tick_next);
  wire drained=&tick_seen;
  wire complete=master_done && in_tick && drained;
  wire timeout_fault=transport_timeout;
  wire frame_fault=frame_start && frame_index!=0 && (!in_tick || !drained);
  wire price_fault=byte_done && (in_tick || price!=prices[frame_index]);
  wire event_fault=(|tick_events) && (!in_tick || frame_start || |(tick_seen & tick_events));
  wire sma_fault=(sum_read || ready_read) && !(tick_seen[0] || price_read);
  wire decision_fault=write_decision && (tick_seen[3] ||
       !(tick_seen[1] || sum_read) || !(tick_seen[2] || ready_read) ||
       decision!=decisions[frame_index]);
  wire miso_fault=response_valid && !response_ok;
  // complete already proves byte + PRICE/SUM/READY/DECISION/MISO.
  // The independent first commit and valid STATUS hits also must be present.
  wire closing_hits=TIMEOUT_DIAG ? (&hits[2:1]) : reached[7];
  wire closure_fault=complete && !closing_hits;
  wire sequence_fault=frame_fault || event_fault || sma_fault || closure_fault;
  wire fault=timeout_fault || sequence_fault || price_fault || decision_fault || miso_fault;
  wire [3:0] fault_code={1'b1,!price_fault,
    price_fault || (!decision_fault && !miso_fault),
    price_fault || (!decision_fault && (miso_fault || !sequence_fault))};
  wire [3:0] displayed_fault=(TIMEOUT_DIAG && timeout_fault && fault_code==15)
                            ? timeout_code : fault_code;
  wire [3:0] displayed_stage=TIMEOUT_DIAG ? ((hits[9] && closing_hits) ? 4'ha : 4'h0) : stage;
  always @(posedge clk) begin
    if (rst) begin
      previous_access<=0;
      in_tick<=0; tick_seen<=0;
      hits<=0; error<=0; led<=0;
    end else begin
      previous_access<=access;
      if(frame_start) in_tick<=0;
      if(byte_done) in_tick<=1;
      tick_seen<=frame_start ? 5'd0 : tick_next;
      hits<=hits | {hits[8], complete, response_valid,
                   write_decision,ready_read,sum_read,price_read,status_valid,first_commit,byte_done};
      error<=error || fault;

      if(!error) led<=fault ? displayed_fault : displayed_stage;
    end
  end
endmodule












