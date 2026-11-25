// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_proyecto_4.h for the primary calling header

#include "Vtb_proyecto_4__pch.h"

void Vtb_proyecto_4___024root___ctor_var_reset(Vtb_proyecto_4___024root* vlSelf);

void Vtb_proyecto_4___024root__ctor(Vtb_proyecto_4___024root* vlSelf, Vtb_proyecto_4__Syms* symsp, const char* namep) {
    vlSelf->vlSymsp = symsp;
    vlSelf->vlNamep = strdup(namep);
    // Construct members
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__leer_serie__encabezado_5);
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_13);
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_15);
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_17);
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_19);
    VL_INPLACE_CONSTRUCT(vlSelf->__Vnontrivs.__VdlySched, *vlSelf->vlSymsp->_vm_contextp__);
    // Reset structure values
    Vtb_proyecto_4___024root___ctor_var_reset(vlSelf);
}

Vtb_proyecto_4___024root::Vtb_proyecto_4___024root(Vtb_proyecto_4__Syms* symsp, const char* namep) {
    Vtb_proyecto_4___024root__ctor(this, symsp, namep);
}

void Vtb_proyecto_4___024root__dtor(Vtb_proyecto_4___024root* vlSelf) {
    // Destroy members
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__VdlySched);
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_19);
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_17);
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_15);
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__chequear__nombre_13);
    VL_INPLACE_DESTRUCT(vlSelf->__Vnontrivs.__Vtask_tb_proyecto_4__DOT__leer_serie__encabezado_5);
    VL_DO_DANGLING(std::free(const_cast<char*>(vlSelf->vlNamep)), vlSelf->vlNamep);
}

Vtb_proyecto_4___024root::~Vtb_proyecto_4___024root() {
    Vtb_proyecto_4___024root__dtor(this);
}
