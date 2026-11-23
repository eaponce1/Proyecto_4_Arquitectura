"""Select the x16 instruction BRAM read enable and optional registered inputs."""
import argparse
import json
from pathlib import Path


def register_read_inputs(top: dict, clock: list, read_inputs: list[int]) -> list[int]:
    """Sample the instruction request one half-cycle ahead of the RAM read."""
    next_bit = 1 + max(bit for net in top["netnames"].values()
                       for bit in net["bits"] if isinstance(bit, int))
    outputs = []
    for index, source in enumerate(read_inputs):
        signal = f"fetch_read_input_q_{index}"
        cell = f"{signal}_SB_DFFN_Q"
        if any(name in top["cells"] or name in top["netnames"] for name in (signal, cell)):
            raise SystemExit(f"Duplicate mapped fetch register {signal}")
        bit = next_bit + index
        top["netnames"][signal] = {"hide_name": 0, "bits": [bit], "attributes": {}}
        top["cells"][cell] = {
            "type": "SB_DFFN",
            "hide_name": 0,
            "parameters": {},
            "attributes": {},
            "port_directions": {"C": "input", "D": "input", "Q": "output"},
            "connections": {"C": clock, "D": [source], "Q": [bit]},
        }
        outputs.append(bit)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--registered-inputs", action="store_true")
    args = parser.parse_args()

    netlist = json.loads(args.netlist.read_text(encoding="utf-8"))
    top = netlist["modules"]["demo_autonoma_bus_detail_top"]
    cells = top["cells"]
    instruction_rams = [cells[f"u_soc.u_ram.mem.0.{half}"] for half in range(2)]
    data_rams = [cells[f"u_soc.u_ram.mem.1.{half}"] for half in range(2)]
    enable = instruction_rams[0]["connections"]["RCLKE"]
    clock = top["ports"]["i_Clk"]["bits"]
    for cell in instruction_rams + data_rams:
        pins = cell["connections"]
        params = cell["parameters"]
        if (cell["type"] != "SB_RAM40_4K" or
                params["READ_MODE"] != "00" or params["WRITE_MODE"] != "00" or
                pins["RCLK"] != clock or pins["RE"] != ["1"] or
                pins["RCLKE"] != (enable if cell in instruction_rams else ["1"])):
            raise SystemExit("Unexpected x16 BRAM instruction/data-port mapping")
    if len(enable) != 1 or not isinstance(enable[0], int):
        raise SystemExit("Expected both instruction halves to share a fetch enable")
    if instruction_rams[0]["connections"]["RADDR"] != instruction_rams[1]["connections"]["RADDR"]:
        raise SystemExit("Instruction halves do not share the read address")

    if args.registered_inputs:
        address = instruction_rams[0]["connections"]["RADDR"]
        if address[7:] != ["0"] * 4 or not all(isinstance(bit, int) for bit in address[:7]):
            raise SystemExit("Phase fetch expects the demo's 7-bit instruction address")
        if "SB_DFFN" not in netlist["modules"]:
            raise SystemExit("Missing falling-edge flip-flop primitive")
        registered = register_read_inputs(top, clock, address[:7] + enable)
        phase_addr = registered[:7]
        phase_enable = registered[7:]
    else:
        phase_enable = enable

    for cell in instruction_rams:
        cell["connections"]["RCLKE"] = ["1"]
        cell["connections"]["RE"] = phase_enable
        if args.registered_inputs:
            cell["connections"]["RADDR"] = phase_addr + ["0"] * 4

    args.output.write_text(json.dumps(netlist), encoding="utf-8")
    description = ("rising-edge reads using the falling-edge address and enable"
                   if args.registered_inputs else "RCLKE=1, RE=fetch enable")
    print(f"Instruction BRAMs (2): {description}. Data port and INIT preserved.")


if __name__ == "__main__":
    main()
