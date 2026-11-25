// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VTB_PROYECTO_4__SYMS_H_
#define VERILATED_VTB_PROYECTO_4__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vtb_proyecto_4.h"

// INCLUDE MODULE CLASSES
#include "Vtb_proyecto_4___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vtb_proyecto_4__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vtb_proyecto_4* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool& __Vm_didInit;

    // MODULE INSTANCE STATE
    union {
        struct {
            Vtb_proyecto_4___024root       TOP;
        } vlInst;
    };

    // CONSTRUCTORS
    Vtb_proyecto_4__Syms(VerilatedContext* contextp, const char* namep, Vtb_proyecto_4* modelp);
    ~Vtb_proyecto_4__Syms();

    // METHODS
    const char* name() const { return vlInst.TOP.vlNamep; }
};

#endif  // guard
