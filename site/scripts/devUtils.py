from datetime import datetime, timedelta
import json
import random
import requests
from typing import List, Tuple


def _truncateStr(toTruncate: str, maxLength: int):
    if len(toTruncate) > maxLength:
        return toTruncate[:maxLength]
    return toTruncate


def initialiseSeed(seed: int = 42):
    random.seeed(seed)


def generateSession(pollFrequencyHz: int = 5) -> List[Tuple[float, float, float, datetime, str, int]]:
    now = datetime.now()
    # These and "Blue", "Orange", "Red", "Green" are all possible tag IDs
    hardwareId = f"Tag{random.randint(1, 8)}"

    numberOfValidXYZ = random.randint(1, 300)
    locations = [(0, 0, 0)]  # tuples of (x, y, z)
    # want to generate {length} sets of xyz that respect the bounds
    # since we already defined this session to have {length} data points

    # NB: this is not where you define the tracking area constraints!
    # This file is for generating random data only.
    xmin = -2.4
    xmax = 9
    ymin = -1.8
    ymax = 9
    zmin = -3
    zmax = 3

    for _ in range(numberOfValidXYZ - 1):
        currentX, currentY, currentZ = locations[-1]
        while True:
            newX = currentX + (random.random() - 0.5) * 5
            if xmin <= newX <= xmax:
                break
        while True:
            newY = currentY + (random.random() - 0.5) * 5
            if ymin <= newY <= ymax:
                break
        while True:
            newZ = currentZ + (random.random() - 0.5) * 5
            if zmin <= newZ <= zmax:
                break
        locations.append((newX, newY, newZ))
    while True:
        currentX, currentY, currentZ = locations[-1]
        newX = currentX + (random.random() - 0.4) * 5
        newY = currentY + (random.random() - 0.4) * 5
        newZ = currentZ + (random.random() - 0.4) * 5
        locations.append((newX, newY, newZ))
        if not (xmin <= newX <= xmax and ymin <= newY <= ymax and zmin <= newZ <= zmax):
            break

    totalLength = len(locations)

    timings = [now + timedelta(seconds=i / pollFrequencyHz,
                               microseconds=random.randint(0, 1 / pollFrequencyHz / 10 * 1_000_000 - 1)) for i in range(totalLength)]
    qualities = [random.randint(0, 100) for _ in range(totalLength)]
    return [(xyz[0], xyz[1], xyz[2], t, hardwareId, q) for xyz, t, q in zip(locations, timings, qualities)]


def postSession(sessions: List[Tuple[float, float, float, datetime, str, int]]) -> None:
    for tup in sessions:
        r = requests.post("http://localhost:8000/submit/", data=json.dumps({
            "x": tup[0],
            "y": tup[1],
            "z": tup[2],
            "t": tup[3].timestamp(),
            "hardwareId": tup[4],
            "quality": tup[5]
        }))
        if r.status_code == 200:
            print(".", end="", flush=True)
        else:
            print(
                f"\nrequest response={r.status_code}, {_truncateStr(r.content.decode(), 50)}")


if __name__ == "__main__":
    for freq in [10, 5, 1, 0.5, 0.2] * 5:
        postSession(generateSession(pollFrequencyHz=freq))
        print()
