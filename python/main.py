
from arduino.app_utils import App, Bridge
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import time
import csv
from pathlib import Path

TEST_NAME = "straight_position_testcsv"
DURATION = 10
SAMPLE_INTERVAL = 0.1

FIXED_R = 10000.0
ADC_MAX = 1023.0

OUTPUT_DIR = Path("/app/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

times = []
sensor_data = [[], [], [], []]

start_time = None
finished = False


def calculate_resistance(reading):
    if reading < 0 or reading >= ADC_MAX:
        return float("nan")

    return FIXED_R * reading / (ADC_MAX - reading)


def save_csv():
    file_path = OUTPUT_DIR / f"{TEST_NAME}.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Time (s)",
            "Sensor 1 (Ohms)",
            "Sensor 2 (Ohms)",
            "Sensor 3 (Ohms)",
            "Sensor 4 (Ohms)"
        ])

        for i in range(len(times)):
            writer.writerow([
                times[i],
                sensor_data[0][i],
                sensor_data[1][i],
                sensor_data[2][i],
                sensor_data[3][i]
            ])

    print(f"CSV saved: {file_path}", flush=True)


def save_plot():
    plt.figure(figsize=(12, 6))

    for i in range(4):
        plt.plot(
            times,
            sensor_data[i],
            label=f"Sensor {i + 1}"
        )

    plt.title(f"SpiRob Resistance vs Time - {TEST_NAME}")
    plt.xlabel("Time (s)")
    plt.ylabel("Resistance (Ohms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    file_path = OUTPUT_DIR / f"{TEST_NAME}.png"
    plt.savefig(file_path, dpi=300)
    plt.close()

    print(f"Plot saved: {file_path}", flush=True)


def loop():
    global start_time, finished

    if finished:
        time.sleep(1)
        return

    if start_time is None:
        start_time = time.monotonic()

    elapsed = time.monotonic() - start_time

    if elapsed >= DURATION:
        finished = True

        if times:
            save_csv()
            save_plot()

        return

    readings = [
        Bridge.call("get_sensor1"),
        Bridge.call("get_sensor2"),
        Bridge.call("get_sensor3"),
        Bridge.call("get_sensor4")
    ]

    times.append(elapsed)

    for i in range(4):
        resistance = calculate_resistance(int(readings[i]))
        sensor_data[i].append(resistance)

    time.sleep(SAMPLE_INTERVAL)


App.run(user_loop=loop)
