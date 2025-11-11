# OpenPCBDB - AI-Native PCB Design Database Standard

> An open, semantic-rich database standard for electronic circuit and PCB design, optimized for AI/ML workflows and human collaboration.

**License:** Apache 2.0 | **Status:** Draft (v0.1.0) | **Language:** JSON/YAML

---

## 🎯 What is OpenPCBDB?

**OpenPCBDB** is a comprehensive, open-source specification for representing electronic circuit designs and PCB layouts in a way that AI systems can understand, analyze, and reason about. Unlike traditional PCB formats that focus primarily on geometric data, OpenPCBDB captures the **semantic meaning**, **design intent**, and **functional relationships** within electronic designs.

### The Problem We Solve

Current PCB design formats (Gerber, ODB++, IPC-2581) are optimized for manufacturing machines, not for AI understanding. They represent *what* is on the board but not *why* it's there or *how* it works. This makes it nearly impossible for AI systems to:

- Understand design intent and functional purpose
- Perform intelligent design validation and optimization
- Learn from existing designs and transfer knowledge
- Assist engineers in design decisions
- Automate complex design tasks

**OpenPCBDB bridges this gap** by providing a rich, semantic data model where every component, net, and design decision is described with its purpose, function, and relationships.

---

## 🚀 Key Features

### 🤖 AI-Native Architecture
- **Semantic Data Model**: Captures design intent, not just geometry
- **Graph-Based Relationships**: Natural representation for Graph Neural Networks (GNNs)
- **ML-Ready Annotations**: Built-in fields for AI training and inference
- **Knowledge Transfer**: Enables AI to learn from one design and apply to others

### 📊 Rich Data Representation
- **Complete Component Definitions**: Electrical, physical, semantic, and procurement data
- **Functional Blocks**: Hierarchical design organization with purpose and relationships
- **Design Intent Capture**: Why decisions were made, alternatives considered, constraints applied
- **Multi-Domain Support**: Analog, digital, power, RF, high-speed signals

### 🔍 Intelligent Queryability
- **Python API**: Comprehensive programmatic access
- **REST/GraphQL APIs**: Web and cloud integration
- **Natural Language Queries**: AI can answer questions like "Why is R1 10kΩ?"
- **Design Pattern Recognition**: Identify common circuits and best practices

### 🎨 Human-Friendly
- **JSON/YAML Format**: Human-readable and version control friendly
- **Self-Documenting**: Embedded documentation and reasoning
- **Extensible**: Add custom fields without breaking compatibility
- **Open Standard**: Community-driven, vendor-neutral

### ⚡ Optimized for Scale
- **Compression Support**: Gzip/Zstandard for efficient storage
- **Reference Architecture**: Shared component libraries reduce redundancy
- **Minimal Mode**: Store only essential data, expand on-demand
- **Chunked Files**: Handle large designs efficiently

---

## 📚 Documentation Structure

The OpenPCBDB specification is organized into comprehensive chapters:

1. **Introduction** - Purpose, principles, and AI capabilities
2. **Scope and Objectives** - What OpenPCBDB covers and design goals
3. **Core Architecture** - Data model principles and graph structure
4. **Data Models** - Detailed schemas for all entities
   - Component Definitions and Instances
   - Nets, Pins, and Connections
   - Functional Blocks
   - PCB Physical Data
5. **API Specification** - Python, REST, and GraphQL interfaces
6. **File Format** - JSON structure, versioning, compression
7. **AI/ML Integration** - Training data, feature extraction, GNN support
8. **Reference Implementation** - Python library and examples
9. **Appendices** - Design patterns, best practices, migration guides
10. **Complex Design Support** - Motherboard and high-speed examples
11. **Future Extensions** - Roadmap and planned features

---

## 🏁 Quick Start

### Example: Component Definition

```json
{
  "type": "ComponentDefinition",
  "id": "res_0603_10k_1pct",
  "identification": {
    "name": "Resistor 10kΩ ±1% 0603",
    "category": "passive.resistor",
    "manufacturer": "Yageo",
    "mpn": "RC0603FR-0710KL"
  },
  "parameters": {
    "resistance": {
      "value": 10000,
      "unit": "ohm",
      "tolerancePercent": 1
    },
    "powerRating": {
      "value": 0.1,
      "unit": "W"
    }
  },
  "semantic": {
    "function": "current_limiting",
    "typicalUseCases": [
      "pull_up_resistor",
      "voltage_divider",
      "current_limiting"
    ],
    "domain": "analog",
    "aiNotes": "General purpose resistor, suitable for most applications"
  }
}
```

### Example: Semantic Net

```json
{
  "type": "Net",
  "id": "net_vcc_5v",
  "name": "VCC_5V",
  "semantic": {
    "type": "power",
    "subType": "supply",
    "purpose": "Main 5V power rail for digital circuitry",
    "function": "Supplies power to MCU and peripheral ICs",
    "critical": true,
    "source": {
      "component": "U2",
      "pin": "out",
      "type": "switching_regulator"
    }
  },
  "electricalCharacteristics": {
    "nominalVoltage": 5.0,
    "tolerancePercent": 5,
    "maxCurrent": 2.0,
    "maxRipple": 0.05
  },
  "aiAnnotations": {
    "patternType": "power_distribution_network",
    "commonIssues": [
      "insufficient_decoupling",
      "voltage_drop_on_long_traces"
    ]
  }
}
```

---

## 🔧 Use Cases

### For AI Systems
- **Design Understanding**: Parse and comprehend existing designs
- **Automated Validation**: Check for design rule violations and best practices
- **Design Generation**: Create new circuits based on specifications
- **Optimization**: Improve designs for cost, performance, or reliability
- **Knowledge Extraction**: Learn patterns from thousands of designs

