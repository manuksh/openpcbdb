# OpenPCBDB Specification v1.0
## Open PCB Design Database Standard
---

**Status:** Draft  
**Version:** 1.1.0  
**Date:** 2025-11-11  
**Authors:** Mintaka LLC, Armenia  
**License:** CC BY 4.0 (documentation) / Apache 2.0 (code)

---
## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Problem Statement](#12-problem-statement)
   - 1.3 [Key Principles](#13-key-principles)
   - 1.4 [AI Capabilities Enabled by OpenPCBDB](#14-ai-capabilities-enabled-by-openpcbdb)
2. [Scope and Objectives](#2-scope-and-objectives)
3. [Core Architecture](#3-core-architecture)
4. [Data Models](#4-data-models)
   - 4.1 [Component Library Model](#41-component-library-model)
   - 4.2 [Design Entity Models](#42-design-entity-models)
      - 4.2.1 [ComponentDefinition](#421-componentdefinition)
      - 4.2.2 [Net](#422-net)
      - 4.2.3 [ComponentInstance](#423-componentinstance)
      - 4.2.4 [FunctionalBlock](#424-functionalblock)
      - 4.2.5 [Module](#425-module) **NEW**
   - 4.3 [Constraint Model](#43-constraint-model)
5. [API Specification](#5-api-specification)
6. [File Format](#6-file-format)
   - 6.1 JSON Format
   - 6.2 Directory Structure for Large Projects
   - 6.3 [Compression and Storage Optimization](#63-compression-and-storage-optimization)
7. [AI/ML Integration](#7-aiml-integration)
8. [Reference Implementation](#8-reference-implementation)
9. [Appendices](#9-appendices)
10. [Complex Design Support: Motherboard Example](#10-complex-design-support-motherboard-example)
    - 10.1 [Motherboard Design Requirements](#101-motherboard-design-requirements)
    - 10.2 [Gap Analysis](#102-gap-analysis-for-motherboard-design)
    - 10.3 [Extended Data Models](#103-extended-data-models-for-motherboard-design)
    - 10.4 [Best Practices for AI](#104-motherboard-design-best-practices-for-ai)
    - 10.5 [Recommendations for v1.0](#105-recommendations-for-v10)
11. [Future Extensions](#11-future-extensions-v20)

---

## 1. Introduction

### 1.1 Purpose

OpenPCBDB is an **AI-native database standard** for electronic circuit and PCB design. This database is specifically designed for **artificial intelligence agents** to be the primary consumers, creators, and collaborators in the electronic design process.

**Primary Purpose**: Enable AI systems to:
- **Understand** electronic designs with full semantic context
- **Reason** about circuit behavior, power domains, signal integrity, and design intent
- **Create** new designs from high-level requirements
- **Modify** existing designs intelligently
- **Analyze** designs for optimization opportunities
- **Validate** designs against electrical and manufacturing constraints
- **Learn** from historical design data to improve future designs

**Why AI-First?**

Traditional PCB databases represent *what* exists (geometric shapes, connections) but not *why* it exists (design intent, functional purpose, engineering decisions). OpenPCBDB is built on the principle that every piece of data must answer:

1. **What is it?** (Component, net, constraint)
2. **Why is it there?** (Purpose, function, design intent)
3. **How does it work?** (Electrical behavior, relationships)
4. **What are the constraints?** (Rules, limits, requirements)

This semantic richness allows AI agents to participate in design as **intelligent collaborators**, not just automation tools.

### 1.2 Problem Statement

**The Challenge**: Current electronic design databases were created for human designers using specific software tools, not for AI agents. This creates fundamental barriers:

**1. Lack of Semantic Understanding**
- Existing formats store *geometry* (lines, shapes, positions) without *meaning*
- AI cannot distinguish between a power net and a signal net without external context
- Component relationships are implicit, not explicit
- Design decisions and reasoning are lost - only the final result is stored

**2. No Design Intent Capture**
- Why was this resistor value chosen? (AI doesn't know)
- Why are these traces matched in length? (AI must guess)
- What is critical vs. optional? (No way to tell)
- What functional blocks exist? (Not represented)

**3. Inadequate for AI Reasoning**
- Cannot query: "Find all voltage regulators supplying 3.3V"
- Cannot analyze: "What components are in the power domain?"
- Cannot validate: "Is this connection electrically safe?"
- Cannot learn: No standardized format for ML training data

**4. Limited Machine Readability**
- Binary formats require reverse engineering
- Proprietary schemas change without notice
- No formal ontology for electronic design concepts
- Inconsistent representation across different sources

**The Solution**: OpenPCBDB provides a **semantic, queryable, AI-native** representation where every element carries its purpose, function, constraints, and relationships explicitly.

### 1.3 Key Principles

**Core Design Philosophy**: *If an AI cannot understand it, it shouldn't be in this format.*

1. **AI-Native Architecture**
   - Every data structure is designed for machine reasoning first
   - Explicit relationships, not implicit geometry
   - Queryable graph structure for traversal and analysis
   - Formal ontology for all electronic design concepts

2. **Semantic Completeness**
   - Every element has a `semantic` field explaining its purpose
   - Design intent is captured, not just the result
   - Engineering decisions are recorded with reasoning
   - Functional context is always present

3. **Machine Learning Ready**
   - Standardized feature extraction for training AI models
   - Graph representation for neural network processing
   - Labeled data for supervised learning
   - Historical design patterns preserved for learning

4. **Intelligent Queryability**
   - Natural language queries supported
   - Complex graph traversal operations
   - Semantic search (find by function, not just name)
   - Constraint satisfaction queries

5. **Self-Describing Data**
   - All attributes have units and ranges
   - Dependencies are explicit
   - Validation rules are embedded
   - Metadata explains everything

6. **Evolutionary Design**
   - Supports design iteration history
   - Change tracking with reasoning
   - Multiple design alternatives
   - Optimization trajectory capture

7. **Human-Supervisable**
   - Human-readable JSON for inspection and override
   - Explainable AI decisions embedded in data
   - Audit trail for all AI modifications
   - Version control friendly

### 1.4 AI Capabilities Enabled by OpenPCBDB

OpenPCBDB enables AI agents to perform these intelligent design tasks:

**Design Understanding & Analysis**
- Parse and comprehend existing circuit designs
- Extract design patterns and best practices
- Identify functional blocks and their purposes
- Analyze power distribution networks
- Detect signal integrity issues
- Evaluate thermal characteristics

**Intelligent Design Generation**
- Generate circuits from natural language specifications
  - Example: "Create a 5V, 2A power supply with overcurrent protection"
- Auto-complete partial designs
- Suggest component selections based on requirements
- Generate test points and debug interfaces
- Create optimal PCB layouts

**Design Validation & Optimization**
- Verify electrical rule compliance
- Check design against manufacturing constraints
- Suggest performance optimizations
- Identify cost reduction opportunities
- Recommend component substitutions
- Validate design for reliability

**Collaborative Design**
- Understand human design intent
- Ask clarifying questions when ambiguous
- Explain design decisions and trade-offs
- Provide design alternatives with reasoning
- Learn from feedback and corrections

**Knowledge Transfer**
- Learn from historical designs
- Build component usage patterns
- Understand domain-specific conventions
- Transfer knowledge across design domains
- Generate design documentation automatically

---

## 2. Scope and Objectives

### 2.1 Scope

OpenPCBDB covers the complete electronic design lifecycle from an **AI reasoning perspective**:

```
Requirements (AI understands) 
    ↓
Schematic Design (AI generates/modifies)
    ↓
Component Selection (AI optimizes)
    ↓
PCB Layout (AI plans/routes)
    ↓
Design Validation (AI verifies)
    ↓
Manufacturing Data (AI prepares)
    ↓
Assembly & Test (AI validates)
```

**What OpenPCBDB Represents:**

1. **Component Knowledge Base**
   - Parametric component definitions
   - Electrical characteristics and behavior
   - Physical properties and constraints
   - Usage patterns and best practices
   - Availability and supply chain data

2. **Schematic Design**
   - Hierarchical circuit structure
   - Component instances with full context
   - Net connectivity with semantic meaning
   - Design intent and functional blocks
   - Power domains and signal types
   - Engineering decisions and trade-offs

3. **PCB Physical Design**
   - Board stack-up and materials
   - Component placement with reasoning
   - Routing topology and constraints
   - Design rules with justification
   - Mechanical constraints
   - Thermal considerations

4. **Design Constraints & Rules**
   - Electrical rules (voltage, current, power)
   - Signal integrity requirements
   - Timing constraints
   - Manufacturing capabilities
   - Cost constraints
   - Reliability requirements

5. **Design History & Alternatives**
   - Design iterations and evolution
   - Alternative solutions explored
   - Optimization decisions
   - Trade-off analysis
   - Lessons learned

**Out of Scope (v1.0):**
- Real-time simulation execution (SPICE models are referenced, not embedded)
- 3D mechanical CAD (interface defined, but not full integration)
- Manufacturing execution control
- Supply chain management (data referenced, not managed)

### 2.2 Objectives

**Primary Objective**: Create a database standard that enables AI agents to become **first-class participants** in electronic design.

**Specific Goals:**

1. **Enable AI Understanding**
   - AI can parse any OpenPCBDB design and understand its purpose
   - AI can extract functional blocks and their relationships
   - AI can identify design patterns and best practices
   - AI can assess design quality and potential issues

2. **Enable AI Generation**
   - AI can create complete designs from requirements
   - AI can generate sub-circuits and functional blocks
   - AI can make intelligent component selections
   - AI can optimize layouts for performance/cost

3. **Enable AI Learning**
   - Standardized format for training AI models
   - Historical design data captured for learning
   - Design patterns explicitly represented
   - Success/failure data included for improvement

4. **Enable AI Collaboration**
   - AI can ask clarifying questions
   - AI can propose alternatives with reasoning
   - AI can explain its decisions
   - AI can incorporate human feedback

5. **Enable Continuous Improvement**
   - AI learns from every design
   - Best practices evolve automatically
   - Component recommendations improve over time
   - Design quality increases with usage

### 2.3 Success Criteria

OpenPCBDB will be considered successful when:

1. **AI Agent Test**: An AI agent can:
   - Load an OpenPCBDB design it has never seen
   - Explain what the design does and why
   - Suggest valid improvements
   - Make modifications that work correctly
   - Generate documentation automatically

2. **Generation Test**: An AI can:
   - Create a working design from natural language requirements
   - Make appropriate component selections
   - Generate manufacturable PCB layouts
   - Pass all design rule checks

3. **Learning Test**: An AI trained on OpenPCBDB data can:
   - Predict design issues before they occur
   - Suggest design patterns appropriate to requirements
   - Transfer knowledge across design domains
   - Improve performance over time

4. **Adoption Test**:
   - Multiple AI systems can work with OpenPCBDB
   - Designs are version-controllable and collaborative
   - Human designers find it intuitive to review
   - The format is extensible for new use cases

---

## 3. Core Architecture

### 3.1 Semantic Graph Model

OpenPCBDB is fundamentally a **semantic graph** where:
- **Nodes** = Design entities (components, nets, constraints, blocks)
- **Edges** = Relationships (connects_to, supplies_power, controls, belongs_to)
- **Properties** = Attributes with semantic meaning

```
┌─────────────────────────────────────────────────────┐
│                   AI Reasoning Layer                │
│  (Natural Language, Graph Queries, ML Models)       │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│              Semantic Graph Layer                   │
│  • Entities with Purpose                            │
│  • Relationships with Meaning                       │
│  • Constraints with Reasoning                       │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│             Data Representation Layer               │
│  • JSON/YAML serialization                          │
│  • Schema validation                                │
│  • Version control                                  │
└─────────────────────────────────────────────────────┘
```

### 3.2 Core Entity Types

**Primary Entities:**

1. **Design** - Top-level container for entire project
2. **Library** - Reusable component and symbol definitions
3. **Component** - Electronic parts (resistors, ICs, connectors)
4. **Module** - Physical separate PCB assembly integrated into parent design (e.g., SoM, DIMM, daughterboard)
5. **Net** - Electrical connections between pins
6. **Pin** - Connection points on components
7. **Constraint** - Rules and requirements
8. **Block** - Functional grouping of components (logical grouping on same PCB)
9. **Port** - Hierarchical interface points

**Relationship Types:**

- `connects_to` - Electrical connection
- `supplies` - Power/signal supply relationship
- `controls` - Control relationship
- `belongs_to` - Hierarchical containment
- `contains` - Module contains internal design
- `instantiates` - Parent design instantiates module
- `interfaces_with` - Module interfaces with parent via connector
- `similar_to` - Design pattern relationship
- `alternative_to` - Design alternative
- `derived_from` - Design evolution

### 3.3 Semantic Metadata Structure

Every entity in OpenPCBDB includes a `semantic` field:

```json
{
  "semantic": {
    "purpose": "Human and AI readable purpose",
    "function": "Specific electrical/mechanical function",
    "domain": "power | signal | clock | analog | digital | mixed",
    "critical": true/false,
    "reasoning": "Why this design decision was made",
    "alternatives": ["Other options that were considered"],
    "confidence": 0.0-1.0  // For AI-generated content
  }
}
```

### 3.4 Layered Architecture

**Layer 1: Core Data Model**
- Fundamental entities (Component, Net, Pin, etc.)
- Basic relationships
- Required attributes
- Core semantic fields

**Layer 2: Domain Extensions**
- Power management specifics
- High-speed digital extensions
- RF/Analog extensions
- Sensor/IoT extensions

**Layer 3: Application Extensions**
- Manufacturing-specific data
- Testing and validation data
- Simulation parameters
- Documentation metadata

**Layer 4: AI/ML Extensions**
- Training labels
- Feature vectors
- Confidence scores
- Explainability data

---

## 4. Data Models

This is the core specification defining how design data is structured for AI reasoning.

### 4.1 Component Library Model

#### 4.1.1 ComponentDefinition

Components are the building blocks of electronic design. For AI to work effectively, components must carry complete semantic information.

**Full Schema:**

```json
{
  "type": "ComponentDefinition",
  "id": "res_0603_10k_1pct",
  "version": "1.0",
  
  "identification": {
    "name": "Resistor 10kΩ ±1% 0603",
    "category": "passive.resistor",
    "subcategory": "precision",
    "manufacturer": "Yageo",
    "mpn": "RC0603FR-0710KL",
    "aliases": ["R_10K_0603", "10k_resistor"]
  },
  
  "parameters": {
    "resistance": {
      "nominal": 10000,
      "min": 9900,
      "max": 10100,
      "unit": "ohm",
      "tolerancePercent": 1
    },
    "powerRating": {
      "value": 0.1,
      "unit": "watt",
      "deratedAt": {
        "temperature": 70,
        "unit": "celsius"
      }
    },
    "voltageRating": {
      "max": 75,
      "unit": "volt"
    },
    "temperatureCoefficient": {
      "value": 100,
      "unit": "ppm_per_celsius"
    },
    "temperatureRange": {
      "min": -55,
      "max": 155,
      "unit": "celsius"
    }
  },
  
  "pins": [
    {
      "id": "1",
      "name": "Terminal1",
      "type": "passive",
      "electricalType": "bidirectional"
    },
    {
      "id": "2",
      "name": "Terminal2",
      "type": "passive",
      "electricalType": "bidirectional"
    }
  ],
  
  "physical": {
    "package": "0603",
    "footprintId": "RES_0603_STD",
    "dimensions": {
      "length": 1.6,
      "width": 0.8,
      "height": 0.55,
      "unit": "mm"
    },
    "mounting": "smd",
    "polarity": false
  },
  
  "semantic": {
    "function": "current_limiting",
    "typicalUseCases": [
      "pull-up",
      "pull-down",
      "current_sense",
      "voltage_divider"
    ],
    "domain": "analog",
    "critical": false,
    "aiNotes": "General purpose resistor, suitable for most applications within ratings"
  },
  
  "procurement": {
    "datasheetUrl": "https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/PYu-RC_Group_51_RoHS_L_11.pdf",
    "typicalCost": {
      "value": 0.012,
      "currency": "USD",
      "quantity": 1,
      "date": "2025-01"
    },
    "lifecycleStatus": "active",
    "leadTimeDays": 30,
    "rohsCompliant": true
  },
  
  "simulation": {
    "spiceModel": "resistor_ideal.sp",
    "behavioralModel": null
  },
  
  "metadata": {
    "created": "2025-01-11T10:00:00Z",
    "modified": "2025-01-11T10:00:00Z",
    "author": "component_library_v1",
    "tags": ["smd", "general_purpose", "precision"],
    "usageCount": 1847,  // How many times used in designs
    "reliabilityScore": 0.98  // AI-computed reliability
  }
}
```

**Key AI-Friendly Features:**
- ✅ Complete parametric data for selection algorithms
- ✅ Semantic use cases for understanding context
- ✅ Procurement data for cost optimization
- ✅ Usage statistics for learning patterns
- ✅ Reliability scores for quality prediction

#### 4.1.2 Integrated Circuit (Complex Component)

```json
{
  "type": "ComponentDefinition",
  "id": "mcu_stm32f103c8t6",
  "identification": {
    "name": "STM32F103C8T6 - ARM Cortex-M3 MCU",
    "category": "ic.microcontroller",
    "manufacturer": "STMicroelectronics",
    "mpn": "STM32F103C8T6"
  },
  
  "parameters": {
    "cpuCore": "ARM Cortex-M3",
    "clockSpeedMax": {"value": 72, "unit": "MHz"},
    "flashMemory": {"value": 64, "unit": "KB"},
    "ram": {"value": 20, "unit": "KB"},
    "supplyVoltage": {"min": 2.0, "max": 3.6, "unit": "V"},
    "ioPins": 37,
    "adcChannels": 10,
    "timers": 7,
    "communication": ["SPI", "I2C", "USART", "USB", "CAN"]
  },
  
  "pins": [
    {
      "id": "1",
      "name": "VBAT",
      "type": "power",
      "electricalType": "power_input",
      "description": "Backup power supply",
      "semantic": {
        "purpose": "RTC and backup register power",
        "voltageRange": {"min": 1.8, "max": 3.6, "unit": "V"},
        "required": false
      }
    },
    {
      "id": "7",
      "name": "PA0",
      "type": "io",
      "electricalType": "bidirectional",
      "alternateFunctions": ["TIM2_CH1", "ADC12_IN0", "WKUP"],
      "semantic": {
        "purpose": "General purpose I/O or alternate function",
        "typicalUses": ["wakeup_pin", "timer_input", "analog_input"]
      }
    }
    // ... all 48 pins defined
  ],
  
  "functionalBlocks": [
    {
      "name": "Core",
      "type": "cpu",
      "description": "ARM Cortex-M3 processor core"
    },
    {
      "name": "PowerManagement",
      "type": "power",
      "pins": ["VDD_1", "VDD_2", "VDD_3", "VSS_1", "VSS_2"],
      "requirements": {
        "decouplingCaps": [
          {"value": 100, "unit": "nF", "quantity": 3, "location": "near_pins"}
        ],
        "bulkCap": {"value": 10, "unit": "uF", "quantity": 1}
      }
    }
  ],
  
  "semantic": {
    "function": "general_purpose_microcontroller",
    "typicalUseCases": [
      "motor_control",
      "sensor_interface",
      "communication_gateway",
      "embedded_control"
    ],
    "domain": "digital",
    "critical": true,
    "aiNotes": "Popular MCU for embedded applications. Requires careful power supply design and crystal oscillator circuit."
  }
}
```

### 4.2 Schematic Model

#### 4.2.1 Design (Top-level)

```json
{
  "type": "Design",
  "name": "Smart_LED_Driver_v2.1",
  "version": "2.1.0",
  
  "metadata": {
    "title": "Smart LED Driver with PWM Control",
    "author": "Jane Smith",
    "company": "Acme Electronics",
    "created": "2025-01-01T00:00:00Z",
    "modified": "2025-01-11T15:30:00Z",
    "status": "production"
  },
  
  "requirements": {
    "inputVoltage": {"min": 9, "max": 12, "nominal": 12, "unit": "V"},
    "outputPower": {"max": 10, "unit": "W"},
    "efficiency": {"min": 85, "unit": "percent"},
    "features": [
      "PWM dimming control",
      "Overcurrent protection",
      "Thermal shutdown"
    ]
  },
  
  "designIntent": {
    "purpose": "Drive high-power LED with variable brightness control",
    "targetApplication": "Automotive interior lighting",
    "keyRequirements": [
      "Automotive grade components (-40°C to +125°C)",
      "EMI compliance",
      "Low cost (<$5 BOM)"
    ],
    "designApproach": "Buck converter topology with PWM dimming"
  },
  
  "library": {
    "componentLibraries": [
      "lib/standard_components.json",
      "lib/automotive_grade.json"
    ],
    "symbolLibrary": "lib/symbols.json"
  },
  
  "schematic": {
    "sheets": ["sheet_001", "sheet_002"],
    "hierarchy": "hierarchy_001"
  },
  
  "blocks": ["block_power_supply", "block_pwm_control", "block_led_driver"],
  
  "nets": ["net_001", "net_002"],  // References to net definitions
  
  "constraints": ["constraint_001", "constraint_002"],
  
  "bom": "bom_001",
  
  "semantic": {
    "complexity": "medium",
    "designPattern": "standard_buck_converter",
    "aiGeneratedPercentage": 35,
    "validated": true,
    "validationDate": "2025-01-10"
  }
}
```

#### 4.2.2 ComponentInstance (in design)

```json
{
  "type": "ComponentInstance",
  "id": "R1",
  "refDesignator": "R1",
  "componentDefinitionId": "res_0603_10k_1pct",
  
  "sheet": "sheet_001",
  "block": "block_pwm_control",
  
  "position": {
    "x": 100.0,
    "y": 50.0,
    "unit": "mm"
  },
  "rotation": 0,
  "mirrored": false,
  
  "propertyOverrides": {
    "valueDisplay": "10kΩ",
    "doNotPopulate": false,
    "substitutionAllowed": true
  },
  
  "pinConnections": [
    {
      "pinId": "1",
      "netId": "net_vcc_3v3",
      "connectionPoint": {"x": 100.0, "y": 50.0}
    },
    {
      "pinId": "2",
      "netId": "net_mcu_pwm_input",
      "connectionPoint": {"x": 105.0, "y": 50.0}
    }
  ],
  
  "semantic": {
    "purpose": "Pull-up resistor for PWM input",
    "function": "Ensures defined logic level when MCU pin is high-impedance",
    "critical": false,
    "reasoning": "10kΩ chosen to balance power consumption and noise immunity",
    "alternativesConsidered": [
      {"value": 4700, "reason": "Too much current draw"},
      {"value": 47000, "reason": "Potentially too weak for noise immunity"}
    ],
    "designRule": "Pull-up resistors for digital inputs should be 10kΩ ±20%"
  },
  
  "analysis": {
    "powerDissipationMax": 0.001,  // Watts
    "temperatureRise": 0.5,  // Celsius
    "reliabilityFactor": 0.99
  }
}
```

#### 4.2.3 Net (Electrical Connection)

This is critical for AI understanding of circuit topology.

```json
{
  "type": "Net",
  "id": "net_vcc_5v",
  "name": "VCC_5V",
  "aliases": ["+5V", "POWER_5V", "VCC"],
  
  "connections": [
    {"component": "U1", "pin": "8"},
    {"component": "C1", "pin": "1"},
    {"component": "C2", "pin": "1"},
    {"component": "R1", "pin": "1"},
    {"component": "LED1", "pin": "anode"},
    {"component": "J1", "pin": "1"}  // Connector power input
  ],
  
  "semantic": {
    "type": "power",
    "subType": "supply",
    "domain": "digital_power",
    "critical": true,
    "purpose": "Main 5V power rail for digital circuitry",
    "function": "Supplies power to MCU and peripheral ICs",
    "source": {"component": "U2", "pin": "out", "type": "switching_regulator"},
    "loads": [
      {"component": "U1", "currentMax": 0.1, "unit": "A"},
      {"component": "LED1", "currentMax": 0.02, "unit": "A"}
    ]
  },
  
  "electricalCharacteristics": {
    "voltage": {
      "nominal": 5.0,
      "min": 4.75,
      "max": 5.25,
      "unit": "V",
      "tolerancePercent": 5
    },
    "current": {
      "typical": 0.15,
      "max": 0.5,
      "unit": "A"
    },
    "impedance": {
      "dcResistanceMax": 0.1,
      "unit": "ohm"
    }
  },
  
  "constraints": {
    "traceWidthMin": 0.5,  // mm
    "traceWidthRecommended": 1.0,  // mm for current capacity
    "viaCountMin": 2,  // Multiple vias for reliability
    "keepAwayDistance": 0.3,  // mm from high-speed signals
    "decoupling": {
      "required": true,
      "capacitors": [
        {"value": 100, "unit": "nF", "quantity": 3, "placement": "distributed"},
        {"value": 10, "unit": "uF", "quantity": 1, "placement": "near_regulator"}
      ]
    }
  },
  
  "pcbRouting": {
    "layerPreference": ["top", "bottom"],  // Avoid inner layers for power
    "plane": false,  // Not a power plane, but a trace
    "polygonPour": true,  // Can use copper pour
    "priority": "high"
  },
  
  "analysis": {
    "voltageDropMax": 0.1,  // V
    "noiseBudget": 50,  // mV peak-to-peak
    "transientResponse": "Must settle within 100us after load step"
  },
  
  "aiAnnotations": {
    "patternType": "power_distribution_network",
    "similarNets": ["net_vcc_3v3", "net_vcc_12v"],
    "commonIssues": [
      "Insufficient decoupling capacitors",
      "Trace width too narrow for current",
      "Voltage drop excessive"
    ],
    "bestPractices": [
      "Place bulk capacitor near power entry",
      "Distribute ceramic capacitors near IC power pins",
      "Use star topology for distribution"
    ]
  }
}
```

#### 4.2.4 FunctionalBlock

AI understands designs better when organized into functional blocks.

```json
{
  "type": "FunctionalBlock",
  "id": "block_pwm_control",
  "name": "PWM Control Circuit",
  
  "components": ["U1", "R1", "R2", "C1", "C2", "Q1"],
  
  "nets": {
    "inputs": ["net_pwm_command", "net_feedback"],
    "outputs": ["net_gate_drive"],
    "power": ["net_vcc_5v", "net_gnd"],
    "internal": ["net_error_signal", "net_compensation"]
  },
  
  "ports": [
    {
      "name": "PWM_IN",
      "direction": "input",
      "type": "digital",
      "net": "net_pwm_command",
      "description": "PWM duty cycle command input"
    },
    {
      "name": "GATE_OUT",
      "direction": "output",
      "type": "analog",
      "net": "net_gate_drive",
      "description": "Gate drive signal for power MOSFET"
    }
  ],
  
  "semantic": {
    "purpose": "Generate gate drive signal for LED driver based on PWM command",
    "function": "PWM controller with feedback compensation",
    "topology": "voltage_mode_control",
    "critical": true,
    "designPattern": "standard_pwm_controller",
    "alternativesEvaluated": [
      {
        "approach": "current_mode_control",
        "pros": ["Better transient response"],
        "cons": ["More complex", "Higher cost"],
        "reasonRejected": "Not needed for LED application"
      }
    ]
  },
  
  "subBlocks": [
    {
      "name": "ErrorAmplifier",
      "components": ["U1A", "R1", "R2", "C1"],
      "function": "Generate error signal from feedback"
    },
    {
      "name": "GateDriver",
      "components": ["Q1", "R3"],
      "function": "Buffer PWM signal to drive MOSFET gate"
    }
  ],
  
  "requirements": {
    "switchingFrequency": {"value": 100, "unit": "kHz"},
    "dutyCycleRange": {"min": 0, "max": 90, "unit": "percent"},
    "responseTime": {"max": 10, "unit": "ms"}
  },
  
  "analysis": {
    "simulated": true,
    "simulationResults": {
      "efficiency": 92,
      "responseTimeMeasured": 8.5,
      "stabilityMargin": {"phase": 60, "gain": 12}
    }
  },
  
  "aiMetadata": {
    "complexityScore": 0.6,
    "reusabilityScore": 0.8,
    "similarBlocksInLibrary": ["standard_buck_controller", "pwm_led_driver"],
    "learningNotes": "Successful design pattern for LED dimming applications"
  }
}
```

#### 4.2.5 Module

**Purpose**: Modules represent **physical separate PCB assemblies** that are integrated into a parent design. Unlike FunctionalBlocks (which are logical groupings on the same PCB), modules are distinct boards with their own complete design hierarchy.

**Key Differences:**
- **FunctionalBlock**: Logical grouping of components on the same PCB (no physical separation)
- **Module**: Physical separate board with connector interface (e.g., System-on-Module, DIMM, M.2 card, daughterboard)

**Use Cases:**
- System-on-Module (SoM) designs (Raspberry Pi Compute Module, i.MX8 modules)
- Memory modules (DIMM, SO-DIMM, LPDDR)
- Wireless modules (WiFi, Bluetooth, Cellular)
- Power modules (DC-DC converter modules, PoE modules)
- Sensor modules (IMU, GPS, camera)
- Display modules (LCD, OLED)
- Interface modules (USB hub, Ethernet PHY)

**Full Schema:**

```json
{
  "type": "ModuleDefinition",
  "id": "module_som_imx8",
  "name": "i.MX8 System-on-Module",
  "version": "1.2",
  
  "identification": {
    "manufacturer": "Example Inc",
    "partNumber": "SOM-IMX8-001",
    "category": "module.som",
    "subcategory": "arm_cortex_a53",
    "description": "Complete embedded Linux computer on a module with i.MX8 processor"
  },
  
  "interface": {
    "connectorType": "board_to_board_connector",
    "connectorMPN": "DF40C-100DP-0.4V",
    "pinCount": 100,
    "pitch": {"value": 0.4, "unit": "mm"},
    "pins": [
      {
        "id": "1",
        "name": "VIN_5V",
        "electricalType": "power_input",
        "voltage": {"nominal": 5.0, "min": 4.75, "max": 5.25, "unit": "V"},
        "currentMax": {"value": 3.0, "unit": "A"},
        "function": "Main power input"
      },
      {
        "id": "2",
        "name": "GND",
        "electricalType": "ground",
        "function": "Ground reference"
      },
      {
        "id": "10",
        "name": "UART0_TX",
        "electricalType": "output",
        "type": "digital",
        "voltage": {"logic": "3.3V", "unit": "V"},
        "function": "Debug UART transmit"
      },
      {
        "id": "20",
        "name": "ETH_MDI0_P",
        "electricalType": "bidirectional",
        "type": "differential",
        "differentialPair": "ETH_MDI0_N",
        "impedance": {"value": 100, "unit": "ohm"},
        "function": "Ethernet PHY differential pair positive"
      },
      {
        "id": "21",
        "name": "ETH_MDI0_N",
        "electricalType": "bidirectional",
        "type": "differential",
        "differentialPair": "ETH_MDI0_P",
        "impedance": {"value": 100, "unit": "ohm"},
        "function": "Ethernet PHY differential pair negative"
      }
    ]
  },
  
  "physical": {
    "formFactor": "custom_som",
    "dimensions": {
      "length": 50,
      "width": 40,
      "height": 5.5,
      "unit": "mm"
    },
    "weight": {"value": 12, "unit": "g"},
    "mounting": "board_to_board_connector",
    "connectorLocation": {
      "x": 25,
      "y": 20,
      "orientation": "bottom",
      "unit": "mm"
    },
    "keepoutZones": [
      {
        "shape": "rectangle",
        "x": 10, "y": 10,
        "width": 5,
        "height": 5,
        "layer": "top",
        "unit": "mm",
        "reason": "Heat spreader clearance for processor"
      }
    ]
  },
  
  "internalDesign": {
    "reference": "designs/som_imx8/som_imx8.opcbdb",
    "type": "opcbdb",
    "componentCount": 247,
    "netCount": 1053,
    "layerCount": 8,
    "complexity": "high",
    "canBeOpened": true,
    "abstraction": "white_box"
  },
  
  "functionalCapabilities": {
    "processor": {
      "type": "i.MX8 QuadLite",
      "architecture": "ARM Cortex-A53",
      "cores": 4,
      "frequency": {"value": 1.5, "unit": "GHz"},
      "features": ["NEON", "TrustZone", "Crypto"]
    },
    "memory": {
      "ram": {"size": 2, "unit": "GB", "type": "LPDDR4", "speed": "3200 MT/s"},
      "storage": {"size": 16, "unit": "GB", "type": "eMMC", "speed": "HS400"}
    },
    "interfaces": [
      "ethernet_1gbit",
      "usb_2.0_host",
      "usb_3.0_host",
      "uart_debug",
      "i2c_x2",
      "spi_x2",
      "gpio_x20",
      "can_x2"
    ],
    "video": ["hdmi_1080p", "lvds_display", "mipi_dsi"],
    "audio": ["i2s", "spdif"]
  },
  
  "powerRequirements": {
    "inputs": [
      {
        "rail": "VIN_5V",
        "voltage": {"nominal": 5.0, "min": 4.75, "max": 5.25, "unit": "V"},
        "currentIdle": {"value": 0.5, "unit": "A"},
        "currentTypical": {"value": 1.2, "unit": "A"},
        "currentPeak": {"value": 3.0, "unit": "A"},
        "purpose": "Main power input"
      }
    ],
    "totalPower": {
      "idle": {"value": 2.5, "unit": "W"},
      "typical": {"value": 6.0, "unit": "W"},
      "peak": {"value": 15.0, "unit": "W"}
    },
    "inrushCurrent": {"value": 5.0, "duration": 10, "unit": "A", "durationUnit": "ms"}
  },
  
  "thermal": {
    "ambientTemperatureRange": {"min": 0, "max": 85, "unit": "°C"},
    "junctionTemperatureMax": {"value": 105, "unit": "°C"},
    "thermalResistance": {"value": 15, "unit": "°C/W", "withHeatsink": 8},
    "coolingRequired": "passive_heatsink_recommended",
    "powerDissipation": {"typical": 6.0, "max": 15.0, "unit": "W"},
    "heatsinkMountingHoles": [
      {"x": 15, "y": 15, "diameter": 2.5, "unit": "mm"},
      {"x": 35, "y": 15, "diameter": 2.5, "unit": "mm"}
    ]
  },
  
  "functionalBlocks": [
    {
      "name": "CPU Complex",
      "description": "i.MX8 QuadLite ARM Cortex-A53 processor with 4 cores",
      "components": ["U1", "C1-C24"],
      "power": {"typical": 3.5, "max": 8.0, "unit": "W"}
    },
    {
      "name": "Memory Subsystem",
      "description": "2GB LPDDR4 RAM with controller",
      "components": ["U2", "U3", "C25-C40"],
      "power": {"typical": 1.0, "max": 3.0, "unit": "W"}
    },
    {
      "name": "Storage",
      "description": "16GB eMMC flash storage",
      "components": ["U4", "C41-C45"],
      "power": {"typical": 0.5, "max": 1.0, "unit": "W"}
    },
    {
      "name": "Power Management",
      "description": "PMIC with multiple voltage rails",
      "components": ["U5", "L1-L5", "C46-C80"],
      "power": {"typical": 0.8, "max": 2.0, "unit": "W"}
    },
    {
      "name": "Ethernet PHY",
      "description": "1Gbit Ethernet transceiver",
      "components": ["U6", "R1-R10", "C81-C90"],
      "power": {"typical": 0.5, "max": 1.0, "unit": "W"}
    }
  ],
  
  "semantic": {
    "purpose": "Complete embedded computer system on a module for rapid system integration",
    "function": "Linux-capable ARM processing module with memory, storage, and peripherals",
    "domain": "digital",
    "critical": true,
    "designPattern": "system_on_module",
    "typicalUseCases": [
      "Industrial control systems",
      "IoT gateways",
      "Medical devices",
      "Embedded vision systems",
      "Building automation",
      "Test and measurement equipment"
    ],
    "reasoning": "Modular approach reduces main board design complexity and time-to-market. Pre-certified module simplifies regulatory compliance.",
    "alternatives": [
      {
        "approach": "Discrete CPU design on main board",
        "pros": ["Full control", "Optimized for specific application", "Lower BOM cost at volume"],
        "cons": ["High complexity", "Long development time (6-12 months)", "Higher risk", "DDR routing expertise required"],
        "reasonRejected": "Development time and complexity too high for product schedule"
      },
      {
        "approach": "Single board computer (Raspberry Pi style)",
        "pros": ["Very low cost", "Ready availability", "Large community"],
        "cons": ["Limited customization", "Non-industrial temp range", "No carrier board integration"],
        "reasonRejected": "Need industrial temperature range and custom I/O integration"
      }
    ]
  },
  
  "procurement": {
    "datasheetUrl": "https://example.com/som-imx8-datasheet.pdf",
    "unitCost": {"value": 85.00, "currency": "USD", "quantity": 100},
    "leadTime": {"typical": 8, "max": 12, "unit": "weeks"},
    "minimumOrderQuantity": 1,
    "lifecycleStatus": "active",
    "availability": "good",
    "alternativeSources": ["Digikey", "Mouser", "Arrow", "Direct from manufacturer"],
    "eolDate": null,
    "replacementPart": null
  },
  
  "designGuidelines": {
    "layoutNotes": [
      "Keep high-speed differential pairs (USB, Ethernet) away from module edges",
      "Provide solid ground plane under module connector on carrier board",
      "Add 100nF decoupling caps on each power pin at carrier board connector",
      "Allow 10mm keepout around module perimeter for heatsink clearance",
      "Route critical signals (clocks, resets) with controlled impedance",
      "Maintain differential pair spacing and impedance through connector"
    ],
    "powerDeliveryNotes": [
      "5V input must support 3A peak current with <100mV ripple",
      "Add bulk capacitance (100uF minimum) near connector on carrier board",
      "Trace width to module connector: minimum 40 mils (1mm) for main power",
      "Use 2oz copper or heavier on power planes",
      "Ensure low impedance ground return path"
    ],
    "thermalNotes": [
      "Mount heatsink on top of processor (mounting holes at specified coordinates)",
      "Ensure airflow over module or use larger heatsink if ambient temp > 50°C",
      "Thermal pad on bottom of module should contact carrier board copper pour",
      "Consider fan for enclosed applications or continuous high CPU load"
    ],
    "signalIntegrityNotes": [
      "USB 3.0 differential pairs: 90Ω impedance, max 5mm length mismatch",
      "Ethernet differential pairs: 100Ω impedance, keep away from switching noise",
      "HDMI signals: 100Ω differential impedance, shield from other signals",
      "Clock signals: Use series termination, avoid vias if possible"
    ]
  },
  
  "complianceAndCertification": {
    "tested": ["FCC_Part_15_Class_B", "CE_EMC", "RoHS", "REACH"],
    "certificationDocuments": [
      {"type": "FCC", "url": "fcc_cert.pdf", "number": "FCC-ID-12345"},
      {"type": "CE", "url": "ce_cert.pdf", "number": "CE-2024-001"}
    ],
    "operatingSystemsSupported": ["Linux", "Android", "Yocto", "Buildroot"]
  },
  
  "aiMetadata": {
    "complexity": "high",
    "reusabilityScore": 0.95,
    "abstractionLevel": "system",
    "blackBox": false,
    "canBeSimulated": true,
    "commonIntegrationIssues": [
      "Power supply noise coupling into analog signals on carrier board",
      "Ground loops if multiple ground connections used incorrectly",
      "Impedance mismatch on high-speed signals at connector interface",
      "Thermal issues if heatsink not properly mounted",
      "Signal integrity problems with long traces on carrier board"
    ],
    "designPatternTags": ["system_on_module", "arm_processor", "industrial_embedded", "linux_computer"],
    "learningNotes": "Module abstracts complex DDR4 routing and power sequencing. Carrier board design complexity reduced by 70%. Time-to-market reduced from 12 months to 3 months."
  }
}
```

**Module Instance in Parent Design:**

When a module is used in a parent design, it is instantiated as a component instance:

```json
{
  "type": "ComponentInstance",
  "instanceId": "MOD1",
  "definitionId": "module_som_imx8",
  "definitionType": "module",
  
  "definition": {
    "$ref": "library/modules/som_imx8.json"
  },
  
  "placement": {
    "x": 50,
    "y": 50,
    "rotation": 0,
    "layer": "top",
    "unit": "mm"
  },
  
  "configuration": {
    "firmwareVersion": "1.2.3",
    "bootMode": "eMMC",
    "customSettings": {
      "enable_ethernet": true,
      "enable_hdmi": false,
      "enable_wifi": false
    }
  },
  
  "semantic": {
    "purpose": "Main processing module for industrial control system",
    "reasoning": "Selected for industrial temperature range (-40 to +85°C) and Linux support with long-term availability",
    "critical": true,
    "instanceSpecific": "Configured for headless operation with Ethernet connectivity only"
  }
}
```

**Multiple Module Instances Example:**

Modules can be instantiated multiple times in a design (e.g., memory modules, redundant systems):

```json
{
  "design": {
    "metadata": {
      "name": "Redundant Control System",
      "description": "Dual SoM design with automatic failover"
    },
    "components": [
      {
        "instanceId": "MOD_PRIMARY",
        "definitionId": "module_som_imx8",
        "definitionType": "module",
        "semantic": {
          "purpose": "Primary controller",
          "role": "master"
        }
      },
      {
        "instanceId": "MOD_BACKUP",
        "definitionId": "module_som_imx8",
        "definitionType": "module",
        "semantic": {
          "purpose": "Backup controller for redundancy",
          "role": "standby_failover"
        }
      }
    ],
    "nets": [
      {
        "id": "net_watchdog",
        "name": "WATCHDOG",
        "connections": [
          {"component": "MOD_PRIMARY", "pin": "GPIO_10"},
          {"component": "MOD_BACKUP", "pin": "GPIO_10"},
          {"component": "U_SUPERVISOR", "pin": "WD_IN"}
        ],
        "semantic": {
          "purpose": "Cross-monitoring watchdog for failover detection"
        }
      }
    ]
  }
}
```

**Module Categories:**

Modules are categorized by their primary function and form factor:

```
module
├── som (System-on-Module)
│   ├── arm_cortex_a
│   ├── arm_cortex_m
│   ├── x86_64
│   ├── risc_v
│   └── fpga
├── memory
│   ├── dimm
│   ├── so_dimm
│   ├── lpddr
│   └── ddr5
├── power
│   ├── dc_dc_module
│   ├── ac_dc_module
│   ├── poe_module
│   └── battery_module
├── wireless
│   ├── wifi_module
│   ├── bluetooth_module
│   ├── cellular_module
│   ├── lora_module
│   └── zigbee_module
├── sensor
│   ├── imu_module
│   ├── gps_module
│   ├── camera_module
│   └── environmental_sensor
├── display
│   ├── lcd_module
│   ├── oled_module
│   ├── e_paper_module
│   └── tft_module
├── interface
│   ├── usb_hub_module
│   ├── ethernet_phy_module
│   ├── can_transceiver_module
│   └── rs485_module
└── expansion
    ├── arduino_shield
    ├── raspberry_pi_hat
    ├── mikroelektronika_click
    └── pc104_module
```

### 4.3 Constraint Model

Constraints are rules that AI must respect during design and validation.

```json
{
  "type": "DesignConstraint",
  "id": "constraint_power_integrity_001",
  "name": "5V Power Rail Voltage Regulation",
  
  "appliesTo": {
    "nets": ["net_vcc_5v"],
    "components": [],
    "blocks": ["block_power_supply"]
  },
  
  "constraintType": "voltage_regulation",
  
  "rule": {
    "parameter": "voltage",
    "nominal": 5.0,
    "tolerance": 0.25,
    "unit": "V",
    "condition": "At all component power pins under all load conditions"
  },
  
  "validation": {
    "method": "simulation",
    "tool": "SPICE",
    "passingCriteria": "Voltage within ±5% at all times"
  },
  
  "semantic": {
    "criticality": "high",
    "reasoning": "MCU requires stable 5V ±5% for reliable operation",
    "consequenceOfViolation": "MCU may reset or malfunction",
    "source": "STM32F103 datasheet requirement"
  },
  
  "aiGuidance": {
    "howToSatisfy": [
      "Use low-dropout regulator with good line regulation",
      "Add adequate decoupling capacitance (min 10µF bulk + 100nF ceramics)",
      "Minimize trace resistance (use wide traces or planes)",
      "Place decoupling caps close to IC power pins"
    ],
    "commonViolations": [
      "Insufficient bulk capacitance",
      "Too much trace resistance from regulator to load",
      "Decoupling capacitors too far from IC pins"
    ]
  }
}
```

### 4.4 PCB Layout Model

```json
{
  "type": "PCBLayout",
  "designId": "Smart_LED_Driver_v2.1",
  
  "board": {
    "outline": {
      "shape": "rectangle",
      "dimensions": {"width": 50, "length": 80, "unit": "mm"},
      "corners": "rounded",
      "cornerRadius": 3.0
    },
    "mountingHoles": [
      {"position": {"x": 5, "y": 5}, "diameter": 3.2, "plated": false}
    ]
  },
  
  "stackup": {
    "layerCount": 2,
    "thicknessTotal": 1.6,
    "unit": "mm",
    "layers": [
      {
        "number": 1,
        "name": "Top",
        "type": "signal",
        "copperThickness": 35,
        "unit": "um"
      },
      {
        "number": 2,
        "name": "Core",
        "type": "dielectric",
        "material": "FR4",
        "thickness": 1.5,
        "dielectricConstant": 4.5
      },
      {
        "number": 3,
        "name": "Bottom",
        "type": "signal",
        "copperThickness": 35,
        "unit": "um"
      }
    ]
  },
  
  "componentPlacement": [
    {
      "refDesignator": "U1",
      "position": {"x": 25.0, "y": 40.0, "unit": "mm"},
      "rotation": 90,
      "side": "top",
      "locked": false,
      "semantic": {
        "placementReasoning": "Central location to minimize trace lengths to peripherals",
        "keepOutZone": {"radius": 5.0, "reason": "Thermal considerations"},
        "placementPriority": "high"
      }
    }
  ],
  
  "routing": {
    "traces": [],  // Individual trace definitions
    "vias": [],
    "planes": [
      {
        "net": "net_gnd",
        "layer": "bottom",
        "type": "solid_pour",
        "clearance": 0.3,
        "thermalRelief": true
      }
    ]
  },
  
  "designRules": {
    "traceWidthMin": 0.15,
    "traceSpacingMin": 0.15,
    "viaDrillMin": 0.3,
    "viaPadDiameterMin": 0.6,
    "unit": "mm"
  },
  
  "semantic": {
    "designApproach": "Auto-routed with manual optimization of critical nets",
    "criticalNetsHandRouted": ["net_gate_drive", "net_vcc_5v"],
    "aiGeneratedPercentage": 75,
    "layoutPattern": "standard_two_layer_smd"
  }
}
```

---

## 5. API Specification

The API is designed for AI agents to query, analyze, create, and modify designs.

### 5.1 Python API (Reference Implementation)

#### 5.1.1 Basic Operations

```python
from openpcbdb import Design, Query, Component, Net

# ========================================
# LOADING AND SAVING
# ========================================

# Load existing design
design = Design.load("smart_led_driver.opcbdb")

# Create new design
new_design = Design(
    name="My_New_Design",
    version="1.0.0",
    author="AI Agent Alpha"
)

# Save design
design.save("output.opcbdb")

# ========================================
# QUERYING COMPONENTS
# ========================================

# Find all resistors
resistors = design.query(
    Query.components()
    .where(category="passive.resistor")
)

# Find resistors in specific range
resistors_10k = design.query(
    Query.components()
    .where(category="passive.resistor")
    .parameter("resistance", min=9000, max=11000)
)

# Find critical components
critical = design.query(
    Query.components()
    .where(semantic__critical=True)
)

# Find components by function
current_sensors = design.query(
    Query.components()
    .where(semantic__function="current_sensing")
)

# ========================================
# QUERYING NETS
# ========================================

# Find all power nets
power_nets = design.query(
    Query.nets()
    .where(semantic__type="power")
)

# Find nets in voltage range
five_volt_nets = design.query(
    Query.nets()
    .where(semantic__type="power")
    .voltage_range(4.5, 5.5)
)

# Find nets connected to specific component
mcu_nets = design.query(
    Query.nets()
    .connected_to(component="U1")
)

# Find critical signal paths
critical_signals = design.query(
    Query.nets()
    .where(
        semantic__type="signal",
        semantic__critical=True
    )
)

# ========================================
# GRAPH TRAVERSAL
# ========================================

# Trace all connections from component
connections = design.trace_connections(
    from_component="U1",
    pin="8",
    max_depth=3
)

# Find all components in power domain
power_domain = design.get_power_domain("VCC_5V")
components_in_domain = power_domain.get_all_components()

# Get component dependencies
dependencies = design.get_dependencies(component="U1")

# Find signal path
path = design.find_signal_path(
    from_component="U1",
    from_pin="PA0",
    to_component="J1",
    to_pin="3"
)
```

#### 5.1.2 AI Analysis API

```python
from openpcbdb.ai import AIAnalyzer, AIGenerator

# ========================================
# SEMANTIC UNDERSTANDING
# ========================================

analyzer = AIAnalyzer(design)

# Get high-level understanding
understanding = analyzer.understand_design()
print(understanding.purpose)  # "LED driver with PWM control"
print(understanding.functional_blocks)  # ['power_supply', 'pwm_control', 'led_driver']
print(understanding.complexity_score)  # 0.65

# Extract design patterns
patterns = analyzer.extract_patterns()
for pattern in patterns:
    print(f"Pattern: {pattern.name}")
    print(f"Confidence: {pattern.confidence}")
    print(f"Components: {pattern.components}")

# Identify design intent
intent = analyzer.get_design_intent()
print(intent.requirements)
print(intent.constraints)
print(intent.trade_offs)

# ========================================
# VALIDATION AND ANALYSIS
# ========================================

# Check for potential issues
issues = analyzer.find_potential_issues()
for issue in issues:
    print(f"Issue: {issue.description}")
    print(f"Severity: {issue.severity}")
    print(f"Location: {issue.component}")
    print(f"Suggestion: {issue.fix_suggestion}")

# Analyze power integrity
power_analysis = analyzer.analyze_power_integrity()
for net in power_analysis.power_nets:
    print(f"Net: {net.name}")
    print(f"  Voltage drop: {net.voltage_drop}V")
    print(f"  Decoupling adequate: {net.decoupling_adequate}")
    print(f"  Issues: {net.issues}")

# Signal integrity analysis
si_analysis = analyzer.analyze_signal_integrity()

# Thermal analysis
thermal = analyzer.analyze_thermal()
hotspots = thermal.get_hotspots()

# ========================================
# DESIGN SUGGESTIONS
# ========================================

# Get improvement suggestions
suggestions = analyzer.suggest_improvements()
for suggestion in suggestions:
    print(f"Suggestion: {suggestion.description}")
    print(f"Impact: {suggestion.estimated_impact}")
    print(f"Difficulty: {suggestion.implementation_difficulty}")
    print(f"How: {suggestion.implementation_steps}")

# Component replacement suggestions
alternatives = analyzer.suggest_component_alternatives(
    component="R1",
    optimize_for="cost"  # or "performance", "availability"
)

# ========================================
# AI GENERATION
# ========================================

generator = AIGenerator()

# Generate from requirements
new_design = generator.generate_from_requirements(
    requirements={
        "type": "power_supply",
        "inputVoltage": {"min": 9, "max": 12, "unit": "V"},
        "outputVoltage": {"nominal": 5.0, "unit": "V"},
        "outputCurrent": {"max": 2.0, "unit": "A"},
        "features": ["overcurrent_protection", "thermal_shutdown"]
    },
    constraints={
        "costTarget": {"max": 3.0, "currency": "USD"},
        "boardArea": {"max": 500, "unit": "mm2"}
    }
)

# Generate functional block
pwm_block = generator.generate_block(
    function="pwm_controller",
    specifications={
        "frequency": {"value": 100, "unit": "kHz"},
        "dutyCycleRange": {"min": 0, "max": 100, "unit": "percent"}
    }
)

# Auto-complete partial design
completed = generator.complete_design(
    partial_design=design,
    missing_blocks=["decoupling", "esd_protection"]
)

# ========================================
# COMPONENT SELECTION
# ========================================

from openpcbdb.ai import ComponentSelector

selector = ComponentSelector(design)

# AI selects best component
best_resistor = selector.select_component(
    requirements={
        "category": "passive.resistor",
        "resistance": 10000,
        "powerRatingMin": 0.1,
        "toleranceMax": 1.0
    },
    context={
        "net": "net_pullup",
        "connectedTo": "U1",
        "application": "pull_up_resistor"
    },
    optimize_for=["cost", "availability", "reliability"]
)

print(f"Selected: {best_resistor.mpn}")
print(f"Reasoning: {best_resistor.selection_reasoning}")

# ========================================
# NATURAL LANGUAGE INTERFACE
# ========================================

from openpcbdb.ai import NaturalLanguageInterface

nl = NaturalLanguageInterface(design)

# Ask questions about design
answer = nl.ask("What is the maximum current on the 5V power rail?")
print(answer)  # "The maximum current on VCC_5V is 0.5A"

answer = nl.ask("Why was a 10kΩ resistor chosen for R1?")
print(answer)  # "R1 is a pull-up resistor. 10kΩ balances..."

# Execute commands
nl.execute("Add a 100nF decoupling capacitor near U1 pin 8")
nl.execute("Increase trace width of VCC_5V to 1mm")

# Get design modifications
modifications = nl.modify("Optimize this design for lower cost")
for mod in modifications:
    print(f"Change: {mod.description}")
    print(f"Savings: ${mod.cost_savings}")
    print(f"Impact: {mod.impact_on_performance}")
```

#### 5.1.3 Machine Learning API

```python
from openpcbdb.ml import FeatureExtractor, DesignPredictor

# ========================================
# FEATURE EXTRACTION FOR ML
# ========================================

extractor = FeatureExtractor(design)

# Get graph representation (for GNNs)
graph = extractor.to_networkx_graph()
# Nodes: components, Edges: connections

# Get feature vectors
features = extractor.extract_features([
    "component_count",
    "net_complexity",
    "power_domain_structure",
    "signal_integrity_metrics",
    "layout_density",
    "cost_estimate"
])

# Export for ML frameworks
pytorch_data = extractor.to_pytorch()
tensorflow_data = extractor.to_tensorflow()

# ========================================
# DESIGN PREDICTION
# ========================================

predictor = DesignPredictor()

# Load pre-trained model
predictor.load_model("openpcbdb_design_quality_v1.pth")

# Predict design quality
quality_score = predictor.predict_quality(design)
print(f"Predicted quality score: {quality_score}")

# Predict potential failures
failures = predictor.predict_failures(design)
for failure in failures:
    print(f"Potential failure: {failure.type}")
    print(f"Probability: {failure.probability}")
    print(f"Location: {failure.component}")

# Predict manufacturing yield
yield_estimate = predictor.predict_yield(design)

# ========================================
# LEARNING FROM DESIGNS
# ========================================

from openpcbdb.ml import DesignLearner

learner = DesignLearner()

# Learn from design corpus
learner.train_on_designs(
    design_files=["design1.opcbdb", "design2.opcbdb"],
    labels={"quality": [0.9, 0.7], "cost": [12.5, 8.3]}
)

# Learn component usage patterns
patterns = learner.learn_component_patterns(
    designs=design_corpus,
    component_type="passive.capacitor"
)

# Generate design rules
rules = learner.extract_design_rules(design_corpus)
for rule in rules:
    print(f"Rule: {rule.description}")
    print(f"Confidence: {rule.confidence}")
    print(f"Examples: {rule.supporting_designs}")
```

### 5.2 REST API (for web/cloud)

```python
# GET /api/v1/designs/{design_id}
# Returns complete design in JSON

# POST /api/v1/designs/analyze
# Body: {design_id, analysis_type}
# Returns analysis results

# POST /api/v1/designs/generate
# Body: {requirements, constraints}
# Returns generated design

# GET /api/v1/designs/{design_id}/query
# Query parameters: ?type=component&category=resistor&value_min=10000
# Returns matching entities

# POST /api/v1/designs/{design_id}/modify
# Body: {modification_type, parameters}
# Returns modified design

# POST /api/v1/designs/{design_id}/validate
# Returns validation report
```

### 5.3 GraphQL API (for flexible queries)

```graphql
query GetDesign {
  design(id: "smart_led_driver") {
    name
    version
    components(category: "passive.resistor") {
      refDesignator
      value
      semantic {
        purpose
        critical
      }
    }
    nets(type: POWER) {
      name
      voltage {
        nominal
        min
        max
      }
      connections {
        component
        pin
      }
    }
  }
}

mutation ModifyDesign {
  addComponent(
    designId: "smart_led_driver"
    component: {
      refDesignator: "C10"
      componentDefId: "cap_0603_100nF"
      position: {x: 25.0, y: 40.0}
    }
  ) {
    success
    component {
      refDesignator
    }
  }
}
```

---

## 6. File Format

### 6.1 JSON Format (Primary)

**File Extension:** `.opcbdb` or `.opcbdb.json`

**Characteristics:**
- Human-readable
- Git-friendly (line-based diffing)
- Widely supported
- Easy to parse

**Structure:**

```json
{
  "opcbdbVersion": "1.0",
  "design": {
    "metadata": {},
    "components": [],
    "nets": [],
    "constraints": []
  }
}
```

### 6.2 Directory Structure for Large Projects

```
project_name/
├── project_name.opcbdb          # Main design file (references others)
├── library/
│   ├── components.json          # Component library
│   ├── custom_components.json
│   └── symbols.json
├── schematic/
│   ├── sheet_001_power.json
│   ├── sheet_002_control.json
│   └── hierarchy.json
├── blocks/
│   ├── power_supply.json
│   └── pwm_controller.json
├── constraints/
│   └── design_rules.json
├── pcb/
│   ├── stackup.json
│   ├── placement.json
│   └── routing.json
├── analysis/
│   ├── simulation_results.json
│   └── drc_reports.json
└── ai/
    ├── training_labels.json
    ├── design_history.json
    └── optimization_log.json
```

### 6.3 Compression and Storage Optimization

**The Challenge**: Full semantic information can create large files for medium/large designs.

**Example File Sizes (Uncompressed JSON with FULL semantic data):**
- Small design (50 components): ~50 MB
- Medium design (500 components): ~500 MB to 5 GB
- Large design (2000 components): ~2 GB to 20 GB

**Why so large?**
Each component with full semantic data: ~100 KB - 10 MB
- Full parameter specifications
- All semantic fields (purpose, reasoning, alternatives)
- AI annotations and learning data
- Design history and iterations
- Procurement and lifecycle data

**Solutions:**

#### 6.3.1 Compression (Recommended)

**Gzip Compression** (built-in, widely supported):

```python
import gzip
import json

# Save compressed
with gzip.open('design.opcbdb.gz', 'wt', encoding='utf-8') as f:
    json.dump(design, f)

# Load compressed
with gzip.open('design.opcbdb.gz', 'rt', encoding='utf-8') as f:
    design = json.load(f)
```

**Typical compression ratios:**
- Small design: 50 MB → 3-5 MB (10-15:1)
- Medium design: 5 GB → 250-500 MB (10-20:1)
- Large design: 20 GB → 1-2 GB (10-20:1)

**Note:** Semantic text compresses extremely well (high redundancy)

**Zstandard (Better compression, faster):**

```python
import zstandard as zstd
import json

# Save with zstd
with open('design.opcbdb.zst', 'wb') as f:
    cctx = zstd.ZstdCompressor(level=19)  # Max compression
    compressed = cctx.compress(json.dumps(design).encode('utf-8'))
    f.write(compressed)

# Typical compression: 20-30:1 ratio (much better than gzip)
# Medium design: 5 GB → 150-250 MB ✅
```

#### 6.3.2 Reference-Based Architecture

Instead of embedding everything, use references:

```json
{
  "type": "ComponentInstance",
  "refDesignator": "R1",
  "componentRef": "lib://standard/res_0603_10k_1pct",  // Reference, not embedded
  "semantic": {
    "purpose": "Pull-up resistor",
    "critical": false
  }
}
```

**Benefits:**
- Component library stored once, referenced many times
- **Reduces file size by 80-95%** for designs with repeated components
- Updates to component library automatically propagate

**Example:**
```
Without references: 
  500 components × 10 MB each = 5 GB ❌

With references:
  Component library: 50 MB (500 unique components)
  Component instances: 500 × 1 KB = 500 KB
  Total: ~50 MB (100x smaller!) ✅
```

#### 6.3.3 Minimal vs. Full Mode

**Minimal Mode** (for storage/transfer):
- Only essential data (connectivity, values, positions)
- Semantic fields optional
- No AI metadata
- No design history
- **~1-5% the size of full mode**

**Full Mode** (for AI processing):
- All semantic information
- AI annotations and learning data
- Design history and alternatives
- Full reasoning and explanations

```python
# Save in minimal mode (essential data only)
design.save("design.opcbdb", mode="minimal")  # 5 MB for 500 components

# Load and expand to full mode (AI infers/adds semantics)
design = Design.load("design.opcbdb", expand=True)  
# AI generates: purposes, reasoning, alternatives, patterns

# Save full mode
design.save("design_full.opcbdb", mode="full")  # 5 GB for 500 components
```

**This is KEY:** Most users work in minimal mode, AI expands to full when needed!

#### 6.3.4 Binary Format Option

**MessagePack** (binary JSON alternative):

```python
import msgpack

# 30-40% smaller than JSON, faster to parse
with open('design.opcbdb.msgpack', 'wb') as f:
    msgpack.pack(design, f)

# File sizes:
# Medium design: 50 MB JSON → 30 MB MessagePack → 2 MB compressed
# (Works best with minimal mode + compression)
```

#### 6.3.5 Streaming/Chunked Format

For very large designs, process in chunks:

```json
{
  "designMetadata": {...},
  "componentChunks": [
    "components_001.json",  // 100 components per file
    "components_002.json",
    "components_003.json"
  ],
  "netChunks": [
    "nets_001.json",
    "nets_002.json"
  ]
}
```

**Benefits:**
- Load only needed portions
- Parallel processing
- Reduced memory footprint

#### 6.3.6 Database Backend Option

For very large projects, use embedded database:

```python
# SQLite backend (still portable, single file)
import sqlite3

db = sqlite3.connect('design.opcbdb.sqlite')

# Query without loading entire design
cursor = db.execute("""
    SELECT * FROM components 
    WHERE category = 'passive.resistor' 
    AND resistance BETWEEN 9000 AND 11000
""")

# File size: Similar to compressed JSON
# Access speed: Much faster for queries
```

#### 6.3.7 Recommended Approach

**For most designs (BEST PRACTICE):**

```
1. Store in MINIMAL mode (essential data only)
2. Use reference-based architecture (library separate)
3. Compress with zstandard
4. AI expands to full mode only when analyzing

Result: Medium design (500 components)
  Full semantic mode:     5 GB          ❌ Too large
  Minimal mode:           5 MB          ⬇️
  + References:           3 MB          ⬇️
  + Zstd compression:     150 KB        ✅ PERFECT!
  
When AI needs full semantics:
  Decompress:             3 MB
  AI expands:             5 GB (in RAM only, not saved)
  AI analyzes and modifies
  Save back as minimal:   150 KB        ✅
```

**For large designs (>1000 components):**

```
1. Use SQLite backend or chunked files
2. Store only essential data
3. AI generates semantics on-demand (not stored)

Result: Large design (2000 components)
  SQLite minimal mode:    10 MB         ✅
  Query without loading entire design
  AI expands portions as needed
```

#### 6.3.8 File Size Comparison Table

**Full Semantic Mode (everything included):**

| Design Size | Components | Full JSON | + References | + Compression | Usable? |
|-------------|-----------|-----------|--------------|---------------|---------|
| Small | 50 | 50 MB | 10 MB | 500 KB | ⚠️ OK |
| Medium | 500 | 5 GB | 100 MB | 5 MB | ❌ Too big |
| Large | 2000 | 20 GB | 400 MB | 20 MB | ❌ Too big |

**Minimal Mode + AI On-Demand (RECOMMENDED):**

| Design Size | Components | Minimal JSON | + References | + Zstd | Final Size | AI Expands To |
|-------------|-----------|--------------|--------------|--------|------------|---------------|
| Small | 50 | 2 MB | 500 KB | 30:1 | **15 KB** ✅ | 50 MB (RAM) |
| Medium | 500 | 5 MB | 3 MB | 30:1 | **100 KB** ✅ | 5 GB (RAM) |
| Large | 2000 | 20 MB | 10 MB | 30:1 | **350 KB** ✅ | 20 GB (RAM) |
| Very Large | 5000 | 50 MB | 25 MB | 30:1 | **850 KB** ✅ | On-demand chunks |

**Key Insight:** 
- Store only essential data (minimal mode)
- AI generates semantic information in RAM when analyzing
- Never save the expanded full semantic data
- Result: **100-200 KB for typical PCB** instead of 5 GB! 🎯

### 6.4 Validation

```python
from openpcbdb.validation import Validator

validator = Validator()

# Validate against schema
result = validator.validate_schema(design)
if not result.valid:
    for error in result.errors:
        print(f"Schema error: {error}")

# Validate electrical rules
result = validator.validate_electrical(design)

# Validate semantic completeness
result = validator.validate_semantics(design)
if not result.complete:
    print(f"Missing semantic data: {result.missing_fields}")
```

---

## 7. AI/ML Integration

### 7.1 Training Data Format

OpenPCBDB designs can be directly used for training AI models.

**Dataset Structure:**

```json
{
  "datasetName": "PCB_Design_Corpus_v1",
  "version": "1.0",
  "designCount": 10000,
  "designs": [
    {
      "file": "design_0001.opcbdb",
      "labels": {
        "qualityScore": 0.92,
        "cost": 15.30,
        "complexity": "medium",
        "applicationDomain": "power_electronics",
        "failureRate": 0.001,
        "manufacturingYield": 0.98
      },
      "metadata": {
        "designerExperience": "expert",
        "designTimeHours": 120,
        "revisionCount": 5
      }
    }
  ]
}
```

### 7.2 Graph Neural Network Integration

```python
from openpcbdb.ml import GraphConverter

converter = GraphConverter()

# Convert to PyTorch Geometric format
pyg_data = converter.to_pytorch_geometric(design)

# Node features: component properties
# Edge features: connection properties
# Graph labels: design quality, cost, etc.

# Use with GNN
import torch
from torch_geometric.nn import GCNConv

class DesignGNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(in_channels=64, out_channels=128)
        self.conv2 = GCNConv(in_channels=128, out_channels=64)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return x

model = DesignGNN()
output = model(pyg_data)
```

### 7.3 Transformer/LLM Integration

```python
from openpcbdb.ml import LLMInterface

# Convert design to text representation for LLMs
llm_interface = LLMInterface(design)

# Generate text description
text = llm_interface.to_text()
# "This is a LED driver circuit with PWM control. 
#  It consists of a power supply block providing 5V,
#  a PWM controller based on..."

# Generate for specific LLM
openai_prompt = llm_interface.to_prompt(format="openai")
claude_prompt = llm_interface.to_prompt(format="claude")

# Parse LLM response back to design
response = """
Add a 100nF capacitor between pin 8 of U1 and ground.
Place it as close as possible to the IC.
"""
modifications = llm_interface.parse_llm_response(response)
design.apply_modifications(modifications)
```

### 7.4 Reinforcement Learning for Design Optimization

```python
from openpcbdb.ml.rl import DesignEnvironment
import gym

# Create RL environment
env = DesignEnvironment(
    initial_design=partial_design,
    goal_specs=requirements
)

# Actions: add component, modify parameter, connect nets, etc.
# Rewards: based on meeting requirements, cost, etc.

# Use with standard RL algorithms
state = env.reset()
done = False
while not done:
    action = agent.select_action(state)
    next_state, reward, done, info = env.step(action)
    agent.learn(state, action, reward, next_state)
    state = next_state

# Final design
final_design = env.get_design()
```

---

## 8. Reference Implementation

### 8.1 Python Library: `pyopenpcbdb`

**Installation:**
```bash
pip install pyopenpcbdb
```

**Basic Usage:**
```python
import openpcbdb

# Load design
design = openpcbdb.load("my_design.opcbdb")

# Query
resistors = design.query.components(category="passive.resistor")

# Analyze
analysis = design.analyze.power_integrity()

# Modify
design.add_component("R10", "resistor_10k")

# Save
design.save("modified_design.opcbdb")
```

### 8.2 Validation Tool

```bash
# Command-line validator
opcbdb-validate my_design.opcbdb

# Output:
# ✓ Schema valid
# ✓ Electrical rules passed
# ✗ Semantic completeness: 3 components missing 'purpose' field
# ✗ Power integrity: VCC_5V missing adequate decoupling
```

### 8.3 Conversion Tools

```bash
# Convert from KiCad
opcbdb-convert --from kicad --input project.kicad_pro --output project.opcbdb

# Convert from Altium
opcbdb-convert --from altium --input project.PrjPcb --output project.opcbdb

# Note: Conversion is lossy - semantic data must be added manually or by AI
```

---

## 9. Appendices

### 9.1 Complete Example: Simple LED Circuit

See `examples/led_blinker/` directory for complete working example.

### 9.2 JSON Schema Definitions

See `schemas/` directory for formal JSON Schema definitions.

### 9.3 Ontology and Taxonomy

**Component Categories:**
```
electronics
├── passive
│   ├── resistor
│   │   ├── fixed
│   │   ├── variable
│   │   └── network
│   ├── capacitor
│   │   ├── ceramic
│   │   ├── electrolytic
│   │   └── film
│   └── inductor
├── active
│   ├── ic
│   │   ├── microcontroller
│   │   ├── analog
│   │   └── digital
│   ├── discrete
│   │   ├── transistor
│   │   ├── diode
│   │   └── mosfet
└── electromechanical
    ├── connector
    ├── switch
    └── relay
```

**Module Categories:**

Modules represent physical separate PCB assemblies:

```
module
├── som (System-on-Module)
│   ├── arm_cortex_a
│   ├── arm_cortex_m
│   ├── x86_64
│   ├── risc_v
│   └── fpga
├── memory
│   ├── dimm
│   ├── so_dimm
│   ├── lpddr
│   └── ddr5
├── power
│   ├── dc_dc_module
│   ├── ac_dc_module
│   ├── poe_module
│   └── battery_module
├── wireless
│   ├── wifi_module
│   ├── bluetooth_module
│   ├── cellular_module
│   ├── lora_module
│   └── zigbee_module
├── sensor
│   ├── imu_module
│   ├── gps_module
│   ├── camera_module
│   └── environmental_sensor
├── display
│   ├── lcd_module
│   ├── oled_module
│   ├── e_paper_module
│   └── tft_module
├── interface
│   ├── usb_hub_module
│   ├── ethernet_phy_module
│   ├── can_transceiver_module
│   └── rs485_module
└── expansion
    ├── arduino_shield
    ├── raspberry_pi_hat
    ├── mikroelektronika_click
    └── pc104_module
```

**Net Types:**
- `power` - Power supply nets
- `ground` - Ground nets
- `signal` - General signals
- `clock` - Clock signals
- `differential` - Differential pairs
- `analog` - Analog signals
- `digital` - Digital signals
- `rf` - Radio frequency
- `high_voltage` - High voltage nets

### 9.4 Best Practices for AI-Friendly Designs

1. **Always include semantic fields**
2. **Document design intent**
3. **Capture alternatives considered**
4. **Include engineering reasoning**
5. **Use consistent naming conventions**
6. **Organize into functional blocks**
7. **Add validation constraints**
8. **Include procurement data**
9. **Track design history**
10. **Add AI training labels when available**

### 9.5 Glossary

- **Semantic Data**: Information about meaning and purpose, not just geometry
- **Design Intent**: The reasoning behind design decisions
- **Functional Block**: Group of components serving a specific function (logical grouping on same PCB)
- **Module**: Physical separate PCB assembly that integrates into parent design (e.g., SoM, DIMM, daughterboard)
- **Component Instance**: Specific occurrence of a component in a design
- **Net**: Electrical connection between component pins
- **Constraint**: Rule or requirement that design must satisfy
- **AI Agent**: Artificial intelligence system that can understand and create designs
- **Carrier Board**: Parent PCB that hosts one or more modules
- **System-on-Module (SoM)**: Complete computer system on a small PCB module

---

## 10. Complex Design Support: Motherboard Example

### 10.1 Motherboard Design Requirements

**Challenge**: Motherboards are among the most complex PCB designs:
- 2000-5000+ components
- 8-16 layer stackups
- High-speed interfaces (PCIe Gen4/5, DDR4/5, USB 3.x/4)
- Complex power delivery (multiple voltage rails, VRMs)
- Strict signal integrity requirements
- EMI/EMC compliance
- Thermal management

**Is OpenPCBDB Ready?** Let's analyze...

### 10.2 Gap Analysis for Motherboard Design

#### ✅ Currently Supported:

1. **Component Library** - Adequate
   - Can represent all component types
   - Parametric search works

2. **Basic Connectivity** - Adequate
   - Net topology representation works
   - Component instances supported

3. **Semantic Information** - Good
   - Design intent capture
   - AI reasoning support

#### ❌ Missing / Needs Enhancement:

1. **High-Speed Signal Integrity**
2. **Complex Power Delivery Networks**
3. **Multi-Layer Stackup Management**
4. **Signal Grouping (Buses, Diff Pairs)**
5. **Timing Constraints**
6. **EMI/EMC Rules**

### 10.3 Extended Data Models for Motherboard Design

#### 10.3.1 High-Speed Differential Pair

**Current Limitation**: Basic net model doesn't capture differential pair relationships.

**Enhancement Needed:**

```json
{
  "type": "DifferentialPair",
  "id": "diff_pcie_lane0",
  "name": "PCIE_TX0",
  
  "nets": {
    "positive": "net_pcie_tx0_p",
    "negative": "net_pcie_tx0_n"
  },
  
  "signalIntegrity": {
    "protocol": "PCIe_Gen4",
    "dataRate": {"value": 16, "unit": "Gbps"},
    "targetImpedance": {
      "differential": {"value": 100, "tolerance": 10, "unit": "ohm"},
      "singleEnded": {"value": 50, "tolerance": 5, "unit": "ohm"}
    },
    "maxSkew": {"value": 5, "unit": "ps"},
    "maxLengthMismatch": {"value": 5, "unit": "mil"},
    "maxTotalLength": {"value": 6, "unit": "inch"}
  },
  
  "routingConstraints": {
    "layerConstraints": ["L3", "L4"],  // Only route on these layers
    "referencePlanes": ["GND", "GND"],  // Required reference planes
    "viaCountMax": 2,
    "matchedViaPlacement": true,
    "minimumSpacing": {"value": 5, "unit": "mil"},
    "couplingLengthMax": {"value": 500, "unit": "mil"}
  },
  
  "termination": {
    "source": {
      "type": "AC_coupled",
      "capacitor": {"value": 100, "unit": "nF"},
      "terminationResistor": {"value": 50, "unit": "ohm"}
    },
    "destination": {
      "type": "DC_coupled",
      "pullupResistors": true
    }
  },
  
  "semantic": {
    "purpose": "PCIe Gen4 x16 slot, lane 0 transmit path",
    "critical": true,
    "signalClass": "high_speed_serial",
    "topology": "point_to_point",
    "eyeDiagramRequirements": {
      "minEyeHeight": {"value": 70, "unit": "mV"},
      "minEyeWidth": {"value": 0.6, "unit": "UI"}
    }
  },
  
  "aiGuidance": {
    "routingStrategy": "Route as tightly coupled pair, maintain constant spacing",
    "commonIssues": [
      "Via stubs causing reflections",
      "Length mismatch > 5 mil",
      "Reference plane discontinuities",
      "Crosstalk from adjacent lanes"
    ],
    "bestPractices": [
      "Use back-drilling for via stubs",
      "Route on stripline layers for better impedance control",
      "Maintain 3W spacing from other differential pairs",
      "Add ground stitching vias near pair routing"
    ]
  }
}
```

#### 10.3.2 Complex Multi-Layer Stackup

**Current Limitation**: Example shows only 2 layers.

**Enhancement Needed:**

```json
{
  "type": "PCBStackup",
  "designId": "ATX_Motherboard_v2",
  "layerCount": 12,
  "finishedThickness": 1.6,
  "unit": "mm",
  
  "layers": [
    {
      "number": 1,
      "name": "Top",
      "type": "signal",
      "copperWeight": 1.0,
      "copperThickness": 35,
      "unit": "um",
      "signalTypes": ["low_speed_digital", "analog"],
      "impedanceControl": false
    },
    {
      "number": 2,
      "name": "GND1",
      "type": "plane",
      "copperWeight": 2.0,
      "copperThickness": 70,
      "net": "GND",
      "planeType": "solid",
      "purpose": "Primary ground plane, reference for Top layer"
    },
    {
      "number": 3,
      "name": "Signal1",
      "type": "signal",
      "copperWeight": 0.5,
      "copperThickness": 18,
      "signalTypes": ["high_speed_differential", "pcie", "usb"],
      "impedanceControl": true,
      "targetImpedance": {
        "stripline": true,
        "differential": 100,
        "singleEnded": 50
      },
      "referencePlanes": {
        "above": "GND1",
        "below": "PWR1"
      }
    },
    {
      "number": 4,
      "name": "PWR1",
      "type": "plane",
      "copperWeight": 2.0,
      "copperThickness": 70,
      "nets": ["VCC_12V", "VCC_5V", "VCC_3.3V"],  // Split power plane
      "planeType": "split",
      "purpose": "Primary power distribution"
    },
    {
      "number": 5,
      "name": "Signal2",
      "type": "signal",
      "copperWeight": 0.5,
      "signalTypes": ["ddr5", "memory_bus"],
      "impedanceControl": true,
      "topology": "t_branch",  // For memory busses
      "lengthMatchingRequired": true
    },
    {
      "number": 6,
      "name": "GND2",
      "type": "plane",
      "net": "GND",
      "planeType": "solid"
    },
    // Mirrored structure for layers 7-12
  ],
  
  "dielectrics": [
    {
      "betweenLayers": [1, 2],
      "material": "RO4350B",  // Low-loss material for high-speed
      "thickness": 100,
      "unit": "um",
      "dielectricConstant": 3.48,
      "lossTangent": 0.0037,
      "purpose": "Controlled impedance for top layer high-speed signals"
    },
    {
      "betweenLayers": [2, 3],
      "material": "FR4",
      "thickness": 200,
      "dielectricConstant": 4.5,
      "lossTangent": 0.02
    }
    // ... more dielectric layers
  ],
  
  "semantic": {
    "stackupStrategy": "Stripline for high-speed signals, split power planes for isolation",
    "signalGrouping": {
      "layers_1_2_11_12": "Low speed signals and power",
      "layers_3_4_9_10": "High-speed differential (PCIe, USB, SATA)",
      "layers_5_6_7_8": "Memory interfaces (DDR5) with tight impedance control"
    },
    "criticalConsiderations": [
      "PCIe Gen4 requires low-loss dielectric (RO4350B)",
      "DDR5 requires tight impedance tolerance (±10%)",
      "Split power planes need careful stitching capacitor placement"
    ]
  }
}
```

#### 10.3.3 Power Delivery Network (PDN)

**Current Limitation**: Basic power net model insufficient for VRM-based PDN.

**Enhancement Needed:**

```json
{
  "type": "PowerDeliveryNetwork",
  "id": "pdn_cpu_vcore",
  "name": "CPU Core Voltage Rail",
  
  "source": {
    "type": "multiphase_vrm",
    "component": "U5",  // VRM controller
    "phases": 8,
    "phaseComponents": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"],
    "outputCapacitors": [
      {"ref": "C10", "value": 470, "unit": "uF", "type": "polymer"},
      {"ref": "C11", "value": 470, "unit": "uF", "type": "polymer"},
      {"ref": "C12", "value": 100, "unit": "uF", "type": "ceramic"},
      {"ref": "C13", "value": 22, "unit": "uF", "type": "ceramic"}
      // ... many more
    ],
    "totalOutputCapacitance": {"value": 2000, "unit": "uF"}
  },
  
  "distributionNetwork": {
    "planeLayers": ["L4", "L6"],
    "planeArea": {"value": 120, "unit": "cm2"},
    "traceWidths": {
      "primary": {"min": 100, "unit": "mil"},
      "secondary": {"min": 50, "unit": "mil"}
    },
    "viaStitching": {
      "required": true,
      "maxSpacing": {"value": 1000, "unit": "mil"},
      "viaType": "0.3mm_drill"
    }
  },
  
  "load": {
    "component": "U1",  // CPU
    "pins": ["VCORE_1", "VCORE_2", /* ... many pins */],
    "totalPins": 150,
    "decouplingStrategy": {
      "bulkCaps": [
        {"value": 220, "unit": "uF", "quantity": 4, "placement": "within_2cm"}
      ],
      "highFreqCaps": [
        {"value": 22, "unit": "uF", "quantity": 10, "placement": "within_5mm"},
        {"value": 10, "unit": "uF", "quantity": 20, "placement": "within_2mm"},
        {"value": 1, "unit": "uF", "quantity": 30, "placement": "at_pin"}
      ]
    }
  },
  
  "electricalSpecifications": {
    "voltage": {
      "nominal": 1.2,
      "min": 1.14,
      "max": 1.26,
      "unit": "V",
      "tolerance": 5,  // percent
      "loadRegulation": 2  // percent
    },
    "current": {
      "idle": {"value": 10, "unit": "A"},
      "typical": {"value": 80, "unit": "A"},
      "max": {"value": 150, "unit": "A"},
      "transientSlewRate": {"value": 100, "unit": "A/us"}
    },
    "impedanceTarget": {
      "dcResistance": {"max": 0.001, "unit": "ohm"},
      "impedance_at_1MHz": {"max": 0.002, "unit": "ohm"},
      "impedance_at_10MHz": {"max": 0.005, "unit": "ohm"}
    },
    "noiseBudget": {
      "rippleMax": {"value": 20, "unit": "mV_pp"},
      "transientOvershoot": {"value": 50, "unit": "mV"}
    }
  },
  
  "analysisRequirements": {
    "pdnImpedanceAnalysis": {
      "frequencyRange": {"min": 1, "max": 100, "unit": "MHz"},
      "targetImpedance": {"max": 0.01, "unit": "ohm"},
      "method": "VNA_measurement_or_simulation"
    },
    "irDropAnalysis": {
      "maxAllowed": {"value": 20, "unit": "mV"},
      "worstCaseCurrent": {"value": 150, "unit": "A"}
    },
    "decouplingEffectiveness": {
      "selfResonanceDistribution": "Spread across 100kHz - 10MHz",
      "impedanceProfile": "Must meet target across full frequency range"
    }
  },
  
  "semantic": {
    "purpose": "High-current, low-voltage power delivery for CPU core",
    "critical": true,
    "complexity": "very_high",
    "designChallenges": [
      "Very high transient current (100A/us)",
      "Extremely tight voltage tolerance (±5%)",
      "Low impedance across wide frequency range",
      "Thermal management of VRM phases"
    ],
    "aiGuidance": {
      "decouplingStrategy": "Use capacitor pyramid: bulk (220uF) → mid (22uF/10uF) → high-freq (1uF)",
      "layoutStrategy": "Star topology from VRM to CPU, minimize loop inductance",
      "commonFailures": [
        "Insufficient decoupling causing voltage droop",
        "Poor via stitching causing current crowding",
        "Inadequate plane area increasing DC resistance"
      ],
      "verificationMethods": [
        "PDN impedance simulation (target < 10mΩ)",
        "IR drop analysis (< 20mV)",
        "Transient simulation (load step response)"
      ]
    }
  }
}
```

#### 10.3.4 Memory Interface (DDR5)

```json
{
  "type": "MemoryInterface",
  "id": "ddr5_channel_a",
  "protocol": "DDR5",
  
  "topology": {
    "type": "fly_by",
    "controller": "U1",  // CPU or memory controller
    "dimmSlots": ["DIMM_A1", "DIMM_A2"],
    "ranksPerDimm": 2
  },
  
  "signalGroups": {
    "addressCommand": {
      "signals": ["A0", "A1", /* ... */ "A16", "BA0", "BA1", "RAS", "CAS", "WE"],
      "topology": "multi_drop",
      "maxLength": {"value": 4, "unit": "inch"},
      "stubLengthMax": {"value": 300, "unit": "mil"},
      "termination": "on_die"
    },
    "dataStrobes": {
      "signals": ["DQS0_P", "DQS0_N", /* ... */ "DQS7_P", "DQS7_N"],
      "type": "differential_pair",
      "topology": "point_to_point",
      "impedance": {"value": 100, "tolerance": 10, "unit": "ohm"},
      "lengthMatching": {"tolerance": 10, "unit": "mil"}
    },
    "data": {
      "signals": ["DQ0", "DQ1", /* ... */ "DQ63"],
      "topology": "point_to_point_per_byte",
      "impedance": {"value": 40, "unit": "ohm"},
      "lengthMatchingWithinByte": {"tolerance": 20, "unit": "mil"},
      "lengthMatchingAcrossBytes": {"tolerance": 500, "unit": "mil"}
    }
  },
  
  "timingConstraints": {
    "clockFrequency": {"value": 4800, "unit": "MHz"},
    "tCK": {"value": 208, "unit": "ps"},
    "setupTime": {"value": 50, "unit": "ps"},
    "holdTime": {"value": 50, "unit": "ps"},
    "flightTimeTolerance": {"value": 100, "unit": "ps"}
  },
  
  "signalIntegrity": {
    "eyeDiagramRequirements": {
      "minEyeHeight": {"value": 150, "unit": "mV"},
      "minEyeWidth": {"value": 0.4, "unit": "UI"}
    },
    "crosstalkMax": {"value": 50, "unit": "mV"},
    "isiMax": {"value": 30, "unit": "mV"}
  },
  
  "semantic": {
    "purpose": "DDR5-4800 memory interface, Channel A",
    "critical": true,
    "complexity": "extreme",
    "aiGuidance": {
      "layoutStrategy": [
        "Route address/command as serpentine to match longest path",
        "Match DQS strobes within ±10mil",
        "Match DQ within byte group to ±20mil",
        "Keep data signals away from clock and address/command",
        "Use ground guards between byte groups"
      ],
      "simulationRequired": [
        "IBIS simulation for signal integrity",
        "Timing analysis for setup/hold",
        "Eye diagram analysis",
        "Crosstalk analysis between adjacent signals"
      ]
    }
  }
}
```

#### 10.3.5 Module Usage in Motherboard Design

**Purpose**: Demonstrate how modules are integrated into complex motherboard designs.

Motherboards commonly use multiple module types:
- System-on-Module (SoM) for main processor
- DIMM/SO-DIMM for memory
- M.2 modules for WiFi, storage
- Mini-PCIe for wireless cards
- Power modules for voltage regulation

**Example: Industrial Motherboard with SoM**

```json
{
  "design": {
    "metadata": {
      "name": "Industrial Motherboard with i.MX8 SoM",
      "description": "Carrier board design for System-on-Module with expansion interfaces"
    },
    
    "components": [
      {
        "instanceId": "MOD_CPU",
        "definitionId": "module_som_imx8",
        "definitionType": "module",
        "definition": {
          "$ref": "library/modules/som_imx8.json"
        },
        "placement": {
          "x": 75,
          "y": 60,
          "rotation": 0,
          "layer": "top"
        },
        "semantic": {
          "purpose": "Main computing module with processor, RAM, and storage",
          "reasoning": "SoM approach reduces carrier board complexity and development time",
          "critical": true
        }
      },
      {
        "instanceId": "MOD_WIFI",
        "definitionId": "module_m2_wifi",
        "definitionType": "module",
        "definition": {
          "manufacturer": "Intel",
          "partNumber": "AX200.NGWG.DTK",
          "category": "module.wireless.wifi_module",
          "interface": {
            "connectorType": "M.2_E_key",
            "interfaces": ["PCIe_Gen3_x1", "USB_2.0", "UART"]
          }
        },
        "placement": {
          "x": 120,
          "y": 40,
          "rotation": 0,
          "layer": "top"
        },
        "semantic": {
          "purpose": "WiFi 6 and Bluetooth 5.2 wireless connectivity",
          "reasoning": "M.2 module allows easy upgrade and certification reuse"
        }
      },
      {
        "instanceId": "MOD_DIMM1",
        "definitionId": "module_so_dimm_ddr4",
        "definitionType": "module",
        "definition": {
          "category": "module.memory.so_dimm",
          "interface": {
            "connectorType": "SO-DIMM_260pin",
            "type": "DDR4"
          },
          "configuration": {
            "capacity": "variable",  // User-installable
            "speed": ["2400", "2666", "3200"]
          }
        },
        "placement": {
          "x": 150,
          "y": 80,
          "rotation": 0,
          "layer": "top"
        },
        "semantic": {
          "purpose": "Expandable system memory slot",
          "reasoning": "SO-DIMM allows user to configure memory capacity (4GB to 32GB)"
        }
      },
      {
        "instanceId": "MOD_POWER_5V",
        "definitionId": "module_dc_dc_12v_5v",
        "definitionType": "module",
        "definition": {
          "category": "module.power.dc_dc_module",
          "interface": {
            "inputVoltage": {"min": 9, "max": 36, "nominal": 12, "unit": "V"},
            "outputVoltage": {"value": 5.0, "unit": "V"},
            "outputCurrent": {"max": 10, "unit": "A"}
          }
        },
        "placement": {
          "x": 30,
          "y": 80,
          "rotation": 0,
          "layer": "top"
        },
        "semantic": {
          "purpose": "Main 5V power rail generation from 12V input",
          "reasoning": "Isolated module reduces EMI and simplifies power design"
        }
      }
    ],
    
    "nets": [
      {
        "id": "net_pcie_to_wifi",
        "name": "PCIE_TO_WIFI",
        "type": "high_speed_differential",
        "connections": [
          {"component": "MOD_CPU", "pin": "PCIE1_TX_P"},
          {"component": "MOD_CPU", "pin": "PCIE1_TX_N"},
          {"component": "MOD_WIFI", "pin": "PCIE_RX_P"},
          {"component": "MOD_WIFI", "pin": "PCIE_RX_N"}
        ],
        "constraints": {
          "impedance": {"value": 100, "unit": "ohm", "type": "differential"},
          "lengthMatch": {"max": 5, "unit": "mil"},
          "routing": "Controlled impedance, avoid vias if possible"
        },
        "semantic": {
          "purpose": "PCIe Gen3 x1 connection from SoM to WiFi module",
          "critical": true
        }
      },
      {
        "id": "net_5v_main",
        "name": "5V_MAIN",
        "type": "power",
        "connections": [
          {"component": "MOD_POWER_5V", "pin": "VOUT"},
          {"component": "MOD_CPU", "pin": "VIN_5V"},
          {"component": "U_USB_HUB", "pin": "VDD"},
          {"component": "J_USB_PORTS", "pin": "VBUS"}
        ],
        "constraints": {
          "minWidth": {"value": 1.0, "unit": "mm"},
          "maxCurrent": {"value": 8.0, "unit": "A"},
          "maxVoltageDrop": {"value": 100, "unit": "mV"}
        },
        "semantic": {
          "purpose": "Main 5V power distribution",
          "critical": true
        }
      }
    ],
    
    "functionalBlocks": [
      {
        "id": "block_compute",
        "name": "Compute Module",
        "components": ["MOD_CPU", "MOD_DIMM1"],
        "purpose": "Main processing with expandable memory"
      },
      {
        "id": "block_connectivity",
        "name": "Wireless Connectivity",
        "components": ["MOD_WIFI", "U_ANTENNA_SWITCH"],
        "purpose": "WiFi and Bluetooth connectivity"
      },
      {
        "id": "block_power",
        "name": "Power Supply",
        "components": ["MOD_POWER_5V", "U_LDO_3V3", "C1-C20"],
        "purpose": "Power generation and distribution"
      }
    ],
    
    "designGuidelines": {
      "moduleIntegration": [
        "SoM connector requires solid ground plane on carrier board",
        "Place 100nF decoupling caps at each power pin on carrier side",
        "High-speed signals (PCIe, USB 3.0) must use controlled impedance routing",
        "M.2 WiFi module requires antenna keepout zone",
        "SO-DIMM socket requires matched length DDR4 routing from CPU",
        "Power module input needs bulk capacitance (470uF minimum)",
        "Allow proper thermal clearance around all modules"
      ],
      "aiNotes": "Module-based design reduces carrier board complexity by 60%. Main processor routing (DDR4, eMMC) is contained in SoM. Carrier board only routes lower-speed interfaces."
    }
  }
}
```

**Module Integration Benefits:**

1. **Reduced Complexity**: SoM contains complex DDR4 routing and power sequencing
2. **Faster Development**: Carrier board design time reduced from 12 months to 3-4 months
3. **Modularity**: Easy to swap compute module for different performance tiers
4. **Certification Reuse**: Pre-certified modules simplify EMC compliance
5. **Risk Reduction**: Proven module design reduces technical risk
6. **Flexibility**: User-installable memory and WiFi modules

**Example: Server Motherboard with Multiple Module Types**

```json
{
  "design": {
    "metadata": {
      "name": "Server Motherboard ATX",
      "description": "2-socket server motherboard with modular components"
    },
    "components": [
      {
        "instanceId": "CPU1_VRM",
        "definitionType": "module",
        "definition": {
          "category": "module.power.vrm_module",
          "phases": 12,
          "outputVoltage": {"min": 0.8, "max": 1.5, "unit": "V"},
          "outputCurrent": {"max": 200, "unit": "A"}
        },
        "semantic": {
          "purpose": "12-phase VRM for CPU1 power delivery",
          "reasoning": "Modular VRM allows thermal and electrical optimization"
        }
      },
      {
        "instanceId": "DIMM_A1",
        "definitionType": "module",
        "definition": {
          "category": "module.memory.dimm",
          "type": "DDR5_RDIMM"
        },
        "semantic": {
          "purpose": "DDR5 RDIMM slot for channel A, rank 0",
          "instanceSpecific": "User-installable, supports 16GB to 128GB"
        }
      },
      {
        "instanceId": "DIMM_A2",
        "definitionType": "module",
        "definition": {"$ref": "#/components/DIMM_A1/definition"}
      },
      {
        "instanceId": "NIC_MEZZ",
        "definitionType": "module",
        "definition": {
          "category": "module.interface.ocp_mezzanine",
          "interfaces": ["PCIe_Gen4_x16"],
          "ports": ["2x25GbE", "2x10GbE"]
        },
        "semantic": {
          "purpose": "OCP 3.0 mezzanine network card",
          "reasoning": "Mezzanine form factor saves PCIe slots and reduces latency"
        }
      },
      {
        "instanceId": "M2_NVME_1",
        "definitionType": "module",
        "definition": {
          "category": "module.storage.m2_nvme",
          "formFactor": "M.2_2280",
          "interface": "PCIe_Gen4_x4"
        },
        "semantic": {
          "purpose": "NVMe SSD boot drive slot"
        }
      }
    ]
  }
}
```

**Key Considerations for Module Integration:**

1. **Interface Specification**: Define clear electrical and mechanical interfaces
2. **Power Requirements**: Account for module inrush current and peak power
3. **Thermal Management**: Ensure adequate cooling for high-power modules
4. **Signal Integrity**: Maintain impedance through connector transitions
5. **Mechanical Constraints**: Keepout zones, mounting holes, connector alignment
6. **Configuration Management**: Track module versions and configurations
7. **Abstraction Levels**: AI can work with modules as black boxes or dive into internal design

**AI Reasoning with Modules:**

```python
# AI can reason about module selection
def select_compute_module(requirements):
    candidates = query_modules(category="module.som")
    
    for module in candidates:
        # Check if module meets requirements
        if module.processor.cores >= requirements.min_cores:
            if module.memory.ram >= requirements.min_memory:
                if module.thermal.ambient_temp_max >= requirements.operating_temp:
                    if module.functionalCapabilities.interfaces.contains(requirements.needed_interfaces):
                        return module
    
    return None

# AI understands abstraction
selected_som = select_compute_module({
    "min_cores": 4,
    "min_memory": 2,  # GB
    "operating_temp": 85,  # °C
    "needed_interfaces": ["ethernet", "usb_3.0", "can"]
})

# AI can optimize carrier board knowing SoM handles DDR routing
carrier_complexity = calculate_complexity(
    exclude_internal_to_modules=True
)
# Result: 70% reduction in carrier board routing complexity
```

### 10.4 Motherboard Design Best Practices for AI

When AI designs or analyzes motherboard-level complexity:

**1. Hierarchical Decomposition**
```
Motherboard
├── Power Subsystem
│   ├── 12V Input
│   ├── CPU VRM (multi-phase)
│   ├── Memory VRM
│   └── I/O VRM
├── CPU Complex
│   ├── Socket
│   ├── VRM
│   └── Decoupling network
├── Memory Subsystem (per channel)
│   ├── DIMM slots
│   ├── Routing topology
│   └── Termination
├── High-Speed I/O
│   ├── PCIe slots (x16, x4, x1)
│   ├── M.2 slots
│   ├── SATA ports
│   └── USB ports
└── Support Logic
    ├── Chipset
    ├── Audio codec
    ├── Network PHY
    └── Super I/O
```

**2. Critical Verification Checks for AI**
- PDN impedance < 10mΩ across load spectrum
- High-speed eye diagrams meet spec
- DDR timing margins > 100ps
- Thermal simulation (hotspots < 85°C)
- EMI compliance (pre-scan simulation)

**3. AI-Guided Design Flow**
```
1. AI generates initial floorplan
2. AI places critical components (CPU, memory, VRM)
3. AI routes high-speed interfaces first
4. AI optimizes power delivery network
5. AI performs SI/PI/Thermal analysis
6. AI iterates based on analysis results
7. Human reviews and approves
```

### 10.5 Recommendations for v1.0

**Include Now:**
- ✅ Enhanced differential pair model (10.3.1)
- ✅ Basic high-speed signal group support
- ✅ Multi-layer stackup with impedance control

**Defer to v1.1:**
- ⏳ Complete PDN analysis framework (10.3.3)
- ⏳ Memory interface timing constraints (10.3.4)
- ⏳ Advanced SI/PI simulation integration

**Defer to v2.0:**
- ⏳ Full motherboard reference design
- ⏳ Thermal simulation integration
- ⏳ EMI/EMC rule checking

---

## 11. Future Extensions (v2.0+)

- Multi-board systems
- Flexible/rigid-flex PCB support
- Advanced 3D mechanical integration
- Real-time collaboration protocols
- Complete SI/PI/Thermal/EMI co-simulation
- Quantum computing readiness

---

**Document Version:** 1.0 Draft  
**Last Updated:** 2025-01-11  
**Status:** Open for Community Review  

**Contributing:** See CONTRIBUTING.md  
**License:** CC BY 4.0 (documentation), Apache 2.0 (code)  
**Repository:** https://github.com/openpcbdb/specification

---

**END OF SPECIFICATION v1.0**
