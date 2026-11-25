// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vtb_proyecto_4__pch.h"

//============================================================
// Constructors

Vtb_proyecto_4::Vtb_proyecto_4(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vtb_proyecto_4__Syms(contextp(), _vcname__, this)}
    , m_evalLoop{*this, /*convergeLimit:*/ 10000}
    , rootp{&(vlSymsp->vlInst.TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vtb_proyecto_4::Vtb_proyecto_4(const char* _vcname__)
    : Vtb_proyecto_4(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vtb_proyecto_4::~Vtb_proyecto_4() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vtb_proyecto_4___024root___eval_debug_assertions(Vtb_proyecto_4___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_static(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___eval_initial(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD bool Vtb_proyecto_4___024root___eval_stl(Vtb_proyecto_4___024root* vlSelf, ::CData/*0:0*/ firstIteration);
void Vtb_proyecto_4___024root___eval_sample(Vtb_proyecto_4___024root* vlSelf);
bool Vtb_proyecto_4___024root___eval_ico(Vtb_proyecto_4___024root* vlSelf, ::CData/*0:0*/ firstIteration);
bool Vtb_proyecto_4___024root___eval_act(Vtb_proyecto_4___024root* vlSelf);
bool Vtb_proyecto_4___024root___eval_inact(Vtb_proyecto_4___024root* vlSelf);
bool Vtb_proyecto_4___024root___eval_nba(Vtb_proyecto_4___024root* vlSelf);
bool Vtb_proyecto_4___024root___eval_obs(Vtb_proyecto_4___024root* vlSelf);
bool Vtb_proyecto_4___024root___eval_react(Vtb_proyecto_4___024root* vlSelf);
void Vtb_proyecto_4___024root___eval_postponed(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_final(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__stl(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__ico(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__act(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__nba(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__obs(Vtb_proyecto_4___024root* vlSelf);
VL_ATTR_COLD void Vtb_proyecto_4___024root___eval_dump_triggers__react(Vtb_proyecto_4___024root* vlSelf);

void Vtb_proyecto_4::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vtb_proyecto_4::eval_step\n"); );
    m_evalLoop.eval();
}

void Vtb_proyecto_4::evalBegin() {
#ifdef VL_DEBUG
    // Debug assertions
    Vtb_proyecto_4___024root___eval_debug_assertions(&(vlSymsp->vlInst.TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
}

void Vtb_proyecto_4::evalEnd() {
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
    vlSymsp->vlInst.TOP.__Vnontrivs.__VdlySched.cleanupForevered();
}

void Vtb_proyecto_4::evalStatic() {
    Vtb_proyecto_4___024root___eval_static(&(vlSymsp->vlInst.TOP));
}

void Vtb_proyecto_4::evalInitial() {
    Vtb_proyecto_4___024root___eval_initial(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalStl(bool firstIteration) {
    return Vtb_proyecto_4___024root___eval_stl(&(vlSymsp->vlInst.TOP), firstIteration);
}

void Vtb_proyecto_4::evalSample() {
    Vtb_proyecto_4___024root___eval_sample(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalIco(bool firstIteration) {
    return Vtb_proyecto_4___024root___eval_ico(&(vlSymsp->vlInst.TOP), firstIteration);
}

bool Vtb_proyecto_4::evalAct() {
    return Vtb_proyecto_4___024root___eval_act(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalInact() {
    return Vtb_proyecto_4___024root___eval_inact(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalNba() {
    return Vtb_proyecto_4___024root___eval_nba(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalObs() {
    return Vtb_proyecto_4___024root___eval_obs(&(vlSymsp->vlInst.TOP));
}

bool Vtb_proyecto_4::evalReact() {
    return Vtb_proyecto_4___024root___eval_react(&(vlSymsp->vlInst.TOP));
}

void Vtb_proyecto_4::evalPostponed() {
    Vtb_proyecto_4___024root___eval_postponed(&(vlSymsp->vlInst.TOP));
}

void Vtb_proyecto_4::evalFinal() {
    Vtb_proyecto_4___024root___eval_final(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersStl() {
    Vtb_proyecto_4___024root___eval_dump_triggers__stl(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersIco() {
    Vtb_proyecto_4___024root___eval_dump_triggers__ico(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersAct() {
    Vtb_proyecto_4___024root___eval_dump_triggers__act(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersNba() {
    Vtb_proyecto_4___024root___eval_dump_triggers__nba(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersObs() {
    Vtb_proyecto_4___024root___eval_dump_triggers__obs(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vtb_proyecto_4::dumpTriggersReact() {
    Vtb_proyecto_4___024root___eval_dump_triggers__react(&(vlSymsp->vlInst.TOP));
}

//============================================================
// Events and timing
bool Vtb_proyecto_4::eventsPending() { return !vlSymsp->vlInst.TOP.__Vnontrivs.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vtb_proyecto_4::nextTimeSlot() { return vlSymsp->vlInst.TOP.__Vnontrivs.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vtb_proyecto_4::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

VL_ATTR_COLD void Vtb_proyecto_4::final() {
    contextp()->executingFinal(true);
    evalFinal();
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vtb_proyecto_4::hierName() const { return vlSymsp->name(); }
const char* Vtb_proyecto_4::modelName() const { return "Vtb_proyecto_4"; }
unsigned Vtb_proyecto_4::threads() const { return 1; }
void Vtb_proyecto_4::prepareClone() const { contextp()->prepareClone(); }
void Vtb_proyecto_4::atClone() const {
    contextp()->threadPoolpOnClone();
}