### For Engineers
- **Design Documentation**: Self-documenting designs with embedded reasoning
- **Knowledge Transfer**: Understand why decisions were made
- **Collaboration**: Share designs with complete context
- **Design Reuse**: Find and adapt proven circuit patterns
- **AI Assistance**: Get intelligent suggestions and validation

### For Organizations
- **IP Management**: Capture and preserve design knowledge
- **Standardization**: Enforce design standards and best practices
- **Training**: Teach new engineers from documented examples
- **Quality**: Ensure consistency across projects
- **Analytics**: Gain insights from design data

---

## 🛠️ Implementation Status

- ✅ Core specification (v0.1.0)
- ✅ Data model schemas
- ✅ API specification
- 🚧 Python reference implementation (in progress)
- 🚧 Component library examples (in progress)
- 📋 REST API implementation (planned)
- 📋 GNN integration examples (planned)
- 📋 Migration tools from legacy formats (planned)

---

## 📖 Reading the Specification

The complete specification is in [`specification.md`](specification.md) - a comprehensive technical document covering:

- **2,662 lines** of detailed specification
- Complete data models with JSON examples
- API definitions and usage patterns
- AI/ML integration guidelines
- Real-world design examples (including motherboards)
- Best practices and design patterns

**Start here**: Read Chapter 1 (Introduction) to understand the AI-native philosophy, then explore the data models in Chapter 4.

---

## 🤝 Contributing

We welcome contributions from the community! This is an open standard that benefits from diverse perspectives.

### How to Contribute

1. **Feedback**: Open issues with suggestions, questions, or concerns
2. **Use Cases**: Share your design scenarios and requirements
3. **Examples**: Contribute example designs in OpenPCBDB format
4. **Implementation**: Help build parsers, converters, and tools
5. **Documentation**: Improve explanations, add tutorials, fix typos

### Discussion Topics

- Additional data model fields for specific domains (RF, power electronics, etc.)
- Compression and optimization strategies
- AI/ML workflow integration
- Migration tools from existing formats
- Industry-specific requirements

---

## 🌟 Design Philosophy

### 1. AI-First, Human-Friendly
Designed primarily for machine reasoning, but remains human-readable and understandable.

### 2. Semantic Completeness
Capture not just *what* is in the design, but *why* and *how* it works.

### 3. Evolutionary
Extensible architecture that can grow with technology without breaking compatibility.

### 4. Open and Collaborative
Community-driven standard, free from vendor lock-in.

### 5. Practical
Balances theoretical completeness with real-world usability and performance.

---

## 🎓 Learning Resources

- **[Specification](specification.md)**: Complete technical specification
- **[Concept Document](concept.txt)**: Original vision and motivation
- **Examples**: Coming soon - sample designs in OpenPCBDB format
- **Tutorials**: Coming soon - step-by-step guides
- **API Reference**: Coming soon - detailed API documentation

---

## 📊 Comparison with Other Formats

| Feature | OpenPCBDB | Gerber | ODB++ | IPC-2581 |
|---------|-----------|--------|-------|----------|
| Semantic Data | ✅ Rich | ❌ None | ⚠️ Limited | ⚠️ Limited |
| Design Intent | ✅ Full | ❌ None | ❌ None | ❌ None |
| AI-Friendly | ✅ Native | ❌ No | ❌ No | ⚠️ Partial |
| Human-Readable | ✅ Yes | ❌ No | ❌ No | ⚠️ Complex |
| Version Control | ✅ Friendly | ⚠️ Binary | ❌ Binary | ⚠️ XML |
| Manufacturing | 🚧 Planned | ✅ Standard | ✅ Yes | ✅ Yes |
| Component Data | ✅ Complete | ❌ None | ⚠️ Basic | ⚠️ Basic |
| Open Standard | ✅ Yes | ✅ Yes | ❌ Proprietary | ✅ Yes |

**Note**: OpenPCBDB is designed to *complement* manufacturing formats, not replace them. It focuses on the design and engineering phase.

---

## 🔮 Roadmap

### Version 0.2 (Q2 2025)
- Python reference implementation
- Component library with 1000+ common parts
- Gerber export capability
- Example designs (power supply, IoT device, etc.)

### Version 0.3 (Q3 2025)
- REST API implementation
- GraphQL query interface
- GNN training examples
- Design validation rules engine

### Version 1.0 (Q4 2025)
- Stable specification
- Full manufacturing output support
- Industry adoption and feedback
- Certification program for tools

---

## 📄 License

This specification is released under the **MIT License**, making it free to use, modify, and distribute.

```
Copyright (c) 2025 OpenPCBDB Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this specification and associated documentation files, to deal in the
specification without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the specification, and to permit persons to whom the specification
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the specification.
```

---

## 💬 Community

- **Issues**: [GitHub Issues](https://github.com/yourusername/OpenPCBDB/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/OpenPCBDB/discussions)
- **Email**: openpcbdb@example.com

---

## 🙏 Acknowledgments

This project builds upon decades of PCB design knowledge and recent advances in AI/ML. We thank the broader electronics and AI communities for their inspiration and contributions.

Special recognition to the teams behind OpenAccess (IC design), which demonstrated the value of open standards in EDA.

---

## ⚠️ Status Note

**OpenPCBDB is currently in DRAFT status (v0.1.0)**. The specification is under active development and may change based on community feedback. We encourage early adopters to experiment and provide feedback, but production use should wait for v1.0.

---

**Star ⭐ this repository if you believe in open, AI-friendly standards for PCB design!**

For questions, suggestions, or collaboration opportunities, please open an issue or start a discussion.
