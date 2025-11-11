# OpenPCBDB Specification Changelog - Version 1.2.0

## Summary

Added comprehensive **User Library Integration** support, enabling OpenPCBDB to connect with external component databases including SQL servers, SQLite files, REST APIs, and file-based systems. Components can now reference manufacturer IDs, part numbers, symbols, footprints, and mechanical models from user-managed libraries.

**Date**: 2025-11-11  
**Version**: 1.1.0 → 1.2.0  
**Status**: Draft

---

## Major Changes

### 1. New Section 4.4: User Library Integration

Complete specification for integrating OpenPCBDB with external user libraries:

#### 4.4.1 Library Configuration
- Support for multiple library types: SQL, SQLite, REST API, JSON
- Priority-based library search order
- Connection configuration for databases and APIs
- Authentication and security settings

#### 4.4.2 SQL Database Library Schema
Complete SQL schema specification including:
- Manufacturers table (`tbl_manufacturers`)
- Components table (`tbl_components`) with:
  - manufacturer_id, mpn, variant, revision
  - electrical_params (JSONB)
  - symbol_id, footprint_id, mechanical_id references
  - Approval workflow fields
  - Full-text search support
- Schematic symbols table (`tbl_schematic_symbols`)
- PCB footprints table (`tbl_pcb_footprints`)
- 3D mechanical models table (`tbl_3d_models`)
- Component relationships table (alternates, substitutions)
- Performance indexes

#### 4.4.3 SQLite Library Schema
Simplified schema for local/embedded libraries:
- Single-file database
- JSON stored as TEXT
- Optimized for local caching

#### 4.4.4 REST API Library Interface
Standard REST API endpoints:
```
GET    /api/v1/components
GET    /api/v1/components/:id
POST   /api/v1/components/search
GET    /api/v1/components/:id/symbol
GET    /api/v1/components/:id/footprint
GET    /api/v1/components/:id/mechanical
```

#### 4.4.5 Component Instance with Library References
Enhanced component instances with:
- `partNumber` object (manufacturer, manufacturerID, mpn, variant, revision)
- `userLibraryReferences` object with:
  - `primary`: Main library reference
  - `symbol`: Schematic symbol reference
  - `footprint`: PCB footprint reference
  - `mechanical`: 3D model reference
  - `fallback`: Alternative library source
- EDA tool mappings (KiCad, Altium)

#### 4.4.6 Library Synchronization
Configuration for bi-directional sync:
- Sync intervals (realtime, hourly, daily, manual)
- Conflict resolution strategies
- Caching mechanisms
- Multi-site synchronization

#### 4.4.7 Query Examples
Python code examples for:
- SQL library queries
- SQLite library queries
- REST API library queries

#### 4.4.8 Library Best Practices
- Library structure organization
- Naming conventions
- Approval workflows
- Multi-site synchronization patterns

### 2. Enhanced ComponentInstance (Section 4.2.2)

Added new fields to ComponentInstance:

```json
{
  "partNumber": {
    "manufacturer": "string",
    "manufacturerID": "string",
    "mpn": "string",
    "variant": "string",
    "revision": "string"
  },
  "userLibraryReferences": {
    "primary": {
      "libraryID": "string",
      "libraryType": "sql|sqlite|rest_api|json",
      "componentID": "string",
      "lastVerified": "timestamp",
      "approvalStatus": "string"
    },
    "symbol": {
      "libraryID": "string",
      "symbolID": "string",
      "symbolReference": "string"
    },
    "footprint": {
      "libraryID": "string",
      "footprintID": "string",
      "footprintReference": "string"
    },
    "mechanical": {
      "libraryID": "string",
      "modelID": "string",
      "mechanicalReference": "string",
      "format": "STEP|IGES|STL|WRL"
    }
  }
}
```

### 3. Updated Table of Contents

Added section 4.4 with 8 subsections:
- 4.4.1 Library Configuration
- 4.4.2 SQL Database Library Schema
- 4.4.3 SQLite Library Schema
- 4.4.4 REST API Library Interface
- 4.4.5 Component Instance with Library References
- 4.4.6 Library Synchronization
- 4.4.7 Query Examples
- 4.4.8 Library Best Practices

### 4. Updated Glossary (Section 9.5)

