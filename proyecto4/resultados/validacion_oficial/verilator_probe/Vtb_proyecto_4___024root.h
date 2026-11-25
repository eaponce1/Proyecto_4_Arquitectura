// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_proyecto_4.h for the primary calling header

#ifndef VERILATED_VTB_PROYECTO_4___024ROOT_H_
#define VERILATED_VTB_PROYECTO_4___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vtb_proyecto_4__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_proyecto_4___024root final {
  public:

    // TRIVIALLY CONSTRUCTIBLE STATE
    ::CData/*0:0*/ tb_proyecto_4__DOT__clk;
    ::CData/*0:0*/ tb_proyecto_4__DOT__sclk;
    ::CData/*0:0*/ tb_proyecto_4__DOT__mosi;
    ::CData/*0:0*/ tb_proyecto_4__DOT__cs_n;
    ::CData/*0:0*/ tb_proyecto_4__DOT__esperando;
    ::CData/*7:0*/ tb_proyecto_4__DOT__decision;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__por_cnt;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__spi_sel;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__per_sel;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__rd_is_per;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__rd_is_spi;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__wr;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o;
    ::CData/*1:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o;
    ::CData/*1:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o;
    ::CData/*1:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__pc_set_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rd;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__wr;
    ::CData/*2:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync;
    ::CData/*2:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync;
    ::CData/*2:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift;
    ::CData/*2:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_q;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_q;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__digit_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_meta_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q;
    ::CData/*3:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_q;
    ::CData/*0:0*/ __Vdfg_Regularize_2114;
    ::CData/*0:0*/ __Vdfg_Regularize_2120;
    ::CData/*0:0*/ __Vdfg_Regularize_2123;
    ::CData/*0:0*/ __Vdfg_Regularize_2124;
    ::CData/*0:0*/ __Vdfg_Regularize_2125;
    ::CData/*0:0*/ __Vdfg_Regularize_2127;
    ::CData/*0:0*/ __Vdfg_Regularize_2135;
    ::CData/*0:0*/ __Vdfg_Regularize_2137;
    ::CData/*0:0*/ __Vdfg_Regularize_2138;
    ::CData/*0:0*/ __Vdfg_Regularize_2139;
    ::CData/*0:0*/ __Vdfg_Regularize_2140;
    ::CData/*3:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__por_cnt_0;
    ::CData/*3:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_170;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_171;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_172;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_173;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_174;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_175;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_176;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_177;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_178;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_179;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_180;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_181;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_182;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_183;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_184;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_185;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_186;
    ::CData/*7:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_187;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_189;
    ::CData/*7:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_190;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_192;
    ::CData/*7:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_193;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_195;
    ::CData/*7:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_196;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_198;
    ::CData/*0:0*/ __Vtrigprevexpr___TOP__tb_proyecto_4__DOT__clk__0;
    ::CData/*0:0*/ __Vtrigprevexpr_he805701c__1;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__RDATA;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__RDATA;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__RDATA;
    ::SData/*11:0*/ tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__RDATA;
    ::SData/*8:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_188;
    ::SData/*8:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_191;
    ::SData/*8:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_194;
    ::SData/*8:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_197;
    ::IData/*31:0*/ tb_proyecto_4__DOT__bits_x;
    ::IData/*31:0*/ tb_proyecto_4__DOT__caja;
    ::IData/*31:0*/ tb_proyecto_4__DOT__acciones;
    ::IData/*31:0*/ tb_proyecto_4__DOT__w;
    ::IData/*31:0*/ tb_proyecto_4__DOT__peak;
    ::IData/*31:0*/ tb_proyecto_4__DOT__max_dd;
    ::IData/*31:0*/ tb_proyecto_4__DOT__ordenes;
    ::IData/*31:0*/ tb_proyecto_4__DOT__ciclos;
    ::IData/*31:0*/ tb_proyecto_4__DOT__peor_caso;
    ::IData/*31:0*/ tb_proyecto_4__DOT__respuestas;
    ::IData/*31:0*/ tb_proyecto_4__DOT__precios_perdidos;
    ::IData/*31:0*/ tb_proyecto_4__DOT__total_tests;
    ::IData/*31:0*/ tb_proyecto_4__DOT__tests_aprobados;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__data_rdata;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_cycle_q;
    ::IData/*17:0*/ tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__b_rdata_o;
    ::IData/*30:0*/ __Vdfg_Regularize_2111;
    ::IData/*31:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12;
    ::IData/*31:0*/ __Vi;
    ::QData/*63:0*/ tb_proyecto_4__DOT__ciclos_acumulados;
    ::VlUnpacked<::IData/*31:0*/, 20000> tb_proyecto_4__DOT__precio;
    ::VlUnpacked<::SData/*15:0*/, 256> tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem;
    ::VlUnpacked<::SData/*15:0*/, 256> tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem;
    ::VlUnpacked<::SData/*15:0*/, 256> tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem;
    ::VlUnpacked<::SData/*15:0*/, 256> tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem;
    ::VlUnpacked<::SData/*15:0*/, 256> tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem;
    ::VlUnpacked<::IData/*31:0*/, 512> tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem;
    ::VlUnpacked<::QData/*63:0*/, 1> __VstlTriggered;
    ::VlUnpacked<::QData/*63:0*/, 1> __VicoTriggered;
    ::VlUnpacked<::QData/*63:0*/, 1> __VactTriggered;
    ::VlUnpacked<::QData/*63:0*/, 1> __VactTriggeredAcc;
    ::VlUnpacked<::QData/*63:0*/, 1> __VnbaTriggered;

    // NOT TRIVIALLY CONSTRUCTIBLE STATE
    union {
        struct {
            ::std::string __Vtask_tb_proyecto_4__DOT__leer_serie__encabezado_5;
            ::std::string __Vtask_tb_proyecto_4__DOT__chequear__nombre_13;
            ::std::string __Vtask_tb_proyecto_4__DOT__chequear__nombre_15;
            ::std::string __Vtask_tb_proyecto_4__DOT__chequear__nombre_17;
            ::std::string __Vtask_tb_proyecto_4__DOT__chequear__nombre_19;
            ::VlDelayScheduler __VdlySched;
        } __Vnontrivs;
    };

    // INTERNAL VARIABLES
    Vtb_proyecto_4__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vtb_proyecto_4___024root(Vtb_proyecto_4__Syms* symsp, const char* namep);
    ~Vtb_proyecto_4___024root();
    VL_UNCOPYABLE(Vtb_proyecto_4___024root);
    VL_UNMOVABLE(Vtb_proyecto_4___024root);

    // INTERNAL METHODS
};


#endif  // guard
