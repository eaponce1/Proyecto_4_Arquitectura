// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_proyecto_4.h for the primary calling header

#include "Vtb_proyecto_4__pch.h"

VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_initial__TOP(Vtb_proyecto_4___024root* vlSelf);
VlCoroutine Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__0(Vtb_proyecto_4___024root* vlSelf);
VlCoroutine Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__1(Vtb_proyecto_4___024root* vlSelf);

void Vtb_proyecto_4___024root___eval_initial(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_initial\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtb_proyecto_4___024root___eval_initial__TOP(vlSelf);
    Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__1(vlSelf);
}

void Vtb_proyecto_4___024root___eval_sample(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_sample\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__ico(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG

bool Vtb_proyecto_4___024root___eval_ico(Vtb_proyecto_4___024root* vlSelf, ::CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_ico\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[0U]) 
                                     | (::IData)((::IData)(firstIteration)));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_proyecto_4___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    return (0U);
}

void Vtb_proyecto_4___024root___trigger_orInto__act_vec_vec(::VlUnpacked<::QData/*63:0*/, 1> &out, const ::VlUnpacked<::QData/*63:0*/, 1> &in);
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___dump_triggers__act(const ::VlUnpacked<::QData/*63:0*/, 1> &triggers, const ::std::string &tag);
#endif  // VL_DEBUG
bool Vtb_proyecto_4___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in);

