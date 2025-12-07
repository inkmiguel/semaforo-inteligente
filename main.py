import argparse
from time import perf_counter

from Trafic import get_cycle_duration, traffic_lighst, traffic_lighst_enum, update_light_state
from YOLO import car_count_stream


LIGHT_SEQUENCE = tuple(traffic_lighst)
LIGHT_INDEX = {light: idx for idx, light in enumerate(LIGHT_SEQUENCE)}


def parse_camera_light(argument: str) -> traffic_lighst:
    normalized = argument.strip().upper()
    try:
        return traffic_lighst[normalized]
    except KeyError as exc:
        valid = ", ".join(light.name.title() for light in traffic_lighst)
        raise argparse.ArgumentTypeError(f"Valor inválido '{argument}'. Usa uno de: {valid}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Monitorea el tráfico detectado por YOLO para un semáforo específico."
    )
    parser.add_argument(
        "--light",
        type=parse_camera_light,
        default=traffic_lighst.NORTH,
        help="Semáforo donde está colocada la cámara (North, South, East, West).",
    )
    return parser


def advance_light(current: traffic_lighst, steps: int = 1) -> traffic_lighst:
    idx = LIGHT_INDEX[current]
    return LIGHT_SEQUENCE[(idx + steps) % len(LIGHT_SEQUENCE)]


def skip_next_lights(current: traffic_lighst, total: int = 3) -> traffic_lighst:
    for _ in range(total):
        current = advance_light(current)
        print(f"Saltando {current.name.title()} por falta de tráfico.")
    print(f"Reanudando monitoreo en {current.name.title()}.")
    return current


def monitor_traffic(camera_light: traffic_lighst) -> None:
    """Open the webcam, run YOLO, and print the current traffic status for a chosen light."""

    print("Abriendo la cámara... cierra la ventana o presiona 'q' para terminar.")
    active_light = camera_light
    last_level: traffic_lighst_enum | None = None
    last_report_time = 0.0
    report_interval = 1.5
    cycle_end = perf_counter()

    for count, _ in car_count_stream():
        level, label = update_light_state(active_light, count)
        now = perf_counter()
        duration = get_cycle_duration(level)
        if level != last_level and duration > 0:
            cycle_end = now + duration
        remaining = max(0.0, cycle_end - now) if duration > 0 else 0.0
        should_report = level != last_level or (now - last_report_time) >= report_interval
        if should_report:
            light_label = active_light.name.title()
            timer_msg = "sin tiempo asignado" if duration <= 0 else f"restante {remaining:.1f}s"
            print(f"[{light_label}] Vehículos detectados: {count} -> {label} ({timer_msg})")
            last_level = level
            last_report_time = now

        if level == traffic_lighst_enum.NO_TRAFFIC:
            active_light = skip_next_lights(active_light)
            cycle_end = perf_counter()
            last_level = None
            continue

        if duration > 0 and remaining <= 0:
            active_light = advance_light(active_light)
            cycle_end = perf_counter()
            last_level = None
            print(f"Cambio de turno -> {active_light.name.title()}")


if __name__ == "__main__":
    cli_args = build_parser().parse_args()
    monitor_traffic(cli_args.light)
