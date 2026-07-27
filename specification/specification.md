# OpenPCBDB Specification
## AI-Native EDA Database Standard

**Status:** Draft  
**Version:** 0.2.0  
**Date:** 2026-07-27  
**Authors:** Alla Vardumyan  
**Company:** Mintaka LLC, Armenia, www.mintaka-ai.com  
**License:** CC BY 4.0 (documentation) / Apache 2.0 (code)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Core Paradigm](#2-core-paradigm)
3. [Workspace Structure](#3-workspace-structure)
4. [Database Files](#4-database-files)
5. [Data Models](#5-data-models)
6. [Validation](#6-validation)
7. [AI Agent Workflow](#7-ai-agent-workflow)
8. [Python API Direction](#8-python-api-direction)
9. [Compatibility and Export](#9-compatibility-and-export)
10. [Examples](#10-examples)
11. [Glossary](#11-glossary)

---

## 1. Introduction

OpenPCBDB is an AI-native EDA database standard for electronic circuit and PCB design.

The goal is not to describe a PCB as one flat JSON file. The goal is to define a design database that an AI hardware agent can create, inspect, validate, explain, and export to existing EDA/manufacturing tools.

OpenPCBDB follows the mature EDA database paradigm used by tools such as Cadence Virtuoso, Synopsys Custom Designer, and OpenAccess:

```text
library / cell / view
```

This makes OpenPCBDB suitable for hierarchical hardware development:

```text
requirements -> libraries -> cells -> views -> validation -> export
```

The primary consumers are:

- AI hardware agents
- Python tooling
- validators
- EDA import/export backends
- human reviewers

---

## 2. Core Paradigm

### 2.1 Library / Cell / View

OpenPCBDB uses the following hierarchy:

```text
Library
  Cell
    View
```

**Library** is a namespace. A workspace may contain multiple libraries.

**Cell** is a reusable design unit. Examples:

```text
amplifier
buck_3v3
usb_input
STM32_MCU_1123
power_system
```

**View** is a representation of a cell. Common views:

```text
symbol
schematic
layout
spice
verilog
manufacturing
```

### 2.2 Identity

Cell names are scoped by library.

```text
Cell identity = library + cell + version
View identity = library + cell + view + version
```

Therefore:

```text
lib_1/buck_3v3
lib_2/buck_3v3
```

are different cells.

### 2.3 Cell Types

A cell may be one of:

```text
leaf
composite
blackbox
external
```

**leaf**: implemented directly with `ComponentInstance` objects in `schematic/view.db`.

**composite**: implemented by instantiating other cells through `CellInstance` objects.

**blackbox**: has a symbol contract but no visible implementation.

**external**: implemented by an external EDA/tool artifact such as SPICE, Verilog, KiCad, GDS, or vendor IP.

### 2.4 Symbol Contract Rule

Parent schematics shall connect to child cells only through the child cell's symbol view ports.

```text
parent schematic -> child symbol/view.db ports
```

Parent schematics shall not connect directly to private nets inside a child `schematic/view.db`.

This rule makes hierarchy clean and allows independent bottom-up validation.

### 2.5 Module vs Cell

`Cell` and `Module` are not the same concept.

```text
Cell   = EDA database design unit
Module = physical separate PCB assembly or packaged subsystem
```

Examples of modules:

```text
System-on-Module
DIMM
M.2 card
daughterboard
certified wireless module
DC/DC converter module
```

A physical module may be represented as a cell, but `Module` remains a physical integration concept.

---

## 3. Workspace Structure

An OpenPCBDB workspace is a directory containing requirements and one or more libraries.

Canonical structure:

```text
project_name/
  design.openPCBDB
  requirements.db
  lib_1/
    library.db
    technology.db
    power_system/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
    buck_3v3/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
      spice/
        circuit.sc
  lib_2/
    library.db
    technology.db
    buck_3v3/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
```

### 3.1 File Extensions

OpenPCBDB files may use `.db` while storing JSON syntax internally.

Recommended canonical filenames:

```text
design.openPCBDB
requirements.db
library.db
technology.db
cell.db
view.db
```

Backend/export files may keep native extensions:

```text
spice/circuit.sc
verilog/module.v
kicad/project.kicad_pcb
manufacturing/gerbers/*
```

### 3.2 Design Manifest

`design.openPCBDB` is the workspace design manifest and database index. It identifies the top cell, requirements file, active libraries, technologies, cells, views, and their paths.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Project",
  "id": "usb_temperature_logger",
  "name": "USB Temperature Logger",
  "version": "0.1.0",
  "top": {
    "library": "lib_1",
    "cell": "top",
    "view": "schematic",
    "path": "lib_1/top/schematic/view.db"
  },
  "requirementsRef": {
    "file": "requirements.db",
    "id": "REQ_USB_TEMP_LOGGER",
    "version": "0.1.0",
    "hash": "sha256:optional"
  },
  "libraries": [
    {
      "name": "lib_1",
      "path": "lib_1/library.db"
    },
    {
      "name": "lib_2",
      "path": "lib_2/library.db"
    }
  ]
}
```

---

## 4. Database Files

### 4.1 `requirements.db`

`requirements.db` describes what must be built. It is separate from implementation.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Requirements",
  "id": "REQ_POWER_SYSTEM_0001",
  "version": "0.1.0",
  "name": "Power System Requirements",
  "requirements": [
    {
      "id": "power.input_usb_5v",
      "type": "electrical",
      "description": "Accept 5V input from USB VBUS.",
      "limits": {
        "voltage": {
          "nominal": 5.0,
          "unit": "V"
        }
      }
    },
    {
      "id": "power.rail_3v3",
      "type": "electrical",
      "description": "Generate regulated 3.3V rail.",
      "limits": {
        "voltage": {
          "nominal": 3.3,
          "tolerance": 0.05,
          "unit": "V"
        },
        "current": {
          "minimum": 0.5,
          "unit": "A"
        }
      }
    }
  ]
}
```

### 4.2 `library.db`

`library.db` identifies a library namespace and points to the technology database.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Library",
  "name": "lib_1",
  "version": "0.1.0",
  "technologyRef": {
    "file": "technology.db",
    "id": "TECH_JLCPCB_6L_STD_1OZ",
    "version": "0.1.0"
  },
  "cells": [
    {
      "cell": "power_system",
      "path": "power_system/cell.db",
      "version": "0.1.0"
    },
    {
      "cell": "buck_3v3",
      "path": "buck_3v3/cell.db",
      "version": "0.1.0"
    }
  ]
}
```

### 4.3 `technology.db`

`technology.db` stores fab/process rules for a library.

It should include:

- fab/manufacturer metadata
- source references
- units
- layer stackup
- dielectric information
- copper weights
- trace/spacing limits
- drill and via rules
- solder mask rules
- finish options
- impedance capabilities
- DRC rule defaults

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Technology",
  "library": "lib_1",
  "id": "TECH_JLCPCB_6L_STD_1OZ",
  "name": "JLCPCB Standard 6-Layer 1 oz PCB Process",
  "version": "0.1.0",
  "fab": {
    "name": "JLCPCB",
    "processClass": "standard_6_layer",
    "capabilityRevision": "2026-07",
    "sourceRefs": [
      {
        "type": "manufacturer_capability_page",
        "name": "JLCPCB 6-Layer PCB Capabilities",
        "url": "https://jlcpcb.com/6-layer-pcb",
        "retrievedAt": "2026-07-27"
      }
    ]
  },
  "units": {
    "length": "mm",
    "copperWeight": "oz",
    "temperature": "C"
  },
  "stackup": {
    "layerCount": 6,
    "boardThickness": {
      "value": 1.6,
      "unit": "mm"
    },
    "typicalLayerOrder": [
      "signal",
      "ground",
      "power",
      "signal",
      "ground",
      "signal"
    ],
    "layers": [
      {
        "id": "L1",
        "name": "Top Signal",
        "type": "signal",
        "material": "copper",
        "copperWeight": {
          "value": 1,
          "unit": "oz"
        }
      },
      {
        "id": "L2",
        "name": "Ground Plane",
        "type": "plane",
        "planeType": "ground",
        "material": "copper",
        "copperWeight": {
          "value": 0.5,
          "unit": "oz"
        }
      }
    ]
  },
  "designRules": {
    "traceWidth": {
      "absoluteMinimum": {
        "value": 0.09,
        "unit": "mm"
      },
      "preferredDefault": {
        "value": 0.12,
        "unit": "mm"
      }
    },
    "traceSpacing": {
      "absoluteMinimum": {
        "value": 0.09,
        "unit": "mm"
      },
      "preferredDefault": {
        "value": 0.12,
        "unit": "mm"
      }
    },
    "drill": {
      "minimum": {
        "value": 0.15,
        "unit": "mm"
      }
    }
  }
}
```

### 4.4 `cell.db`

`cell.db` stores cell identity, metadata, requirements references, technology references, and view references.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Cell",
  "library": "lib_1",
  "cell": "buck_3v3",
  "id": "CELL_BUCK_3V3",
  "name": "5V to 3.3V Buck Regulator",
  "cellType": "leaf",
  "version": "0.1.0",
  "technologyRef": {
    "file": "../technology.db",
    "id": "TECH_JLCPCB_6L_STD_1OZ",
    "version": "0.1.0"
  },
  "requirementsRef": {
    "file": "../../requirements.db",
    "ids": [
      "power.rail_3v3"
    ],
    "version": "0.1.0"
  },
  "views": {
    "symbol": {
      "path": "symbol/view.db",
      "type": "CellSymbol",
      "version": "0.1.0"
    },
    "schematic": {
      "path": "schematic/view.db",
      "type": "Schematic",
      "version": "0.1.0"
    },
    "layout": {
      "path": "layout/view.db",
      "type": "PCBLayout",
      "version": "0.1.0",
      "optional": true
    }
  },
  "semantic": {
    "purpose": "Convert 5V input into a regulated 3.3V rail.",
    "function": "Switching buck regulator leaf cell",
    "reasoning": "The regulator is isolated as a reusable cell with explicit input, output, enable, and ground ports."
  }
}
```

### 4.5 `symbol/view.db`

The symbol view is the public logical interface of a cell.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "CellSymbol",
  "library": "lib_1",
  "cell": "buck_3v3",
  "view": "symbol",
  "version": "0.1.0",
  "ports": [
    {
      "id": "vin",
      "name": "VIN",
      "direction": "input",
      "electricalType": "power",
      "voltage": {
        "nominal": 5.0,
        "unit": "V"
      },
      "required": true
    },
    {
      "id": "vout",
      "name": "3V3",
      "direction": "output",
      "electricalType": "power",
      "voltage": {
        "nominal": 3.3,
        "unit": "V"
      },
      "required": true
    },
    {
      "id": "gnd",
      "name": "GND",
      "direction": "passive",
      "electricalType": "ground",
      "required": true
    }
  ],
  "interfaces": [
    {
      "id": "power_in",
      "type": "power",
      "ports": [
        "vin",
        "gnd"
      ]
    },
    {
      "id": "power_out",
      "type": "power",
      "ports": [
        "vout",
        "gnd"
      ]
    }
  ]
}
```

### 4.6 `schematic/view.db`

The schematic view stores logical implementation.

Leaf cells contain components and nets.

Composite cells contain `CellInstance` objects and nets between instance ports.

Schematic constraints are stored inside `schematic/view.db` because they apply to the electrical/logical implementation of that view.

Example composite schematic:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "Schematic",
  "library": "lib_1",
  "cell": "power_system",
  "view": "schematic",
  "version": "0.1.0",
  "externalPorts": [
    {
      "symbolPort": "usb_5v",
      "net": "USB_5V"
    },
    {
      "symbolPort": "rail_3v3",
      "net": "3V3"
    }
  ],
  "instances": [
    {
      "id": "X_BUCK_3V3",
      "type": "CellInstance",
      "library": "lib_1",
      "cell": "buck_3v3",
      "cellRef": "../../buck_3v3/cell.db",
      "viewBinding": {
        "connectivity": "../../buck_3v3/symbol/view.db",
        "implementation": "../../buck_3v3/schematic/view.db",
        "physical": "../../buck_3v3/layout/view.db"
      },
      "semantic": {
        "purpose": "Generate the 3.3V rail.",
        "function": "Instantiates a reusable buck regulator cell.",
        "reasoning": "The parent schematic connects through public symbol ports while the child schematic remains private."
      }
    }
  ],
  "constraints": [
    {
      "id": "rail_3v3_voltage",
      "type": "voltage",
      "net": "3V3",
      "nominal": {
        "value": 3.3,
        "unit": "V"
      },
      "tolerance": {
        "value": 5,
        "unit": "%"
      },
      "requirementRefs": [
        "power.rail_3v3"
      ]
    }
  ],
  "nets": [
    {
      "id": "NET_3V3",
      "name": "3V3",
      "connections": [
        {
          "instance": "X_BUCK_3V3",
          "port": "vout"
        },
        {
          "instance": "self",
          "port": "rail_3v3"
        }
      ]
    }
  ]
}
```

Example leaf component:

```json
{
  "type": "ComponentInstance",
  "refDesignator": "U1",
  "componentDefinitionId": "BUCK_REGULATOR_ADJ",
  "partNumber": {
    "manufacturer": "Generic",
    "mpn": "BUCK-ADJ-1A"
  },
  "userLibraryReferences": {
    "symbol": "regulator:Buck_Adjustable",
    "footprint": "package:SOT-23-6"
  },
  "semantic": {
    "purpose": "Convert VIN to regulated 3.3V.",
    "function": "Step-down switching regulator",
    "reasoning": "A buck regulator is efficient for converting USB 5V to a 3.3V rail.",
    "requirementRefs": [
      "power.rail_3v3"
    ]
  }
}
```

### 4.7 `layout/view.db`

The layout view stores physical implementation or floorplan.

It uses the OpenPCBDB `PCBLayout` model and must reference a technology database.

Layout constraints are stored inside `layout/view.db` because they apply to the physical implementation of that view.

Example:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "PCBLayout",
  "library": "lib_1",
  "cell": "buck_3v3",
  "view": "layout",
  "version": "0.1.0",
  "technologyRef": {
    "file": "../../technology.db",
    "id": "TECH_JLCPCB_6L_STD_1OZ",
    "version": "0.1.0"
  },
  "layoutType": "leaf",
  "constraints": [
    {
      "id": "power_trace_width_3v3",
      "type": "trace_width",
      "nets": [
        "3V3"
      ],
      "minimum": {
        "value": 0.5,
        "unit": "mm"
      },
      "requirementRefs": [
        "power.rail_3v3"
      ]
    },
    {
      "id": "switching_node_area",
      "type": "copper_area_max",
      "net": "SW",
      "maximum": {
        "value": 50,
        "unit": "mm2"
      }
    }
  ],
  "placements": [
    {
      "refDesignator": "U1",
      "position": {
        "x": 0,
        "y": 0,
        "unit": "mm"
      },
      "rotation": {
        "value": 0,
        "unit": "deg"
      }
    }
  ],
  "routing": [],
  "zones": [],
  "drc": {
    "status": "unknown",
    "reports": []
  }
}
```

---

## 5. Data Models

### 5.1 Common Fields

Every OpenPCBDB JSON database object should include:

```json
{
  "openpcbdbVersion": "0.2.0",
  "type": "ObjectType",
  "version": "0.1.0"
}
```

Most design objects should include semantic information:

```json
{
  "semantic": {
    "purpose": "Human and AI readable purpose",
    "function": "Specific electrical, logical, or physical function",
    "reasoning": "Why this design decision was made",
    "assumptions": [],
    "confidence": 1.0
  }
}
```

### 5.2 References

References are relative to the file that contains them unless explicitly marked otherwise.

Common reference shapes:

```json
{
  "file": "../technology.db",
  "id": "TECH_JLCPCB_6L_STD_1OZ",
  "version": "0.1.0"
}
```

```json
{
  "path": "schematic/view.db",
  "type": "Schematic",
  "version": "0.1.0"
}
```

Hashes are optional but recommended for release/frozen designs:

```json
{
  "file": "requirements.db",
  "id": "REQ_POWER_SYSTEM_0001",
  "version": "0.1.0",
  "hash": "sha256:optional"
}
```

### 5.3 Ports

Ports are public connection points in `symbol/view.db`.

Port directions:

```text
input
output
bidirectional
passive
power_in
power_out
ground
no_connect
```

Electrical types:

```text
power
ground
analog
digital
clock
reset
enable
differential
rf
passive
```

### 5.4 Nets

Nets connect component pins, cell instance ports, or external symbol ports.

Example:

```json
{
  "id": "NET_USB_5V",
  "name": "USB_5V",
  "connections": [
    {
      "instance": "self",
      "port": "usb_5v"
    },
    {
      "instance": "X_BUCK_3V3",
      "port": "vin"
    }
  ],
  "semantic": {
    "purpose": "Distribute USB input power.",
    "function": "5V power net",
    "reasoning": "Connects the public parent power input to the child regulator input."
  }
}
```

### 5.5 Component Definitions

Component definitions describe reusable electronic parts.

Component definitions may live:

- inside OpenPCBDB libraries
- in external SQL/SQLite libraries
- in vendor/library services
- in EDA tool libraries

OpenPCBDB component instances reference component definitions by stable id.

### 5.6 Component Instances

Component instances are used inside leaf schematic views.

Required fields:

- `type`
- `refDesignator`
- `componentDefinitionId`

Recommended fields:

- `partNumber`
- `userLibraryReferences`
- `semantic`

### 5.7 Cell Instances

Cell instances are used inside composite schematic views.

Required fields:

- `type`
- `id`
- `library`
- `cell`
- `cellRef`
- `viewBinding.connectivity`

Recommended bindings:

```text
connectivity -> symbol/view.db
implementation -> schematic/view.db
physical -> layout/view.db
simulation -> spice/circuit.sc
rtl -> verilog/module.v
```

### 5.8 View-Local Constraints

OpenPCBDB does not define a required top-level `constraints.db` file.

Constraints should be stored where they apply:

```text
schematic/view.db  electrical and logical constraints
layout/view.db     physical, routing, placement, and manufacturing constraints
technology.db      fab/process capabilities and absolute manufacturing limits
requirements.db    product intent and externally imposed goals
```

This keeps constraints local to the representation they validate.

Examples of schematic constraints:

```text
voltage
current
power_domain
pin_compatibility
decoupling_required
clock_frequency
interface_protocol
```

Examples of layout constraints:

```text
trace_width
clearance
differential_impedance
matched_length
placement_region
keepout
thermal_relief
copper_area_max
```

`technology.db` should not store project-specific design intent. It stores what the fabrication process can manufacture. View-local constraints may be stricter than technology limits.

---

## 6. Validation

OpenPCBDB validation is bottom-up by default.

### 6.1 Reference Validation

Validators shall check:

- referenced files exist
- referenced ids match
- referenced versions match
- hashes match when provided
- paths are resolved relative to the containing file

### 6.2 Symbol/Schematic Validation

For each cell:

- every `externalPort.symbolPort` in `schematic/view.db` exists in `symbol/view.db`
- every required symbol port is implemented or intentionally marked unconnected
- parent schematic connections only reference child symbol ports
- parent schematic does not reference child internal component pins or private nets

### 6.3 Leaf Cell ERC

For leaf cells:

- component pins exist
- nets connect compatible electrical types
- power pins are supplied
- ground references exist
- schematic constraints are internally consistent
- required decoupling rules are satisfied when rules are present
- semantic requirement references are valid

### 6.4 Composite Cell ERC

For composite cells:

- each `CellInstance` resolves to a valid child cell
- each child symbol view resolves
- each connected port exists
- port directions and electrical types are compatible
- required child ports are connected unless explicitly optional

### 6.5 Layout DRC

For each layout view:

- `technologyRef` resolves
- layers used by layout exist in technology
- traces satisfy technology width/spacing rules
- vias satisfy drill/diameter/annular ring rules
- mask, paste, copper, and keepouts satisfy technology rules
- layout constraints are satisfied
- layout connectivity matches schematic connectivity

### 6.6 Requirements Traceability

Validators should produce a requirements coverage report:

```text
requirement id -> cells -> components/nets/view-local constraints -> validation result
```

Every important AI-generated engineering decision should reference one or more requirement ids.

---

## 7. AI Agent Workflow

OpenPCBDB is designed for hardware agents such as Copernic.

### 7.1 Planning

AI agents should plan top-down:

```text
1. Read design.openPCBDB.
2. Read requirements.db.
3. Identify or create the top cell.
4. Decompose top cell into child cells.
5. Create symbol views for cell contracts.
6. Create schematic views for implementation.
7. Create layout constraints and layout views.
```

### 7.2 Validation

AI agents should validate bottom-up:

```text
1. Validate leaf cells.
2. Validate each leaf schematic against its symbol.
3. Validate each leaf layout against its schematic and technology.
4. Validate composite cell instances against child symbols.
5. Validate top cell requirements coverage.
6. Request human approval before manufacturing export.
```

### 7.3 Unknowns and Approvals

AI agents shall not silently guess high-impact engineering information.

Use explicit fields:

```json
{
  "unknowns": [
    "Maximum ambient temperature is not specified."
  ],
  "assumptions": [
    "Assume 25 C ambient for initial regulator sizing."
  ],
  "requiresApproval": [
    "Confirm 0.5 A minimum 3.3V rail current."
  ]
}
```

---

## 8. Python API Direction

The reference Python API should treat OpenPCBDB as a database workspace, not as one flat design file.

Example:

```python
from openpcbdb import Workspace

workspace = Workspace.open("project_name/design.openPCBDB")
requirements = workspace.requirements()

top = workspace.top_cell()
symbol = top.view("symbol")
schematic = top.view("schematic")

report = workspace.validate()
report.raise_if_blocking()
```

Creating a cell:

```python
lib = workspace.library("lib_1")

cell = lib.create_cell(
    cell="buck_3v3",
    name="5V to 3.3V Buck Regulator",
    cell_type="leaf"
)

cell.create_symbol_view()
cell.create_schematic_view()
cell.create_layout_view(technology=lib.technology())
```

Instantiating a child cell:

```python
parent = workspace.cell("lib_1", "power_system")
child = workspace.cell("lib_1", "buck_3v3")

parent.schematic.instantiate(
    id="X_BUCK_3V3",
    cell=child,
    connectivity_view="symbol",
    implementation_view="schematic",
    physical_view="layout"
)
```

---

## 9. Compatibility and Export

OpenPCBDB is the semantic source of truth. Existing EDA formats are import/export targets.

Possible exports:

```text
KiCad schematic/layout
Altium project
SPICE netlist
Verilog/RTL
Gerber/Excellon
BOM/CPL
STEP/3D assembly
```

Import/export may be lossy because many EDA formats do not preserve full semantic reasoning.

---

## 10. Examples

The current reference example is:

```text
examples/hierarchical_cell_library/
```

It demonstrates:

- `requirements.db`
- multiple libraries
- duplicate cell names across libraries
- `technology.db`
- `cell.db`
- `symbol/view.db`
- `schematic/view.db`
- `layout/view.db`
- leaf and composite cells
- bottom-up reference validation

---

## 11. Glossary

**AI-native**: Designed so an AI agent can reason about purpose, constraints, and validation, not only parse geometry.

**Cell**: Reusable database design unit inside a library.

**CellInstance**: Instance of a child cell inside a composite parent schematic.

**Composite Cell**: Cell implemented by instantiating other cells.

**Leaf Cell**: Cell implemented directly with component instances.

**Library**: Namespace containing cells and technology.

**Module**: Physical separate PCB assembly or packaged subsystem.

**Port**: Public connection point in a symbol view.

**Requirements**: External product or project constraints and goals.

**Technology**: Fabrication/process database for layout validation.

**View**: One representation of a cell, such as symbol, schematic, layout, SPICE, or Verilog.

---

**END OF SPECIFICATION**
