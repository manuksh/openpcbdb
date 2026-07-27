from __future__ import annotations

from typing import Any

from .base import View


class SchematicView(View):
    """Schematic view API for instances and nets."""

    def readInsts(self) -> list[dict[str, Any]]:
        """Read all schematic instances."""
        instances = self.data.get("instances", [])
        components = self.data.get("components", [])
        result: list[dict[str, Any]] = []
        if isinstance(instances, list):
            result.extend(instances)
        if isinstance(components, list):
            result.extend(components)
        return result

    def readInstances(self) -> list[dict[str, Any]]:
        """Read all schematic instances."""
        return self.readInsts()

    def readNets(self) -> list[dict[str, Any]]:
        """Read schematic nets."""
        nets = self.data.get("nets", [])
        return list(nets) if isinstance(nets, list) else []

    def readNet(self, netName: str) -> dict[str, Any]:
        """Read one schematic net by id or name."""
        for net in self.readNets():
            if net.get("id") == netName or net.get("name") == netName:
                return dict(net)
        raise KeyError(f"Net not found: {netName}")

    def createNet(
        self,
        netName: str,
        name: str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a schematic net."""
        nets = [net for net in self.readNets() if net.get("id") != netName]
        net: dict[str, Any] = {
            "id": netName,
            "name": name or netName,
            "connections": [],
        }
        if properties:
            net.update(properties)
        nets.append(net)
        self.data["nets"] = nets
        self.save()
        return net

    def connect(self, netName: str, connection: dict[str, Any]) -> None:
        """Add a connection to a schematic net."""
        nets = self.readNets()
        for net in nets:
            if net.get("id") == netName or net.get("name") == netName:
                connections = net.get("connections", [])
                if not isinstance(connections, list):
                    connections = []
                connections.append(connection)
                net["connections"] = connections
                self.data["nets"] = nets
                self.save()
                return
        raise KeyError(f"Net not found: {netName}")

    def disconnect(self, netName: str, connection: dict[str, Any]) -> None:
        """Remove a connection from a schematic net."""
        nets = self.readNets()
        for net in nets:
            if net.get("id") == netName or net.get("name") == netName:
                connections = net.get("connections", [])
                if isinstance(connections, list):
                    net["connections"] = [item for item in connections if item != connection]
                self.data["nets"] = nets
                self.save()
                return
        raise KeyError(f"Net not found: {netName}")

    def createCellInst(
        self,
        instName: str,
        libName: str,
        cellName: str,
        viewBinding: dict[str, str] | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a CellInstance."""
        instances = self.data.get("instances", [])
        if not isinstance(instances, list):
            instances = []
        instance: dict[str, Any] = {
            "id": instName,
            "type": "CellInstance",
            "library": libName,
            "cell": cellName,
        }
        if viewBinding:
            instance["viewBinding"] = viewBinding
        if properties:
            instance.update(properties)
        instances.append(instance)
        self.data["instances"] = instances
        self.save()
        return instance

    def createComponentInst(
        self,
        refDes: str,
        componentDefinitionId: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a ComponentInstance."""
        components = self.data.get("components", [])
        if not isinstance(components, list):
            components = []
        component: dict[str, Any] = {
            "type": "ComponentInstance",
            "refDesignator": refDes,
            "componentDefinitionId": componentDefinitionId,
        }
        if properties:
            component.update(properties)
        components.append(component)
        self.data["components"] = components
        self.save()
        return component