bool Vtb_proyecto_4___024root___eval_act(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_act\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VactExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        ::CData/*0:0*/ __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_he805701c__0;
        __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_he805701c__0 = 0;
        __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_he805701c__0 
            = (0x0fU == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt));
        vlSelfRef.__VactTriggered[0U] = (::QData)((::IData)(
                                                            ((vlSelfRef.__Vnontrivs.__VdlySched.awaitingCurrentTime() 
                                                              << 2U) 
                                                             | ((((~ (::IData)(__Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_he805701c__0)) 
                                                                  & (::IData)(vlSelfRef.__Vtrigprevexpr_he805701c__1)) 
                                                                 << 1U) 
                                                                | ((::IData)(vlSelfRef.tb_proyecto_4__DOT__clk) 
                                                                   & (~ (::IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_proyecto_4__DOT__clk__0)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_proyecto_4__DOT__clk__0 
            = vlSelfRef.tb_proyecto_4__DOT__clk;
        vlSelfRef.__Vtrigprevexpr_he805701c__1 = __Vinline_0__eval_triggers_vec__act___Vtrigprevexpr_he805701c__0;
    }
    Vtb_proyecto_4___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_proyecto_4___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vtb_proyecto_4___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vtb_proyecto_4___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        {
            // Inlined CFunc: _timing_resume
            if ((((4ULL & vlSelfRef.__VactTriggered[0U])) != 0ULL)) {
                vlSelfRef.__Vnontrivs.__VdlySched.resume();
            }
        }
    }
    return (__VactExecute);
}

bool Vtb_proyecto_4___024root___eval_inact(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_inact\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__Vnontrivs.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 9, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vtb_proyecto_4___024root___nba_sequent__TOP__0(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___nba_sequent__TOP__1(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___nba_sequent__TOP__2(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___nba_sequent__TOP__3(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___trigger_clear__act(::VlUnpacked<::QData/*63:0*/, 1> &out);

bool Vtb_proyecto_4___024root___eval_nba(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_nba\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtb_proyecto_4___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_body__nba
            if ((((1ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
                Vtb_proyecto_4___024root___nba_sequent__TOP__0(vlSelf);
            }
            if ((((3ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
                Vtb_proyecto_4___024root___nba_sequent__TOP__1(vlSelf);
            }
            if ((((1ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
                Vtb_proyecto_4___024root___nba_sequent__TOP__2(vlSelf);
            }
            if ((((3ULL & vlSelfRef.__VnbaTriggered[0U])) != 0ULL)) {
                Vtb_proyecto_4___024root___nba_sequent__TOP__3(vlSelf);
            }
        }
        Vtb_proyecto_4___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

bool Vtb_proyecto_4___024root___eval_obs(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_obs\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

bool Vtb_proyecto_4___024root___eval_react(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_react\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

void Vtb_proyecto_4___024root___eval_postponed(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_postponed\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VlCoroutine Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__0(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::IData/*31:0*/ tb_proyecto_4__DOT__fd;
    tb_proyecto_4__DOT__fd = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__ref_q;
    tb_proyecto_4__DOT__ref_q = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__ref_w;
    tb_proyecto_4__DOT__ref_w = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__presupuesto;
    tb_proyecto_4__DOT__presupuesto = 0;
    ::IData/*31:0*/ tb_proyecto_4__DOT__unnamedblk3__DOT__n;
    tb_proyecto_4__DOT__unnamedblk3__DOT__n = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__leer_serie____Vlvbound_h3eba6be2__0_0;
    __Vtask_tb_proyecto_4__DOT__leer_serie____Vlvbound_h3eba6be2__0_0 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1;
    __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__leer_serie__fd_2;
    __Vtask_tb_proyecto_4__DOT__leer_serie__fd_2 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__leer_serie__t_3;
    __Vtask_tb_proyecto_4__DOT__leer_serie__t_3 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__leer_serie__r_4;
    __Vtask_tb_proyecto_4__DOT__leer_serie__r_4 = 0;
    ::CData/*7:0*/ __Vtask_tb_proyecto_4__DOT__spi__enviar_6;
    __Vtask_tb_proyecto_4__DOT__spi__enviar_6 = 0;
    ::CData/*7:0*/ __Vtask_tb_proyecto_4__DOT__spi__recibido_7;
    __Vtask_tb_proyecto_4__DOT__spi__recibido_7 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8;
    __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8 = 0;
    ::CData/*7:0*/ __Vtask_tb_proyecto_4__DOT__ejecutar__decision_9;
    __Vtask_tb_proyecto_4__DOT__ejecutar__decision_9 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__ejecutar__p_10;
    __Vtask_tb_proyecto_4__DOT__ejecutar__p_10 = 0;
    ::IData/*31:0*/ __Vtask_tb_proyecto_4__DOT__ejecutar__q_11;
    __Vtask_tb_proyecto_4__DOT__ejecutar__q_11 = 0;
    ::CData/*0:0*/ __Vtask_tb_proyecto_4__DOT__chequear__ok_12;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_12 = 0;
    ::CData/*0:0*/ __Vtask_tb_proyecto_4__DOT__chequear__ok_14;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_14 = 0;
    ::CData/*0:0*/ __Vtask_tb_proyecto_4__DOT__chequear__ok_16;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_16 = 0;
    ::CData/*0:0*/ __Vtask_tb_proyecto_4__DOT__chequear__ok_18;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_18 = 0;
    // Body
    __Vtask_tb_proyecto_4__DOT__leer_serie____Vlvbound_h3eba6be2__0_0 = 0U;
    __Vtask_tb_proyecto_4__DOT__leer_serie__t_3 = 0U;
    __Vtask_tb_proyecto_4__DOT__leer_serie__r_4 = 0U;
    vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__leer_serie__encabezado_5 = ""s;
    __Vtask_tb_proyecto_4__DOT__leer_serie__fd_2 = VL_FOPEN_NN("proyecto4/resultados/validacion_oficial/practica_meta.csv"s
                                                               , "r"s);
    ;
    if (VL_UNLIKELY(((0U == __Vtask_tb_proyecto_4__DOT__leer_serie__fd_2)))) {
        VL_WRITEF_NX("ERROR: no se encontro proyecto4/resultados/validacion_oficial/practica_meta.csv\n",0);
        VL_FINISH_MT("proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 43, "");
    }
    __Vtask_tb_proyecto_4__DOT__leer_serie__r_4 = VL_FGETS_NI(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__leer_serie__encabezado_5, __Vtask_tb_proyecto_4__DOT__leer_serie__fd_2);
    __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1 = 0U;
    while (VL_GTS_III(32, 0x00004e20U, __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1)) {
        if (VL_LIKELY(((0x4e1fU >= (0x00007fffU & __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1))))) {
            __Vtask_tb_proyecto_4__DOT__leer_serie__r_4 
                = VL_FSCANF_INX(__Vtask_tb_proyecto_4__DOT__leer_serie__fd_2,"%d,%d\n",2
                                , '#',32,&(__Vtask_tb_proyecto_4__DOT__leer_serie__t_3)
                                , '#',32,&(vlSelfRef.tb_proyecto_4__DOT__precio
                                           [(0x00007fffU 
                                             & __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1)])) ;
        } else {
            __Vtask_tb_proyecto_4__DOT__leer_serie__r_4 
                = VL_FSCANF_INX(__Vtask_tb_proyecto_4__DOT__leer_serie__fd_2,"%d,%d\n",2
                                , '#',32,&(__Vtask_tb_proyecto_4__DOT__leer_serie__t_3)
                                , '#',32,&(__Vtask_tb_proyecto_4__DOT__leer_serie____Vlvbound_h3eba6be2__0_0)) ;
        }
        __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1 
            = ((::IData)(1U) + __Vtask_tb_proyecto_4__DOT__leer_serie__unnamedblk1__DOT__n_1);
    }
    VL_FCLOSE_I(__Vtask_tb_proyecto_4__DOT__leer_serie__fd_2); tb_proyecto_4__DOT__fd 
        = VL_FOPEN_NN("C:/Users/Edu Ponce/Downloads/Proyecto-2_Juego-en-Assembly-main (1)/Proyecto-2_Juego-en-Assembly-main/pochoco_soc-main/proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2/decisiones.csv"s
                      , "w"s);
    ;
    VL_FWRITEF_NX(tb_proyecto_4__DOT__fd,"tick,precio,decision,caja,acciones,patrimonio\n",0);
    co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x00000000003d0900ULL, 
                                                     nullptr, 
                                                     "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                     123);
    tb_proyecto_4__DOT__unnamedblk3__DOT__n = 0U;
    while (VL_GTS_III(32, 0x00004e20U, tb_proyecto_4__DOT__unnamedblk3__DOT__n)) {
        __Vtask_tb_proyecto_4__DOT__spi__recibido_7 = 0;
        vlSelfRef.tb_proyecto_4__DOT__cs_n = 0U;
        __Vtask_tb_proyecto_4__DOT__spi__enviar_6 = 
            ((0x4e1fU >= (0x00007fffU & tb_proyecto_4__DOT__unnamedblk3__DOT__n))
              ? (0x000000ffU & vlSelfRef.tb_proyecto_4__DOT__precio
                 [(0x00007fffU & tb_proyecto_4__DOT__unnamedblk3__DOT__n)])
              : 0U);
        co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x00000000000f4240ULL, 
                                                         nullptr, 
                                                         "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                         54);
        __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8 = 0U;
        __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8 = 7U;
        while (VL_LTES_III(32, 0U, __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8)) {
            vlSelfRef.tb_proyecto_4__DOT__mosi = (1U 
                                                  & ((::IData)(__Vtask_tb_proyecto_4__DOT__spi__enviar_6) 
                                                     >> 
                                                     (7U 
                                                      & __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8)));
            co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x000000000007a120ULL, 
                                                             nullptr, 
                                                             "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                             57);
            vlSelfRef.tb_proyecto_4__DOT__sclk = 1U;
            if ((::IData)((((~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                                >> 1U)) & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift) 
                                           >> 7U)) 
                           & (~ ((~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                                     >> 1U)) & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift) 
                                                >> 7U)))))) {
                vlSelfRef.tb_proyecto_4__DOT__bits_x 
                    = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__bits_x);
            }
            __Vtask_tb_proyecto_4__DOT__spi__recibido_7 
                = (((~ ((::IData)(1U) << (7U & __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8))) 
                    & (::IData)(__Vtask_tb_proyecto_4__DOT__spi__recibido_7)) 
                   | (0x00ffU & ((::IData)(((~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                                                >> 1U)) 
                                            & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift) 
                                               >> 7U))) 
                                 << (7U & __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8))));
            co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x000000000007a120ULL, 
                                                             nullptr, 
                                                             "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                             60);
            vlSelfRef.tb_proyecto_4__DOT__sclk = 0U;
            __Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8 
                = (__Vtask_tb_proyecto_4__DOT__spi__unnamedblk2__DOT__b_8 
                   - (::IData)(1U));
        }
        co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x000000000007a120ULL, 
                                                         nullptr, 
                                                         "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                         62);
        __Vtask_tb_proyecto_4__DOT__ejecutar__p_10 
            = ((0x4e1fU >= (0x00007fffU & tb_proyecto_4__DOT__unnamedblk3__DOT__n))
                ? vlSelfRef.tb_proyecto_4__DOT__precio
               [(0x00007fffU & tb_proyecto_4__DOT__unnamedblk3__DOT__n)]
                : 0U);
        vlSelfRef.tb_proyecto_4__DOT__cs_n = 1U;
        vlSelfRef.tb_proyecto_4__DOT__decision = __Vtask_tb_proyecto_4__DOT__spi__recibido_7;
        __Vtask_tb_proyecto_4__DOT__ejecutar__decision_9 
            = vlSelfRef.tb_proyecto_4__DOT__decision;
        __Vtask_tb_proyecto_4__DOT__ejecutar__q_11 
            = (0x0000003fU & (::IData)(__Vtask_tb_proyecto_4__DOT__ejecutar__decision_9));
        if ((1U == (3U & ((::IData)(__Vtask_tb_proyecto_4__DOT__ejecutar__decision_9) 
                          >> 6U)))) {
            if (VL_GTS_III(32, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11, 
                           VL_DIVS_III(32, (vlSelfRef.tb_proyecto_4__DOT__caja 
                                            - (::IData)(5U)), __Vtask_tb_proyecto_4__DOT__ejecutar__p_10))) {
                __Vtask_tb_proyecto_4__DOT__ejecutar__q_11 
                    = VL_DIVS_III(32, (vlSelfRef.tb_proyecto_4__DOT__caja 
                                       - (::IData)(5U)), __Vtask_tb_proyecto_4__DOT__ejecutar__p_10);
            }
            if (VL_LTS_III(32, 0U, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11)) {
                vlSelfRef.tb_proyecto_4__DOT__caja 
                    = (vlSelfRef.tb_proyecto_4__DOT__caja 
                       - ((::IData)(5U) + VL_MULS_III(32, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11, __Vtask_tb_proyecto_4__DOT__ejecutar__p_10)));
                vlSelfRef.tb_proyecto_4__DOT__acciones 
                    = (vlSelfRef.tb_proyecto_4__DOT__acciones 
                       + __Vtask_tb_proyecto_4__DOT__ejecutar__q_11);
                vlSelfRef.tb_proyecto_4__DOT__ordenes 
                    = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__ordenes);
            }
        } else if ((2U == (3U & ((::IData)(__Vtask_tb_proyecto_4__DOT__ejecutar__decision_9) 
                                 >> 6U)))) {
            if (VL_GTS_III(32, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11, vlSelfRef.tb_proyecto_4__DOT__acciones)) {
                __Vtask_tb_proyecto_4__DOT__ejecutar__q_11 
                    = vlSelfRef.tb_proyecto_4__DOT__acciones;
            }
            if ((VL_LTS_III(32, 0U, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11) 
                 & VL_LTES_III(32, 5U, (vlSelfRef.tb_proyecto_4__DOT__caja 
                                        + VL_MULS_III(32, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11, __Vtask_tb_proyecto_4__DOT__ejecutar__p_10))))) {
                vlSelfRef.tb_proyecto_4__DOT__caja 
                    = (vlSelfRef.tb_proyecto_4__DOT__caja 
                       + (VL_MULS_III(32, __Vtask_tb_proyecto_4__DOT__ejecutar__q_11, __Vtask_tb_proyecto_4__DOT__ejecutar__p_10) 
                          - (::IData)(5U)));
                vlSelfRef.tb_proyecto_4__DOT__acciones 
                    = (vlSelfRef.tb_proyecto_4__DOT__acciones 
                       - __Vtask_tb_proyecto_4__DOT__ejecutar__q_11);
                vlSelfRef.tb_proyecto_4__DOT__ordenes 
                    = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__ordenes);
            }
        }
        vlSelfRef.tb_proyecto_4__DOT__w = (vlSelfRef.tb_proyecto_4__DOT__caja 
                                           + VL_MULS_III(32, vlSelfRef.tb_proyecto_4__DOT__acciones, __Vtask_tb_proyecto_4__DOT__ejecutar__p_10));
        if (VL_GTS_III(32, vlSelfRef.tb_proyecto_4__DOT__w, vlSelfRef.tb_proyecto_4__DOT__peak)) {
            vlSelfRef.tb_proyecto_4__DOT__peak = vlSelfRef.tb_proyecto_4__DOT__w;
        }
        if (VL_GTS_III(32, (vlSelfRef.tb_proyecto_4__DOT__peak 
                            - vlSelfRef.tb_proyecto_4__DOT__w), vlSelfRef.tb_proyecto_4__DOT__max_dd)) {
            vlSelfRef.tb_proyecto_4__DOT__max_dd = 
                (vlSelfRef.tb_proyecto_4__DOT__peak 
                 - vlSelfRef.tb_proyecto_4__DOT__w);
        }
        VL_FWRITEF_NX(tb_proyecto_4__DOT__fd,"%0d,%0d,%02h,%0d,%0d,%0d\n",6
                      , '~',32,tb_proyecto_4__DOT__unnamedblk3__DOT__n
                      , '~',32,((0x4e1fU >= (0x00007fffU 
                                             & tb_proyecto_4__DOT__unnamedblk3__DOT__n))
                                 ? vlSelfRef.tb_proyecto_4__DOT__precio
                                [(0x00007fffU & tb_proyecto_4__DOT__unnamedblk3__DOT__n)]
                                 : 0U), '#',8,(::IData)(vlSelfRef.tb_proyecto_4__DOT__decision)
                      , '~',32,vlSelfRef.tb_proyecto_4__DOT__caja
                      , '~',32,vlSelfRef.tb_proyecto_4__DOT__acciones
                      , '~',32,vlSelfRef.tb_proyecto_4__DOT__w);
        co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x000000003b09d4a0ULL, 
                                                         nullptr, 
                                                         "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                         129);
        tb_proyecto_4__DOT__unnamedblk3__DOT__n = ((::IData)(1U) 
                                                   + tb_proyecto_4__DOT__unnamedblk3__DOT__n);
    }
    VL_FCLOSE_I(tb_proyecto_4__DOT__fd); tb_proyecto_4__DOT__ref_q 
        = VL_DIVS_III(32, (::IData)(0x0000270bU), vlSelfRef.tb_proyecto_4__DOT__precio[0U]);
    tb_proyecto_4__DOT__ref_w = (((::IData)(0x0000270bU) 
                                  - VL_MULS_III(32, tb_proyecto_4__DOT__ref_q, vlSelfRef.tb_proyecto_4__DOT__precio[0U])) 
                                 + VL_MULS_III(32, tb_proyecto_4__DOT__ref_q, vlSelfRef.tb_proyecto_4__DOT__precio[19999U]));
    tb_proyecto_4__DOT__presupuesto = 0x000060baU;
    VL_WRITEF_NX("Patrimonio final:          %0d\nOrdenes ejecutadas:        %0d\nPerdida maxima:            %0d\nNo operar:                 10000\nComprar y mantener:        %0d\nPeor caso precio->decision: %0d ciclos (disponibles: %0d)\nCiclos promedio precio->decision: %0.2f (%0d respuestas)\nSuma de ciclos de respuesta: %0d\nDetalle por tick en decisiones.csv\n",9
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__w
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__ordenes
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__max_dd
                 , '~',32,tb_proyecto_4__DOT__ref_w
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__peor_caso
                 , '~',32,tb_proyecto_4__DOT__presupuesto
                 , 'D',((0U != vlSelfRef.tb_proyecto_4__DOT__respuestas)
                         ? ((1.0 * VL_ITOR_D_Q(64, vlSelfRef.tb_proyecto_4__DOT__ciclos_acumulados)) 
                            / VL_ISTOR_D_I(32, vlSelfRef.tb_proyecto_4__DOT__respuestas))
                         : 0.0), '~',32,vlSelfRef.tb_proyecto_4__DOT__respuestas
                 , '#',64,vlSelfRef.tb_proyecto_4__DOT__ciclos_acumulados);
    vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_13 = "MISO sin valores X"s;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_12 = (0U 
                                                   == vlSelfRef.tb_proyecto_4__DOT__bits_x);
    vlSelfRef.tb_proyecto_4__DOT__total_tests = ((::IData)(1U) 
                                                 + vlSelfRef.tb_proyecto_4__DOT__total_tests);
    if (__Vtask_tb_proyecto_4__DOT__chequear__ok_12) {
        vlSelfRef.tb_proyecto_4__DOT__tests_aprobados 
            = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__tests_aprobados);
        VL_WRITEF_NX("PASS %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_13));
    } else {
        VL_WRITEF_NX("FAIL %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_13));
    }
    vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_15 = "el programa escribe DECISION"s;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_14 = VL_LTS_III(32, 0U, vlSelfRef.tb_proyecto_4__DOT__respuestas);
    vlSelfRef.tb_proyecto_4__DOT__total_tests = ((::IData)(1U) 
                                                 + vlSelfRef.tb_proyecto_4__DOT__total_tests);
    if (__Vtask_tb_proyecto_4__DOT__chequear__ok_14) {
        vlSelfRef.tb_proyecto_4__DOT__tests_aprobados 
            = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__tests_aprobados);
        VL_WRITEF_NX("PASS %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_15));
    } else {
        VL_WRITEF_NX("FAIL %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_15));
    }
    vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_17 = "el programa lee todos los precios"s;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_16 = (0U 
                                                   == vlSelfRef.tb_proyecto_4__DOT__precios_perdidos);
    vlSelfRef.tb_proyecto_4__DOT__total_tests = ((::IData)(1U) 
                                                 + vlSelfRef.tb_proyecto_4__DOT__total_tests);
    if (__Vtask_tb_proyecto_4__DOT__chequear__ok_16) {
        vlSelfRef.tb_proyecto_4__DOT__tests_aprobados 
            = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__tests_aprobados);
        VL_WRITEF_NX("PASS %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_17));
    } else {
        VL_WRITEF_NX("FAIL %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_17));
    }
    vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_19 = "la decision llega antes del siguiente tick"s;
    __Vtask_tb_proyecto_4__DOT__chequear__ok_18 = VL_LTS_III(32, vlSelfRef.tb_proyecto_4__DOT__peor_caso, tb_proyecto_4__DOT__presupuesto);
    vlSelfRef.tb_proyecto_4__DOT__total_tests = ((::IData)(1U) 
                                                 + vlSelfRef.tb_proyecto_4__DOT__total_tests);
    if (__Vtask_tb_proyecto_4__DOT__chequear__ok_18) {
        vlSelfRef.tb_proyecto_4__DOT__tests_aprobados 
            = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__tests_aprobados);
        VL_WRITEF_NX("PASS %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_19));
    } else {
        VL_WRITEF_NX("FAIL %s\n",1, 'S',&(vlSelfRef.__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_19));
    }
    VL_WRITEF_NX("Testbenchs aprobados: %0d/%0d\n",2
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__tests_aprobados
                 , '~',32,vlSelfRef.tb_proyecto_4__DOT__total_tests);
    VL_FINISH_MT("proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 153, "");
    co_return;
}

VlCoroutine Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__1(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_initial__TOP__Vtiming__1\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    while (VL_LIKELY(!vlSymsp->_vm_contextp__->gotFinish())) {
        co_await vlSelfRef.__Vnontrivs.__VdlySched.delay(0x0000000000004e20ULL, 
                                                         nullptr, 
                                                         "proyecto4/resultados/validacion_oficial/corridas/mmio_sma10_base/ronda_2\\tb_proyecto_4_configurado.sv", 
                                                         23);
        vlSelfRef.tb_proyecto_4__DOT__clk = (1U & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__clk)));
    }
    co_return;
}

bool Vtb_proyecto_4___024root___trigger_anySet__ico(const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___trigger_anySet__ico\n"); );
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

bool Vtb_proyecto_4___024root___trigger_anySet__act(const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___trigger_anySet__act\n"); );
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

void Vtb_proyecto_4___024root___nba_sequent__TOP__0(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___nba_sequent__TOP__0\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_38;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_38 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_39;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_39 = 0;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_40;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_40 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_41;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_41 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_42;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_42 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_43;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_43 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_44;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_44 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_45;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_45 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_46;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_46 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_47;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_47 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_48;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_48 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_49;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_49 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_50;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_50 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_51;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_51 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_52;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_52 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_53;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_53 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_54;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_54 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_55;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_55 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_56;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_56 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_57;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_57 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_58;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_58 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_59;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_59 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_60;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_60 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_61;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_61 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_62;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_62 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_63;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_63 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_64;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_64 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_65;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_65 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_66;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_66 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_67;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_67 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_68;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_68 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_69;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_69 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_70;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_70 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_71;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_71 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_72;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_72 = 0;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_73;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_73 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_74;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_74 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_75;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_75 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_76;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_76 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_77;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_77 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_78;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_78 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_79;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_79 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_80;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_80 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_81;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_81 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_82;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_82 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_83;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_83 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_84;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_84 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_85;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_85 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_86;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_86 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_87;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_87 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_88;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_88 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_89;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_89 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_90;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_90 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_91;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_91 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_92;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_92 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_93;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_93 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_94;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_94 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_95;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_95 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_96;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_96 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_97;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_97 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_98;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_98 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_99;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_99 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_100;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_100 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_101;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_101 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_102;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_102 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_103;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_103 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_104;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_104 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_105;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_105 = 0;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_106;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_106 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_107;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_107 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_108;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_108 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_109;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_109 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_110;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_110 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_111;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_111 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_112;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_112 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_113;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_113 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_114;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_114 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_115;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_115 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_116;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_116 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_117;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_117 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_118;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_118 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_119;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_119 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_120;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_120 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_121;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_121 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_122;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_122 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_123;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_123 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_124;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_124 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_125;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_125 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_126;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_126 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_127;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_127 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_128;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_128 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_129;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_129 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_130;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_130 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_131;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_131 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_132;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_132 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_133;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_133 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_134;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_134 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_135;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_135 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_136;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_136 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_137;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_137 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_138;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_138 = 0;
    ::CData/*0:0*/ __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_139;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_139 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_140;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_140 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_141;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_141 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_142;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_142 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_143;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_143 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_144;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_144 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_145;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_145 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_146;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_146 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_147;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_147 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_148;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_148 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_149;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_149 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_150;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_150 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_151;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_151 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_152;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_152 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_153;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_153 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_154;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_154 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_155;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_155 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_156;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_156 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_157;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_157 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_158;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_158 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_159;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_159 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_160;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_160 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_161;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_161 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_162;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_162 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_163;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_163 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_164;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_164 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_165;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_165 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_166;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_166 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_167;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_167 = 0;
    ::CData/*0:0*/ __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_168;
    __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_168 = 0;
    ::CData/*7:0*/ __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_169;
    __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_169 = 0;
    // Body
    vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__por_cnt_0 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt;
    vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_172 = 0U;
    vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_189 = 0U;
    vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_192 = 0U;
    vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_195 = 0U;
    vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_198 = 0U;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_40 = 0U;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_73 = 0U;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_106 = 0U;
    __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_139 = 0U;
    vlSelfRef.tb_proyecto_4__DOT__ciclos = ((::IData)(1U) 
                                            + vlSelfRef.tb_proyecto_4__DOT__ciclos);
    if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o) {
        vlSelfRef.tb_proyecto_4__DOT__ciclos = 0U;
        vlSelfRef.tb_proyecto_4__DOT__esperando = 1U;
        if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q) {
            vlSelfRef.tb_proyecto_4__DOT__precios_perdidos 
                = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__precios_perdidos);
        }
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_170 
            = (1U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_171 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_172 = 1U;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_173 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 1U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_174 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_175 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 2U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_176 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_177 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 3U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_178 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_179 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 4U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_180 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_181 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 5U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_182 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_183 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 6U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_184 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
        vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_185 
            = (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o) 
                     >> 7U));
        vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_186 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
    } else if ((((::IData)(vlSelfRef.tb_proyecto_4__DOT__esperando) 
                 & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__wr)) 
                & (8U == (0x000000fcU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)))) {
        if (VL_GTS_III(32, vlSelfRef.tb_proyecto_4__DOT__ciclos, vlSelfRef.tb_proyecto_4__DOT__peor_caso)) {
            vlSelfRef.tb_proyecto_4__DOT__peor_caso 
                = vlSelfRef.tb_proyecto_4__DOT__ciclos;
        }
        vlSelfRef.tb_proyecto_4__DOT__respuestas = 
            ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__respuestas);
        vlSelfRef.tb_proyecto_4__DOT__ciclos_acumulados 
            = (vlSelfRef.tb_proyecto_4__DOT__ciclos_acumulados 
               + (::QData)((::IData)(vlSelfRef.tb_proyecto_4__DOT__ciclos)));
        vlSelfRef.tb_proyecto_4__DOT__esperando = 0U;
    }
    if ((0x0fU != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt))) {
        vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__por_cnt_0 
            = (0x0000000fU & ((::IData)(1U) + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt)));
    }
    if ((((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
              >> 0x0000001fU)) & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o)) 
         & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o))) {
        if ((1U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o))) {
            vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_187 
                = (0x000000ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o);
            vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_188 
                = (0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                  >> 2U));
            vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_189 = 1U;
        }
        if ((2U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o))) {
            vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_190 
                = (0x000000ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
                                  >> 8U));
            vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_191 
                = (0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                  >> 2U));
            vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_192 = 1U;
        }
        if ((4U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o))) {
            vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_193 
                = (0x000000ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
                                  >> 0x10U));
            vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_194 
                = (0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                  >> 2U));
            vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_195 = 1U;
        }
        if ((8U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o))) {
            vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_196 
                = (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
                   >> 0x18U);
            vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_197 
                = (0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                  >> 2U));
            vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_198 = 1U;
        }
    }
    if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__wr) {
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_38 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000010U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_39 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_40 = 1U;
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_41 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000011U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_42 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_43 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000012U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_44 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_45 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000013U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_46 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_47 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000014U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_48 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_49 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000015U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_50 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_51 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000016U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_52 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_53 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000017U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_54 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_55 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000018U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_56 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_57 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000019U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_58 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_59 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001aU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_60 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_61 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001bU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_62 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_63 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001cU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_64 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_65 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001dU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_66 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_67 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001eU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_68 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_69 
            = (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
               >> 0x0000001fU);
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_70 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_71 
            = (1U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o);
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_72 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_73 = 1U;
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_74 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 1U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_75 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_76 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 2U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_77 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_78 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 3U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_79 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_80 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 4U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_81 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_82 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 5U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_83 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_84 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 6U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_85 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_86 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 7U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_87 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_88 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 8U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_89 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_90 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 9U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_91 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_92 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000aU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_93 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_94 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000bU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_95 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_96 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000cU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_97 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_98 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000dU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_99 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_100 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000eU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_101 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_102 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000fU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_103 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_104 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000010U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_105 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_106 = 1U;
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_107 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000011U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_108 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_109 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000012U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_110 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_111 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000013U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_112 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_113 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000014U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_114 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_115 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000015U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_116 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_117 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000016U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_118 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_119 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000017U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_120 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_121 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000018U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_122 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_123 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x00000019U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_124 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_125 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001aU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_126 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_127 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001bU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_128 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_129 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001cU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_130 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_131 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001dU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_132 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_133 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000001eU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_134 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_135 
            = (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
               >> 0x0000001fU);
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_136 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_137 
            = (1U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o);
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_138 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_139 = 1U;
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_140 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 1U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_141 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_142 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 2U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_143 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_144 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 3U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_145 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_146 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 4U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_147 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_148 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 5U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_149 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_150 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 6U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_151 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_152 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 7U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_153 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_154 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 8U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_155 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_156 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 9U));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_157 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_158 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000aU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_159 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_160 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000bU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_161 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_162 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000cU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_163 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_164 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000dU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_165 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_166 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000eU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_167 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
        __Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_168 
            = (1U & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__rf_wdata_o 
                     >> 0x0000000fU));
        __Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_169 
            = (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                              >> 7U));
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__b_rdata_o 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
        [(0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                         >> 2U))];
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__RDATA 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
        [(0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                         >> 0x00000014U))];
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
        [(0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                         >> 0x00000014U))];
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__RDATA 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
        [(0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                         >> 0x0000000fU))];
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__RDATA 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
        [(0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                         >> 0x0000000fU))];
    if (__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_40) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_39] 
            = ((0xfffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_39]) 
               | (::SData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_38));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_42] 
            = ((0xfffdU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_42]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_41)) 
                  << 1U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_44] 
            = ((0xfffbU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_44]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_43)) 
                  << 2U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_46] 
            = ((0xfff7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_46]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_45)) 
                  << 3U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_48] 
            = ((0xffefU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_48]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_47)) 
                  << 4U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_50] 
            = ((0xffdfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_50]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_49)) 
                  << 5U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_52] 
            = ((0xffbfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_52]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_51)) 
                  << 6U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_54] 
            = ((0xff7fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_54]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_53)) 
                  << 7U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_56] 
            = ((0xfeffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_56]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_55)) 
                  << 8U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_58] 
            = ((0xfdffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_58]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_57)) 
                  << 9U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_60] 
            = ((0xfbffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_60]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_59)) 
                  << 0x0000000aU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_62] 
            = ((0xf7ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_62]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_61)) 
                  << 0x0000000bU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_64] 
            = ((0xefffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_64]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_63)) 
                  << 0x0000000cU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_66] 
            = ((0xdfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_66]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_65)) 
                  << 0x0000000dU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_68] 
            = ((0xbfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_68]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_67)) 
                  << 0x0000000eU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_70] 
            = ((0x7fffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_70]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__mem_69)) 
                  << 0x0000000fU));
    }
    if (__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_73) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_72] 
            = ((0xfffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_72]) 
               | (::SData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_71));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_75] 
            = ((0xfffdU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_75]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_74)) 
                  << 1U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_77] 
            = ((0xfffbU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_77]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_76)) 
                  << 2U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_79] 
            = ((0xfff7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_79]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_78)) 
                  << 3U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_81] 
            = ((0xffefU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_81]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_80)) 
                  << 4U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_83] 
            = ((0xffdfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_83]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_82)) 
                  << 5U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_85] 
            = ((0xffbfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_85]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_84)) 
                  << 6U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_87] 
            = ((0xff7fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_87]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_86)) 
                  << 7U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_89] 
            = ((0xfeffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_89]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_88)) 
                  << 8U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_91] 
            = ((0xfdffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_91]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_90)) 
                  << 9U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_93] 
            = ((0xfbffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_93]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_92)) 
                  << 0x0000000aU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_95] 
            = ((0xf7ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_95]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_94)) 
                  << 0x0000000bU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_97] 
            = ((0xefffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_97]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_96)) 
                  << 0x0000000cU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_99] 
            = ((0xdfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_99]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_98)) 
                  << 0x0000000dU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_101] 
            = ((0xbfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_101]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_100)) 
                  << 0x0000000eU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_103] 
            = ((0x7fffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_103]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__mem_102)) 
                  << 0x0000000fU));
    }
    if (__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_106) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_105] 
            = ((0xfffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_105]) 
               | (::SData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_104));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_108] 
            = ((0xfffdU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_108]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_107)) 
                  << 1U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_110] 
            = ((0xfffbU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_110]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_109)) 
                  << 2U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_112] 
            = ((0xfff7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_112]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_111)) 
                  << 3U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_114] 
            = ((0xffefU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_114]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_113)) 
                  << 4U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_116] 
            = ((0xffdfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_116]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_115)) 
                  << 5U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_118] 
            = ((0xffbfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_118]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_117)) 
                  << 6U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_120] 
            = ((0xff7fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_120]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_119)) 
                  << 7U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_122] 
            = ((0xfeffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_122]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_121)) 
                  << 8U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_124] 
            = ((0xfdffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_124]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_123)) 
                  << 9U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_126] 
            = ((0xfbffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_126]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_125)) 
                  << 0x0000000aU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_128] 
            = ((0xf7ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_128]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_127)) 
                  << 0x0000000bU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_130] 
            = ((0xefffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_130]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_129)) 
                  << 0x0000000cU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_132] 
            = ((0xdfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_132]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_131)) 
                  << 0x0000000dU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_134] 
            = ((0xbfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_134]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_133)) 
                  << 0x0000000eU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_136] 
            = ((0x7fffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_136]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__mem_135)) 
                  << 0x0000000fU));
    }
    if (__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_139) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_138] 
            = ((0xfffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_138]) 
               | (::SData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_137));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_141] 
            = ((0xfffdU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_141]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_140)) 
                  << 1U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_143] 
            = ((0xfffbU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_143]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_142)) 
                  << 2U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_145] 
            = ((0xfff7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_145]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_144)) 
                  << 3U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_147] 
            = ((0xffefU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_147]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_146)) 
                  << 4U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_149] 
            = ((0xffdfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_149]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_148)) 
                  << 5U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_151] 
            = ((0xffbfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_151]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_150)) 
                  << 6U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_153] 
            = ((0xff7fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_153]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_152)) 
                  << 7U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_155] 
            = ((0xfeffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_155]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_154)) 
                  << 8U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_157] 
            = ((0xfdffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_157]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_156)) 
                  << 9U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_159] 
            = ((0xfbffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_159]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_158)) 
                  << 0x0000000aU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_161] 
            = ((0xf7ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_161]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_160)) 
                  << 0x0000000bU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_163] 
            = ((0xefffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_163]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_162)) 
                  << 0x0000000cU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_165] 
            = ((0xdfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_165]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_164)) 
                  << 0x0000000dU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_167] 
            = ((0xbfffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_167]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_166)) 
                  << 0x0000000eU));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem[__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_169] 
            = ((0x7fffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem
                [__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_169]) 
               | ((::SData)((::IData)(__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__mem_168)) 
                  << 0x0000000fU));
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o 
        = (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_hi__DOT__RDATA) 
            << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA));
}

