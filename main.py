
import json
import math
import random
import csv


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def ascii_route(agent, warehouse, destination):
    print("\nASCII Route Visualization")
    print(f"{agent} ---> {warehouse} ---> {destination}")


def find_nearest_agent(warehouse_location, agents):
    nearest_agent = None
    minimum_distance = float('inf')

    for agent in agents:
        distance = euclidean_distance(agent["location"], warehouse_location)

        if distance < minimum_distance:
            minimum_distance = distance
            nearest_agent = agent

    return nearest_agent, minimum_distance


def export_best_agent_csv(best_agent, report):
    with open("best_agent.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Agent ID",
            "Packages Delivered",
            "Total Distance",
            "Efficiency"
        ])

        writer.writerow([
            best_agent,
            report[best_agent]["packages_delivered"],
            report[best_agent]["total_distance"],
            report[best_agent]["efficiency"]
        ])


def simulate_delivery(data):

    warehouses = {
        warehouse["id"]: warehouse["location"]
        for warehouse in data["warehouses"]
    }

    agents = data["agents"]
    packages = data["packages"]

    report = {}

    for agent in agents:
        report[agent["id"]] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "efficiency": 0.0,
            "delays": 0
        }

    # Dynamic Agent Joining
    new_agent = {
        "id": "A4",
        "location": [20, 20]
    }

    agents.append(new_agent)

    report[new_agent["id"]] = {
        "packages_delivered": 0,
        "total_distance": 0.0,
        "efficiency": 0.0,
        "delays": 0
    }

    print("\nNew Agent Joined Mid-Day: A4")

    for package in packages:

        warehouse_id = package["warehouse_id"]
        warehouse_location = warehouses[warehouse_id]

        nearest_agent, agent_distance = find_nearest_agent(
            warehouse_location,
            agents
        )

        delivery_distance = euclidean_distance(
            warehouse_location,
            package["destination"]
        )

        total_distance = agent_distance + delivery_distance

        # Random Delivery Delay
        delay = random.choice([0, 5, 10])

        if delay > 0:
            print(f"Package {package['id']} delayed by {delay} minutes")

        total_distance += delay

        agent_id = nearest_agent["id"]

        report[agent_id]["packages_delivered"] += 1
        report[agent_id]["total_distance"] += total_distance

        if delay > 0:
            report[agent_id]["delays"] += 1

        ascii_route(
            agent_id,
            warehouse_id,
            package["destination"]
        )

    for agent_id in report:

        packages_delivered = report[agent_id]["packages_delivered"]
        total_distance = report[agent_id]["total_distance"]

        if packages_delivered > 0:
            report[agent_id]["efficiency"] = round(
                total_distance / packages_delivered,
                2
            )

        report[agent_id]["total_distance"] = round(total_distance, 2)

    best_agent = min(
        report,
        key=lambda agent: (
            report[agent]["efficiency"]
            if report[agent]["packages_delivered"] > 0
            else float('inf')
        )
    )

    report["best_agent"] = best_agent

    export_best_agent_csv(best_agent, report)

    return report


def save_report(report, output_file):
    with open(output_file, 'w') as file:
        json.dump(report, file, indent=4)


def main():

    input_file = "base_case.json"
    output_file = "report.json"

    try:
        data = load_data(input_file)

        report = simulate_delivery(data)

        save_report(report, output_file)

        print("\nSimulation Completed Successfully!")
        print(json.dumps(report, indent=4))

    except FileNotFoundError:
        print("Input JSON file not found.")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
