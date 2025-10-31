import time
import sys
import os
import random

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slowly(text, delay=0.03):
    """Prints text one character at a time for a dramatic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def press_enter_to_continue():
    """Waits for the user to press Enter."""
    input("\n[Press Enter to continue...]")

# --- ASCII ART ---

TITLE_ART = r"""
===================================================================
__________.__            __  .__         __________                    
\______   \  |__   _____/  |_|__| ____   \____    /____   ____   ____  
 |     ___/  |  \ /  _ \   __\  |/ ___\    /     //  _ \ /    \_/ __ \ 
 |    |   |   Y  (  <_> )  | |  \  \___   /     /(  <_> )   |  \  ___/ 
 |____|   |___|  /\____/|__| |__|\___  > /_______ \____/|___|  /\___  >
               \/                    \/          \/          \/     \/ 

                  T H E   T R A I L
===================================================================
"""

PLANKTON_ART = r"""
        ,
       / \
      / _ \
     | / \ |
     | \_/ |
      \ _ /
       \ /
        '
"""

# --- GAME OVER / WIN ---

def game_over(message):
    """Handles the game over sequence."""
    clear_screen()
    print_slowly("...GAME OVER...")
    print("\n=======================================================")
    print_slowly(message)
    print("=======================================================\n")
    print_slowly(f"You survived for {player_stats['day']} days.")
    print_slowly(f"You reached a final depth of {player_stats['depth']} meters.")

def game_win():
    """Handles the win sequence."""
    clear_screen()
    print_slowly("...YOU'VE REACHED THE PHOTIC ZONE!...")
    print("\n=======================================================")
    print_slowly(f"You are bathed in glorious, life-giving sunlight at {player_stats['depth']}m.")
    print_slowly("You can photosynthesize, grow, and divide.")
    print_slowly("Your perilous journey is over. You have succeeded!")
    print_slowly(f"It took you {player_stats['day']} days to reach the photic zone.")

# --- NEW HELPER FUNCTION ---
def get_choice_input(prompt, options):
    """Gets a valid numbered choice from the user."""
    print_slowly(prompt)
    for i, option in enumerate(options):
        print(f"  {i + 1}. {option}")
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(options)}): ")
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num - 1 # Return 0-based index
            else:
                print(f"That is not a valid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- RANDOM EVENTS ---

def event_copepod(stats):
    """A grazer attacks!"""
    print_slowly("!!! A COPEPOD !!!")
    
    # Check for Cyst Form
    if stats['cyst_form_ready']:
        choice_idx = get_choice_input("Your Cyst Form is ready! Use it to block the attack?", ["Yes, use it!", "No, save it."])
        if choice_idx == 0:
            stats['cyst_form_ready'] = False
            print_slowly("You form a hard cyst! The copepod bumps uselessly off you and leaves.")
            return stats # Exit event early

    print_slowly("A massive, hungry grazer lunges at you from the gloom!")
    energy_loss = random.randint(20, 35)
    
    # Check for Toxin Defense
    if 'toxin_defense' in stats['upgrades']:
        energy_loss = int(energy_loss * 0.6)
        print_slowly("Your toxins make the copepod recoil! Reduced damage.")
        
    stats['energy'] -= energy_loss
    print_slowly(f"You expend {energy_loss} energy in a desperate evasion maneuver and escape!")
    return stats

def event_virus(stats):
    """A virus attacks!"""
    print_slowly("!!! A VIRUS ATTACKS !!!")
    print_slowly("A giant virus, a relative of 'V-27', latches onto your cell wall!")
    
    base_chance = 0.5 # Base chance of infection
    
    if 'viral_resistance' in stats['upgrades']:
        base_chance -= 0.2
    if stats.get('virophage') == 'active':
        base_chance = 0.1 # Virophage is very effective
        
    if random.random() < base_chance:
        energy_loss = random.randint(15, 30)
        stats['energy'] -= energy_loss
        print_slowly(f"Your internal defenses fight it off, but it costs you {energy_loss} energy.")
    else:
        if stats.get('virophage') == 'active':
            print_slowly("Your integrated Virophage attacks the giant virus! It is neutralized!")
        else:
            print_slowly("Your defenses activate just in time and neutralize the viral particle!")
    return stats

def event_upwelling(stats):
    """A strong current appears."""
    print_slowly("...An Upwelling Current...")
    print_slowly("You are caught in a powerful column of rising water!")
    depth_gain = random.randint(20, 50)
    stats['depth'] -= depth_gain
    print_slowly(f"It's a free ride! You are pushed {depth_gain} meters closer to the surface.")
    return stats

def event_downwelling(stats):
    """A sinking current appears."""
    print_slowly("...A Downwelling Current...")
    print_slowly("A cold, heavy current drags you back down into the dark...")
    depth_loss = random.randint(15, 40)
    stats['depth'] += depth_loss
    print_slowly(f"You fight against it, but you are pulled {depth_loss} meters deeper.")
    return stats

def event_marine_snow(stats):
    """Find a nutrient-rich particle."""
    print_slowly("...Marine Snow...")
    print_slowly("A particle of nutrient-rich 'marine snow' drifts past.")
    energy_gain = random.randint(15, 25)
    stats['energy'] += energy_gain
    print_slowly(f"You absorb it, gaining {energy_gain} energy!")
    return stats

# --- NEW EVENTS ---

def event_symbiosis(stats):
    """A choice to take on a symbiont."""
    if stats.get('symbiont') is not None:
        print_slowly("...A strange bacteria approaches, but you already have a symbiont.")
        return stats
        
    print_slowly("...Symbiosis Opportunity...")
    print_slowly("A small, quivering bacterium bumps into you. It seems to want to attach.")
    choice_idx = get_choice_input("Allow it to form a symbiosis?", ["Yes, take the risk.", "No, stay independent."])
    
    if choice_idx == 0:
        if random.random() < 0.5:
            stats['symbiont'] = 'good'
            print_slowly("It's a helpful symbiont! It begins producing trace nutrients for you.")
        else:
            stats['symbiont'] = 'bad'
            print_slowly("It's a parasite! It starts slowly draining your energy.")
    else:
        print_slowly("You reject the bacterium and it drifts away.")
    return stats

def event_virophage(stats):
    """A choice to integrate a virophage."""
    if stats.get('virophage') is not None:
        print_slowly("...A virophage floats by, but your genome is already occupied.")
        return stats
        
    print_slowly("...Virophage Detected...")
    print_slowly("A tiny virophage (a virus that infects other viruses) is nearby. You could integrate its DNA.")
    choice_idx = get_choice_input("Integrate the virophage DNA?", ["Yes, high risk, high reward.", "No, it's too dangerous."])
    
    if choice_idx == 0:
        if random.random() < 0.75:
            stats['virophage'] = 'active'
            print_slowly("Success! The virophage DNA is now part of your genome, ready to defend you.")
        else:
            stats['virophage'] = 'failed'
            energy_loss = random.randint(30, 45)
            stats['energy'] -= energy_loss
            print_slowly(f"The integration failed! The foreign DNA causes a massive {energy_loss} energy loss!")
    else:
        print_slowly("You decide against tampering with your genome.")
    return stats

def event_bioluminescence(stats):
    """A choice to glow for nutrients, risking attack."""
    print_slowly("...Bioluminescence...")
    print_slowly("You have the ability to produce a faint glow to attract nutrients.")
    choice_idx = get_choice_input("Activate your glow?", ["Yes, light up.", "No, stay dark."])
    
    if choice_idx == 0:
        if random.random() < 0.6:
            energy_gain = random.randint(20, 30)
            stats['energy'] += energy_gain
            print_slowly(f"It worked! Nutrients drift towards your light. You gain {energy_gain} energy.")
        else:
            print_slowly("Your glow attracts the wrong attention... a Copepod appears!")
            press_enter_to_continue()
            stats = event_copepod(stats) # Trigger a copepod attack
    else:
        print_slowly("You remain hidden in the dark.")
    return stats
    
def event_dead_zone(stats):
    """A simple negative event."""
    print_slowly("...Anoxic Dead Zone...")
    print_slowly("You drift into a patch of water with no oxygen. It's suffocating.")
    energy_loss = random.randint(5, 15)
    stats['energy'] -= energy_loss
    print_slowly(f"You expend {energy_loss} energy just to survive until you drift out.")
    return stats


# List of possible random events
# We make good events slightly less common than bad ones
RANDOM_EVENTS = [
    event_copepod, event_copepod,  # Higher chance of copepod
    event_virus, event_virus,
    event_downwelling, event_downwelling,
    event_upwelling,
    event_marine_snow,
    event_symbiosis, # New
    event_virophage, # New
    event_bioluminescence, # New
    event_dead_zone # New
]

# --- NEW: EVOLUTION STORE ---
EVOLUTION_UPGRADES = {
    'flagella': {
        'name': "Flagella",
        'cost': 15,
        'desc': "A tail. Reduces energy cost of 'Swim upwards' by 30%."
    },
    'toxin_defense': {
        'name': "Toxin Defense",
        'cost': 9,
        'desc': "Reduces energy loss from Copepod attacks by 40%."
    },
    'cyst_form': {
        'name': "Cyst Form (One-Time)",
        'cost': 12,
        'desc': "A one-time-use ability to completely block one Copepod attack."
    },
    'nutrient_sensors': {
        'name': "Nutrient Sensors",
        'cost': 18,
        'desc': "Increases chance and amount of energy from 'Rest' or 'Hunt'."
    },
    'viral_resistance': {
        'name': "Viral Resistance",
        'cost': 10,
        'desc': "Reduces the chance of energy loss from a virus attack."
    },
    'energy_storage': {
        'name': "Energy Storage",
        'cost': 10,
        'desc': "Increases your maximum energy from 100 to 130."
    }
}


# --- GAME STATE ---

player_stats = {
    'depth': 360,  # Start at 300 meters
    'energy': 100, # Starting energy
    'max_energy': 100, # Max energy
    'day': 1,
    'photic_zone_depth': 60, # The depth at which photosynthesis is possible
    'upgrades': set(), # Use a set for fast lookups
    'symbiont': None, # Can be 'good' or 'bad'
    'virophage': None, # Can be 'active' or 'failed'
    'cyst_form_ready': False
}

# --- MAIN GAME FUNCTIONS ---

def display_status():
    """Clears and displays the current game status."""
    clear_screen()
    print(TITLE_ART)
    print(PLANKTON_ART)
    print("===================================================================")
    print(f" Day: {player_stats['day']}")
    print("===================================================================")
    print(f" Current Depth:  {player_stats['depth']} meters")
    print(f" Target Depth:   {player_stats['photic_zone_depth']} meters (Photic Zone)")
    print(f" Energy:         {player_stats['energy']} / {player_stats['max_energy']}")
    print("--- Status ---")
    if player_stats['upgrades']: print(f" Upgrades: {', '.join(name.replace('_', ' ').capitalize() for name in player_stats['upgrades'])}")
    if player_stats.get('symbiont'): print(f" Symbiont: {player_stats['symbiont'].capitalize()}")
    if player_stats.get('virophage') == 'active': print(" Virophage: Active")
    if player_stats['cyst_form_ready']: print(" Cyst Form: Ready")
    print("===================================================================\n")

def get_player_choice():
    """Presents choices and gets valid input."""
    
    # Check if we are in the photic zone
    in_photic_zone = player_stats['depth'] <= player_stats['photic_zone_depth']
    
    if in_photic_zone:
        print_slowly(f"You are in the Photic Zone (Target: {player_stats['photic_zone_depth']}m)! You can feel the sun.")
        print("What will you do?")
        print("  1. Swim for the surface (High energy cost)")
        print("  2. Photosynthesize (Gain energy, but sink slightly)")
        print("  3. Dive for nutrients (Risk depth for potential energy)")
    else:
        print_slowly("You are in the dark. You must conserve energy.")
        print("What will you do?")
        print("  1. Swim upwards (High energy cost)")
        print("  2. Rest and absorb (Low energy cost, chance for trace nutrients)")
        print("  3. Hunt for nutrient pockets (Medium cost, bigger chance)")

    while True:
        try:
            choice = input("\nEnter choice (1, 2, or 3): ")
            choice_num = int(choice)
            if 1 <= choice_num <= 3:
                return choice_num
            else:
                print("That is not a valid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def resolve_action(choice):
    """Updates game state based on player's choice."""
    
    in_photic_zone = player_stats['depth'] <= player_stats['photic_zone_depth']
    
    if in_photic_zone:
        # --- Photic Zone Actions ---
        if choice == 1:
            # Swim for the surface
            energy_cost = random.randint(10, 15)
            if 'flagella' in player_stats['upgrades']:
                energy_cost = int(energy_cost * 0.7)
            
            depth_gain = random.randint(15, 30)
            player_stats['energy'] -= energy_cost
            player_stats['depth'] -= depth_gain
            print_slowly(f"You burn {energy_cost} energy and swim {depth_gain} meters closer to the sun!")
            if 'flagella' in player_stats['upgrades']:
                print_slowly("Your flagella makes swimming easier!")
            
        elif choice == 2:
            # Photosynthesize
            energy_gain = random.randint(15, 25)
            depth_loss = random.randint(2, 8) # Sinking
            player_stats['energy'] += energy_gain
            player_stats['depth'] += depth_loss
            print_slowly(f"You soak in the weak sunlight, gaining {energy_gain} energy.")
            print_slowly(f"While resting, you sink {depth_loss} meters.")
            
        elif choice == 3:
            # Dive for nutrients
            energy_cost = random.randint(5, 10)
            depth_loss = random.randint(10, 20)
            player_stats['energy'] -= energy_cost
            player_stats['depth'] += depth_loss
            print_slowly(f"You dive back down {depth_loss} meters, costing {energy_cost} energy...")
            
            base_chance = 0.6
            if 'nutrient_sensors' in player_stats['upgrades']:
                base_chance = 0.8
                
            if random.random() < base_chance:
                energy_gain = random.randint(20, 30)
                if 'nutrient_sensors' in player_stats['upgrades']:
                    energy_gain += random.randint(5, 10)
                player_stats['energy'] += energy_gain
                print_slowly(f"Success! You find a nutrient pocket and gain {energy_gain} energy!")
            else:
                print_slowly("...but you find nothing.")
                
    else:
        # --- Deep Zone Actions ---
        if choice == 1:
            # Swim upwards
            energy_cost = random.randint(12, 18)
            if 'flagella' in player_stats['upgrades']:
                energy_cost = int(energy_cost * 0.7)
                
            depth_gain = random.randint(20, 35)
            player_stats['energy'] -= energy_cost
            player_stats['depth'] -= depth_gain
            print_slowly(f"You burn {energy_cost} energy and swim {depth_gain} meters up.")
            if 'flagella' in player_stats['upgrades']:
                print_slowly("Your flagella makes swimming easier!")
            
        elif choice == 2:
            # Rest and absorb
            energy_cost = random.randint(2, 5)
            depth_loss = random.randint(3, 10) # Sinking
            player_stats['energy'] -= energy_cost
            player_stats['depth'] += depth_loss
            print_slowly(f"You rest, consuming {energy_cost} energy and sinking {depth_loss} meters.")
            
            base_chance = 0.3
            if 'nutrient_sensors' in player_stats['upgrades']:
                base_chance = 0.5
            
            if random.random() < base_chance:
                energy_gain = random.randint(5, 10)
                if 'nutrient_sensors' in player_stats['upgrades']:
                    energy_gain += random.randint(3, 6)
                player_stats['energy'] += energy_gain
                print_slowly(f"You absorbed some trace nutrients, gaining {energy_gain} energy!")

        elif choice == 3:
            # Hunt for nutrient pockets
            energy_cost = random.randint(5, 10)
            player_stats['energy'] -= energy_cost
            print_slowly(f"You spend {energy_cost} energy hunting for a nutrient pocket...")
            
            base_chance = 0.5
            if 'nutrient_sensors' in player_stats['upgrades']:
                base_chance = 0.75
                
            if random.random() < base_chance:
                energy_gain = random.randint(15, 30)
                if 'nutrient_sensors' in player_stats['upgrades']:
                    energy_gain += random.randint(5, 10)
                player_stats['energy'] += energy_gain
                print_slowly(f"Success! You find one and gain {energy_gain} energy!")
            else:
                print_slowly("...but you come up empty.")

    # Clamp energy to max
    if player_stats['energy'] > player_stats['max_energy']:
        player_stats['energy'] = player_stats['max_energy']
        
    # Clamp depth to not go below starting depth
    if player_stats['depth'] > 360:
        player_stats['depth'] = 360

