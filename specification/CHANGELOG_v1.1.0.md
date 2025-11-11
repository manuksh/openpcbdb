# OpenPCBDB Specification Changelog - Version 1.1.0

## Summary

Added comprehensive **Module** entity support to OpenPCBDB specification, enabling representation of physical separate PCB assemblies (System-on-Module, DIMM, M.2 cards, daughterboards, etc.) within parent designs.

**Date**: 2025-11-11  
**Version**: 1.0.0 → 1.1.0  
**Status**: Draft

---

## Major Changes

### 1. New Entity Type: Module (Section 4.2.5)

Added complete Module entity specification including:

- **ModuleDefinition** schema with comprehensive attributes:
  - Identification and categorization
  - Interface specification (connector, pins, electrical characteristics)
  - Physical dimensions and mounting
  - Internal design reference
  - Functional capabilities
  - Power requirements
  - Thermal characteristics
  - Functional blocks within module
  - Semantic metadata
  - Procurement information
  - Design guidelines
  - Compliance and certification
  - AI metadata

- **Module Instance** pattern for using modules in parent designs
- **Multiple Module Instances** example showing redundant systems
- **Module Categories** taxonomy

### 2. Updated Core Entity Types (Section 3.2)

**Before:**
```
1. Design
2. Library
3. Component
4. Net
5. Pin
6. Constraint
7. Block
8. Port
```

**After:**
```
1. Design
2. Library
3. Component
4. Module - Physical separate PCB assembly (NEW)
5. Net
6. Pin
7. Constraint
8. Block - Functional grouping (clarified as logical)
9. Port
```

### 3. New Relationship Types (Section 3.2)

Added module-specific relationships:
- `contains` - Module contains internal design
- `instantiates` - Parent design instantiates module
- `interfaces_with` - Module interfaces with parent via connector

### 4. Module Taxonomy (Section 9.3)

Added complete module categorization:

```
module
├── som (System-on-Module)
├── memory (DIMM, SO-DIMM, etc.)
├── power (DC-DC, AC-DC, PoE modules)
├── wireless (WiFi, Bluetooth, Cellular, LoRa, Zigbee)
├── sensor (IMU, GPS, Camera, Environmental)
├── display (LCD, OLED, E-Paper, TFT)
├── interface (USB Hub, Ethernet PHY, CAN, RS485)
└── expansion (Arduino, Raspberry Pi HAT, MikroElektronika, PC104)
```

### 5. Motherboard Example Updates (Section 10.3.5)

Added new subsection **"Module Usage in Motherboard Design"** with:

- Industrial motherboard example with SoM integration
- Server motherboard with multiple module types
- Module integration benefits
- Key considerations for module integration
- AI reasoning examples with modules

Examples include:
- System-on-Module (i.MX8)
- M.2 WiFi module
- SO-DIMM memory module
- DC-DC power module
- Server VRM module
- DIMM/RDIMM modules
- OCP mezzanine network card
- M.2 NVMe storage

### 6. Updated Glossary (Section 9.5)

Added new terms:
- **Module**: Physical separate PCB assembly that integrates into parent design
- **Carrier Board**: Parent PCB that hosts one or more modules
- **System-on-Module (SoM)**: Complete computer system on a small PCB module

Updated existing term:
- **Functional Block**: Clarified as "logical grouping on same PCB" to distinguish from Module

### 7. Updated Table of Contents

Added detailed Data Models subsections:
```
4. Data Models
   - 4.1 Component Library Model
   - 4.2 Design Entity Models
      - 4.2.1 ComponentDefinition
      - 4.2.2 Net
      - 4.2.3 ComponentInstance
      - 4.2.4 FunctionalBlock
      - 4.2.5 Module **NEW**
   - 4.3 Constraint Model
```

---

## Key Benefits of Module Support

### 1. Hierarchical Design
Enables complex designs with modular architecture:
```
Motherboard
├── CPU SoM (200+ internal components)
├── Memory DIMM slots
├── WiFi Module
└── Power Supply Module
```

### 2. Abstraction Levels
- **Black Box**: Use module without knowing internal design
- **White Box**: AI can analyze internal design if available

### 3. Real-World Scenarios
- Raspberry Pi Compute Module
- Arduino shields
- M.2 WiFi/storage cards
- DIMM memory modules
- MikroElektronika Click boards
- PC/104 modules
- VRM modules
- OCP mezzanine cards

### 4. Design Complexity Reduction
- Carrier board design complexity: **reduced by 60-70%**
- Development time: **12 months → 3-4 months**
- Technical risk: **significantly reduced**

### 5. AI Capabilities
AI can now:
- Select appropriate modules based on requirements
- Reason about module interfaces and compatibility
- Optimize carrier board design knowing module internals
- Calculate system-level metrics across module boundaries
- Reuse pre-certified modules for compliance

---

## Schema Changes

### New Component Instance Type

Modules are instantiated using the existing ComponentInstance structure with `definitionType: "module"`:

