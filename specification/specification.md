# OpenPCBDB Specification v1.0
## Open PCB Design Database Standard
---

**Status:** Draft  
**Version:** 1.3.0  
**Date:** 2025-11-11  
**Authors:** Manuk Shemsyan
**Company:** Mintaka LLC, Armenia, www.mintaka-ai.com  
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
      - 4.2.2 [ComponentInstance](#422-componentinstance)
      - 4.2.3 [Net](#423-net)
      - 4.2.4 [FunctionalBlock](#424-functionalblock)
      - 4.2.5 [Module](#425-module)
      - 4.2.6 [NetClass](#426-netclass)
   - 4.3 [Constraint Model](#43-constraint-model)
   - 4.4 [User Library Integration](#44-user-library-integration)
      - 4.4.1 [Library Configuration](#441-library-configuration)
      - 4.4.2 [SQL Database Schema](#442-sql-database-library-schema)
      - 4.4.3 [SQLite Schema](#443-sqlite-library-schema)
      - 4.4.4 [REST API Interface](#444-rest-api-library-interface)
      - 4.4.5 [Component Instance with Library References](#445-component-instance-with-library-references)
      - 4.4.6 [Library Synchronization](#446-library-synchronization)
      - 4.4.7 [Query Examples](#447-query-examples)
      - 4.4.8 [Library Best Practices](#448-library-best-practices)
   - 4.5 [Physical Routing Model](#45-physical-routing-model) 
      - 4.5.1 [Trace Geometry](#451-trace-geometry)
      - 4.5.2 [Via Definitions](#452-via-definitions)
      - 4.5.3 [Copper Polygons](#453-copper-polygons)
   - 4.6 [Manufacturing Layers](#46-manufacturing-layers) 
      - 4.6.1 [Pad Geometries](#461-pad-geometries)
      - 4.6.2 [Silkscreen Graphics](#462-silkscreen-graphics)
      - 4.6.3 [Solder Mask](#463-solder-mask)
      - 4.6.4 [Solder Paste](#464-solder-paste)
   - 4.7 [Manufacturing Data](#47-manufacturing-data) 
      - 4.7.1 [Gerber Files](#471-gerber-files)
      - 4.7.2 [Drill Files](#472-drill-files)
      - 4.7.3 [Assembly Data](#473-assembly-data)
   - 4.8 [3D Mechanical Integration](#48-3d-mechanical-integration) 
      - 4.8.1 [Component Models](#481-component-models)
      - 4.8.2 [Keepout Zones](#482-keepout-zones)
   - 4.9 [Design Rule Checking](#49-design-rule-checking)
      - 4.9.1 [Rule Definitions](#491-rule-definitions)
      - 4.9.2 [Violation Reporting](#492-violation-reporting)
   - 4.10 [Electrical Rule Checking](#410-electrical-rule-checking) 
      - 4.10.1 [Pin Compatibility Rules](#4101-pin-compatibility-rules)
      - 4.10.2 [Power and Ground Validation](#4102-power-and-ground-validation)
      - 4.10.3 [ERC Violation Reporting](#4103-erc-violation-reporting)
5. [API Specification](#6-api-specification)
6. [File Format](#7-file-format)
   - 6.1 [JSON Format](#71-json-format-primary)
   - 6.2 [Directory Structure for Large Projects](#72-directory-structure-for-large-projects)
   - 6.3 [Compression and Storage Optimization](#73-compression-and-storage-optimization)
7. [AI/ML Integration](#8-aiml-integration)
8. [Reference Implementation](#9-reference-implementation)
9. [Appendices](#10-appendices)
10. [Complex Design Support: Motherboard Example](#11-complex-design-support-motherboard-example)
    - 10.1 [Motherboard Design Requirements](#111-motherboard-design-requirements)
    - 10.2 [Gap Analysis](#112-gap-analysis-for-motherboard-design)
    - 10.3 [Extended Data Models](#113-extended-data-models-for-motherboard-design)
    - 10.4 [Best Practices for AI](#114-motherboard-design-best-practices-for-ai)
    - 10.5 [Recommendations for v1.0](#115-recommendations-for-v10)
11. [Future Extensions](#12-future-extensions-v20)

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

Component instances represent actual component placements in the design with references to both OpenPCBDB definitions and external user libraries.

```json
{
  "type": "ComponentInstance",
  "id": "R1",
  "refDesignator": "R1",
  "componentDefinitionId": "res_0603_10k_1pct",
  
  // Part identification for procurement
  "partNumber": {
    "manufacturer": "Yageo",
    "manufacturerID": "MFR_YAGEO_001",
    "mpn": "RC0603FR-0710KL",
    "variant": "standard",
    "revision": "A"
  },
  
  // User library references
  "userLibraryReferences": {
    "primary": {
      "libraryID": "company_approved_parts",
      "libraryType": "sql",  // "sql", "sqlite", "json", "rest_api"
      "componentID": "COMP_RES_0603_10K_001",
      "lastVerified": "2025-01-10",
      "approvalStatus": "qualified"
    },
    "symbol": {
      "libraryID": "company_schematic_symbols",
      "symbolID": "SYM_RESISTOR_0603",
      "symbolReference": "resistor_2terminal"
    },
    "footprint": {
      "libraryID": "company_pcb_footprints",
      "footprintID": "FP_R_0603_1608Metric",
      "footprintReference": "RES_0603_STD"
    },
    "mechanical": {
      "libraryID": "company_3d_models",
      "modelID": "MECH_R_0603_STD",
      "mechanicalReference": "resistor_0603.step",
      "format": "STEP"
    }
  },
  
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

#### 4.2.6 NetClass

**Purpose**: NetClass entities define reusable sets of routing rules and electrical characteristics for groups of nets. This allows AI to efficiently manage and understand nets with similar requirements (e.g., all power nets, all high-speed signals).

**Key Differences from Constraints:**
- **NetClass**: Defines a template of routing rules that can be applied to multiple nets
- **Constraint**: Defines specific validation rules for design verification

**Use Cases:**
- Power distribution nets (wide traces, low impedance)
- High-speed differential pairs (controlled impedance, matched length)
- Low-speed digital signals (default routing)
- Analog signals (shielding, separation from digital)
- Clock distribution (specific impedance, length matching)

**Full Schema:**

```json
{
  "type": "NetClass",
  "id": "netclass_power_5v",
  "name": "Power_5V",
  "version": "1.0",
  
  "description": "Routing rules for 5V power distribution nets",
  
  "routingRules": {
    "traceWidth": {
      "min": 0.5,
      "typical": 1.0,
      "max": 2.0,
      "unit": "mm",
      "reasoning": "Based on 500mA max current and 10°C temperature rise"
    },
    "clearance": {
      "min": 0.2,
      "typical": 0.3,
      "unit": "mm"
    },
    "viaDiameter": {
      "min": 0.4,
      "typical": 0.6,
      "unit": "mm"
    },
    "viaDrillDiameter": {
      "min": 0.2,
      "typical": 0.3,
      "unit": "mm"
    },
    "viaCount": {
      "min": 2,
      "reasoning": "Redundancy for reliability"
    },
    "differentialPair": {
      "enabled": false
    }
  },
  
  "electricalRules": {
    "maxCurrent": {
      "value": 0.5,
      "unit": "A"
    },
    "maxVoltage": {
      "value": 5.5,
      "unit": "V"
    },
    "impedance": {
      "controlled": false
    }
  },
  
  "layerPreferences": {
    "preferred": ["top", "bottom"],
    "avoided": ["inner1", "inner2"],
    "allowPlane": false,
    "allowPolygonPour": true
  },
  
  "semantic": {
    "purpose": "Power distribution nets requiring wide traces",
    "domain": "power",
    "critical": true,
    "typicalNets": ["VCC", "VDD", "5V", "3V3"],
    "aiNotes": "Always verify current capacity calculations. Consider voltage drop over trace length."
  },
  
  "metadata": {
    "created": "2025-01-11T10:00:00Z",
    "author": "design_team",
    "usageCount": 127
  }
}
```

**High-Speed Differential Pair NetClass Example:**

```json
{
  "type": "NetClass",
  "id": "netclass_usb_diff",
  "name": "USB_Differential",
  
  "description": "USB 2.0 differential pair routing rules",
  
  "routingRules": {
    "traceWidth": {
      "min": 0.15,
      "typical": 0.2,
      "max": 0.25,
      "unit": "mm",
      "reasoning": "Calculated for 90Ω differential impedance on 1.6mm FR4"
    },
    "clearance": {
      "min": 0.2,
      "typical": 0.3,
      "unit": "mm"
    },
    "differentialPair": {
      "enabled": true,
      "spacing": {
        "value": 0.15,
        "tolerance": 0.02,
        "unit": "mm"
      },
      "impedance": {
        "differential": 90,
        "tolerance": 10,
        "unit": "ohm"
      },
      "lengthMatching": {
        "intraPairSkew": {
          "max": 0.15,
          "unit": "mm"
        },
        "interPairSkew": {
          "max": 5.0,
          "unit": "mm"
        }
      },
      "viasAllowed": false,
      "layerChangesAllowed": false
    }
  },
  
  "electricalRules": {
    "maxFrequency": {
      "value": 480,
      "unit": "MHz"
    },
    "impedance": {
      "controlled": true,
      "differential": 90,
      "tolerance": 10,
      "unit": "ohm"
    },
    "riseTime": {
      "typical": 1.5,
      "unit": "ns"
    }
  },
  
  "layerPreferences": {
    "preferred": ["top"],
    "avoided": [],
    "allowPlane": false,
    "requiresContinuousGround": true
  },
  
  "semantic": {
    "purpose": "High-speed differential signaling",
    "domain": "high_speed_digital",
    "critical": true,
    "typicalNets": ["USB_DP", "USB_DM", "D+", "D-"],
    "designPattern": "differential_pair_90ohm",
    "aiNotes": "Keep traces as short as possible. Avoid vias and layer changes. Route away from switching power supplies. Minimize stubs."
  }
}
```

**Default/Low-Speed NetClass Example:**

```json
{
  "type": "NetClass",
  "id": "netclass_default",
  "name": "Default",
  
  "description": "Default routing rules for general signals",
  
  "routingRules": {
    "traceWidth": {
      "min": 0.15,
      "typical": 0.2,
      "unit": "mm"
    },
    "clearance": {
      "min": 0.15,
      "typical": 0.2,
      "unit": "mm"
    },
    "viaDiameter": {
      "min": 0.4,
      "typical": 0.6,
      "unit": "mm"
    },
    "viaDrillDiameter": {
      "min": 0.2,
      "typical": 0.3,
      "unit": "mm"
    },
    "differentialPair": {
      "enabled": false
    }
  },
  
  "electricalRules": {
    "impedance": {
      "controlled": false
    }
  },
  
  "semantic": {
    "purpose": "General purpose signals with no special requirements",
    "domain": "digital",
    "critical": false,
    "aiNotes": "Standard manufacturing design rules apply"
  }
}
```

**Net Referencing NetClass:**

When defining nets, reference the NetClass to inherit all routing rules:

```json
{
  "type": "Net",
  "id": "net_vcc_5v",
  "name": "VCC_5V",
  "netClass": "netclass_power_5v",
  
  "connections": [
    {"component": "U1", "pin": "8"},
    {"component": "C1", "pin": "1"}
  ],
  
  "semantic": {
    "type": "power",
    "purpose": "Main 5V power rail"
  }
}
```

**Design-Level NetClass Definitions:**

NetClasses are defined at the design level:

```json
{
  "type": "Design",
  "name": "USB_Hub_Board",
  
  "netClasses": [
    {
      "$ref": "netclass_default"
    },
    {
      "$ref": "netclass_power_5v"
    },
    {
      "$ref": "netclass_usb_diff"
    },
    {
      "type": "NetClass",
      "id": "netclass_custom_clock",
      "name": "Clock_Signals",
      "routingRules": {
        "traceWidth": {"min": 0.2, "unit": "mm"},
        "clearance": {"min": 0.3, "unit": "mm"}
      },
      "semantic": {
        "purpose": "Clock distribution with controlled routing"
      }
    }
  ],
  
  "nets": [
    {
      "id": "net_vcc",
      "name": "VCC",
      "netClass": "netclass_power_5v"
    },
    {
      "id": "net_usb_dp",
      "name": "USB_DP",
      "netClass": "netclass_usb_diff",
      "differentialPairWith": "net_usb_dm"
    },
    {
      "id": "net_usb_dm",
      "name": "USB_DM",
      "netClass": "netclass_usb_diff",
      "differentialPairWith": "net_usb_dp"
    }
  ]
}
```

**AI Benefits:**

1. **Pattern Recognition**: AI can learn that all nets in "netclass_usb_diff" require similar careful routing
2. **Auto-Assignment**: AI can automatically assign appropriate NetClasses to new nets based on semantic analysis
3. **Validation**: AI can verify that net routing complies with NetClass rules before manufacturing
4. **Optimization**: AI can suggest trace width adjustments within NetClass constraints
5. **Knowledge Transfer**: NetClass definitions can be reused across projects

**Common NetClass Categories:**

```
netclass
├── power
│   ├── high_current (>1A)
│   ├── medium_current (100mA-1A)
│   ├── low_current (<100mA)
│   └── analog_power (low noise requirements)
├── signal
│   ├── default (general digital)
│   ├── high_speed_single_ended
│   ├── differential_pair
│   │   ├── usb_2.0 (90Ω)
│   │   ├── usb_3.0 (90Ω)
│   │   ├── ethernet_100base (100Ω)
│   │   ├── pcie (85Ω)
│   │   ├── hdmi (100Ω)
│   │   └── lvds (100Ω)
│   ├── clock
│   └── reset
├── analog
│   ├── high_impedance
│   ├── audio
│   └── sensor
└── special
    ├── antenna (RF)
    ├── shielded
    └── esd_protected
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

### 4.4 User Library Integration

OpenPCBDB supports integration with external user-managed component libraries, enabling companies to maintain approved component databases in various formats including SQL databases, SQLite files, REST APIs, and file-based systems.

#### 4.4.1 Library Configuration

Configure library sources in the design metadata:

```json
{
  "design": {
    "metadata": {
      "name": "Industrial Gateway",
      "libraryConfiguration": {
        "searchOrder": ["user_primary", "user_secondary", "vendor", "community", "standard"],
        "userLibraries": [
          {
            "libraryID": "company_approved_parts",
            "name": "Company Approved Parts Database",
            "type": "sql",
            "priority": 1,
            "connection": {
              "host": "db.company.com",
              "port": 5432,
              "database": "component_library",
              "schema": "approved_parts",
              "authMethod": "environment"  // Credentials from environment variables
            },
            "tables": {
              "components": "tbl_components",
              "symbols": "tbl_schematic_symbols",
              "footprints": "tbl_pcb_footprints",
              "mechanical": "tbl_3d_models",
              "manufacturers": "tbl_manufacturers"
            },
            "approvalWorkflow": true,
            "lastSync": "2025-01-11T08:00:00Z"
          },
          {
            "libraryID": "local_cache",
            "name": "Local SQLite Cache",
            "type": "sqlite",
            "priority": 2,
            "connection": {
              "file": "libraries/cache/components.db"
            },
            "readOnly": false,
            "syncWithPrimary": true
          },
          {
            "libraryID": "vendor_official",
            "name": "Vendor Component Library API",
            "type": "rest_api",
            "priority": 3,
            "connection": {
              "baseURL": "https://api.vendor.com/components/v1",
              "authMethod": "api_key",
              "rateLimit": 100  // requests per minute
            }
          },
          {
            "libraryID": "legacy_json",
            "name": "Legacy JSON Library",
            "type": "json",
            "priority": 4,
            "connection": {
              "path": "libraries/legacy/",
              "indexFile": "components_index.json"
            }
          }
        ]
      }
    }
  }
}
```

#### 4.4.2 SQL Database Library Schema

Standard SQL schema for component libraries:

```sql
-- Manufacturers table
CREATE TABLE tbl_manufacturers (
    manufacturer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(500),
    contact_info TEXT,
    certification_level VARCHAR(50),  -- 'preferred', 'approved', 'acceptable'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Components table
CREATE TABLE tbl_components (
    component_id VARCHAR(100) PRIMARY KEY,
    manufacturer_id VARCHAR(50) REFERENCES tbl_manufacturers(manufacturer_id),
    mpn VARCHAR(100) NOT NULL,  -- Manufacturer Part Number
    variant VARCHAR(50),
    revision VARCHAR(20),
    category VARCHAR(100),  -- 'passive.resistor', 'active.ic', etc.
    subcategory VARCHAR(100),
    description TEXT,
    datasheet_url VARCHAR(500),
    
    -- Electrical parameters (JSON for flexibility)
    electrical_params JSONB,
    
    -- Physical properties
    package VARCHAR(50),
    dimensions JSONB,  -- {length, width, height, unit}
    weight_grams DECIMAL(10,4),
    mounting_type VARCHAR(50),  -- 'SMD', 'THT', 'module'
    
    -- References to other tables
    symbol_id VARCHAR(100),
    footprint_id VARCHAR(100),
    mechanical_id VARCHAR(100),
    
    -- Procurement
    typical_cost DECIMAL(10,4),
    currency VARCHAR(3),
    lead_time_days INTEGER,
    lifecycle_status VARCHAR(50),  -- 'active', 'nrnd', 'obsolete'
    rohs_compliant BOOLEAN,
    
    -- Approval workflow
    approval_status VARCHAR(50),  -- 'draft', 'pending', 'approved', 'rejected'
    approved_by VARCHAR(100),
    approval_date DATE,
    
    -- Metadata
    created_by VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_verified TIMESTAMP,
    
    -- Full-text search
    search_vector TSVECTOR
);

-- Schematic symbols table
CREATE TABLE tbl_schematic_symbols (
    symbol_id VARCHAR(100) PRIMARY KEY,
    symbol_reference VARCHAR(200) NOT NULL,  -- Symbol name/reference
    library_name VARCHAR(100),
    description TEXT,
    pin_count INTEGER,
    pins JSONB,  -- Array of pin definitions
    graphic_data TEXT,  -- SVG, KiCad S-expr, or other format
    format VARCHAR(50),  -- 'svg', 'kicad_symbol', 'altium_lib'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- PCB footprints table
CREATE TABLE tbl_pcb_footprints (
    footprint_id VARCHAR(100) PRIMARY KEY,
    footprint_reference VARCHAR(200) NOT NULL,
    library_name VARCHAR(100),
    description TEXT,
    pad_count INTEGER,
    pads JSONB,  -- Array of pad definitions
    dimensions JSONB,  -- Outline dimensions
    keepout_zones JSONB,
    graphic_data TEXT,  -- Footprint geometry
    format VARCHAR(50),  -- 'kicad_footprint', 'ipc_7351', 'altium_pcblib'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 3D mechanical models table
CREATE TABLE tbl_3d_models (
    mechanical_id VARCHAR(100) PRIMARY KEY,
    mechanical_reference VARCHAR(200) NOT NULL,
    description TEXT,
    file_path VARCHAR(500),
    file_format VARCHAR(50),  -- 'STEP', 'IGES', 'STL', 'WRL'
    file_size_bytes INTEGER,
    bounding_box JSONB,  -- {length, width, height}
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Component relationships (alternates, substitutions)
CREATE TABLE tbl_component_relationships (
    relationship_id SERIAL PRIMARY KEY,
    component_id VARCHAR(100) REFERENCES tbl_components(component_id),
    related_component_id VARCHAR(100) REFERENCES tbl_components(component_id),
    relationship_type VARCHAR(50),  -- 'alternate', 'substitute', 'upgrade', 'downgrade'
    notes TEXT,
    created_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_components_mpn ON tbl_components(mpn);
CREATE INDEX idx_components_category ON tbl_components(category);
CREATE INDEX idx_components_manufacturer ON tbl_components(manufacturer_id);
CREATE INDEX idx_components_approval ON tbl_components(approval_status);
CREATE INDEX idx_components_lifecycle ON tbl_components(lifecycle_status);
CREATE INDEX idx_components_search ON tbl_components USING GIN(search_vector);
```

#### 4.4.3 SQLite Library Schema

For local/embedded libraries, use simplified SQLite schema:

```sql
-- SQLite version (simplified, single-file)
CREATE TABLE components (
    component_id TEXT PRIMARY KEY,
    manufacturer TEXT,
    manufacturer_id TEXT,
    mpn TEXT NOT NULL,
    category TEXT,
    description TEXT,
    datasheet_url TEXT,
    electrical_params TEXT,  -- JSON as TEXT
    package TEXT,
    symbol_id TEXT,
    footprint_id TEXT,
    mechanical_id TEXT,
    typical_cost REAL,
    approval_status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE symbols (
    symbol_id TEXT PRIMARY KEY,
    symbol_reference TEXT,
    pin_count INTEGER,
    pins TEXT,  -- JSON as TEXT
    graphic_data TEXT,
    format TEXT
);

CREATE TABLE footprints (
    footprint_id TEXT PRIMARY KEY,
    footprint_reference TEXT,
    pad_count INTEGER,
    pads TEXT,  -- JSON as TEXT
    graphic_data TEXT,
    format TEXT
);

CREATE TABLE mechanical_models (
    mechanical_id TEXT PRIMARY KEY,
    mechanical_reference TEXT,
    file_path TEXT,
    file_format TEXT
);

CREATE INDEX idx_comp_mpn ON components(mpn);
CREATE INDEX idx_comp_category ON components(category);
```

#### 4.4.4 REST API Library Interface

Standard REST API endpoints for component libraries:

```
GET    /api/v1/components              # List components (paginated)
GET    /api/v1/components/:id          # Get component details
POST   /api/v1/components/search       # Search components
GET    /api/v1/components/:id/symbol   # Get symbol data
GET    /api/v1/components/:id/footprint # Get footprint data
GET    /api/v1/components/:id/mechanical # Get 3D model

GET    /api/v1/manufacturers           # List manufacturers
GET    /api/v1/symbols                 # List symbols
GET    /api/v1/footprints              # List footprints

# Example query parameters
GET /api/v1/components?category=passive.resistor&mpn=RC0603*&limit=50
POST /api/v1/components/search
{
  "query": "10k resistor 0603",
  "filters": {
    "category": "passive.resistor",
    "approval_status": "approved",
    "lifecycle_status": "active"
  }
}
```

#### 4.4.5 Component Instance with Library References

Complete example showing library integration:

```json
{
  "type": "ComponentInstance",
  "instanceId": "U1",
  "refDesignator": "U1",
  
  // Part identification
  "partNumber": {
    "manufacturer": "Texas Instruments",
    "manufacturerID": "MFR_TI_001",
    "mpn": "TPS63001DRCR",
    "variant": "tape_and_reel",
    "revision": "C"
  },
  
  // User library references
  "userLibraryReferences": {
    "primary": {
      "libraryID": "company_approved_parts",
      "libraryType": "sql",
      "componentID": "COMP_IC_DCDC_TPS63001",
      "query": {
        "table": "tbl_components",
        "where": "mpn = 'TPS63001DRCR' AND approval_status = 'approved'"
      },
      "lastVerified": "2025-01-10T14:30:00Z",
      "approvalStatus": "approved",
      "approvedBy": "Engineering Team",
      "approvalDate": "2024-11-15"
    },
    
    "symbol": {
      "libraryID": "company_schematic_symbols",
      "libraryType": "sql",
      "symbolID": "SYM_IC_DCDC_10PIN_VSON",
      "symbolReference": "IC_DCDC_BUCK_BOOST_10PIN",
      "query": {
        "table": "tbl_schematic_symbols",
        "where": "symbol_id = 'SYM_IC_DCDC_10PIN_VSON'"
      },
      "format": "kicad_symbol",
      "pins": {
        "count": 11,  // 10 pins + 1 thermal pad
        "mapping": {
          "1": "VOUT",
          "2": "FB",
          "3": "L2",
          "4": "GND",
          "5": "L1",
          "6": "VIN",
          "7": "EN",
          "8": "PS_SYNC",
          "9": "VINA",
          "10": "PAD"
        }
      }
    },
    
    "footprint": {
      "libraryID": "company_pcb_footprints",
      "libraryType": "sql",
      "footprintID": "FP_VSON10_3x3MM",
      "footprintReference": "VSON-10_3x3mm_P0.5mm",
      "query": {
        "table": "tbl_pcb_footprints",
        "where": "footprint_id = 'FP_VSON10_3x3MM'"
      },
      "format": "ipc_7351",
      "padCount": 11,
      "thermalPad": true
    },
    
    "mechanical": {
      "libraryID": "company_3d_models",
      "libraryType": "sql",
      "modelID": "MECH_VSON10_3x3",
      "mechanicalReference": "TPS63001_3D_MODEL",
      "query": {
        "table": "tbl_3d_models",
        "where": "mechanical_id = 'MECH_VSON10_3x3'"
      },
      "file": "models/IC/TPS63001_VSON10.step",
      "format": "STEP",
      "offset": {"x": 0, "y": 0, "z": 0},
      "rotation": {"x": 0, "y": 0, "z": 0},
      "scale": 1.0
    },
    
    // Alternative/fallback library
    "fallback": {
      "libraryID": "vendor_ti_library",
      "libraryType": "rest_api",
      "componentID": "TI_TPS63001DRCR",
      "apiEndpoint": "https://api.ti.com/components/TPS63001DRCR",
      "note": "Use if primary library unavailable"
    }
  },
  
  // EDA tool specific mappings (for compatibility)
  "edaMappings": {
    "KiCad": {
      "library": "Power_Management",
      "symbol": "TPS63001",
      "footprint": "Package_SON:VSON-10-1EP_3x3mm_P0.5mm_EP1.65x2.4mm"
    },
    "Altium": {
      "schematicLib": "PowerICs.SchLib",
      "component": "TPS63001",
      "pcbLib": "PowerICs.PcbLib",
      "footprint": "VSON10_3X3"
    }
  },
  
  "placement": {
    "x": 50.0,
    "y": 50.0,
    "rotation": 0,
    "layer": "top",
    "unit": "mm"
  }
}
```

#### 4.4.6 Library Synchronization

Configure synchronization between OpenPCBDB and user libraries:

```json
{
  "librarySyncConfiguration": {
    "enabled": true,
    "syncInterval": "hourly",  // "realtime", "hourly", "daily", "manual"
    "syncDirection": "bidirectional",  // "read_only", "write_only", "bidirectional"
    
    "mappings": [
      {
        "libraryID": "company_approved_parts",
        "opcbdbField": "componentDefinitionId",
        "libraryField": "component_id",
        "syncRules": {
          "onUpdate": "notify",  // "auto_update", "notify", "ignore"
          "onDelete": "archive",  // "delete", "archive", "ignore"
          "onApprovalChange": "update_status"
        }
      }
    ],
    
    "conflictResolution": {
      "strategy": "user_library_wins",  // "user_library_wins", "opcbdb_wins", "manual"
      "notifyOnConflict": true,
      "logPath": "logs/library_sync.log"
    },
    
    "caching": {
      "enabled": true,
      "localCache": "cache/library_cache.db",
      "cacheTTL": 3600,  // seconds
      "preloadCategories": ["passive.resistor", "passive.capacitor"]
    }
  }
}
```

#### 4.4.7 Query Examples

**SQL Library Query:**
```python
import openpcbdb

# Connect to user library
library = openpcbdb.UserLibrary.connect(
    library_id="company_approved_parts",
    type="sql",
    host="db.company.com",
    database="component_library"
)

# Query for component
results = library.query("""
    SELECT c.component_id, c.mpn, c.description, 
           s.symbol_reference, f.footprint_reference
    FROM tbl_components c
    LEFT JOIN tbl_schematic_symbols s ON c.symbol_id = s.symbol_id
    LEFT JOIN tbl_pcb_footprints f ON c.footprint_id = f.footprint_id
    WHERE c.category = 'passive.resistor'
      AND c.electrical_params->>'resistance' = '10000'
      AND c.package = '0603'
      AND c.approval_status = 'approved'
    LIMIT 10
""")

# Use component in design
for comp in results:
    instance = openpcbdb.ComponentInstance(
        refDesignator=f"R{n}",
        partNumber={
            "mpn": comp['mpn']
        },
        userLibraryReferences={
            "primary": {
                "libraryID": "company_approved_parts",
                "componentID": comp['component_id']
            }
        }
    )
```

**SQLite Library Query:**
```python
# Connect to SQLite library
library = openpcbdb.UserLibrary.connect(
    library_id="local_cache",
    type="sqlite",
    file="libraries/cache/components.db"
)

# Search components
results = library.search(
    category="active.ic",
    mpn_pattern="TPS6300%",
    approval_status="approved"
)
```

**REST API Library Query:**
```python
# Connect to REST API library
library = openpcbdb.UserLibrary.connect(
    library_id="vendor_official",
    type="rest_api",
    base_url="https://api.vendor.com/components/v1",
    api_key=os.getenv("VENDOR_API_KEY")
)

# Search via API
results = library.get(
    endpoint="/components/search",
    params={
        "query": "buck-boost converter",
        "category": "power_management",
        "voltage_range": "2.5-5.5V"
    }
)
```

#### 4.4.8 Library Best Practices

**1. Library Structure Organization:**
```
company_library/
├── components/
│   ├── passive/
│   │   ├── resistors.json
│   │   └── capacitors.json
│   ├── active/
│   └── modules/
├── symbols/
│   ├── schematic/
│   │   ├── resistors/
│   │   └── ics/
│   └── formats/
│       ├── kicad/
│       └── altium/
├── footprints/
│   ├── smd/
│   └── tht/
├── mechanical/
│   ├── step/
│   └── wrl/
└── config/
    ├── library_config.json
    └── sync_rules.json
```

**2. Naming Conventions:**
```json
{
  "namingConventions": {
    "componentID": "COMP_{CATEGORY}_{TYPE}_{SPEC}_{INDEX}",
    "symbolID": "SYM_{TYPE}_{PINCOUNT}_{VARIANT}",
    "footprintID": "FP_{PACKAGE}_{SIZE}_{VARIANT}",
    "mechanicalID": "MECH_{PACKAGE}_{SIZE}",
    
    "examples": {
      "componentID": "COMP_RES_0603_10K_001",
      "symbolID": "SYM_RESISTOR_2PIN_HORIZ",
      "footprintID": "FP_R_0603_1608Metric",
      "mechanicalID": "MECH_R_0603_STD"
    }
  }
}
```

**3. Approval Workflow:**
```json
{
  "approvalWorkflow": {
    "stages": [
      {
        "stage": "draft",
        "description": "Initial component entry",
        "allowedActions": ["edit", "submit_for_review"]
      },
      {
        "stage": "pending_review",
        "description": "Awaiting engineering review",
        "requiredReviewers": ["electrical_engineer", "pcb_designer"],
        "allowedActions": ["approve", "reject", "request_changes"]
      },
      {
        "stage": "approved",
        "description": "Approved for use in designs",
        "restrictions": ["no_edit_without_reapproval"],
        "allowedActions": ["use_in_design", "mark_for_update"]
      },
      {
        "stage": "obsolete",
        "description": "End of life, use discouraged",
        "allowedActions": ["view_only", "find_replacement"]
      }
    ]
  }
}
```

**4. Multi-Site Synchronization:**
```json
{
  "multiSiteSync": {
    "sites": [
      {
        "siteID": "HQ_USA",
        "libraryURL": "https://lib-usa.company.com",
        "role": "primary",
        "syncMode": "push"
      },
      {
        "siteID": "FACTORY_CHINA",
        "libraryURL": "https://lib-china.company.com",
        "role": "replica",
        "syncMode": "pull",
        "syncInterval": "daily"
      }
    ],
    "conflictResolution": "primary_wins",
    "auditLog": true
  }
}
```

### 4.5 Physical Routing Model

OpenPCBDB v1.3.0 adds comprehensive physical implementation details for complete PCB manufacturing support. These sections capture actual trace geometry, via positions, and copper polygons required for fabrication.

#### 4.5.1 Trace Geometry

Trace routing defines the exact physical paths of copper traces connecting component pads.

**Schema:**

```json
{
  "routing": {
    "traces": [
      {
        "id": "trace_001",
        "net": "net_vcc_5v",
        "layer": "top",
        "width": 0.5,
        "unit": "mm",
        
        "segments": [
          {
            "type": "line",
            "start": {"x": 10.5, "y": 20.3},
            "end": {"x": 15.8, "y": 20.3}
          },
          {
            "type": "arc",
            "center": {"x": 15.8, "y": 22.3},
            "radius": 2.0,
            "startAngle": 270,
            "endAngle": 0,
            "unit": "degrees"
          },
          {
            "type": "line",
            "start": {"x": 17.8, "y": 22.3},
            "end": {"x": 25.0, "y": 22.3}
          }
        ],
        
        "connections": [
          {"component": "U1", "pin": "8", "position": {"x": 10.5, "y": 20.3}},
          {"component": "R1", "pin": "1", "position": {"x": 25.0, "y": 22.3}}
        ],
        
        "properties": {
          "impedance": {"target": 50, "actual": 51.2, "unit": "ohm"},
          "length": {"value": 18.5, "unit": "mm"},
          "netClass": "power",
          "keepout": false
        },
        
        "semantic": {
          "purpose": "5V power trace from regulator to MCU",
          "critical": true,
          "reasoning": "Wide trace (0.5mm) for 500mA current capacity",
          "routingStrategy": "Manual routing for power integrity"
        }
      }
    ]
  }
}
```

**Segment Types:**

| Type | Parameters | Description |
|------|------------|-------------|
| `line` | start, end | Straight trace segment |
| `arc` | center, radius, startAngle, endAngle | Curved segment for corners/teardrops |
| `bezier` | start, end, control1, control2 | Smooth curve using Bezier |

#### 4.5.2 Via Definitions

Vias provide electrical connections between PCB layers with exact positions and drill specifications.

**Schema:**

```json
{
  "vias": [
    {
      "id": "via_001",
      "position": {"x": 15.5, "y": 20.3, "unit": "mm"},
      "net": "net_vcc_5v",
      
      "type": "through_hole",
      
      "drill": {
        "diameter": 0.3,
        "tolerance": 0.05,
        "unit": "mm",
        "plated": true
      },
      
      "pad": {
        "diameter": 0.6,
        "shape": "circle",
        "unit": "mm"
      },
      
      "layers": {
        "start": "top",
        "end": "bottom",
        "connections": ["L1", "L2"]
      },
      
      "annularRing": {
        "minimum": 0.15,
        "actual": 0.15,
        "unit": "mm"
      },
      
      "properties": {
        "tented": false,
        "thermal": true,
        "stitching": false,
        "testPoint": false
      },
      
      "semantic": {
        "purpose": "Layer transition for power net",
        "critical": true,
        "reasoning": "Required for power plane connection"
      }
    }
  ]
}
```

**Via Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| `through_hole` | Connects all layers | Standard via |
| `blind` | Outer to inner layer only | High-density routing |
| `buried` | Internal layers only | Advanced HDI |
| `micro` | Laser-drilled (<0.15mm) | Fine-pitch BGA |

#### 4.5.3 Copper Polygons

Copper polygons (pour zones) provide large copper areas for power/ground planes with automatic clearances and thermal reliefs.

**Schema:**

```json
{
  "planes": [
    {
      "id": "plane_gnd_bottom",
      "net": "GND",
      "layer": "bottom",
      "type": "solid_pour",
      
      "outline": [
        {"x": 0.5, "y": 0.5},
        {"x": 79.5, "y": 0.5},
        {"x": 79.5, "y": 49.5},
        {"x": 0.5, "y": 49.5}
      ],
      "unit": "mm",
      "closed": true,
      
      "islands": [
        {
          "outline": [
            {"x": 10, "y": 10},
            {"x": 20, "y": 10},
            {"x": 20, "y": 20},
            {"x": 10, "y": 20}
          ],
          "reason": "Keepout for mounting hole"
        }
      ],
      
      "thermalRelief": {
        "enabled": true,
        "connectionWidth": 0.3,
        "connectionCount": 4,
        "gap": 0.3,
        "unit": "mm",
        "applyTo": "all_pads"
      },
      
      "clearance": {
        "default": 0.3,
        "power": 0.5,
        "signal": 0.25,
        "unit": "mm"
      },
      
      "hatch": {
        "enabled": false,
        "width": 0.5,
        "spacing": 2.0,
        "angle": 45,
        "unit": "mm"
      },
      
      "priority": 1,
      
      "properties": {
        "locked": false,
        "keepout": false,
        "minArea": 1.0
      },
      
      "semantic": {
        "purpose": "Primary ground plane for bottom layer",
        "critical": true,
        "reasoning": "Solid plane provides low impedance ground return path",
        "designPattern": "ground_plane"
      }
    }
  ]
}
```

### 4.6 Manufacturing Layers

Manufacturing layer definitions specify pad geometries, silkscreen graphics, and solder mask/paste openings required for PCB fabrication and assembly.

#### 4.6.1 Pad Geometries

Pad definitions specify exact shapes and properties for each component connection point.

**Schema:**

```json
{
  "componentPlacement": [
    {
      "refDesignator": "R1",
      "position": {"x": 25.0, "y": 30.0, "unit": "mm"},
      "rotation": 0,
      "side": "top",
      
      "pads": [
        {
          "id": "1",
          "number": "1",
          "position": {"x": 0, "y": 0, "unit": "mm"},
          
          "shape": "rectangle",
          "size": {
            "width": 0.6,
            "height": 0.8,
            "unit": "mm"
          },
          
          "layers": ["top_copper", "top_mask", "top_paste"],
          
          "hole": null,
          
          "soldermask": {
            "expansion": 0.05,
            "unit": "mm",
            "defined": true
          },
          
          "solderpaste": {
            "reduction": 0.05,
            "unit": "mm",
            "defined": true
          },
          
          "properties": {
            "net": "net_vcc_5v",
            "thermal": false,
            "testPoint": false,
            "plated": true
          },
          
          "semantic": {
            "function": "Component terminal for voltage input",
            "critical": false
          }
        }
      ]
    }
  ]
}
```

**Pad Shapes:**

| Shape | Use Case | Parameters |
|-------|----------|------------|
| `rectangle` | Standard SMD | width, height |
| `circle` | Round pads, THT | diameter |
| `oval` | Elongated pads | width, height |
| `rounded_rect` | Rounded corners | width, height, radius |
| `custom` | Complex shapes | polygon points |

#### 4.6.2 Silkscreen Graphics

Silkscreen layer defines component designators, values, and board markings.

**Schema:**

```json
{
  "silkscreen": {
    "layers": ["top_silkscreen", "bottom_silkscreen"],
    
    "text": [
      {
        "id": "text_001",
        "content": "R1",
        "position": {"x": 25.0, "y": 32.0, "unit": "mm"},
        "layer": "top_silkscreen",
        "height": 1.0,
        "width": 0.8,
        "thickness": 0.15,
        "unit": "mm",
        "rotation": 0,
        "mirrored": false,
        "font": "standard",
        "justification": "center",
        "type": "refdes",
        "visible": true,
        
        "semantic": {
          "purpose": "Component reference designator",
          "linkedComponent": "R1"
        }
      }
    ],
    
    "lines": [
      {
        "id": "line_001",
        "layer": "top_silkscreen",
        "start": {"x": 10.0, "y": 10.0},
        "end": {"x": 70.0, "y": 10.0},
        "width": 0.15,
        "unit": "mm",
        "semantic": {
          "purpose": "Board outline indicator"
        }
      }
    ],
    
    "circles": [
      {
        "id": "circle_001",
        "layer": "top_silkscreen",
        "center": {"x": 20.0, "y": 20.0},
        "radius": 2.0,
        "width": 0.15,
        "filled": false,
        "unit": "mm",
        "semantic": {
          "purpose": "Polarity indicator for polarized component"
        }
      }
    ]
  }
}
```

#### 4.6.3 Solder Mask

Solder mask defines openings that expose copper pads for soldering.

**Schema:**

```json
{
  "soldermask": {
    "layers": ["top_mask", "bottom_mask"],
    
    "color": "green",
    "finish": "matte",
    
    "global": {
      "expansion": 0.05,
      "unit": "mm",
      "minimumSliver": 0.1
    },
    
    "openings": [
      {
        "id": "mask_001",
        "layer": "top_mask",
        "associatedPad": {
          "component": "R1",
          "pad": "1"
        },
        "shape": "rectangle",
        "size": {"width": 0.7, "height": 0.9, "unit": "mm"},
        "position": {"x": 25.0, "y": 30.0},
        "expansion": 0.05,
        "semantic": {
          "purpose": "Solder mask opening for component pad"
        }
      }
    ],
    
    "properties": {
      "thickness": 0.025,
      "unit": "mm",
      "dielectricConstant": 3.3
    }
  }
}
```

#### 4.6.4 Solder Paste

Solder paste (stencil) defines apertures for solder paste application.

**Schema:**

```json
{
  "solderpaste": {
    "layers": ["top_paste", "bottom_paste"],
    
    "stencil": {
      "thickness": 0.125,
      "material": "stainless_steel",
      "laserCut": true,
      "electropolished": true
    },
    
    "global": {
      "reduction": 0.05,
      "unit": "mm",
      "ratioToPad": 0.9
    },
    
    "apertures": [
      {
        "id": "paste_001",
        "layer": "top_paste",
        "associatedPad": {
          "component": "R1",
          "pad": "1"
        },
        "shape": "rectangle",
        "size": {"width": 0.55, "height": 0.75, "unit": "mm"},
        "position": {"x": 25.0, "y": 30.0},
        "reduction": 0.05,
        
        "properties": {
          "split": false,
          "rounded": false
        },
        
        "semantic": {
          "purpose": "Solder paste deposit for component pad"
        }
      }
    ]
  }
}
```

### 4.7 Manufacturing Data

Manufacturing data includes Gerber files, drill data, and assembly information for PCB fabrication.

#### 4.7.1 Gerber Files

Gerber file references for each manufacturing layer.

**Schema:**

```json
{
  "manufacturing": {
    "version": "1.0",
    "generatedDate": "2025-01-11T10:00:00Z",
    
    "gerberFiles": {
      "format": "RS-274X",
      "unit": "mm",
      "precision": "4.6",
      
      "layers": [
        {
          "type": "copper",
          "layer": "top",
          "file": "gerber/top_copper.gbr",
          "md5": "abc123...",
          "fileSize": 125634
        },
        {
          "type": "copper",
          "layer": "bottom",
          "file": "gerber/bottom_copper.gbr"
        },
        {
          "type": "soldermask",
          "layer": "top",
          "file": "gerber/top_mask.gbr"
        },
        {
          "type": "silkscreen",
          "layer": "top",
          "file": "gerber/top_silk.gbr"
        },
        {
          "type": "solderpaste",
          "layer": "top",
          "file": "gerber/top_paste.gbr"
        },
        {
          "type": "outline",
          "file": "gerber/board_outline.gbr"
        }
      ]
    },
    
    "fabricationNotes": {
      "material": "FR4",
      "thickness": 1.6,
      "copperWeight": {
        "outer": 35,
        "inner": 35,
        "unit": "um"
      },
      "surfaceFinish": "ENIG",
      "minTraceWidth": 0.15,
      "minTraceSpacing": 0.15,
      "minHoleSize": 0.25,
      "unit": "mm",
      "color": {
        "soldermask": "green",
        "silkscreen": "white"
      }
    }
  }
}
```

#### 4.7.2 Drill Files

Drill file specifications for plated and non-plated holes.

**Schema:**

```json
{
  "drillFiles": {
    "format": "Excellon",
    "unit": "mm",
    
    "files": [
      {
        "type": "plated_through_hole",
        "file": "gerber/drill_pth.drl",
        "toolList": [
          {"tool": "T01", "diameter": 0.3, "count": 45},
          {"tool": "T02", "diameter": 0.8, "count": 12},
          {"tool": "T03", "diameter": 1.0, "count": 4}
        ]
      },
      {
        "type": "non_plated_through_hole",
        "file": "gerber/drill_npth.drl",
        "toolList": [
          {"tool": "T01", "diameter": 3.2, "count": 4}
        ]
      }
    ]
  }
}
```

#### 4.7.3 Assembly Data

Assembly information including pick-and-place and BOM data.

**Schema:**

```json
{
  "assemblyData": {
    "pickAndPlace": {
      "format": "CSV",
      "file": "assembly/pick_and_place.csv",
      "columns": ["Designator", "X", "Y", "Rotation", "Side", "PartNumber"],
      "unit": "mm",
      "origin": "bottom_left"
    },
    
    "bom": {
      "format": "CSV",
      "file": "assembly/bom.csv",
      "columns": ["Designator", "Quantity", "PartNumber", "Manufacturer", "Description", "Value"],
      "groupBy": "partNumber"
    },
    
    "assemblyDrawing": {
      "format": "PDF",
      "file": "assembly/assembly_drawing.pdf",
      "includes": [
        "Component placement",
        "Polarity indicators",
        "Critical assembly notes",
        "Test point locations"
      ]
    }
  }
}
```

### 4.8 3D Mechanical Integration

3D mechanical data enables collision checking and mechanical validation.

#### 4.8.1 Component Models

3D model references for each component.

**Schema:**

```json
{
  "mechanical3D": {
    "board": {
      "model": "mechanical/board_3d.step",
      "format": "STEP",
      "origin": {"x": 0, "y": 0, "z": 0},
      "unit": "mm"
    },
    
    "components": [
      {
        "refDesignator": "U1",
        "model": "mechanical/stm32f103.step",
        "format": "STEP",
        "position": {"x": 25.0, "y": 40.0, "z": 0},
        "rotation": {"x": 0, "y": 0, "z": 90},
        "scale": 1.0,
        "boundingBox": {
          "length": 7.0,
          "width": 7.0,
          "height": 1.2,
          "unit": "mm"
        },
        "semantic": {
          "purpose": "3D representation for mechanical clearance checking"
        }
      }
    ]
  }
}
```

#### 4.8.2 Keepout Zones

3D keepout zones for mechanical clearance.

**Schema:**

```json
{
  "keepoutZones": [
    {
      "id": "keepout_001",
      "shape": "cylinder",
      "position": {"x": 5, "y": 5},
      "radius": 1.6,
      "height": 10.0,
      "layer": "all",
      "unit": "mm",
      "semantic": {
        "purpose": "Mounting screw clearance",
        "reasoning": "M3 screw with 10mm standoff height"
      }
    }
  ],
  
  "collisionChecks": {
    "enabled": true,
    "minClearance": 0.5,
    "checkWith": ["components", "enclosure", "mounting_hardware"]
  }
}
```

### 4.9 Design Rule Checking

Design rule definitions and violation reporting for validation.

#### 4.9.1 Rule Definitions

Complete design rule specifications.

**Schema:**

```json
{
  "designRules": {
    "version": "1.0",
    "lastChecked": "2025-01-11T15:30:00Z",
    
    "rules": {
      "clearance": {
        "copperToCopper": {
          "minimum": 0.15,
          "recommended": 0.2,
          "unit": "mm"
        },
        "copperToOutline": {
          "minimum": 0.3,
          "unit": "mm"
        },
        "copperToHole": {
          "minimum": 0.25,
          "unit": "mm"
        }
      },
      
      "traceWidth": {
        "minimum": 0.15,
        "maximum": 10.0,
        "power": {
          "minimum": 0.5,
          "recommended": 1.0
        },
        "signal": {
          "minimum": 0.15,
          "recommended": 0.2
        },
        "unit": "mm"
      },
      
      "via": {
        "drillMinimum": 0.25,
        "padMinimum": 0.5,
        "annularRingMinimum": 0.15,
        "unit": "mm"
      }
    }
  }
}
```

#### 4.9.2 Violation Reporting

Design rule violation tracking and reporting.

**Schema:**

```json
{
  "violations": [
    {
      "id": "violation_001",
      "rule": "clearance.copperToCopper",
      "severity": "error",
      "description": "Traces too close on layer top",
      "location": {
        "layer": "top",
        "position": {"x": 15.3, "y": 22.7},
        "objects": ["trace_005", "trace_012"],
        "actual": 0.12,
        "required": 0.15,
        "unit": "mm"
      },
      "suggestion": "Increase spacing or reroute one trace",
      
      "semantic": {
        "impact": "Manufacturing yield risk",
        "reasoning": "Insufficient clearance may cause shorts",
        "priority": "high"
      }
    }
  ],
  
  "statistics": {
    "errors": 1,
    "warnings": 3,
    "info": 0,
    "passed": false
  }
}
```

---

### 4.10 Electrical Rule Checking

Electrical rule definitions and validation for circuit correctness and safety.

#### 4.10.1 Pin Compatibility Rules

Pin-to-pin electrical compatibility checking to prevent connection errors.

**Schema:**

```json
{
  "electricalRules": {
    "version": "1.0",
    "lastChecked": "2025-01-11T15:30:00Z",
    
    "pinCompatibility": {
      "rules": [
        {
          "id": "erc_rule_001",
          "name": "Output to Output Conflict",
          "severity": "error",
          "description": "Two output pins cannot be directly connected",
          "pattern": {
            "pin1Type": "output",
            "pin2Type": "output",
            "action": "error"
          },
          "semantic": {
            "reasoning": "Multiple drivers can cause bus contention and damage",
            "impact": "Circuit malfunction or component damage",
            "exceptions": [
              "Open-drain/open-collector outputs with pull-up",
              "Tri-state outputs with proper bus arbitration"
            ]
          }
        },
        {
          "id": "erc_rule_002",
          "name": "Unconnected Input Pin",
          "severity": "warning",
          "description": "Input pin not connected to any net",
          "pattern": {
            "pinType": "input",
            "connected": false,
            "action": "warning"
          },
          "semantic": {
            "reasoning": "Floating inputs can cause unpredictable behavior",
            "impact": "Undefined logic levels, noise susceptibility",
            "exceptions": [
              "Pins with internal pull-up/pull-down",
              "Unused inputs on multi-gate packages"
            ]
          }
        },
        {
          "id": "erc_rule_003",
          "name": "Power Pin Not Connected",
          "severity": "error",
          "description": "Power input pin not connected to power net",
          "pattern": {
            "pinType": "power_input",
            "connected": false,
            "action": "error"
          },
          "semantic": {
            "reasoning": "Components require power to function",
            "impact": "Component will not operate"
          }
        },
        {
          "id": "erc_rule_004",
          "name": "Input Without Driver",
          "severity": "error",
          "description": "Input pin connected to net with no driver",
          "pattern": {
            "pinType": "input",
            "netHasOutput": false,
            "action": "error"
          },
          "semantic": {
            "reasoning": "Inputs need a signal source",
            "impact": "Undefined logic state"
          }
        },
        {
          "id": "erc_rule_005",
          "name": "Conflicting Power Nets",
          "severity": "error",
          "description": "Different voltage power nets shorted together",
          "pattern": {
            "net1Type": "power",
            "net2Type": "power",
            "net1Voltage": "3.3V",
            "net2Voltage": "5V",
            "connected": true,
            "action": "error"
          },
          "semantic": {
            "reasoning": "Shorting different voltages causes damage",
            "impact": "Power supply damage, board failure"
          }
        }
      ],
      
      "pinTypeMatrix": {
        "description": "Pin compatibility matrix for connection validation",
        "matrix": {
          "output_to_input": "ok",
          "output_to_output": "error",
          "output_to_bidirectional": "ok",
          "output_to_passive": "ok",
          "output_to_power": "error",
          "output_to_ground": "error",
          
          "input_to_input": "warning",
          "input_to_bidirectional": "ok",
          "input_to_passive": "ok",
          "input_to_power": "error",
          "input_to_ground": "error",
          
          "bidirectional_to_bidirectional": "ok",
          "bidirectional_to_passive": "ok",
          "bidirectional_to_power": "error",
          "bidirectional_to_ground": "error",
          
          "passive_to_passive": "ok",
          "passive_to_power": "ok",
          "passive_to_ground": "ok",
          
          "power_to_power": "warning",
          "power_to_ground": "error",
          
          "ground_to_ground": "ok"
        }
      }
    }
  }
}
```

**Pin Type Definitions:**

```json
{
  "pinTypes": {
    "output": {
      "description": "Actively drives signal (push-pull)",
      "canDrive": true,
      "canReceive": false,
      "examples": ["CMOS output", "TTL output"]
    },
    "input": {
      "description": "Only receives signal",
      "canDrive": false,
      "canReceive": true,
      "examples": ["Digital input", "Analog input"]
    },
    "bidirectional": {
      "description": "Can drive or receive (tri-state)",
      "canDrive": true,
      "canReceive": true,
      "examples": ["I2C SDA", "SPI MISO/MOSI"]
    },
    "open_drain": {
      "description": "Can pull low, requires pull-up",
      "canDrive": "pull_down_only",
      "canReceive": true,
      "requiresPullup": true,
      "examples": ["I2C SCL/SDA", "Open collector"]
    },
    "passive": {
      "description": "No active drive (resistor, capacitor)",
      "canDrive": false,
      "canReceive": false,
      "examples": ["Resistor terminal", "Capacitor terminal"]
    },
    "power_input": {
      "description": "Power supply input",
      "canDrive": false,
      "canReceive": true,
      "criticalConnection": true
    },
    "power_output": {
      "description": "Power supply output",
      "canDrive": true,
      "canReceive": false,
      "criticalConnection": true
    },
    "ground": {
      "description": "Ground reference",
      "canDrive": false,
      "canReceive": true,
      "criticalConnection": true
    }
  }
}
```

#### 4.10.2 Power and Ground Validation

Validation rules for power distribution and grounding.

**Schema:**

```json
{
  "powerValidation": {
    "rules": [
      {
        "id": "erc_power_001",
        "name": "Power Net Voltage Mismatch",
        "severity": "error",
        "description": "Component power pin voltage does not match supply voltage",
        "check": {
          "componentPin": {
            "type": "power_input",
            "ratedVoltage": {"min": 4.5, "max": 5.5, "unit": "V"}
          },
          "connectedNet": {
            "type": "power",
            "voltage": {"nominal": 3.3, "unit": "V"}
          },
          "result": "error"
        },
        "semantic": {
          "reasoning": "Applying wrong voltage can damage component",
          "impact": "Component damage or malfunction"
        }
      },
      {
        "id": "erc_power_002",
        "name": "Excessive Current Draw",
        "severity": "warning",
        "description": "Total load exceeds power supply capacity",
        "check": {
          "powerSupply": {
            "component": "U1",
            "pin": "VOUT",
            "maxCurrent": {"value": 1.0, "unit": "A"}
          },
          "totalLoad": {
            "calculated": 1.2,
            "unit": "A"
          },
          "result": "warning"
        },
        "semantic": {
          "reasoning": "Overloading power supply causes voltage drop or shutdown",
          "impact": "System instability or shutdown"
        }
      },
      {
        "id": "erc_power_003",
        "name": "Missing Decoupling Capacitor",
        "severity": "warning",
        "description": "IC power pin without nearby decoupling capacitor",
        "check": {
          "component": "U5",
          "pinType": "power_input",
          "decouplingCapacitor": {
            "present": false,
            "required": true,
            "recommendedValue": {"value": 100, "unit": "nF"},
            "maxDistance": {"value": 5, "unit": "mm"}
          },
          "result": "warning"
        },
        "semantic": {
          "reasoning": "Decoupling caps stabilize power and reduce noise",
          "impact": "Signal integrity issues, EMI problems"
        }
      },
      {
        "id": "erc_power_004",
        "name": "Ground Not Connected",
        "severity": "error",
        "description": "Component ground pin not connected",
        "check": {
          "component": "U3",
          "pinType": "ground",
          "connected": false,
          "result": "error"
        },
        "semantic": {
          "reasoning": "Ground connection is essential for circuit operation",
          "impact": "Component will not function"
        }
      },
      {
        "id": "erc_power_005",
        "name": "Multiple Ground Nets",
        "severity": "warning",
        "description": "Design has multiple separate ground nets",
        "check": {
          "groundNets": ["GND", "AGND", "DGND"],
          "isolated": true,
          "result": "warning"
        },
        "semantic": {
          "reasoning": "Intentional ground splits require careful design",
          "impact": "Potential ground loops or reference issues",
          "validUseCases": [
            "Analog/digital ground separation with single-point connection",
            "Isolated power supplies"
          ]
        }
      },
      {
        "id": "erc_power_006",
        "name": "Voltage Regulator Input Too Low",
        "severity": "error",
        "description": "Regulator input voltage below minimum dropout requirement",
        "check": {
          "regulator": "U2",
          "inputVoltage": {"nominal": 3.5, "unit": "V"},
          "outputVoltage": {"nominal": 3.3, "unit": "V"},
          "dropout": {"min": 0.3, "unit": "V"},
          "margin": 0.2,
          "result": "error"
        },
        "semantic": {
          "reasoning": "Insufficient headroom causes regulation failure",
          "impact": "Output voltage will be below specification"
        }
      }
    ]
  }
}
```

#### 4.10.3 ERC Violation Reporting

ERC-specific violation tracking and reporting with AI-friendly suggestions.

**Schema:**

```json
{
  "ercViolations": [
    {
      "id": "erc_violation_001",
      "rule": "erc_rule_001",
      "ruleName": "Output to Output Conflict",
      "severity": "error",
      "category": "pin_compatibility",
      
      "description": "Two output pins driving the same net",
      
      "location": {
        "net": "net_data_bus_0",
        "pins": [
          {"component": "U1", "pin": "DOUT", "pinType": "output"},
          {"component": "U2", "pin": "Q", "pinType": "output"}
        ]
      },
      
      "electricalDetails": {
        "pin1": {
          "component": "U1",
          "pin": "DOUT",
          "type": "output",
          "driveStrength": "4mA",
          "outputVoltage": {"high": 3.3, "low": 0, "unit": "V"}
        },
        "pin2": {
          "component": "U2",
          "pin": "Q",
          "type": "output",
          "driveStrength": "8mA",
          "outputVoltage": {"high": 3.3, "low": 0, "unit": "V"}
        },
        "conflict": "Both pins actively drive - bus contention"
      },
      
      "suggestions": [
        {
          "action": "Add tri-state control",
          "description": "Convert one output to tri-state and add output-enable logic",
          "effort": "medium",
          "aiConfidence": 0.9
        },
        {
          "action": "Add isolation resistor",
          "description": "Add series resistor to one output (temporary workaround)",
          "effort": "low",
          "aiConfidence": 0.3,
          "note": "Not recommended for production"
        },
        {
          "action": "Use multiplexer",
          "description": "Add 2:1 mux to select between outputs",
          "effort": "high",
          "aiConfidence": 0.8
        }
      ],
      
      "semantic": {
        "impact": "Bus contention will cause excessive current draw and potential component damage",
        "criticality": "high",
        "mustFix": true,
        "reasoning": "Multiple active drivers create undefined voltage levels and stress components",
        "relatedViolations": []
      },
      
      "aiMetadata": {
        "patternType": "output_conflict",
        "commonCause": "Copy-paste error or misunderstanding of bus architecture",
        "learningNote": "Always verify only one driver is active on a net at any time"
      }
    },
    {
      "id": "erc_violation_002",
      "rule": "erc_rule_002",
      "ruleName": "Unconnected Input Pin",
      "severity": "warning",
      "category": "pin_connectivity",
      
      "description": "Digital input pin left floating",
      
      "location": {
        "component": "U3",
        "pin": "RESET_N",
        "pinType": "input"
      },
      
      "electricalDetails": {
        "pin": {
          "component": "U3",
          "pin": "RESET_N",
          "type": "input",
          "function": "Active-low reset",
          "internalPullup": false,
          "schmittTrigger": false
        },
        "risk": "Undefined state - may float high or low"
      },
      
      "suggestions": [
        {
          "action": "Add pull-up resistor",
          "description": "Connect 10kΩ pull-up to VCC to keep inactive high",
          "effort": "low",
          "aiConfidence": 0.95
        },
        {
          "action": "Connect to reset circuit",
          "description": "Connect to power-on reset IC or RC circuit",
          "effort": "medium",
          "aiConfidence": 0.7
        },
        {
          "action": "Tie directly to VCC",
          "description": "If reset function not needed, tie directly to VCC",
          "effort": "low",
          "aiConfidence": 0.5,
          "note": "Only if reset functionality is not required"
        }
      ],
      
      "semantic": {
        "impact": "Unpredictable operation - device may reset randomly due to noise",
        "criticality": "medium",
        "mustFix": true,
        "reasoning": "Floating inputs are susceptible to noise and ESD"
      }
    },
    {
      "id": "erc_violation_003",
      "rule": "erc_power_002",
      "ruleName": "Excessive Current Draw",
      "severity": "warning",
      "category": "power_budget",
      
      "description": "Total load current exceeds regulator capability",
      
      "location": {
        "powerNet": "net_vcc_3v3",
        "source": {"component": "U1", "pin": "VOUT"},
        "loads": [
          {"component": "U2", "current": 0.15},
          {"component": "U3", "current": 0.35},
          {"component": "U4", "current": 0.25},
          {"component": "LED1", "current": 0.02},
          {"component": "LED2", "current": 0.02}
        ]
      },
      
      "electricalDetails": {
        "supplyCapacity": {"max": 0.5, "typical": 0.8, "unit": "A"},
        "totalLoad": {"calculated": 0.79, "unit": "A"},
        "margin": {"percentage": -56.7, "note": "Negative margin indicates overload"}
      },
      
      "suggestions": [
        {
          "action": "Use higher current regulator",
          "description": "Replace with 1A or 1.5A version of same regulator family",
          "effort": "low",
          "aiConfidence": 0.9,
          "componentSuggestions": ["LM1117-1.5A", "AMS1117-1A"]
        },
        {
          "action": "Add second regulator",
          "description": "Split load between two regulators",
          "effort": "high",
          "aiConfidence": 0.6
        },
        {
          "action": "Reduce LED current",
          "description": "Increase LED series resistors to reduce current to 10mA each",
          "effort": "low",
          "aiConfidence": 0.7,
          "savingsCurrent": 0.04
        }
      ],
      
      "semantic": {
        "impact": "Regulator thermal shutdown or voltage droop under load",
        "criticality": "high",
        "mustFix": true,
        "reasoning": "Exceeding current rating causes instability and potential damage"
      }
    }
  ],
  
  "summary": {
    "totalViolations": 3,
    "errors": 1,
    "warnings": 2,
    "info": 0,
    "categories": {
      "pin_compatibility": 1,
      "pin_connectivity": 1,
      "power_budget": 1
    },
    "mustFixCount": 3,
    "ercPassed": false
  },
  
  "aiSummary": {
    "criticalIssues": [
      "Output-to-output conflict on net_data_bus_0 - requires immediate attention"
    ],
    "designQuality": "poor",
    "estimatedFixEffort": "medium",
    "commonPatterns": [
      "Missing pull-up/pull-down resistors on inputs",
      "Power budget not validated during component selection"
    ]
  }
}
```

**ERC Severity Levels:**

```json
{
  "severityLevels": {
    "error": {
      "description": "Fundamental electrical error that will cause malfunction or damage",
      "color": "red",
      "blockManufacturing": true,
      "examples": [
        "Output-to-output conflict",
        "Power voltage mismatch",
        "Ground not connected"
      ]
    },
    "warning": {
      "description": "Potential issue that may cause problems",
      "color": "orange",
      "blockManufacturing": false,
      "requiresReview": true,
      "examples": [
        "Unconnected input",
        "Current budget exceeded",
        "Missing decoupling capacitor"
      ]
    },
    "info": {
      "description": "Design suggestion or best practice recommendation",
      "color": "blue",
      "blockManufacturing": false,
      "requiresReview": false,
      "examples": [
        "Component value optimization available",
        "Alternative component suggested"
      ]
    }
  }
}
```

**AI Benefits for ERC:**

1. **Automated Validation**: AI can automatically check all electrical rules before manufacturing
2. **Smart Suggestions**: AI provides context-aware fixes ranked by confidence and effort
3. **Pattern Learning**: AI learns common ERC violations in specific design patterns
4. **Preventative Design**: AI can suggest component connections that avoid violations
5. **Impact Analysis**: AI explains the real-world consequences of each violation

---

## 6. API Specification

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

**File Extension:** `.opcbdb`

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

## 8. AI/ML Integration

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

## 9. Reference Implementation

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

## 10. Appendices

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
- **User Library**: External component database managed by user/company (SQL, SQLite, REST API, or file-based)
- **Library Reference**: Link from component instance to external library entry
- **Symbol Reference**: Schematic symbol representation identifier in library
- **Footprint Reference**: PCB footprint identifier in library
- **Mechanical Reference**: 3D model identifier in library
- **Manufacturer ID**: Unique identifier for component manufacturer in library system
- **MPN**: Manufacturer Part Number - unique part identifier from manufacturer
- **Approval Status**: Component qualification state (draft, pending, approved, rejected, obsolete)
- **Library Synchronization**: Process of keeping OpenPCBDB and external libraries in sync
- **Trace**: Copper path on PCB connecting component pads; defined by width, layer, and segment geometry
- **Segment**: Individual section of a trace (line, arc, or bezier curve)
- **Via**: Plated hole connecting traces between PCB layers
- **Through-Hole Via**: Via connecting all PCB layers from top to bottom
- **Blind Via**: Via connecting outer layer to one or more inner layers (not through board)
- **Buried Via**: Via connecting only inner layers (not visible from surface)
- **Micro Via**: Small laser-drilled via typically less than 0.15mm diameter
- **Copper Polygon**: Large copper area (pour zone) typically for power/ground planes
- **Thermal Relief**: Spoke pattern connecting pad to copper plane (reduces heat sinking during soldering)
- **Annular Ring**: Copper ring around via hole between drill and pad edge
- **Pad**: Copper area on PCB where component lead is soldered
- **SMD Pad**: Surface mount pad without through-hole
- **THT Pad**: Through-hole technology pad with plated hole
- **Silkscreen**: Screen-printed layer showing component outlines, text, and logos
- **Solder Mask**: Protective coating on copper with openings at pads
- **Solder Paste**: Solder cream applied through stencil for SMD assembly
- **Stencil**: Metal sheet with apertures for applying solder paste
- **Aperture**: Opening in stencil for paste deposition on pad
- **Gerber Files**: Industry-standard manufacturing files for PCB fabrication
- **RS-274X**: Extended Gerber format specification
- **Excellon**: Standard drill file format
- **Pick-and-Place**: Machine-readable component position file for automated assembly
- **BOM (Bill of Materials)**: Complete list of components with quantities and part numbers
- **DRC (Design Rule Check)**: Automated checking of design against manufacturing constraints
- **Keepout Zone**: 3D area where components cannot be placed
- **Clearance**: Minimum spacing between copper features
- **Impedance Control**: Specific trace width/spacing for controlled electrical impedance
- **Stackup**: Layer structure of PCB (copper and dielectric layers)
- **STEP File**: Standard 3D mechanical model format (ISO 10303)

---

## 11. Complex Design Support: Motherboard Example

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

## 12. Future Extensions (v2.0+)

- Multi-board systems
- Flexible/rigid-flex PCB support
- Advanced 3D mechanical integration
- Real-time collaboration protocols
- Complete SI/PI/Thermal/EMI co-simulation
- Quantum computing readiness

---

**Document Version:** 1.3.0 Draft  
**Last Updated:** 2025-01-11  
**Status:** Open for Community Review  

**Contributing:** See CONTRIBUTING.md  
**License:** CC BY 4.0 (documentation), Apache 2.0 (code)  
**Repository:** https://github.com/openpcbdb/specification

---

**END OF SPECIFICATION v1.3.0**
