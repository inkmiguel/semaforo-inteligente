import argparse
from time import perf_counter

from Trafic import traffic_lighst, traffic_lighst_enum, update_light_state
from YOLO import car_count_stream


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


def monitor_traffic(camera_light: traffic_lighst) -> None:
    """Open the webcam, run YOLO, and print the current traffic status for a chosen light."""

    print("Abriendo la cámara... cierra la ventana o presiona 'q' para terminar.")
    last_level: traffic_lighst_enum | None = None
    last_report_time = 0.0
    report_interval = 1.5

    for count, _ in car_count_stream():
        level, label = update_light_state(camera_light, count)
        now = perf_counter()
        should_report = level != last_level or (now - last_report_time) >= report_interval
        if should_report:
            light_label = camera_light.name.title()
            print(f"[{light_label}] Vehículos detectados: {count} -> {label}")
            last_level = level
            last_report_time = now


if __name__ == "__main__":
    cli_args = build_parser().parse_args()
    monitor_traffic(cli_args.light)
