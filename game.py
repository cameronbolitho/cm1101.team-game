from map import locations
from items import items
from player import *
from gameparser import normalise_input
from time import sleep, clock


# Take timed input, timed in seconds.
def input_fast_enough(prompt, correct_input, max_time):
    # Record the time before and after the user types their input.
    start_time = clock()
    user_input = input(correct_input)
    end_time = clock()

    # Return True if they were fast enough and gave the correct input.
    time_taken = end_time - start_time
    if user_input == correct_input and time_taken <= max_time:
        return True
    else:
        return False


# Items in inventory
def list_of_items(items):

    # Create a string of items
    string_of_items = ""
    for item in items:
        if item != items[len(items) - 1]:
            string_of_items = string_of_items + item["name"] + ", "
        else:
            string_of_items = string_of_items + item["name"]
    return string_of_items


# Items in the location
def print_location_items(location):
    # If there are no items, 
    if location["items"] == []:
        return


# Print the current location
def print_location(location):

    # Introduce location
    print("You're currently located in the " + location["name"] + "...")
    # Describe location
    print(location["description"])
    print()
    # Display items in location
    print_location_items(location)


# Available exits
def exit_leads_to(exits, direction):
    return locations[exits[direction]]["name"]


# Valid exits
def is_valid_exit(chosen_exit, exits):

    return chosen_exit in exits


# Print exits
def print_exit(direction, leads_to):

    print("GO " + direction.upper() + " to " + leads_to + ".")


# Print menu
def print_menu(exits, location_items, inv_items):

    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    # Item options
    for item in location_items:
        print("TAKE " + item["id"].upper() + " to take " + item["name"] + ".")
    for item in inv_items:
        print("DROP " + item["id"].upper() + " to drop " + item["name"] + ".")

    print("What do you want to do?")


# Execute Functions
# Execute go
def execute_go(direction):
    global current_location
    if is_valid_exit(direction, current_location["exits"]):
        current_location = move(current_location["exits"], direction)
    else:
        print("You cannot go there.")

# Execute take
def execute_take(item_id):

    found = False

    for item in current_location["items"]:
        if item_id == item["id"] and inventory_mass(inventory) + item["mass"] <= max_mass:
            inventory.append(item)
            current_location["items"].remove(item)
            found = True
            print(item_id, " added to inventory")
# OPTIONAL - MASS CAPACITY FUNCTION
        elif inventory_mass(inventory) + item["mass"] > max_mass:
            print("You've reach your maximum mass capacity")
            # Display mass status
            print("You're carrying" + str(inventory_mass(inventory) +
                  item["mass"]) + "kg, this is too much!")
            return
    # Necessary reject
    if found == False:
        print("You cannot take that.")


# Execute drop
def execute_drop(item_id):

    success = False
    for items in inventory:
        if item_id == items["id"]:
            current_location["items"].append(items)
            inventory.remove(items)
            print(items["name"] + " dropped.")
            success = True
    if success == False:
        print("You cannot drop that.")


# Execute command
def execute_command(command):

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


# Inventory mass
def inventory_mass(inventory):

    # Original mass
    x = 0

    # Adding mass to the inventory
    for item in inventory:
        x += item["mass"]

    # Returning the new mass
    return x


# Menu
def menu(exits, location_items, inv_items):

    # Display menu
    print_menu(exits, location_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    # Return the input
    return normalised_user_input


# Print the player's health
def print_health():
    print("Your current health is " + str(health) + "/" + str(max_health) + ".")


# Move
def move(exits, direction):
    return locations[exits[direction]]


# Show opening text
def display_title_sequence():
    f = open("title.txt")

    # Print lines one at a time, separated with blank lines.
    for line in f:
        sleep(0.4)
        print(line[:-1])  # The last character will be a newline so shouldn't be printed.


# Allow the player to choose a character.
def choose_character():
    global inventory, max_mass, current_location, max_health, health
    # Ask the user who to play as, repeat as long as they give invalid input.
    choice = input("Would you like to play as Luke or Han?").lower().strip()
    while choice != "luke" and choice != "han":
        print("You can only choose Luke or Han.")
        choice = input("Would you like to play as Luke or Han?").lower().strip()
    
    if choice == "luke":
        inventory = luke_inventory
        max_mass = luke_max_mass
        current_location = luke_start_location
        max_health = luke_max_health
        health = luke_max_health
    elif choice == "han":
        inventory = han_inventory
        max_mass = han_max_mass
        current_location = han_start_location
        max_health = han_max_health
        health = han_max_health


# Main function
def main():
    # Introduction (ready to play etc)
    input("Press enter when you're ready to play")

    # Show the title sequence
    display_title_sequence()

    print()

    # Allow the user to select a character
    choose_character()

    while True:
        # Print status
        print_location(current_location)
        print_health()

        # Show possible actions
        command = menu(current_location["exits"],
                       current_location["items"], inventory)

        # Execute the user's commands
        execute_command(command)


if __name__ == "__main__":
    main()