def trigger_event():
    """40% chance to trigger a random event."""
    if random.random() < 0.40:
        print("\n-------------------------------------------------------")
        print_slowly("...Something is happening!...")
        event = random.choice(RANDOM_EVENTS)
        event(player_stats) # Call the event function, passing stats
        print("-------------------------------------------------------")
    
    press_enter_to_continue()


def show_intro():
    """Display the intro text."""
    clear_screen()
    print(TITLE_ART)
    print_slowly("You are Micromonas, a tiny phytoplankton.")
    print_slowly(f"You have been knocked deep into the ocean, down to {player_stats['depth']} meters.")
    print_slowly("You are far below the 'photic zone', the layer of water where sunlight can reach.")
    print_slowly(f"You must make it back to {player_stats['photic_zone_depth']}m or less to photosynthesize and survive.")
    print_slowly(f"You have {player_stats['energy']} energy. Manage it wisely.")
    print_slowly("Good luck.")
    press_enter_to_continue()

# --- NEW: EVOLUTION STORE FUNCTION ---
def run_evolution_store():
    """Runs the evolution store interface."""
    clear_screen()
    print_slowly("...A strange calm falls over you. You feel a genetic shift...")
    print("\n=======================================================")
    print("         E V O L U T I O N   S T O R E")
    print("=======================================================\n")
    print_slowly("You can spend energy to gain permanent advantages.")
    
    # Find upgrades player doesn't have
    available_upgrades = []
    for key, upgrade in EVOLUTION_UPGRADES.items():
        if key not in player_stats['upgrades']:
            # Special check for cyst form
            if key == 'cyst_form' and player_stats['cyst_form_ready']:
                continue # Don't offer if they have one ready
            available_upgrades.append(key)
    
    if not available_upgrades:
        print_slowly("You have already evolved every available advantage!")
        press_enter_to_continue()
        return

    # Select 3 random upgrades to display
    num_to_offer = min(len(available_upgrades), 3)
    offered_keys = random.sample(available_upgrades, num_to_offer)
    
    while True:
        print(f"\nYour current energy: {player_stats['energy']}\n")
        
        options = []
        for key in offered_keys:
            upgrade = EVOLUTION_UPGRADES[key]
            options.append(f"{upgrade['name']} (Cost: {upgrade['cost']}) - {upgrade['desc']}")
        options.append("Leave the store.")
        
        choice_idx = get_choice_input("Choose an evolution:", options)
        
        if choice_idx == len(options) - 1:
            print_slowly("You finish your adaptations and continue the journey.")
            press_enter_to_continue()
            break # Exit the store loop
            
        # --- Handle purchase ---
        selected_key = offered_keys[choice_idx]
        selected_upgrade = EVOLUTION_UPGRADES[selected_key]
        
        if player_stats['energy'] >= selected_upgrade['cost']:
            # Pay cost
            player_stats['energy'] -= selected_upgrade['cost']
            
            # Apply upgrade
            if selected_key == 'cyst_form':
                player_stats['cyst_form_ready'] = True
            elif selected_key == 'energy_storage':
                player_stats['max_energy'] += 30
                player_stats['energy'] += 30 # Get the energy boost now
                player_stats['upgrades'].add(selected_key)
            else:
                player_stats['upgrades'].add(selected_key)
                
            print_slowly(f"\nSuccessfully acquired {selected_upgrade['name']}!")
            
            # Remove from offered list
            offered_keys.pop(choice_idx)
            
            if not offered_keys:
                print_slowly("Nothing left to buy this time.")
                press_enter_to_continue()
                break # Exit store
        else:
            print_slowly("\nYou don't have enough energy for this evolution.")
            
        press_enter_to_continue()
        clear_screen()
        print("\n=======================================================")
        print("         E V O L U T I O N   S T O R E")
        print("=======================================================\n")