void Vtb_proyecto_4___024root___nba_sequent__TOP__1(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___nba_sequent__TOP__1\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::CData/*3:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16 = 0;
    ::SData/*11:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17 = 0;
    ::CData/*2:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18 = 0;
    ::CData/*2:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19 = 0;
    ::CData/*2:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20 = 0;
    ::CData/*7:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21 = 0;
    ::CData/*2:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22 = 0;
    ::CData/*7:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23 = 0;
    ::CData/*3:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30 = 0;
    ::IData/*17:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31 = 0;
    ::IData/*31:0*/ __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33 = 0;
    // Body
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync;
    vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q;
    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift;
    vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q;
    if ((0x0fU == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt))) {
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33 
            = ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q);
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19 
            = ((6U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync) 
                      << 1U)) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__mosi));
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18 
            = ((6U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync) 
                      << 1U)) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__sclk));
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20 
            = ((6U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                      << 1U)) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__cs_n));
        if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert) {
            __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22 = 0U;
            __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21 
                = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold;
        } else if ((1U & (~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                             >> 1U)))) {
            if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r) {
                __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22 
                    = (7U & ((::IData)(1U) + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt)));
            }
            if ((::IData)((4U == (6U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync))))) {
                __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21 
                    = ((0U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt))
                        ? (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold)
                        : (0x000000feU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift) 
                                          << 1U)));
            }
        }
        if ((1U & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert)))) {
            if ((1U & (~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                          >> 1U)))) {
                if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r) {
                    __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23 
                        = ((0x000000feU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift) 
                                           << 1U)) 
                           | (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync) 
                                    >> 1U)));
                }
            }
        }
        if (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q) 
             != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q))) {
            __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30 
                = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q;
            __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31 = 0U;
        } else if ((0x0003d08fU != vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q)) {
            __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31 
                = (0x0003ffffU & ((::IData)(1U) + vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q));
        }
        if ((1U & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o)))) {
            vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12 
                = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__pc_set_o)
                    ? ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o)
                        ? (0xfffffffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                        : (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q 
                           + (((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                ? ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                    ? ((0x00000010U 
                                        & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                        ? vlSelfRef.__Vdfg_Regularize_2111
                                        : ((8U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                            ? ((4U 
                                                & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                ? (
                                                   (2U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                    ? 
                                                   ((1U 
                                                     & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)
                                                     ? 
                                                    ((((0x00000ffeU 
                                                        & ((- (::IData)(
                                                                        (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                         >> 0x0000001fU))) 
                                                           << 1U)) 
                                                       | (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                          >> 0x0000001fU)) 
                                                      << 0x00000013U) 
                                                     | ((0x0007f800U 
                                                         & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                            >> 1U)) 
                                                        | ((0x00000400U 
                                                            & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                               >> 0x0000000aU)) 
                                                           | (0x000003ffU 
                                                              & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                                                 >> 0x00000015U)))))
                                                     : vlSelfRef.__Vdfg_Regularize_2111)
                                                    : vlSelfRef.__Vdfg_Regularize_2111)
                                                : vlSelfRef.__Vdfg_Regularize_2111)
                                            : vlSelfRef.__Vdfg_Regularize_2111))
                                    : vlSelfRef.__Vdfg_Regularize_2111)
                                : vlSelfRef.__Vdfg_Regularize_2111) 
                              << 1U))) : ((::IData)(4U) 
                                          + vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q));
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q 
                = (1U & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__pc_set_o)));
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q 
                = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q;
        }
        if (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o) 
             & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o)))) {
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_per 
                = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__per_sel;
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_spi 
                = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__spi_sel;
        }
        if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rd) {
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o 
                = ((0x00000080U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                    ? 0U : ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                             ? 0U : ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                      ? 0U : ((0x00000010U 
                                               & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                               ? ((8U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                   ? 0U
                                                   : 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? 0U
                                                    : 
                                                   (0x0aU 
                                                    == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q))))
                                               : ((8U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                   ? 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q)
                                                    : 0U)
                                                   : 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_q)
                                                    : 
                                                   ((2U 
                                                     & ((~ 
                                                         ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
                                                          >> 1U)) 
                                                        << 1U)) 
                                                    | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q))))))));
        }
        if (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o) {
            vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15 
                = ((9U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q))
                    ? 0U : (0x0000000fU & ((::IData)(1U) 
                                           + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q))));
            if ((0x0aU > (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q))) {
                __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16 
                    = (0x0000000fU & ((::IData)(1U) 
                                      + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q)));
                __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17 
                    = (0x00000fffU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q) 
                                      + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o)));
            } else {
                __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17 
                    = (0x00000fffU & (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q) 
                                       - (0x000000ffU 
                                          & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__RDATA))) 
                                      + (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o)));
            }
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_q 
                = ((0x000000feU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift) 
                                   << 1U)) | (1U & 
                                              ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync) 
                                               >> 1U)));
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q = 1U;
        } else if ((::IData)(((4U == (0x000000fcU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)) 
                              & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rd)))) {
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q = 0U;
        }
        if (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access) 
             & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o)))) {
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o 
                = ((0x00000080U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                    ? 0U : ((0x00000040U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                             ? 0U : ((0x00000020U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                      ? 0U : ((0x00000010U 
                                               & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                               ? ((8U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                   ? 0U
                                                   : 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? 0U
                                                    : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_cycle_q))
                                               : ((8U 
                                                   & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                   ? 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q
                                                    : (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_q))
                                                   : 
                                                  ((4U 
                                                    & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                                    ? (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_q)
                                                    : (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__digit_q)))))));
        }
        if (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__wr) 
             & (8U == (0x000000fcU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)))) {
            vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold 
                = (0x000000ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o);
        }
        if ((((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access) 
              & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o)) 
             & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o))) {
            if ((0U != (0x0000003fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                       >> 2U)))) {
                if ((1U == (0x0000003fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                           >> 2U)))) {
                    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_cycle_q 
                        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q;
                    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_q 
                        = (0x0000000fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o);
                }
            }
            if ((0U == (0x0000003fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o 
                                       >> 2U)))) {
                vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__digit_q 
                    = (0x000000ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o);
            }
        }
        if (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q) 
             == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q))) {
            if ((0x0003d08fU == vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q)) {
                vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_q 
                    = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q;
            }
        }
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_meta_q;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_meta_q = 0x0fU;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_o;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o;
    } else {
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19 = 0U;
        vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20 = 7U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31 = 0U;
        __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21 = 0U;
        vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12 = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_per = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_spi = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_hold = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__new_price_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_cycle_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__led_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__digit_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_sync_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_meta_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q = 0U;
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q = 0U;
    }
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__tx_shift_21;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt_22;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync_18;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__sum_q_17;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__count_q_16;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync_20;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r 
        = (::IData)((2U == (6U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_sync))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert 
        = (::IData)((4U == (6U & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata 
        = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_per)
            ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__rdata_o
            : ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__rd_is_spi)
                ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rdata_o
                : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__b_rdata_o));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift_23;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync_19;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_valid_o 
        = ((~ ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_sync) 
               >> 1U)) & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__sclk_r) 
                          & ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__cs_assert)) 
                             & (7U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__bit_cnt)))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__cycle_q_33;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__debounce_q_31;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q 
        = __Vdly__tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__btn_candidate_q_30;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__price_o 
        = ((0x000000feU & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__rx_shift) 
                           << 1U)) | (1U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_spi__DOT__mosi_sync) 
                                            >> 1U)));
}