Added new terms:
- **User Library**: External component database managed by user/company
- **Library Reference**: Link from component instance to external library entry
- **Symbol Reference**: Schematic symbol representation identifier
- **Footprint Reference**: PCB footprint identifier
- **Mechanical Reference**: 3D model identifier
- **Manufacturer ID**: Unique identifier for component manufacturer
- **MPN**: Manufacturer Part Number
- **Approval Status**: Component qualification state
- **Library Synchronization**: Process of keeping libraries in sync

---

## Key Benefits

### For Companies
✅ **Approved Parts Management**: Maintain company-approved component databases  
✅ **Procurement Integration**: Direct link to purchasing systems via MPN  
✅ **Multi-Site Sync**: Synchronize libraries across global locations  
✅ **Approval Workflows**: Built-in component qualification process  
✅ **Version Control**: Track component revisions and updates  

### For Designers
✅ **Flexible Storage**: Use SQL, SQLite, REST API, or file-based libraries  
✅ **Symbol/Footprint Management**: Direct links to schematic symbols and PCB footprints  
✅ **3D Model Integration**: Reference mechanical models from library  
✅ **Fallback Libraries**: Multiple library sources for redundancy  
✅ **EDA Tool Compatibility**: Maps to KiCad, Altium, Eagle formats  

### For AI Systems
✅ **Component Discovery**: Query libraries for approved components  
✅ **Parametric Search**: Find components by electrical specifications  
✅ **Approval Status**: Check if components are qualified for use  
✅ **Alternative Finding**: Locate substitutes and alternates  
✅ **Cost Optimization**: Access procurement data for BOM optimization  

---

## Use Cases Enabled

### 1. Enterprise Component Management
```
Company SQL Database (PostgreSQL)
├── 50,000+ approved components
├── Custom approval workflow
├── Multi-site synchronization
├── Integration with ERP/PLM systems
└── Real-time availability checking
```

### 2. Local Development Cache
```
Local SQLite File
├── Cached approved components
├── Offline access
├── Fast queries
└── Syncs with central database
```

### 3. Vendor API Integration
```
Component Vendor REST API
├── Real-time pricing
├── Stock availability
├── Latest datasheets
└── Alternative suggestions
```

### 4. Legacy Library Support
```
Existing JSON/File-based Libraries
├── Import from KiCad
├── Import from Altium
├── Gradual migration to OpenPCBDB
└── Maintain compatibility
```

---

## Library Types Supported

| Type | Use Case | Connection | Performance |
|------|----------|------------|-------------|
| **SQL** | Enterprise, Multi-user | Network/TCP | High (indexed) |
| **SQLite** | Local, Embedded | File | Very High (local) |
| **REST API** | Vendor integration | HTTP/HTTPS | Medium (network) |
| **JSON** | Legacy, Simple | File system | High (cached) |

---

## Database Schema Highlights

### SQL Schema Features
- **Full-text Search**: Fast component searching with TSVECTOR
- **JSONB Parameters**: Flexible electrical parameter storage
- **Foreign Keys**: Maintain referential integrity
- **Indexes**: Optimized for common queries
- **Approval Workflow**: Built-in component qualification
- **Relationships**: Track alternates and substitutions

### SQLite Schema Features
- **Single File**: Easy backup and distribution
- **JSON as TEXT**: Simple parameter storage
- **Indexes**: Fast category and MPN lookups
- **Portable**: Works across platforms
- **No Server**: Embedded database

---

## API Integration

### REST API Endpoints
```
GET    /api/v1/components?category=passive.resistor&mpn=RC0603*
POST   /api/v1/components/search
GET    /api/v1/components/:id/symbol
GET    /api/v1/components/:id/footprint
GET    /api/v1/components/:id/mechanical
```

### Query Example
```python
library = openpcbdb.UserLibrary.connect(
    library_id="company_approved_parts",
    type="sql",
    host="db.company.com"
)

results = library.query("""
    SELECT * FROM tbl_components 
    WHERE category = 'passive.resistor'
      AND electrical_params->>'resistance' = '10000'
      AND approval_status = 'approved'
""")
```

---

## Synchronization Features

### Sync Modes
- **Read-Only**: Query library, no updates
- **Write-Only**: Push changes to library
- **Bidirectional**: Two-way synchronization