# --- MAIN GAME LOOP ---

def main():
    """Main game loop."""
    show_intro()
    
    while True:
        
        # --- Daily Persistent Effects ---
        if player_stats.get('symbiont') == 'good':
            player_stats['energy'] += 3 # Small daily boost
            if player_stats['energy'] > player_stats['max_energy']:
                player_stats['energy'] = player_stats['max_energy']
        elif player_stats.get('symbiont') == 'bad':
            player_stats['energy'] -= 4 # Small daily drain
            
        # 1. Display Status
        display_status()
        
        # --- Check for Evolution Store ---
        if player_stats['day'] > 1 and player_stats['day'] % 10 == 0:
            run_evolution_store()
            # After store, redisplay status in case energy/max energy changed
            display_status()
            
        # 2. Check Win/Loss Conditions
        if player_stats['energy'] <= 0:
            game_over("You ran out of energy and dissolved into the deep.")
            break
            
        if player_stats['depth'] <= player_stats['photic_zone_depth']:
            # Win condition: reach the photic zone
            display_status() # Show the final winning status
            game_win()
            break
            
        # 3. Get Player Action
        choice = get_player_choice()
        
        # 4. Resolve Action
        clear_screen()
        resolve_action(choice)
        
        # 5. Check for game over *after* action
        if player_stats['energy'] <= 0:
            display_status()
            game_over("Your last action drained your remaining energy. You dissolve...")
            break
        
        # 6. Trigger Random Event (if not a win/loss)
        if player_stats['depth'] > player_stats['photic_zone_depth']:
            trigger_event()
        
        # 7. Increment Day
        player_stats['day'] += 1

if __name__ == "__main__":
    main()