void Vtb_proyecto_4___024root___nba_sequent__TOP__2(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___nba_sequent__TOP__2\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    ::IData/*31:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__imm_i = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2118;
    __Vdfg_Regularize_2118 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2119;
    __Vdfg_Regularize_2119 = 0;
    ::CData/*0:0*/ __Vdfg_Regularize_2121;
    __Vdfg_Regularize_2121 = 0;
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__por_cnt 
        = vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__por_cnt_0;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__RDATA 
        = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
        [vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q];
    if ((1U & (~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o)))) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
            = vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
            [(0x000001ffU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q 
                             >> 2U))];
    }
    if (vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_172) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_171] 
            = ((0xfffeU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_171]) 
               | (::SData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_170));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_174] 
            = ((0xfffdU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_174]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_173)) 
                  << 1U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_176] 
            = ((0xfffbU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_176]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_175)) 
                  << 2U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_178] 
            = ((0xfff7U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_178]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_177)) 
                  << 3U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_180] 
            = ((0xffefU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_180]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_179)) 
                  << 4U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_182] 
            = ((0xffdfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_182]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_181)) 
                  << 5U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_184] 
            = ((0xffbfU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_184]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_183)) 
                  << 6U));
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_186] 
            = ((0xff7fU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_186]) 
               | ((::SData)((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__u_history__DOT__mem_185)) 
                  << 7U));
    }
    if (vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_189) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_188] 
            = ((0xffffff00U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_188]) 
               | (::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_187));
    }
    if (vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_192) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_191] 
            = ((0xffff00ffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_191]) 
               | ((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_190) 
                  << 8U));
    }
    if (vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_195) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_194] 
            = ((0xff00ffffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_194]) 
               | ((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_193) 
                  << 0x00000010U));
    }
    if (vlSelfRef.__Vdly_Set__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_198) {
        vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem[vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_197] 
            = ((0x00ffffffU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem
                [vlSelfRef.__Vdly_Dim0__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_197]) 
               | ((::IData)(vlSelfRef.__Vdly_Val__tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__mem_196) 
                  << 0x00000018U));
    }
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_sign_o 
        = (1U & ((0x00004000U != (0x0000607cU & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)) 
                 | (~ (3U == (3U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o)))));
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_wdata_o 
        = ((0U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
            ? (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                << 0x00000018U) | ((0x00ff0000U & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                                                   << 0x00000010U)) 
                                   | ((0x0000ff00U 
                                       & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                                          << 8U)) | 
                                      (0x000000ffU 
                                       & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA)))))
            : ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
                ? (((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA) 
                    << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankB__DOT__u_lo__DOT__RDATA))
                : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_wdata_o));
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__is_jalr_o 
        = (((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
            & (0U == (0x00000018U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o))) 
           & (::IData)(vlSelfRef.__Vdfg_Regularize_2139));
}

