
# SUTT Backend Task 1 - Cab Pool Matcher

A command-line Python application for matching BITS Pilani
students with cabs travelling to Delhi or Jaipur.

## Features

- Add student ride requests
- View waiting students and cabs
- Load cabs from a JSON file
- Preview cab matches without assigning seats
- Dispatch cabs
- Prioritise senior students
- First-come-first-served ordering within the same year
- Separate priority queues for each destination and time slot
- Input validation and error handling

## Technologies Used

- Python 3
- json
- heapq
- datetime

No external packages are required.

## How to Run

1. Install Python 3.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Run:

   python main.py

5. Use the terminal menu.

## Project Files

- main.py: Classes, menu, matching and dispatch logic
- cabs.json: Initial cab details
- README.md: Project documentation
- .gitignore: Git exclusions

## Cab Configuration

The program reads cab details from cabs.json.

Each cab contains:

- cab_id
- driver
- capacity (1 to 4)
- destination (Delhi or Jaipur)
- time_slot (Morning, Afternoon, Evening or Night)

Cabs are processed in the order they appear in the JSON file.

## Priority Queue Logic

A separate priority queue is maintained for each
destination and time-slot combination.

Each student is stored in the heap as:

    (-year, request_order, student)

Python's heapq is a min-heap.

Negative years ensure that fifth-year students have
the highest priority.

Request order ensures that students in the same year
are selected in first-come-first-served order.

## Find Matches

Find Matches copies the waiting queues and simulates
allocations without modifying the actual queues.

Students are not assigned seats during preview.

## Dispatch Cab

The operator selects a destination, time slot and cab.

The highest-priority waiting students are removed
from the actual queue and added to the selected cab.

The cab is marked as departed and cannot accept
new passengers.

## Edge Cases

### Half-empty cab

A cab may leave with fewer passengers than its capacity.

### No cabs left

Students can continue submitting requests.
They remain waiting until a suitable cab is available.
Dispatch shows a message if no open cab exists.

### Same-year students

A unique request number ensures that the student
who requested earlier gets priority.

### Empty waiting queue

Dispatch does not change any data if no students
are waiting for the selected trip.

### Invalid input

Invalid destinations, time slots, years and cab IDs
are handled with error messages.

## Time Complexity

Let n be the number of waiting students for a trip
and C be the number of cabs.

- Add one request: O(log n)
- Add 1,000 requests: O(1000 log 1000)
- Select up to 4 passengers: O(log n)
- Find an open cab: O(C)
- Complete dispatch: O(C + log n)

## Design Decisions

- Classes are used to represent students and cabs.
- Dictionaries group students by trip.
- Heaps provide efficient priority-based selection.
- Request numbers ensure fair tie-breaking.
- JSON keeps cab configuration separate from Python code.
- Previewing uses copies of queues to prevent data changes.
- The program uses a simple terminal menu.