### Sync Intervals
- **Realtime**: Immediate synchronization
- **Hourly**: Scheduled hourly updates
- **Daily**: Daily batch synchronization
- **Manual**: On-demand synchronization

### Conflict Resolution
- **User Library Wins**: External library takes precedence
- **OpenPCBDB Wins**: Local changes take precedence
- **Manual**: User resolves conflicts

---

## Approval Workflow

### Component Lifecycle States
1. **Draft**: Initial entry, editable
2. **Pending Review**: Awaiting approval
3. **Approved**: Qualified for use in designs
4. **Obsolete**: End of life, discouraged

### Workflow Actions
- **Submit for Review**: Move from draft to pending
- **Approve**: Qualify component for use
- **Reject**: Decline component
- **Request Changes**: Send back for modifications
- **Mark Obsolete**: Flag end-of-life

---

## Migration Path

### From Existing Libraries

**Step 1: Connect Existing Library**
```json
{
  "libraryID": "existing_parts_db",
  "type": "sql",
  "connection": {
    "host": "current-db.company.com",
    "database": "parts"
  }
}
```

**Step 2: Map Schema**
```json
{
  "tables": {
    "components": "parts",
    "symbols": "schematic_symbols",
    "footprints": "pcb_footprints"
  }
}
```

**Step 3: Reference in Components**
```json
{
  "userLibraryReferences": {
    "primary": {
      "libraryID": "existing_parts_db",
      "componentID": "12345"
    }
  }
}
```

---

## Backward Compatibility

✅ **100% Backward Compatible** with v1.1.0

- Existing designs work unchanged
- `userLibraryReferences` is optional
- Components without library references remain valid
- No breaking changes to existing schemas

---

## Implementation Checklist

### For Tool Developers

**Phase 1: Basic Library Support**
- [ ] Parse library configuration
- [ ] Connect to SQL databases
- [ ] Connect to SQLite files
- [ ] Query components from libraries
- [ ] Display library-referenced components

**Phase 2: Advanced Features**
- [ ] REST API library integration
- [ ] Library synchronization
- [ ] Symbol/footprint/mechanical references
- [ ] Approval workflow integration
- [ ] Multi-library search

**Phase 3: Enterprise Features**
- [ ] Multi-site synchronization
- [ ] Conflict resolution
- [ ] Caching mechanisms
- [ ] Performance optimization
- [ ] Audit logging

---

## Documentation Updates

### New Sections
- 4.4 User Library Integration (complete specification)
- 4.4.1 through 4.4.8 (subsections)

### Updated Sections
- 4.2.2 ComponentInstance (added library references)
- Table of Contents (added section 4.4)
- 9.5 Glossary (added 9 new terms)

### Code Examples
- 3 Python query examples (SQL, SQLite, REST API)
- Complete SQL schema (~120 lines)
- Complete SQLite schema (~30 lines)
- Multiple JSON configuration examples

---

## Statistics

**Lines Added**: ~650 lines  
**New Sections**: 1 major section (4.4) with 8 subsections  
**Updated Sections**: 3 sections  
**New Glossary Terms**: 9 terms  
**Code Examples**: 10+ complete examples  
**SQL Schema**: 120 lines (PostgreSQL compatible)  
**SQLite Schema**: 30 lines  

**Specification Size**: 3502 lines → 4152 lines (+18%)

---

## Next Steps

### For v1.3.0 (Potential)
- EDA tool plugin specifications
- Visual library browser
- Component lifecycle management
- Automated BOM generation
- Supply chain integration
- Cost optimization algorithms

---

## Summary

Version 1.2.0 adds enterprise-grade component library management to OpenPCBDB:

✅ **SQL/SQLite Support**: Connect to company databases  
✅ **REST API Integration**: Link to vendor APIs  
✅ **Complete Schema**: Production-ready database design  
✅ **Approval Workflows**: Component qualification process  
✅ **Multi-Site Sync**: Global library synchronization  
✅ **Symbol/Footprint/3D**: Complete component references  
✅ **Backward Compatible**: No breaking changes  

**Version 1.2.0 is ready for enterprise deployment.**

---

**Date**: 2025-11-11  
**Author**: Mintaka LLC, Armenia  
**License**: CC BY 4.0 (documentation) / Apache 2.0 (code)  
**Status**: Draft, ready for implementation

