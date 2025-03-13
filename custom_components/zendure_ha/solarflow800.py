import logging
from typing import Any, Callable
from homeassistant.core import HomeAssistant
from homeassistant.components.number import NumberMode
from .const import DOMAIN
from .zenduredevice import ZendureDevice

_LOGGER = logging.getLogger(__name__)


class SolarFlow800(ZendureDevice):
    def __init__(self, hass: HomeAssistant, h_id: str, h_prod: str, name: str) -> None:
        """Initialise SolarFlow800."""
        super().__init__(hass, h_id, h_prod, name, "SolarFlow 800")

    def sensorsCreate(self) -> None:
        binairies = [
            self.binary("masterSwitch", "Master Switch", None, None, "switch"),
            self.binary("buzzerSwitch", "Buzzer Switch", None, None, "switch"),
            self.binary("wifiState", "WiFi State", None, None, "switch"),
            self.binary("heatState", "Heat State", None, None, "switch"),
            self.binary("reverseState", "Reverse State", None, None, "switch"),
        ]
        self.async_add_entities(binairies)

        numbers = [
            self.number("outputLimit", "Output Limit", None, "W", "power", 0, 800, NumberMode.SLIDER),
            self.number("inputLimit", "Input Limit", None, "W", "power", 0, 1200, NumberMode.SLIDER),
        ]
        self.async_add_entities(numbers)

        switches = [
            self.switch("lampSwitch", "Lamp Switch", None, None, "switch"),
        ]
        self.async_add_entities(switches)

        sensors = [
            self.sensor("chargingMode", "Charging Mode"),
            self.sensor("hubState", "Hub State"),
            self.sensor("solarInputPower", "Solar Input Power", None, "W", "power"),
            self.sensor("packInputPower", "Pack Input Power", None, "W", "power"),
            self.sensor("outputPackPower", "Output Pack Power", None, "W", "power"),
            self.sensor("outputHomePower", "Output Home Power", None, "W", "power"),
            self.sensor("remainOutTime", "Remain Out Time", None, "min", "duration"),
            self.sensor("remainInputTime", "Remain Input Time", None, "min", "duration"),
            self.sensor("packNum", "Pack Num", None),
            self.sensor("electricLevel", "Electric Level", None, "%", "battery"),
            self.sensor("socSet", "socSet", "{{ value | int / 10 }}", "%"),
            self.sensor("minSoc", "minSOC", "{{ value | int / 10 }}", "%"),
            self.sensor("inverseMaxPower", "Inverse Max Power", None, "W"),
            self.sensor("gridInputPower", "grid Input Power", None, "W", "power"),
            self.sensor("pass", "Pass Mode", None),
            self.sensor("strength", "WiFi strength", None),
            self.sensor("hyperTmp", "Hyper Temperature", "{{ (value | float/10 - 273.15) | round(2) }}", "°C", "temperature"),
            self.sensor(
                "acMode",
                "AC Mode",
                """{% set u = (value | int) %}
                {% set d = {
                0: 'None',
                1: "AC input mode",
                2: "AC output mode" } %}
                {{ d[u] if u in d else '???' }}""",
            ),
            self.sensor(
                "autoModel",
                "Auto Model",
                """{% set u = (value | int) %}
                {% set d = {
                0: 'Nothing',
                6: 'Battery priority mode',
                7: 'Appointment mode',
                8: 'Smart Matching Mode',
                9: 'Smart CT Mode',
                10: 'Electricity Price' } %}
                {{ d[u] if u in d else '???' }}""",
            ),
            self.sensor(
                "packState",
                "Pack State",
                """{% set u = (value | int) %}
                {% set d = {
                0: 'Sleeping',
                1: 'Charging',
                2: 'Discharging' } %}
                {{ d[u] if u in d else '???' }}""",
            ),
        ]
        self.async_add_entities(sensors)