extern const ::VlUnpacked<::CData/*0:0*/, 128> Vtb_proyecto_4__ConstPool__CONSARRAY_9;

void Vtb_proyecto_4___024root___nba_sequent__TOP__3(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___nba_sequent__TOP__3\n"); );
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
    ::SData/*15:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf = 0;
    ::CData/*7:0*/ tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte = 0;
    ::IData/*31:0*/ __Vdfg_Regularize_2122;
    __Vdfg_Regularize_2122 = 0;
    // Body
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q 
        = vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_sma10__DOT__pointer_q_15;
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q 
        = vlSelfRef.__Vdly__tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_q_12;
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
        = ((1U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o))
            ? vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__pc_id_q
            : ((((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_hi__DOT__RDATA) 
                 << 0x00000010U) | (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__u_bankA__DOT__u_lo__DOT__RDATA)) 
               & (- (::IData)((2U != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__alu_op_a_sel_o))))));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                  >> 6U)) & ((::IData)(vlSelfRef.__Vdfg_Regularize_2120) 
                             & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__ops_valid_q) 
                                & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q)))));
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_we_o 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((~ (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                  >> 6U)) & ((::IData)(vlSelfRef.__Vdfg_Regularize_2140) 
                             & (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o 
        = ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__busy_q)) 
           & (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__lsu_req_o));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__cmp_lt 
        = (1U & ((::IData)((tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                            >> 0x0000001fU)) ^ ((__Vdfg_Regularize_2122 
                                                 >> 0x0000001fU) 
                                                & ((tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__operand_a 
                                                    >> 0x0000001fU) 
                                                   ^ (::IData)(
                                                               (tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__sum_ext 
                                                                >> 0x0000001fU))))));
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
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__per_sel 
        = (::IData)((0x80000000U == (0x80010000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_be_o 
        = (0x0000000fU & ((0U == (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o))
                           ? ((::IData)(1U) << (3U 
                                                & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o))
                           : (((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                                ? 0x0cU : 3U) | (- (::IData)(
                                                             (1U 
                                                              != (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_decoder__DOT__lsu_type_o)))))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__spi_sel 
        = (::IData)((0x80010000U == (0x80010000U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf 
        = (0x0000ffffU & ((2U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                           ? (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata 
                              >> 0x00000010U) : vlSelfRef.tb_proyecto_4__DOT__dut__DOT__data_rdata));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_rf__DOT__wr 
        = ((::IData)(vlSelfRef.__Vdfg_Regularize_2114) 
           & ((::IData)(vlSelfRef.__Vdfg_Regularize_2123) 
              & ((~ (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_ctrl__DOT__stall_o)) 
                 & ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_if__DOT__valid_q) 
                    & (0U != (0x0000000fU & (vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_ram__DOT__a_rdata_o 
                                             >> 7U)))))));
    vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_periph__DOT__access 
        = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o) 
           & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__per_sel));
    tb_proyecto_4__DOT__dut__DOT__spi_req = ((::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__data_req_o) 
                                             & (::IData)(vlSelfRef.tb_proyecto_4__DOT__dut__DOT__spi_sel));
    tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lbyte 
        = (0x000000ffU & ((1U & vlSelfRef.tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_id__DOT__u_alu__DOT__result_o)
                           ? ((::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf) 
                              >> 8U) : (::IData)(tb_proyecto_4__DOT__dut__DOT__u_core__DOT__u_lsu__DOT__lhalf)));
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
}

void Vtb_proyecto_4___024root___trigger_orInto__act_vec_vec(::VlUnpacked<::QData/*63:0*/, 1> &out, const ::VlUnpacked<::QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((::IData)(1U) + n);
    } while ((0U >= n));
}

void Vtb_proyecto_4___024root___trigger_clear__act(::VlUnpacked<::QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___trigger_clear__act\n"); );
    // Locals
    ::IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((::IData)(1U) + n);
    } while ((1U > n));
}

#ifdef VL_DEBUG
void Vtb_proyecto_4___024root___eval_debug_assertions(Vtb_proyecto_4___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_proyecto_4___024root___eval_debug_assertions\n"); );
    Vtb_proyecto_4__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
