#Japhet Melquisedec D. Gonzales
#CS-241
def calc_taxi_fare(distance_km, travel_time_mins):
    base_fare = 40
    cost_per_minute = 2
    cost_per_km = 13.50
    
    total_fare = base_fare + (cost_per_minute * travel_time_mins) + (cost_per_km * distance_km)
    return round(total_fare, 2)

# I wanted the program to have input so it wont be hard coded like the example of copilot
try:
    distance = float(input("Please Enter the distance traveled (in kilometers): "))
    time = float(input("Please Enter the travel time (in minutes): "))
    fare = calc_taxi_fare(distance, time)
    print(f"The total fare for traveling {distance} km in {time} minutes is Php {fare:.2f}.")
except ValueError:
    print("Please enter valid numeric values for distance and time!")