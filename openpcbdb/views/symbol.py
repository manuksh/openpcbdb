from __future__ import annotations

from typing import Any

from .base import View


class SymbolView(View):
    """Symbol view API for public cell ports."""

    def readPorts(self) -> list[dict[str, Any]]:
        """Read all symbol ports."""
        ports = self.data.get("ports", [])
        return list(ports) if isinstance(ports, list) else []

    def readPort(self, portName: str) -> dict[str, Any]:
        """Read one symbol port."""
        for port in self.readPorts():
            if port.get("id") == portName or port.get("name") == portName:
                return dict(port)
        raise KeyError(f"Port not found: {portName}")

    def createPort(
        self,
        portName: str,
        direction: str,
        electricalType: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a public symbol port."""
        ports = [port for port in self.readPorts() if port.get("id") != portName]
        port: dict[str, Any] = {
            "id": portName,
            "name": properties.get("name", portName) if properties else portName,
            "direction": direction,
            "electricalType": electricalType,
        }
        if properties:
            port.update(properties)
        ports.append(port)
        self.data["ports"] = ports
        self.save()
        return port

    def updatePort(self, portName: str, properties: dict[str, Any]) -> None:
        """Update a public symbol port."""
        ports = self.readPorts()
        for port in ports:
            if port.get("id") == portName:
                port.update(properties)
                self.data["ports"] = ports
                self.save()
                return
        raise KeyError(f"Port not found: {portName}")

    def deletePort(self, portName: str) -> None:
        """Delete a public symbol port."""
        self.data["ports"] = [port for port in self.readPorts() if port.get("id") != portName]
        self.save()
