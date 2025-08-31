import random
import time
import os

# --- Game Configuration ---

# A dictionary defining the properties of each available crop
# 'growth_time': Days it takes to mature
# 'seed_price': Cost to buy one seed
# 'sell_price': Money earned from one harvested crop
# 'icon': A simple character to represent the crop
CROP_DATA = {
    'wheat': {
        'growth_time': 4,
        'seed_price': 10,
        'sell_price': 25,
        'icon': '🌾',
        'info': 'A staple grain. Hardy and reliable.'
    },
    'corn': {
        'growth_time': 5,
        'seed_price': 15,
        'sell_price': 40,
        'icon': '🌽',
        'info': 'A sweet and popular vegetable. Sells for a good price.'
    },
    'potato': {
        'growth_time': 3,
        'seed_price': 5,
        'sell_price': 15,
        'icon': '🥔',
        'info': 'Grows quickly, but sells for less. Good for beginners.'
    },
    'carrot': {
        'growth_time': 3,
        'seed_price': 8,
        'sell_price': 20,
        'icon': '🥕',
        'info': 'A fast-growing and profitable root vegetable.'
    }
}

# Starting conditions for the player
INITIAL_MONEY = 100
INITIAL_PLOTS = 4
GAME_GOAL = 500 # The amount of money to win the game

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def print_slow(text):
    """Prints text slowly for a more immersive feel."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)
    print()

# --- Main Game Class ---

class FarmingGame:
    """Manages the state and logic of the farming game."""

    def __init__(self):
        self.money = INITIAL_MONEY
        self.day = 1
        # Each plot is a dictionary representing its state
        self.farm_plots = [{'crop': None, 'growth_stage': 0, 'watered': False} for _ in range(INITIAL_PLOTS)]
        self.inventory = {'wheat seeds': 5, 'potato seeds': 5}
        self.game_over = False

    def display_status(self):
        """Displays the current status of the farm, money, and day."""
        print("="*40)
        print(f"☀️  Day: {self.day}  | 💰 Money: ${self.money}")
        print(f"🎯 Goal: Reach ${GAME_GOAL}")
        print("-"*40)
        print("🌱 Your Farm Plots:")

        plot_display = []
        for i, plot in enumerate(self.farm_plots):
            if plot['crop'] is None:
                plot_display.append(f"  [{i+1}] Empty Land")
            else:
                crop_name = plot['crop']
                icon = CROP_DATA[crop_name]['icon']
                growth_time = CROP_DATA[crop_name]['growth_time']
                progress = plot['growth_stage']
                
                # Visual progress bar
                progress_bar = "#" * progress + "." * (growth_time - progress)
                
                status = "Dry" if not plot['watered'] else "Watered"
                
                if progress >= growth_time:
                    plot_display.append(f"  [{i+1}] {icon} {crop_name.capitalize()} [READY] {status}")
                else:
                    plot_display.append(f"  [{i+1}] {icon} {crop_name.capitalize()} [{progress_bar}] {status}")
        
        for line in plot_display:
            print(line)
        print("="*40)

    def display_inventory(self):
        """Shows the player's current inventory."""
        print("📦 Your Inventory:")
        if not self.inventory:
            print("  - Empty")
        else:
            for item, count in self.inventory.items():
                print(f"  - {count}x {item.capitalize()}")
        print("-"*40)

    def advance_day(self):
        """Advances the game by one day, growing crops and handling events."""
        self.day += 1
        print_slow("\n🌅 A new day dawns...")

        # Grow crops and reset watered status
        for plot in self.farm_plots:
            if plot['crop'] is not None:
                if plot['watered']:
                    plot['growth_stage'] += 1
                    print(f"  - Your {plot['crop']} grew a little!")
                else:
                    print(f"  - Your {plot['crop']} didn't grow. It needs water!")
                plot['watered'] = False # Soil dries out overnight

        # Random Events
        self.handle_random_event()
        
        # Check for win condition
        if self.money >= GAME_GOAL:
            print_slow(f"\n🎉 CONGRATULATIONS! You've reached ${self.money} and built a successful farm! 🎉")
            self.game_over = True

    def handle_random_event(self):
        """Introduces a random event for the day."""
        chance = random.random() # Generates a float between 0.0 and 1.0
        if chance < 0.15: # 15% chance of a bad event
            print("  - 蝗虫 A swarm of pests attacked! Some crops may be damaged.")
            # Simple effect: one random growing crop loses a growth stage
            growing_plots = [p for p in self.farm_plots if p['crop'] is not None and p['growth_stage'] < CROP_DATA[p['crop']]['growth_time']]
            if growing_plots:
                plot_to_damage = random.choice(growing_plots)
                plot_to_damage['growth_stage'] = max(0, plot_to_damage['growth_stage'] - 1)
                print(f"  - Your {plot_to_damage['crop']} in plot was set back a day!")
        elif chance < 0.30: # 15% chance of a good event (total 30%)
            print("  - 🌧️ Gentle rains fell overnight! All your plots have been watered.")
            for plot in self.farm_plots:
                plot['watered'] = True
        # else: 70% chance of a normal day

    def plant(self):
        """Allows the player to plant a seed in a plot."""
        self.display_inventory()
        seed_to_plant = input("Which seed do you want to plant? (e.g., 'wheat') > ").lower()
        
        seed_name = f"{seed_to_plant} seeds"
        if seed_name not in self.inventory or self.inventory[seed_name] == 0:
            print("❌ You don't have any of those seeds.")
            return

        try:
            plot_num = int(input(f"Which plot to plant it in? (1-{len(self.farm_plots)}) > ")) - 1
            if not 0 <= plot_num < len(self.farm_plots):
                print("❌ That's not a valid plot number.")
                return
            if self.farm_plots[plot_num]['crop'] is not None:
                print("❌ There's already something growing in that plot!")
                return
            
            # Plant the seed
            self.farm_plots[plot_num] = {'crop': seed_to_plant, 'growth_stage': 0, 'watered': False}
            self.inventory[seed_name] -= 1
            if self.inventory[seed_name] == 0:
                del self.inventory[seed_name]
            
            print(f"Planted {seed_to_plant} in plot {plot_num + 1}. Don't forget to water it!")

        except ValueError:
            print("❌ Please enter a valid number.")

    def water(self):
        """Allows the player to water a plot."""
        try:
            plot_num = int(input(f"Which plot to water? (1-{len(self.farm_plots)}) > ")) - 1
            if not 0 <= plot_num < len(self.farm_plots):
                print("❌ That's not a valid plot number.")
                return
            if self.farm_plots[plot_num]['crop'] is None:
                print("❌ You can't water an empty plot.")
                return
            
            self.farm_plots[plot_num]['watered'] = True
            print(f"💧 You watered plot {plot_num + 1}. Your {self.farm_plots[plot_num]['crop']} will grow tomorrow.")

        except ValueError:
            print("❌ Please enter a valid number.")

    def harvest(self):
        """Allows the player to harvest a mature crop."""
        try:
            plot_num = int(input(f"Which plot to harvest? (1-{len(self.farm_plots)}) > ")) - 1
            if not 0 <= plot_num < len(self.farm_plots):
                print("❌ That's not a valid plot number.")
                return

            plot = self.farm_plots[plot_num]
            if plot['crop'] is None:
                print("❌ Nothing to harvest there.")
                return

            crop_name = plot['crop']
            if plot['growth_stage'] < CROP_DATA[crop_name]['growth_time']:
                print(f"❌ Your {crop_name} is not ready to be harvested yet!")
                return
            
            # Harvest the crop
            sell_price = CROP_DATA[crop_name]['sell_price']
            self.money += sell_price
            print(f"✅ You harvested the {crop_name} and sold it for ${sell_price}!")
            
            # Reset the plot
            self.farm_plots[plot_num] = {'crop': None, 'growth_stage': 0, 'watered': False}

        except ValueError:
            print("❌ Please enter a valid number.")
            
    def visit_shop(self):
        """Allows the player to buy more seeds."""
        print("\n🏪 Welcome to the Farmer's Market!")
        print("Here's what's for sale (per seed):")
        for crop, data in CROP_DATA.items():
            print(f"  - {crop.capitalize()} Seeds: ${data['seed_price']} ({data['info']})")
        print("\nType 'exit' to leave the shop.")
        
        while True:
            choice = input("What would you like to buy? > ").lower()
            if choice == 'exit':
                break
            
            if choice in CROP_DATA:
                price = CROP_DATA[choice]['seed_price']
                if self.money >= price:
                    self.money -= price
                    seed_name = f"{choice} seeds"
                    self.inventory[seed_name] = self.inventory.get(seed_name, 0) + 1
                    print(f"You bought 1 {choice} seed. You have ${self.money} left.")
                else:
                    print("❌ You don't have enough money for that.")
            else:
                print("❌ We don't sell that here.")
    
    def run(self):
        """The main game loop."""
        clear_screen()
        print_slow("🌾 Welcome to 'Digital Farmer' - A Learning Adventure! 🌾")
        print_slow("Your goal is to earn $500 by planting, watering, and harvesting crops.")
        input("\nPress Enter to start your first day...")

        while not self.game_over:
            clear_screen()
            self.display_status()
            
            print("\nWhat would you like to do?")
            print("[P]lant a seed")
            print("[W]ater a crop")
            print("[H]arvest a crop")
            print("[S]hop for seeds")
            print("[I]nspect inventory")
            print("[N]ext Day")
            print("[Q]uit Game")
            
            action = input("> ").lower()

            if action == 'p':
                self.plant()
            elif action == 'w':
                self.water()
            elif action == 'h':
                self.harvest()
            elif action == 's':
                self.visit_shop()
            elif action == 'i':
                self.display_inventory()
            elif action == 'n':
                self.advance_day()
            elif action == 'q':
                print("Come back to the farm soon!")
                self.game_over = True
            else:
                print("❓ Invalid command. Try again.")
            
            if not self.game_over:
                input("\nPress Enter to continue...")

# --- Start the Game ---
if __name__ == "__main__":
    game = FarmingGame()
    game.run()