// One-shot physical probe: capture the first committed Espino PC after the
// first SPI price byte. This module is observation-only.
//
// LED encoding is the captured PC_ID[5:2] (word-address index):
//   0000: reset / no first SPI byte yet
//   0001: first SPI byte received; no post-byte commit captured yet
//   0101: first post-byte commit had PC_ID 0x14 (expected LW STATUS)
//   0110: first post-byte commit had PC_ID 0x18 (expected ANDI)
//   0111: first post-byte commit had PC_ID 0x1C (expected BEQ)
//   1000: first post-byte commit had PC_ID 0x20
//   0011: first post-byte commit had PC_ID 0x0C (unexpected for expected flow)
//   Other values: raw PC_ID[5:2] of the first post-byte commit.
//
// The probe captures the full PC and instruction in snapshot registers for
// simulation assertions. They are left unconnected by the physical top and
// therefore can be optimized away by synthesis.
module first_post_byte_pc_probe (
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        byte_done_i,
    input  wire        instr_valid_id_i,
    input  wire        stall_i,
    input  wire [31:0] pc_id_i,
    input  wire [31:0] instr_id_i,
    output wire [3:0]  led_o,
    output wire        snapshot_valid_o,
    output wire [31:0] snapshot_pc_o,
    output wire [31:0] snapshot_instr_o
);
    reg byte_seen_q = 1'b0;
    reg snapshot_valid_q = 1'b0;
    reg [3:0] led_q = 4'b0000;
    reg [31:0] snapshot_pc_q = 32'b0;
    reg [31:0] snapshot_instr_q = 32'b0;

    wire commit_evt = instr_valid_id_i && !stall_i;

    always @(posedge clk_i) begin
        if (!rst_ni) begin
            byte_seen_q      <= 1'b0;
            snapshot_valid_q <= 1'b0;
            led_q            <= 4'b0000;
            snapshot_pc_q    <= 32'b0;
            snapshot_instr_q <= 32'b0;
        end else begin
            if (byte_done_i)
                byte_seen_q <= 1'b1;

            if (!snapshot_valid_q) begin
                // Include byte_done_i so a simultaneous byte/commit edge is
                // captured. This is independent of all previous LED stages.
                if ((byte_seen_q || byte_done_i) && commit_evt) begin
                    snapshot_valid_q <= 1'b1;
                    snapshot_pc_q    <= pc_id_i;
                    snapshot_instr_q <= instr_id_i;
                    led_q            <= pc_id_i[5:2];
                end else if (byte_done_i) begin
                    led_q <= 4'b0001;
                end
            end
        end
    end

    assign led_o = led_q;
    assign snapshot_valid_o = snapshot_valid_q;
    assign snapshot_pc_o = snapshot_pc_q;
    assign snapshot_instr_o = snapshot_instr_q;
endmodule
