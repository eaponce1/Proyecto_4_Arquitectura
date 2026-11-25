// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_proyecto_4.h for the primary calling header

#include "Vtb_proyecto_4__pch.h"

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_static(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_static\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.tb_proyecto_4__DOT__clk = 0U;
        vlSelfRef.tb_proyecto_4__DOT__sclk = 0U;
        vlSelfRef.tb_proyecto_4__DOT__mosi = 0U;
        vlSelfRef.tb_proyecto_4__DOT__cs_n = 1U;
        vlSelfRef.tb_proyecto_4__DOT__bits_x = 0U;
        vlSelfRef.tb_proyecto_4__DOT__caja = 0x00002710U;
        vlSelfRef.tb_proyecto_4__DOT__acciones = 0U;
        vlSelfRef.tb_proyecto_4__DOT__w = 0x00002710U;
        vlSelfRef.tb_proyecto_4__DOT__peak = 0x00002710U;
        vlSelfRef.tb_proyecto_4__DOT__max_dd = 0U;
        vlSelfRef.tb_proyecto_4__DOT__ordenes = 0U;
        vlSelfRef.tb_proyecto_4__DOT__ciclos = 0U;
        vlSelfRef.tb_proyecto_4__DOT__peor_caso = 0U;
        vlSelfRef.tb_proyecto_4__DOT__respuestas = 0U;
        vlSelfRef.tb_proyecto_4__DOT__precios_perdidos = 0U;
        vlSelfRef.tb_proyecto_4__DOT__ciclos_acumulados = 0ULL;
        vlSelfRef.tb_proyecto_4__DOT__esperando = 0U;
        vlSelfRef.tb_proyecto_4__DOT__total_tests = 0U;
        vlSelfRef.tb_proyecto_4__DOT__tests_aprobados = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt = 0U;
    }
    vlSelfRef.__Vtrigprevexpr___TOP__tb_proyecto_4__DOT__clk__0 = 0U;
    vlSelfRef.__Vtrigprevexpr_he805701c__1 = 0U;
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((::IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtb_proyecto_4___024root___trigger_anySet__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &in);
VL_ATTR_COLD void Vtb_proyecto_4___024root___stl_comb__TOP__0(Vtb_proyecto_4___024root* vlSelf);

VL_ATTR_COLD bool Vtb_proyecto_4___024root___eval_stl(Vtb_proyecto_4___024root* vlSelf, ::CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_stl\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VstlExecute;
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (::IData)((::IData)(firstIteration)));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_proyecto_4___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtb_proyecto_4___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_body__stl
            if ((((1ULL & vlSelfRef.__VstlTriggered[0U])) != 0ULL)) {
                Vtb_proyecto_4___024root___stl_comb__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__stl(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__stl\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtb_proyecto_4___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__ico(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__ico\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtb_proyecto_4___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__act(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__act\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtb_proyecto_4___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__nba(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__nba\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtb_proyecto_4___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__obs(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__obs\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__react(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_dump_triggers__react\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_final(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_final\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_initial__TOP(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_initial__TOP\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i;
    tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i = 0;
    // Body
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000100U, tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[(0x000000ffU 
                                                                                & tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i)] = 0U;
        tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i 
            = ((::IData)(1U) + tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i);
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[0U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[1U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[2U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[3U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[4U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[5U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[6U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[7U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[8U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[9U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[10U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[11U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[12U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[13U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[14U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[15U] = 0U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__i = 0x00000010U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000100U, tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[(0x000000ffU 
                                                                                & tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i)] = 0U;
        tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i 
            = ((::IData)(1U) + tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i);
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[0U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[1U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[2U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[3U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[4U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[5U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[6U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[7U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[8U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[9U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[10U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[11U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[12U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[13U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[14U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[15U] = 0U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__i = 0x00000010U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000100U, tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[(0x000000ffU 
                                                                                & tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i)] = 0U;
        tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i 
            = ((::IData)(1U) + tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i);
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[0U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[1U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[2U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[3U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[4U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[5U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[6U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[7U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[8U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[9U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[10U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[11U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[12U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[13U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[14U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[15U] = 0U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__i = 0x00000010U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000100U, tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[(0x000000ffU 
                                                                                & tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i)] = 0U;
        tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i 
            = ((::IData)(1U) + tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i);
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[0U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[1U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[2U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[3U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[4U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[5U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[6U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[7U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[8U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[9U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[10U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[11U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[12U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[13U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[14U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[15U] = 0U;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__i = 0x00000010U;
    tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000100U, tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[(0x000000ffU 
                                                                                & tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i)] = 0U;
        tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i 
            = ((::IData)(1U) + tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i);
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[0U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[1U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[2U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[3U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[4U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[5U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[6U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[7U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[8U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[9U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[10U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[11U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[12U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[13U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[14U] = 0U;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[15U] = 0U;
    tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__i = 0x00000010U;
    VL_READMEM_N(true, 32, 512, 0, "proyecto4/alternativas/mmio_sma10/sw/trade.hex"s
                 ,  &(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem)
                 , 0, ~0ULL);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (::IData)(Vtb_proyecto_4___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtb_proyecto_4___024root___trigger_anySet__stl(const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___trigger_anySet__stl\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((::IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

extern const ::VlUnpacked<::CData/*0:0*/, 128> Vtb_proyecto_4__ConstPool__CONSARRAY_9;

VL_ATTR_COLD void Vtb_proyecto_4___024root___stl_comb__TOP__0(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___stl_comb__TOP__0\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__spi_req;
    tb_proyecto_4__DOT__dut__DOT__spi_req = 0;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a = 0;
    ::QData/*32:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext = 0;
    ::CData/*0:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i = 0;
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf = 0;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2118;
    __Vdfg_Regularize_2118 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2119;
    __Vdfg_Regularize_2119 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2121;
    __Vdfg_Regularize_2121 = 0;
    ::IData/*31:0*/ __Vdfg_Regularize_2122;
    __Vdfg_Regularize_2122 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2126;
    __Vdfg_Regularize_2126 = 0;
    ::CData/*3:0*/ __Vdfg_Regularize_2128;
    __Vdfg_Regularize_2128 = 0;
    ::IData/*31:0*/ __Vdfg_Regularize_2130;
    __Vdfg_Regularize_2130 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2136;
    __Vdfg_Regularize_2136 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2141;
    __Vdfg_Regularize_2141 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2142;
    __Vdfg_Regularize_2142 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2143;
    __Vdfg_Regularize_2143 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2144;
    __Vdfg_Regularize_2144 = 0;
    // Body
    vlSelfRef.__Vdfg_Regularize_2111 = ((0x7ffff000U 
                                         & ((- (::IData)(
                                                         (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                          >> 0x0000001fU))) 
                                            << 0x0000000cU)) 
                                        | ((((2U & 
                                              (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                               >> 0x0000001eU)) 
                                             | (1U 
                                                & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                   >> 7U))) 
                                            << 0x0000000aU) 
                                           | ((0x000003f0U 
                                               & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 0x00000015U)) 
                                              | (0x0000000fU 
                                                 & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                    >> 8U)))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o 
        = ((0x000000feU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift) 
                           << 1U)) | (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync) 
                                            >> 1U)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r 
        = (::IData)((2U == (6U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert 
        = (::IData)((4U == (6U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o 
        = (1U & ((0x00004000U != (0x0000607cU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                 | (~ (3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata 
        = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_per)
            ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o
            : ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_spi)
                ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o
                : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__b_rdata_o));
    vlSelfRef.__Vdfg_Regularize_2135 = ((~ ((0U == 
                                             (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                              >> 0x00000019U)) 
                                            | (::IData)(
                                                        (0x40000000U 
                                                         == 
                                                         (0xfe007000U 
                                                          & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))) 
                                        & (0x33U == 
                                           (0x0000007fU 
                                            & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)));
    __Vdfg_Regularize_2121 = (1U & ((0U != (0x00007000U 
                                            & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                    | (~ (3U == (3U 
                                                 & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))));
    __Vdfg_Regularize_2144 = (1U & ((~ (3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))) 
                                    | (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                       >> 3U)));
    __Vdfg_Regularize_2141 = (::IData)((7U == (7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)));
    __Vdfg_Regularize_2128 = ((0x00002000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                               ? ((0x00001000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                   ? 4U : 3U) : ((0x00001000U 
                                                  & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                  ? 
                                                 ((0x40000000U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                   ? 7U
                                                   : 6U)
                                                  : 2U));
    __Vdfg_Regularize_2126 = ((0x33U == (0x0000007fU 
                                         & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                              | (0x13U == (0x0000007fU 
                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)));
    __Vdfg_Regularize_2136 = ((0x23U == (0x0000007fU 
                                         & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                              | (0x63U == (0x0000007fU 
                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o 
        = (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__RDATA) 
            << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o 
        = (((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
             ? (2U & ((- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                          >> 4U)))) 
                      & ((- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                             >> 2U)))) 
                         & ((- (::IData)((1U & (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                   >> 3U))))) 
                            & (- (::IData)((3U == (3U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))))))
             : (1U & ((- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                          >> 4U)))) 
                      & ((- (::IData)((3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))) 
                         & ((- (::IData)((1U & (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                   >> 3U))))) 
                            & (- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 2U))))))))) 
           & (- (::IData)((1U & (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                    >> 6U))))));
    __Vdfg_Regularize_2142 = (1U & ((0U != (0x0000000cU 
                                            & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                    | (~ (3U == (3U 
                                                 & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))));
    __Vdfg_Regularize_2143 = (1U & ((~ (3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))) 
                                    | (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                       >> 2U)));
    __Vdfg_Regularize_2119 = (::IData)((3U == (0x0000000bU 
                                               & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i 
        = (((- (::IData)((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                          >> 0x0000001fU))) << 0x0000000cU) 
           | (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
              >> 0x00000014U));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o 
        = ((~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
               >> 1U)) & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r) 
                          & ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert)) 
                             & (7U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt)))));
    vlSelfRef.__Vdfg_Regularize_2139 = (::IData)(((0x00000060U 
                                                   == 
                                                   (0x00000060U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                                  & (::IData)(__Vdfg_Regularize_2141)));
    vlSelfRef.__Vdfg_Regularize_2127 = ((::IData)(__Vdfg_Regularize_2126) 
                                        & ((1U == (7U 
                                                   & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                      >> 0x0000000cU))) 
                                           | (5U == 
                                              (7U & 
                                               (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                >> 0x0000000cU)))));
    vlSelfRef.__Vdfg_Regularize_2137 = ((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                         >> 0x00000018U) 
                                        & ((0x33U == 
                                            (0x0000007fU 
                                             & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                           | (::IData)(__Vdfg_Regularize_2136)));
    vlSelfRef.__Vdfg_Regularize_2138 = ((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                         >> 0x00000013U) 
                                        & ((::IData)(__Vdfg_Regularize_2126) 
                                           | ((::IData)(__Vdfg_Regularize_2136) 
                                              | ((3U 
                                                  == 
                                                  (0x0000007fU 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                                 | (0x67U 
                                                    == 
                                                    (0x0000007fU 
                                                     & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))));
    if ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o 
            = (2U & ((- (::IData)((::IData)((0x00000024U 
                                             == (0x00000034U 
                                                 & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))) 
                     & (- (::IData)((3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o = 2U;
    } else {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o 
            = (1U & ((- (::IData)((3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))) 
                     & ((- (::IData)((1U & (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                               >> 3U))))) 
                        & ((- (::IData)((1U & (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 4U))))) 
                           & ((- (::IData)((1U & (~ 
                                                  (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                   >> 5U))))) 
                              & (- (::IData)((1U & 
                                              (~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 2U))))))))));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o 
            = ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                ? ((0x00000010U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                    ? 2U : ((8U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                             ? 2U : ((4U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                      ? 2U : ((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                               ? ((1U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                   ? 
                                                  (((1U 
                                                     == 
                                                     (7U 
                                                      & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                         >> 0x0000000cU)))
                                                     ? 1U
                                                     : 2U) 
                                                   & (- (::IData)(
                                                                  (0U 
                                                                   != 
                                                                   (7U 
                                                                    & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                       >> 0x0000000cU))))))
                                                   : 2U)
                                               : 2U))))
                : ((0x00000010U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                    ? 2U : ((8U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                             ? 2U : ((4U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                      ? 2U : ((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                               ? ((1U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                   ? 
                                                  ((0x00002000U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                    ? 2U
                                                    : 
                                                   (1U 
                                                    & (- (::IData)(
                                                                   (1U 
                                                                    & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                       >> 0x0000000cU))))))
                                                   : 2U)
                                               : 2U)))));
    }
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
        = ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o))
            ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q
            : ((((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__RDATA) 
                 << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__RDATA)) 
               & (- (::IData)((2U != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o))))));
    __Vdfg_Regularize_2118 = ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                  >> 2U)) & (::IData)(__Vdfg_Regularize_2119));
    if ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) {
        vlSelfRef.__Vdfg_Regularize_2124 = (1U & ((~ 
                                                   (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                    >> 5U)) 
                                                  | ((0x00000010U 
                                                      & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                      ? (::IData)(
                                                                  ((0U 
                                                                    != 
                                                                    (0x0000000cU 
                                                                     & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                                                   | (::IData)(__Vdfg_Regularize_2121)))
                                                      : 
                                                     ((8U 
                                                       & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                       ? 
                                                      ((~ 
                                                        (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                         >> 2U)) 
                                                       | (~ 
                                                          (3U 
                                                           == 
                                                           (3U 
                                                            & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))))
                                                       : 
                                                      ((4U 
                                                        & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                        ? (::IData)(__Vdfg_Regularize_2121)
                                                        : 
                                                       ((~ 
                                                         (3U 
                                                          == 
                                                          (3U 
                                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))) 
                                                        | (::IData)(
                                                                    (0x00002000U 
                                                                     == 
                                                                     (0x00006000U 
                                                                      & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))))))));
        vlSelfRef.__Vdfg_Regularize_2123 = (::IData)(
                                                     ((0x00000020U 
                                                       == 
                                                       (0x00000030U 
                                                        & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                                      & (::IData)(__Vdfg_Regularize_2141)));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o 
            = (0x0000000fU & (((0x00004000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                ? ((0x00002000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                    ? (0x0eU | (- (::IData)(
                                                            (1U 
                                                             & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                >> 0x0000000cU)))))
                                    : ((0x00001000U 
                                        & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                        ? 0x0dU : 0x0cU))
                                : (((0x00001000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                     ? 0x0bU : 0x0aU) 
                                   & (- (::IData)((1U 
                                                   & (~ 
                                                      (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                       >> 0x0000000dU))))))) 
                              & (- (::IData)((::IData)(
                                                       (0x00000023U 
                                                        == 
                                                        (0x0000003fU 
                                                         & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))))));
    } else if ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) {
        vlSelfRef.__Vdfg_Regularize_2124 = (1U & ((0x00000010U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                   ? (::IData)(__Vdfg_Regularize_2144)
                                                   : 
                                                  ((~ 
                                                    ((0U 
                                                      == 
                                                      (7U 
                                                       & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                          >> 0x0000000cU))) 
                                                     | ((1U 
                                                         == 
                                                         (7U 
                                                          & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                             >> 0x0000000cU))) 
                                                        | (2U 
                                                           == 
                                                           (7U 
                                                            & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                               >> 0x0000000cU)))))) 
                                                   | (::IData)(__Vdfg_Regularize_2142))));
        vlSelfRef.__Vdfg_Regularize_2123 = ((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                             >> 4U) 
                                            & (::IData)(__Vdfg_Regularize_2119));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o 
            = (0x0000000fU & ((- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 4U)))) 
                              & (((0x00004000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                   ? (::IData)(__Vdfg_Regularize_2128)
                                   : ((0x00002000U 
                                       & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                       ? ((0x00001000U 
                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                           ? 9U : 8U)
                                       : ((0x00001000U 
                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                           ? 5U : (1U 
                                                   & (- (::IData)(
                                                                  (1U 
                                                                   & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                      >> 0x0000001eU)))))))) 
                                 & (- (::IData)((::IData)(__Vdfg_Regularize_2118))))));
    } else {
        if ((0x00000010U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) {
            vlSelfRef.__Vdfg_Regularize_2124 = (1U 
                                                & (::IData)(__Vdfg_Regularize_2144));
            vlSelfRef.__Vdfg_Regularize_2123 = __Vdfg_Regularize_2119;
        } else {
            vlSelfRef.__Vdfg_Regularize_2124 = (1U 
                                                & ((8U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                    ? 
                                                   ((~ 
                                                     (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                      >> 2U)) 
                                                    | (::IData)(__Vdfg_Regularize_2121))
                                                    : 
                                                   (((0x00004000U 
                                                      & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                      ? 
                                                     (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                      >> 0x0000000dU)
                                                      : 
                                                     (3U 
                                                      == 
                                                      (3U 
                                                       & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                          >> 0x0000000cU)))) 
                                                    | (::IData)(__Vdfg_Regularize_2143))));
            vlSelfRef.__Vdfg_Regularize_2123 = __Vdfg_Regularize_2118;
        }
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o 
            = (0x0000000fU & ((- (::IData)((1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                  >> 4U)))) 
                              & (((0x00004000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                   ? (::IData)(__Vdfg_Regularize_2128)
                                   : ((0x00002000U 
                                       & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                       ? ((0x00001000U 
                                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                           ? 9U : 8U)
                                       : (5U & (- (::IData)(
                                                            (1U 
                                                             & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                >> 0x0000000cU))))))) 
                                 & (- (::IData)((::IData)(__Vdfg_Regularize_2118))))));
    }
    __Vdfg_Regularize_2130 = ((8U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                               ? tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i
                               : ((4U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                   ? ((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                       ? ((1U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                           ? (0xfffff000U 
                                              & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                           : tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i)
                                       : tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i)
                                   : tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i));
    vlSelfRef.__Vdfg_Regularize_2120 = ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                            >> 4U)) 
                                        & (::IData)(__Vdfg_Regularize_2118));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b 
        = ((1U & ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                   ? (::IData)(((0x00000020U != (0x00000038U 
                                                 & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                | (::IData)(__Vdfg_Regularize_2143)))
                   : (::IData)(((0x00000030U != (0x00000030U 
                                                 & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                | (::IData)(__Vdfg_Regularize_2142)))))
            ? ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                ? tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i
                : ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                    ? ((0x00000010U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                        ? __Vdfg_Regularize_2130 : 
                       (((- (::IData)((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                       >> 0x0000001fU))) 
                         << 0x0000000cU) | ((0x00000fe0U 
                                             & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                >> 0x00000014U)) 
                                            | (0x0000001fU 
                                               & ((8U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                   ? 
                                                  (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                   >> 0x00000014U)
                                                   : 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                    ? 
                                                   (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                    >> 0x00000014U)
                                                    : 
                                                   ((2U 
                                                     & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                     ? 
                                                    ((1U 
                                                      & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                      ? 
                                                     (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                      >> 7U)
                                                      : 
                                                     (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                      >> 0x00000014U))
                                                     : 
                                                    (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                     >> 0x00000014U))))))))
                    : ((0x00000010U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                        ? __Vdfg_Regularize_2130 : tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i)))
            : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o);
    vlSelfRef.__Vdfg_Regularize_2140 = ((vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                         >> 5U) & (::IData)(vlSelfRef.__Vdfg_Regularize_2120));
    vlSelfRef.__Vdfg_Regularize_2125 = ((::IData)(vlSelfRef.__Vdfg_Regularize_2123) 
                                        & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                           >> 0x0000000bU));
    __Vdfg_Regularize_2122 = (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
                              ^ vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b);
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
        = (0x00000001ffffffffULL & ((::QData)((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a)) 
                                    + ((::QData)((::IData)(
                                                           (0U 
                                                            != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o)))) 
                                       + (::QData)((::IData)(
                                                             ((0U 
                                                               != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                                                               ? 
                                                              (~ vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b)
                                                               : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b))))));
    vlSelfRef.__Vdfg_Regularize_2114 = (1U & (~ ((0x73U 
                                                  == 
                                                  (0x0000007fU 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                                 | ((::IData)(vlSelfRef.__Vdfg_Regularize_2127) 
                                                    | ((::IData)(vlSelfRef.__Vdfg_Regularize_2135) 
                                                       | ((::IData)(vlSelfRef.__Vdfg_Regularize_2137) 
                                                          | ((::IData)(vlSelfRef.__Vdfg_Regularize_2138) 
                                                             | ((::IData)(vlSelfRef.__Vdfg_Regularize_2124) 
                                                                | (::IData)(vlSelfRef.__Vdfg_Regularize_2125)))))))));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt 
        = (1U & ((::IData)((tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                            >> 0x0000001fU)) ^ ((__Vdfg_Regularize_2122 
                                                 >> 0x0000001fU) 
                                                & ((tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
                                                    >> 0x0000001fU) 
                                                   ^ (::IData)(
                                                               (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                                                                >> 0x0000001fU))))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o 
        = (((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
            & (0U == (0x00000018U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_2139));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                  >> 6U)) & ((::IData)(vlSelfRef.__Vdfg_Regularize_2120) 
                             & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q) 
                                & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q)))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
        = ((8U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
            ? ((4U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                ? (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext)
                : ((2U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                    ? (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext)
                    : (1U & ((1U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                              ? (~ (::IData)((tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                                              >> 0x00000020U)))
                              : (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt)))))
            : ((4U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                ? ((2U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                    ? (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext)
                    : ((1U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                        ? (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext)
                        : (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
                           & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b)))
                : ((2U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                    ? ((1U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))
                        ? (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
                           | vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b)
                        : __Vdfg_Regularize_2122) : (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext))));
    if ((0U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
            = (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                << 0x00000018U) | ((0x00ff0000U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                                                   << 0x00000010U)) 
                                   | ((0x0000ff00U 
                                       & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                                          << 8U)) | 
                                      (0x000000ffU 
                                       & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA)))));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o 
            = (0x0000000fU & ((::IData)(1U) << (3U 
                                                & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)));
    } else {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
            = ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
                ? (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                    << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA))
                : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o);
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o 
            = (0x0000000fU & (((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                ? 0x0cU : 3U) | (- (::IData)(
                                                             (1U 
                                                              != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))))));
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                  >> 6U)) & ((::IData)(vlSelfRef.__Vdfg_Regularize_2140) 
                             & (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o 
        = ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q)) 
           & (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__per_sel 
        = (::IData)((0x80000000U == (0x80010000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__spi_sel 
        = (::IData)((0x80010000U == (0x80010000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf 
        = (0x0000ffffU & ((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                           ? (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata 
                              >> 0x00000010U) : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o 
        = (((0x73U == (0x0000007fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
            | ((::IData)(vlSelfRef.__Vdfg_Regularize_2127) 
               | ((::IData)(vlSelfRef.__Vdfg_Regularize_2135) 
                  | ((::IData)(vlSelfRef.__Vdfg_Regularize_2137) 
                     | ((::IData)(vlSelfRef.__Vdfg_Regularize_2138) 
                        | ((::IData)(vlSelfRef.__Vdfg_Regularize_2125) 
                           | ((::IData)(vlSelfRef.__Vdfg_Regularize_2124) 
                              | ((~ (::IData)(vlSelfRef.__Vdfg_Regularize_2140)) 
                                 | (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                    >> 6U))))))))) 
           & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access 
        = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o) 
           & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__per_sel));
    tb_proyecto_4__DOT__dut__DOT__spi_req = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o) 
                                             & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__spi_sel));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte 
        = (0x000000ffU & ((1U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                           ? ((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf) 
                              >> 8U) : (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o 
        = (((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q)) 
            & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q)) 
           | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__pc_set_o 
        = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q) 
           & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q) 
              & ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o)) 
                 & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o) 
                    | ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
                       & ((::IData)(((8U == (0x00000018U 
                                             & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                     & (::IData)(vlSelfRef.__Vdfg_Regularize_2139))) 
                          | (::IData)((((0x00000060U 
                                         == (0x00000060U 
                                             & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                                        & (::IData)(vlSelfRef.__Vdfg_Regularize_2120)) 
                                       & Vtb_proyecto_4__ConstPool__CONSARRAY_9
                                       [(((0U == (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext)) 
                                          << 6U) | 
                                         (((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt) 
                                           << 5U) | 
                                          ((0x00000010U 
                                            & ((~ (::IData)(
                                                            (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                                                             >> 0x00000020U))) 
                                               << 4U)) 
                                           | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o))))]))))))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rd 
        = ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o)) 
           & (::IData)(tb_proyecto_4__DOT__dut__DOT__spi_req));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__wr 
        = ((::IData)(tb_proyecto_4__DOT__dut__DOT__spi_req) 
           & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o) 
              & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
        = ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o))
            ? ((0U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
                ? (((- (::IData)((((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte) 
                                   >> 7U) & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o)))) 
                    << 8U) | (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte))
                : ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
                    ? (((- (::IData)((((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf) 
                                       >> 0x0000000fU) 
                                      & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o)))) 
                        << 0x00000010U) | (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf))
                    : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata))
            : ((2U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o))
                ? ((::IData)(4U) + vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q)
                : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__wr 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((::IData)(vlSelfRef.__Vdfg_Regularize_2123) 
              & ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o)) 
                 & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q) 
                    & (0U != (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                             >> 7U)))))));
}

bool Vtb_proyecto_4___024root___trigger_anySet__ico(const ::VlUnpacked<::QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (::IData)(Vtb_proyecto_4___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vtb_proyecto_4___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (::IData)(Vtb_proyecto_4___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (::IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge tb_proyecto_4.clk)\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(negedge (4'hf == tb_proyecto_4.dut.por_cnt))\n");
    }
    if ((1U & (::IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_proyecto_4___024root___ctor_var_reset(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___ctor_var_reset\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    for (int __Vi0 = 0; __Vi0 < 20000; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__precio[__Vi0] = 0;
    }
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tb_proyecto_4__DOT__decision = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15306204047375165976ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__data_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12641094066854935835ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__spi_sel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13573909546887521665ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__per_sel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13782564240580455193ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__rd_is_per = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9826397652284995839ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__rd_is_spi = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9665086905742587952ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14629447742033416377ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__RDATA = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1555791898184285394ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18290073129406224726ull);
    }
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14167148520476540964ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6959000077490560340ull);
    }
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__RDATA = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3068655000108679531ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11357182187002278754ull);
    }
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__RDATA = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16780588979361250987ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13317397984400167574ull);
    }
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5423606615645959170ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9130216874983890136ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10464276933984930956ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_b = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8030371133929171004ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8591031746913466520ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_operator_o = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10540987240620036384ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15371062659794136254ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__rf_wd_sel_o = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18342511021195075972ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10910616283695332173ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14910855481220017030ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7300919350187062407ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__pc_set_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12072357817052948364ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3862877502390493495ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12839933191916671812ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16974470413694015070ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12260372803563727160ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12250634885502798407ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17783149744293634535ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 225817002397263710ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5074577720182286624ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2644477398408519655ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18131542795092121977ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17193685579758420025ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15856495485413509855ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 10575837437792923670ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__RDATA = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15682056837744401377ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5397387074479894007ull);
    }
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13721566727280791038ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11098695822665120803ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7032283637290523999ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rd = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3946028879686164387ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8388610718767448349ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14529846495644879780ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16608887225312073025ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9999484893582591121ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17541120552496515750ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2306908743404584560ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7232974811877812486ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2419316532785199674ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9153960451295381436ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3758794271995067306ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_q = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16450613384690495083ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6072286337129010360ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4665744629225152295ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13721854220625128686ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10463036308818841883ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__digit_q = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5488172828888639508ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6652291396415522ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_cycle_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9084697491423596161ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_meta_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4246104094893329101ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1510427164940560665ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15198618930722013123ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6998479207017301397ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 14554936344776974861ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9874873598650177360ull);
    vlSelf->tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__b_rdata_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12104809337316545260ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16875192959145403228ull);
    }
    vlSelf->__Vdfg_Regularize_2111 = 0;
    vlSelf->__Vdfg_Regularize_2114 = 0;
    vlSelf->__Vdfg_Regularize_2120 = 0;
    vlSelf->__Vdfg_Regularize_2123 = 0;
    vlSelf->__Vdfg_Regularize_2124 = 0;
    vlSelf->__Vdfg_Regularize_2125 = 0;
    vlSelf->__Vdfg_Regularize_2127 = 0;
    vlSelf->__Vdfg_Regularize_2135 = 0;
    vlSelf->__Vdfg_Regularize_2137 = 0;
    vlSelf->__Vdfg_Regularize_2138 = 0;
    vlSelf->__Vdfg_Regularize_2139 = 0;
    vlSelf->__Vdfg_Regularize_2140 = 0;
    vlSelf->__Vdly__tb_proyecto_4__DOT__dut__DOT__por_cnt_0 = 0;
    vlSelf->__Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12 = 0;
    vlSelf->__Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_170 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_171 = 0;
    vlSelf->__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_172 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_173 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_174 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_175 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_176 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_177 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_178 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_179 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_180 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_181 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_182 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_183 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_184 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_185 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_186 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_187 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_188 = 0;
    vlSelf->__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_189 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_190 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_191 = 0;
    vlSelf->__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_192 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_193 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_194 = 0;
    vlSelf->__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_195 = 0;
    vlSelf->__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_196 = 0;
    vlSelf->__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_197 = 0;
    vlSelf->__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_198 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_proyecto_4__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr_he805701c__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}
