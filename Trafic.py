"""Traffic helpers to translate raw vehicle counts into statuses."""

from enum import Enum
from typing import Dict, Tuple


class traffic_lighst(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class traffic_lighst_enum(Enum):
    NO_TRAFFIC = 0
    LIGHT_TRAFFIC = 1
    MODERATE_TRAFFIC = 2
    HEAVY_TRAFFIC = 3


traffic_status: Dict[traffic_lighst_enum, str] = {
    traffic_lighst_enum.NO_TRAFFIC: "No hay tráfico",
    traffic_lighst_enum.LIGHT_TRAFFIC: "Tráfico ligero",
    traffic_lighst_enum.MODERATE_TRAFFIC: "Tráfico moderado",
    traffic_lighst_enum.HEAVY_TRAFFIC: "Tráfico pesado",
}


traffic_light_state: Dict[traffic_lighst, traffic_lighst_enum] = {
    light: traffic_lighst_enum.NO_TRAFFIC for light in traffic_lighst
}


traffic_cycle_duration: Dict[traffic_lighst_enum, float] = {
    traffic_lighst_enum.NO_TRAFFIC: 0.0,
    traffic_lighst_enum.LIGHT_TRAFFIC: 10.0,
    traffic_lighst_enum.MODERATE_TRAFFIC: 20.0,
    traffic_lighst_enum.HEAVY_TRAFFIC: 35.0,
}


# Lighter bands sit first so the first match determines the level.
traffic_thresholds: Tuple[Tuple[traffic_lighst_enum, int], ...] = (
    (traffic_lighst_enum.NO_TRAFFIC, 0),
    (traffic_lighst_enum.LIGHT_TRAFFIC, 1),
    (traffic_lighst_enum.MODERATE_TRAFFIC, 2),
    (traffic_lighst_enum.HEAVY_TRAFFIC, 3),
)


def evaluate_traffic(count: int) -> Tuple[traffic_lighst_enum, str]:
    """Return the traffic enum and label that corresponds to a vehicle count."""

    sanitized_count = max(0, count)
    for level, max_value in traffic_thresholds:
        if sanitized_count <= max_value:
            return level, traffic_status[level]
    return traffic_lighst_enum.HEAVY_TRAFFIC, traffic_status[traffic_lighst_enum.HEAVY_TRAFFIC]


def update_light_state(light: traffic_lighst, count: int) -> Tuple[traffic_lighst_enum, str]:
    """Update the cached status for a given traffic light based on the latest count."""

    level, label = evaluate_traffic(count)
    traffic_light_state[light] = level
    return level, label


def get_light_status(light: traffic_lighst) -> traffic_lighst_enum:
    """Return the latest enum status for a specific traffic light."""

    return traffic_light_state[light]


def describe_light_status(light: traffic_lighst) -> str:
    """Return the human-friendly label for the current status of a traffic light."""

    return traffic_status[get_light_status(light)]


def get_cycle_duration(level: traffic_lighst_enum) -> float:
    """Return the timer duration (seconds) associated with a traffic level."""

    return traffic_cycle_duration[level]

