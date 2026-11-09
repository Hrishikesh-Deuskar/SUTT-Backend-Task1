
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


def find_matches(cabs):
    print("\n--- Possible Cab Matches ---")

    temp_queues = {}

    for trip in queues:
        temp_queues[trip] = queues[trip].copy()

    open_cabs = 0

    for cab in cabs:
        if cab.departed:
            continue

        open_cabs += 1

        print("\nCab:", cab.cab_id, "| Driver:", cab.driver)
        print("Trip:", cab.destination, "-", cab.time_slot)

        trip = (cab.destination, cab.time_slot)

        if trip not in temp_queues:
            print("No students waiting for this trip.")
            continue

        temp_queue = temp_queues[trip]
        seats = cab.capacity - len(cab.passengers)

        count = 0

        while count < seats and len(temp_queue) > 0:
            entry = heapq.heappop(temp_queue)
            student = entry[2]

            print("  ", student.name, "| Year:", student.year)

            count += 1

        if count == 0:
            print("No students available.")

        print("Potential passengers:", count, "/", cab.capacity)

    if open_cabs == 0:
        print("No open cabs available.")

    print("\nThis was only a preview. No seats were assigned.")


def dispatch_cab(cabs):
    print("\n--- Dispatch Cab ---")

    destination = input(
        "Destination (Delhi/Jaipur): "
    ).strip().title()

    if destination not in ["Delhi", "Jaipur"]:
        print("Invalid destination.")
        return

    time_slot = input(
        "Time slot (Morning/Afternoon/Evening/Night): "
    ).strip().title()

    if time_slot not in ["Morning", "Afternoon", "Evening", "Night"]:
        print("Invalid time slot.")
        return

    trip = (destination, time_slot)

    available_cabs = []

    for cab in cabs:
        if cab.destination == destination and cab.time_slot == time_slot:
            if not cab.departed:
                available_cabs.append(cab)

    if len(available_cabs) == 0:
        print("No open cab available for this trip.")
        return

    if trip not in queues or len(queues[trip]) == 0:
        print("No students waiting for this trip.")
        return

    print("\nAvailable cabs:")

    for cab in available_cabs:
        print(
            "Cab:", cab.cab_id,
            "| Driver:", cab.driver,
            "| Capacity:", cab.capacity
        )

    try:
        cab_id = int(input("Enter cab ID to dispatch: "))
    except ValueError:
        print("Please enter a valid cab ID.")
        return

    selected_cab = None

    for cab in available_cabs:
        if cab.cab_id == cab_id:
            selected_cab = cab
            break

    if selected_cab is None:
        print("Invalid cab ID or cab already departed.")
        return

    seats = selected_cab.capacity - len(selected_cab.passengers)

    count = 0

    while count < seats and len(queues[trip]) > 0:
        entry = heapq.heappop(queues[trip])
        student = entry[2]

        selected_cab.passengers.append(student)

        count += 1

    selected_cab.departed = True

    print("\nCab dispatched successfully!")
    print("Cab:", selected_cab.cab_id)
    print("Driver:", selected_cab.driver)
    print("Passengers:", count, "/", selected_cab.capacity)

    for student in selected_cab.passengers:
        print("  ", student.name, "| Year:", student.year)

