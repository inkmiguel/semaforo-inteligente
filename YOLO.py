"""Helpers around the Ultralytics YOLO model for vehicle counting."""

from typing import Callable, Iterator, Optional, Tuple

from ultralytics import YOLO
from ultralytics.engine.results import Results

model = YOLO("yolo11n.pt")

traffic_classes_id = [2, 3, 5, 7]


def car_count_stream(
    source: int | str = 0,
    show: bool = True,
    save: bool = False,
    verbose: bool = False,
) -> Iterator[Tuple[int, Results]]:
    """Yield the number of tracked vehicles for each processed frame."""

    tracking_iterator = model.track(
        source=source,
        show=show,
        save=save,
        verbose=verbose,
        classes=traffic_classes_id,
        stream=True,
        persist=True,
    )
    for result in tracking_iterator:
        detections = result.boxes
        vehicle_count = len(detections) if detections is not None else 0
        yield vehicle_count, result


def detect_cars(
    source: int | str = 0,
    show: bool = True,
    save: bool = False,
    verbose: bool = False,
    on_count: Optional[Callable[[int, Results], None]] = None,
) -> None:
    """Run tracking and invoke the optional callback with the latest vehicle count."""

    for count, result in car_count_stream(source, show, save, verbose):
        if on_count:
            on_count(count, result)


if __name__ == "__main__":
    detect_cars()