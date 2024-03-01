import random
import math

def linear_probabilities(distance):
    if distance <= 5:
        return 0.8 + (0.99 - 0.8) * (5 - distance) / 5  
    elif distance <= 12:
        return 0.99 - (0.49 / 7) * (distance - 5)  
    else:
        return max(0.3, 0.99 - (0.69 / 88) * (distance - 12))  


def simulate_infection(days):
    infected_people = set([(0, 0)])  

    for day in range(days):
        new_infections = set()

        for person in infected_people:
    
            distance = random.choices(list(range(1, 21)), weights=[linear_probabilities(d) for d in range(1, 21)])[0]
            
            angle = random.uniform(0, 2 * math.pi)
            
            new_x = person[0] + distance * math.cos(angle)
            new_y = person[1] + distance * math.sin(angle)
            new_location = (new_x, new_y)
            
            new_infections.add(new_location)

        infected_people.update(new_infections)

    return infected_people


def calculate_lockdown_circumference(infected_people):
    max_distance = 0
    for person in infected_people:
        distance_from_home = math.sqrt(person[0]**2 + person[1]**2)
        max_distance = max(max_distance, distance_from_home)
    return 2 * math.pi * max_distance

if __name__ == "__main__":
    
    distances_probabilities = {
        5: 0.8,
        8: 0.5,
        12: 0.3
    }


    def interpolate_probabilities(start_distance, end_distance, start_probability, end_probability):
        probabilities = {}
        for distance in range(start_distance, end_distance + 1):
            weight = (distance - start_distance) / (end_distance - start_distance)
            probability = start_probability + weight * (end_probability - start_probability)
            probabilities[distance] = probability
        return probabilities


    interpolated_probabilities = {}
    distances = list(distances_probabilities.keys())
    for i in range(len(distances) - 1):
        start_distance = distances[i]
        end_distance = distances[i + 1]
        start_probability = distances_probabilities[start_distance]
        end_probability = distances_probabilities[end_distance]
        interpolated_probabilities.update(interpolate_probabilities(start_distance, end_distance, start_probability, end_probability))

    
    distances_probabilities.update(interpolated_probabilities)

    
    distances_probabilities = dict(sorted(distances_probabilities.items()))


    for distance, probability in distances_probabilities.items():
        print("Distance {}: Probability {}".format(distance, probability))

    
    num_days = int(input("Enter the number of days for simulation: "))

    
    infected_people = simulate_infection(num_days)

    
    lockdown_circumference = calculate_lockdown_circumference(infected_people)

    print("Circumference needed for lockdown after", num_days, "days:", lockdown_circumference)

