# How to Use OpenPCBDB Specification with AI

## Do I Need to Provide the Specification Every Time?

**No, you don't need to provide the full specification every time!**

## 📁 Best Approach: Keep It In Your Workspace

Since the specification file is already in your workspace at `specification/specification.md`, 
the AI can:

1. **Read it when needed** - Access it from your workspace files
2. **Reference it for schema details** - When generating designs
3. **Access it automatically** - It's part of your project files

### For Future Design Requests

Simply say:
- "Create a buck converter design following OpenPCBDB format"
- "Generate a USB power supply in .opcbdb format"
- "Design an LED driver circuit"

The AI will read the specification from your workspace to ensure correct format.

## 💡 Alternative Approaches

### Option 1: Condensed Schema Reference (Recommended)

Create a shorter file like `specification/QUICK_SCHEMA.md` with just the JSON structures:

```json
// Component Instance Template
{
  "type": "ComponentInstance",
  "refDesignator": "R1",
  "componentDefinitionId": "...",
  "partNumber": {...},
  "userLibraryReferences": {...},
  "semantic": {
    "purpose": "...",
    "function": "...",
    "reasoning": "..."
  }
}

// Net Template
{
  "type": "Net",
  "name": "VCC_5V",
  "semantic": {
    "type": "power",
    "purpose": "..."
  },
  "electricalCharacteristics": {...}
}
```

**Size**: ~50-100 lines instead of 4199 lines

### Option 2: JSON Schema Files

As mentioned in section 9.2 of the spec, create formal JSON Schema files:

```
schemas/
├── component-definition.schema.json
├── component-instance.schema.json
├── net.schema.json
├── module.schema.json
└── design.schema.json
```

### Option 3: Template Designs

Keep example designs in `examples/` directory:

```
examples/
├── minimal_design.opcbdb          # Bare minimum valid design
├── simple_led_blinker.opcbdb      # Basic example
├── buck_converter.opcbdb          # Power supply example
└── templates/
    └── design_template.opcbdb     # Starter template
```

## 🎯 What AI Actually Needs

### Essential (must know):
- ✅ Design requirements (what you want to build)
- ✅ JSON structure for entities (ComponentInstance, Net, etc.)
- ✅ Required fields (type, id, semantic, etc.)

### Nice to have (can look up):
- 📚 Component categories taxonomy
- 📚 Best practices and AI guidance fields
- 📚 Detailed examples and use cases

### Don't need every time:
- ❌ Full documentation prose
- ❌ Extensive examples for every entity type
- ❌ Complete ontology details
- ❌ Implementation chapters

## 🔄 Practical Workflow

### First Time (initial setup):
```
You: "Here's my OpenPCBDB specification"
AI: *reads and understands the format* ✅
```

### Future Design Requests:
```
You: "Create a 5V power supply design"
AI: *reads spec from workspace if needed*
    *generates design in correct format*
```

### Quick Designs:
```
You: "Add a resistor R5 (10kΩ) to existing design"
AI: *remembers the format from previous conversation*
    *or quickly checks the schema*
    *generates the component instance*
```

## 📝 Recommendation: Create Quick Reference

Create a minimal file for day-to-day use:

**`specification/DESIGN_SCHEMA.md`** (~100 lines):

```markdown
# OpenPCBDB Quick Schema Reference

## Design Structure
{
  "opcbdbVersion": "1.2.0",
  "design": {
    "metadata": { "name": "...", "version": "..." },
    "components": [ /* ComponentInstance objects */ ],
    "nets": [ /* Net objects */ ],
    "blocks": [ /* FunctionalBlock objects */ ]
  }
}

## ComponentInstance
{
  "type": "ComponentInstance",
  "refDesignator": "R1",
  "componentDefinitionId": "...",
  "partNumber": { "manufacturer": "...", "mpn": "..." },
  "semantic": { "purpose": "...", "reasoning": "..." }
}

## Net
{
  "type": "Net",
  "name": "VCC_5V",
  "semantic": { "type": "power", "purpose": "..." },
  "electricalCharacteristics": { "voltage": {...}, "current": {...} }
}
```

## ✅ Summary

**You don't need to provide the specification every time!**

- **Within a conversation**: AI already knows it
- **Future conversations**: AI can read it from your workspace
- **For quick designs**: A condensed schema reference is helpful
- **Best practice**: Keep the spec in workspace, optionally create quick reference

## 🚀 Quick Start Commands

### Create a New Design
```
"Create a [design type] with [requirements]"
Example: "Create a 3.3V voltage regulator with 1A output"
```

### Modify Existing Design
```
"Add [component] to [design file]"
Example: "Add a 10uF decoupling capacitor near U1"
```

### Validate Design
```
"Validate [design file] against OpenPCBDB spec"
Example: "Validate my_design.opcbdb"
```

### Generate Documentation
```
"Generate documentation for [design file]"
Example: "Create a BOM for power_supply.opcbdb"
```

## 📚 Reference Files Location

- Full Specification: `specification/specification.md` (4199 lines)
- Version: 1.2.0
- Date: 2025-11-11
- Author: Alla Vardumyan
- Company: Mintaka LLC, Armenia (www.mintaka-ai.com)

## 🔑 Key Features Available

1. **Component Library Integration**
   - SQL databases (PostgreSQL, MySQL)
   - SQLite files (local/embedded)
   - REST APIs (vendor integration)
   - JSON files (legacy support)

2. **Module Support**
   - System-on-Module (SoM)
   - Memory modules (DIMM, SO-DIMM)
   - Power modules
   - Wireless modules
   - Display modules

3. **User Library References**
   - ManufacturerID and Part Numbers
   - Symbol references
   - Footprint references
   - Mechanical (3D model) references

4. **Semantic Design Intent**
   - Purpose and function for every component
   - Design reasoning and alternatives considered
   - AI guidance and best practices
   - Critical component marking

## 💡 Tips for Best Results

1. **Be specific** about requirements (voltage, current, temperature range)
2. **Mention constraints** (cost, size, temperature rating)
3. **Specify critical features** (overcurrent protection, thermal shutdown)
4. **Reference existing designs** if building on previous work
5. **Ask for explanations** to understand AI reasoning

## 🆘 Getting Help

For detailed information on specific topics, refer to:
- Section 4.2: Component definitions and instances
- Section 4.4: User library integration
- Section 6: File formats and compression
- Section 9.5: Glossary of terms
- Section 10: Complex design examples

---

**Document**: HOWTO.md
**Created**: 2025-11-11
**Purpose**: Quick guide for using OpenPCBDB specification with AI
**Related**: specification/specification.md (v1.2.0)