```json
{
  "type": "ComponentInstance",
  "instanceId": "MOD1",
  "definitionId": "module_som_imx8",
  "definitionType": "module",  // Distinguishes from regular components
  "definition": {
    "$ref": "library/modules/som_imx8.json"
  }
}
```

### Module Interface Definition

New structured interface specification:

```json
{
  "interface": {
    "connectorType": "board_to_board_connector",
    "connectorMPN": "DF40C-100DP-0.4V",
    "pinCount": 100,
    "pins": [
      {
        "id": "1",
        "name": "VIN_5V",
        "electricalType": "power_input",
        "voltage": {"nominal": 5.0, "unit": "V"},
        "currentMax": {"value": 3.0, "unit": "A"}
      }
    ]
  }
}
```

### Internal Design Reference

Modules can reference their internal OpenPCBDB design:

```json
{
  "internalDesign": {
    "reference": "designs/som_imx8/som_imx8.opcbdb",
    "type": "opcbdb",
    "componentCount": 247,
    "netCount": 1053,
    "complexity": "high",
    "canBeOpened": true,
    "abstraction": "white_box"
  }
}
```

---

## Backward Compatibility

✅ **Fully backward compatible** with v1.0.0 designs

- Existing designs without modules continue to work unchanged
- Module support is additive, not breaking
- Tools can ignore module entities if not supported
- FunctionalBlock remains unchanged (clarified in documentation only)

---

## Migration Guide

### For Existing Designs

No migration required. Existing designs remain valid.

### For New Designs with Modules

1. Define modules in library:
   ```
   library/
   └── modules/
       ├── som_imx8.json
       ├── wifi_m2.json
       └── power_module.json
   ```

2. Instantiate modules in design:
   ```json
   {
     "components": [
       {
         "instanceId": "MOD1",
         "definitionType": "module",
         "definitionId": "som_imx8"
       }
     ]
   }
   ```

3. Connect module pins in nets:
   ```json
   {
     "nets": [
       {
         "connections": [
           {"component": "MOD1", "pin": "UART0_TX"}
         ]
       }
     ]
   }
   ```

---

## Implementation Notes

### For Tool Developers

1. **Parser Updates**: Add support for `definitionType: "module"` in component instances
2. **Module Library**: Implement module library loading and caching
3. **Hierarchy Navigation**: Support drilling into module internal design
4. **Connector Representation**: Handle module interface and pin mappings
5. **Abstraction Levels**: Support both black-box and white-box module views

### For AI Systems

1. **Module Selection**: Implement module search and recommendation
2. **Interface Matching**: Validate module compatibility with parent design
3. **Power Budget**: Calculate system power including all modules
4. **Thermal Analysis**: Consider module power dissipation
5. **Cost Optimization**: Compare module vs discrete component approaches

---

## Documentation Updates

### New Sections
- 4.2.5 Module (complete specification)
- 10.3.5 Module Usage in Motherboard Design (practical examples)

### Updated Sections
- 3.2 Core Entity Types (added Module)
- 9.3 Ontology and Taxonomy (added Module Categories)
- 9.5 Glossary (added Module-related terms)
- Table of Contents (expanded Data Models section)

### Enhanced Sections
- Section 10 examples now show realistic module integration

---

## Examples Provided

### 1. System-on-Module Definition
Complete ModuleDefinition for i.MX8 SoM with:
- 100-pin interface
- Power requirements
- Thermal specifications
- Internal functional blocks
- Design guidelines

### 2. Industrial Motherboard
Carrier board with:
- SoM for processing
- M.2 WiFi module
- SO-DIMM memory slot
- DC-DC power module

### 3. Server Motherboard
Complex design with:
- VRM modules
- Multiple DIMM slots
- OCP mezzanine network card
- M.2 NVMe storage

### 4. Redundant System
Dual SoM design with failover capability

---

## Future Considerations (Not in v1.1.0)

Potential future enhancements:
- Module compatibility database
- Automated module selection algorithms
- Module certification tracking
- Version compatibility matrices
- Module simulation models
- Standardized connector definitions

---

## Contributors

- Specification updates: Mintaka LLC, Armenia
- Module concept: Industry requirements for modular designs
- Use cases: Industrial motherboards, embedded systems, servers

---

## References

### Industry Standards
- OCP (Open Compute Project) specifications
- JEDEC memory module standards
- PCI-SIG M.2 specifications
- SGET SoM specifications

### Related OpenPCBDB Sections
- Section 4.2.4: FunctionalBlock (logical grouping)
- Section 4.2.5: Module (physical separation) **NEW**
- Section 10: Complex design examples

---

## Summary Statistics

**Lines Added**: ~850 lines  
**New Sections**: 2 major sections (4.2.5, 10.3.5)  
**Updated Sections**: 5 sections  
**New Taxonomy Categories**: 40+ module types  
**Code Examples**: 6 complete JSON examples  
**Python Examples**: 2 AI reasoning examples  

**Specification Size**: 2668 lines → 3522 lines (+32%)

---

**Version 1.1.0 Status**: Draft, ready for review  
**Next Version**: 1.2.0 (planned features TBD)

