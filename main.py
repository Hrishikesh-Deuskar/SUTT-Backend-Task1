
import json
import heapq
from datetime import datetime


class RideRequest:
    def __init__(self, name, destination, time_slot, year, order):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.order = order
        self.request_time = datetime.now()


class Cab:
    def __init__(self, cab_id, driver, capacity, destination, time_slot):
        self.cab_id = cab_id
        self.driver = driver
        self.capacity = capacity
        self.destination = destination
        self.time_slot = time_slot
        self.departed = False
        self.passengers = []


def load_cabs():
    cabs = []

    with open("cabs.json", "r") as file:
        data = json.load(file)

    ids = []

    for item in data:
        if item["cab_id"] in ids:
            raise ValueError("Duplicate cab ID.")

        ids.append(item["cab_id"])

        if not 1 <= item["capacity"] <= 4:
            raise ValueError("Cab capacity must be between 1 and 4.")

        if item["destination"] not in ["Delhi", "Jaipur"]:
            raise ValueError("Invalid cab destination.")

        if item["time_slot"] not in ["Morning", "Afternoon", "Evening", "Night"]:
            raise ValueError("Invalid cab time slot.")

        cab = Cab(
            item["cab_id"],
            item["driver"],
            item["capacity"],
            item["destination"],
            item["time_slot"]
        )

        cabs.append(cab)

    return cabs

queues = {}
request_number = 0


def add_request():
    global request_number

    print("\n--- Add Ride Request ---")

    name = input("Student name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    destination = input("Destination (Delhi/Jaipur): ").strip().title()

    if destination not in ["Delhi", "Jaipur"]:
        print("Invalid destination.")
        return

    time_slot = input(
        "Time slot (Morning/Afternoon/Evening/Night): "
    ).strip().title()

    if time_slot not in ["Morning", "Afternoon", "Evening", "Night"]:
        print("Invalid time slot.")
        return

    try:
        year = int(input("Year (1-5): "))
    except ValueError:
        print("Year must be a number.")
        return

    if year < 1 or year > 5:
        print("Year must be between 1 and 5.")
        return

    student = RideRequest(
        name,
        destination,
        time_slot,
        year,
        request_number
    )

    request_number += 1

    trip = (destination, time_slot)

    if trip not in queues:
        queues[trip] = []

    heapq.heappush(
        queues[trip],
        (-year, student.order, student)
    )

    print("Ride request added successfully!")


def view_status(cabs):
    print("\n--- Waiting Students ---")

    found = False

    for trip in queues:
        print("\nTrip:", trip[0], "-", trip[1])

        waiting = sorted(queues[trip])

        for entry in waiting:
            student = entry[2]

            print(
                student.name,
                "| Year:", student.year,
                "| Requested:", student.request_time.strftime("%H:%M:%S")
            )

            found = True

    if not found:
        print("No students waiting.")

    print("\n--- All Cabs ---")

    for cab in cabs:
        if cab.departed:
            status = "Departed"
        else:
            status = "Open"

        print(
            "\nCab:", cab.cab_id,
            "| Driver:", cab.driver,
            "| Destination:", cab.destination,
            "| Time:", cab.time_slot,
            "| Seats:", str(len(cab.passengers)) + "/" + str(cab.capacity),
            "| Status:", status
        )

        for student in cab.passengers:
            print("  Passenger:", student.name, "| Year:", student.year)


