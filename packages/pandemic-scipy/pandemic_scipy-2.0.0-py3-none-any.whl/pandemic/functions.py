from pandemic import world_map_drawer
from pandemic import data_unloader
from typing import Any
import tkinter as tk
from tkinter import messagebox
from functools import partial
import random
import os
import sys
import time

BUILDING_DOCS = os.environ.get("READTHEDOCS") == "True" or "sphinx" in sys.modules
# Define global variables to track remaining cards and actions
remaining_player_cards = 2  # The number of player cards to draw (fixed)
remaining_infection_cards = 2  # This depends on the infection rate (can be dynamic)
game_over = False  # A variable signalling game over
player_draw_locked = False
playercards_drawn = 0
infectioncards_drawn = 0
operations_expert_switch = True
if "Quarantine Specialist" in data_unloader.in_game_roles:
    quarantined_cities = ["Atlanta", "Washington", "Miami", "Chicago"]
else:
    quarantined_cities = []
if "Medic" in data_unloader.in_game_roles:
    medic_protected_city = "Atlanta"
else:
    medic_protected_city = ""
mobile_hospital_active = False
improved_sanitation_active = False
infectionless_night = False

if not BUILDING_DOCS:
    def discard(player_id, amount_to_discard, purpose):
        # Get the current player's hand and role
        role = data_unloader.in_game_roles[player_id]
        player_hand = data_unloader.current_hand
        action_confirmed = False  # <‑‑ NEW FLAG
        selected_cards = []

        def submit_selection():
            nonlocal selected_cards, action_confirmed
            # Gather the cards selected by the player (checkboxes)
            selected_cards = [card for name, (var, card) in card_vars.items() if var.get() == 1]

            # Check if the selected amount is correct
            if len(selected_cards) != amount_to_discard:
                messagebox.showerror("Invalid Selection", f"Please select exactly {amount_to_discard} card(s).")
                return

            # ===================== Purpose-specific validation =====================
            if purpose == "discover_cure":
                # Ensure all cards are city cards
                # Ensure all selected cards are **city** cards
                if not all(card.get("cardtype", "city_card") == "city_card"  # ← default!
                           for card in selected_cards):
                    messagebox.showerror(
                        "Invalid Selection",
                        "All selected cards must be city cards to discover a cure."
                    )
                    return

                # Ensure all cards are the same color
                # colours of the selected cards
                colors = [card.get("color")  # city cards carry their own colour
                          for card in selected_cards]
                if len(set(colors)) != 1:
                    messagebox.showerror("Invalid Selection",
                                         "You must select cards of the same color to discover a cure.")
                    return

                cure_color = colors[0]

                # Discard the cards and update cure status
                for card in selected_cards:
                    data_unloader.players_hands[player_id] = [
                        c for c in data_unloader.players_hands[player_id] if c["name"] != card["name"]
                    ]
                    data_unloader.playercard_discard.append({"name": card["name"], "cardtype": "city_card"})

                color_to_index = {"yellow": 0, "red": 1, "blue": 2, "black": 3}
                disease_index = color_to_index[cure_color]

                if data_unloader.infection_status[disease_index] == 0:
                    data_unloader.infection_status[disease_index] = 1
                    data_unloader.actions -= 1
                    world_map_drawer.queue_game_text(
                        f"💊 Player {player_id + 1} discovered a cure for the {cure_color} disease!", delay = 1500)
                    # Check if the Medic is present and auto-remove cubes from his current city
                    if "Medic" in data_unloader.in_game_roles:
                        medic_id = data_unloader.in_game_roles.index("Medic")  # Much simpler!
                        medic_city = data_unloader.players_locations[medic_id]
                        infection_levels = data_unloader.cities[medic_city]["infection_levels"]

                        if infection_levels[disease_index] > 0:
                            cubes_removed = infection_levels[disease_index]
                            infection_levels[disease_index] = 0
                            data_unloader.infection_cubes[disease_index] += cubes_removed
                            world_map_drawer.queue_game_text(
                                f"🧪 Medic removed all {cure_color} cubes from {medic_city} after curing the disease!", delay = 1500
                            )
                            world_map_drawer.update_text(medic_id)

                    world_map_drawer.update_disease_status(disease_index)
                    world_map_drawer.update_text(player_id)
                    check_game_over()
                    action_confirmed = True  # <‑‑ mark success
                else:
                    world_map_drawer.queue_game_text(f"💊 The {cure_color} disease has already been cured.", delay = 1500)

            elif purpose == "direct_flight":
                # You must discard the card of the city you are flying to
                destination_card = selected_cards[0]
                current_city = data_unloader.players_locations[player_id]
                if destination_card["name"] not in data_unloader.cities or destination_card["name"] == current_city:
                    messagebox.showerror("Invalid Selection", f"You must discard a destination city card.")
                    return
                data_unloader.cities[current_city]["player_amount"] -= 1
                data_unloader.cities[destination_card["name"]]["player_amount"] += 1
                data_unloader.actions -= 1
                world_map_drawer.queue_game_text(f"🛩️ Player {player_id + 1} moved to {destination_card['name']}!", delay = 1500)
                world_map_drawer.update_player_marker(player_id, destination_card["name"])
                world_map_drawer.update_text(player_id)
                action_confirmed = True  # <‑‑ mark success
                if role == "Quarantine Specialist":
                    quarantined_cities.clear()
                    quarantined_cities.append(destination_card["name"])
                    for neighbour in data_unloader.cities[destination_card["name"]]["relations"]:
                        quarantined_cities.append(neighbour)
                elif role == "Medic":
                    medic_protected_city = destination_card["name"]
                    infection_levels = data_unloader.cities[destination_card["name"]]["infection_levels"]
                    for i, cubes in enumerate(infection_levels):
                        if cubes > 0 and data_unloader.infection_status[i] >= 1:  # if cured
                            data_unloader.infection_cubes[i] += cubes
                            infection_levels[i] = 0
                            world_map_drawer.queue_game_text(
                                f"🧪 Medic removed all {['yellow', 'red', 'blue', 'black'][i]} infection cubes in {destination_card['name']} by direct flight!", delay = 1500
                            )
                    world_map_drawer.update_text(player_id)
            elif purpose == "charter_flight":
                global operations_expert_switch
                # You must discard the card of the city you are currently in
                destination_card = selected_cards[0]
                current_city = data_unloader.players_locations[player_id]
                if role == "Operations Expert" and not operations_expert_switch and data_unloader.cities[current_city]["research_center"] != 1:
                    messagebox.showerror("Invalid city", f"{current_city} has no research center!")
                    return
                elif role != "Operations Expert" and destination_card["name"] != current_city:
                    messagebox.showerror("Invalid Selection",
                                         f"You must discard the current city card: {current_city}.")
                    return

                # Show a popup to select the destination city
                def choose_charter_destination():
                    dest_popup = tk.Toplevel()
                    dest_popup.title("Select Destination City")
                    dest_popup.geometry("400x300")
                    tk.Label(dest_popup, text="Choose a destination city:").pack(pady=10)

                    city_var = tk.StringVar(value=list(data_unloader.cities.keys())[0])  # default to the first city
                    city_menu = tk.OptionMenu(dest_popup, city_var, *data_unloader.cities.keys())
                    city_menu.pack(pady=10)

                    def confirm_destination():
                        global operations_expert_switch
                        nonlocal action_confirmed
                        destination = city_var.get()
                        data_unloader.cities[current_city]["player_amount"] -= 1
                        data_unloader.cities[destination_card["name"]]["player_amount"] += 1
                        data_unloader.actions -= 1
                        world_map_drawer.queue_game_text(f"🛩️ Player {player_id + 1} moved to {destination}!", delay = 1500)
                        world_map_drawer.update_player_marker(player_id, destination)
                        world_map_drawer.update_text(player_id)
                        action_confirmed = True  # <‑‑ mark success
                        dest_popup.destroy()
                        if role == "Operations Expert":
                            operations_expert_switch = False
                        elif role == "Quarantine Specialist":
                            quarantined_cities.clear()
                            quarantined_cities.append(destination)
                            for neighbour in data_unloader.cities[destination]["relations"]:
                                quarantined_cities.append(neighbour)
                        elif role == "Medic":
                            medic_protected_city = destination
                            infection_levels = data_unloader.cities[destination]["infection_levels"]
                            for i, cubes in enumerate(infection_levels):
                                if cubes > 0 and data_unloader.infection_status[i] >= 1:  # if cured
                                    data_unloader.infection_cubes[i] += cubes
                                    infection_levels[i] = 0
                                    world_map_drawer.queue_game_text(
                                        f"🧪 Medic removed all {['yellow', 'red', 'blue', 'black'][i]} infection cubes in {destination} by charter flight!", delay = 1500
                                    )
                            world_map_drawer.update_text(player_id)

                    tk.Button(dest_popup, text="Confirm", command=confirm_destination).pack(pady=10)
                    dest_popup.grab_set()
                    dest_popup.wait_window()

                choose_charter_destination()

            elif purpose == "build_research_center":
                current_city = data_unloader.players_locations[player_id]
                selected_card = selected_cards[0]

                if selected_card["name"] not in data_unloader.cities:
                    messagebox.showerror("Invalid Card", "You must discard a city card to build a research center.")
                    return

                if selected_card["name"] != current_city:
                    messagebox.showerror("Wrong City",
                                         f"You can only build a research center in your current city: {current_city}.")
                    return

                success = oe_build_research_center(player_id)
                if success:
                    action_confirmed = True  # let the discarding section run
                else:
                    action_confirmed = False  # nothing happened → don’t discard

            elif purpose == "card_overflow":
                # No validation needed; player is just discarding any cards to reduce hand to 7
                # Ensure the correct number of cards are discarded
                if len(selected_cards) != amount_to_discard:
                    messagebox.showerror("Invalid Selection", f"You must select exactly {amount_to_discard} card(s).")
                    return
                world_map_drawer.update_text(player_id)
                # No special validation otherwise, just proceed with discard
                action_confirmed = True

            # ===================== Apply Discard =====================
            if action_confirmed:
                for card in selected_cards:
                    player_hand.remove(card)
                    data_unloader.playercard_discard.append(card)

                # Update the player's hand in the global data structure
                data_unloader.players_hands[player_id] = player_hand
                world_map_drawer.update_text(player_id)

                # Only close the popup if discard succeeded
                popup.destroy()
            else:
                # If nothing valid was selected (e.g., for overflow), keep the popup open
                messagebox.showwarning("Discard Required", "You must discard the required number of cards to proceed.")

        # ===================== Create Discard Popup =====================
        popup = tk.Toplevel()
        popup.title(f"Discard Cards ({purpose.replace('_', ' ').title()})")
        popup.geometry("800x400")
        popup.resizable(False, False)

        # 🛡️ Prevent closing with X
        if purpose == "card_overflow":
            def on_close_blocked():
                messagebox.showwarning("Action Required", "You must discard cards before continuing.")
            popup.protocol("WM_DELETE_WINDOW", on_close_blocked)
        # Instruction label
        tk.Label(popup, text=f"Select {amount_to_discard} card(s) to discard:").pack(pady=10)

        # Dictionary to keep track of checkboxes
        card_vars = {}
        for card in player_hand:
            var = tk.IntVar()
            cb = tk.Checkbutton(popup, text=card, variable=var)
            cb.pack(anchor="w")
            card_vars[card["name"]] = (var, card)

        # Submit/discard button
        submit_btn = tk.Button(popup, text="Discard", command=submit_selection)
        submit_btn.pack(pady=20)
        popup.grab_set()  # Makes the popup modal — locks focus
        popup.wait_window()  # Waits until popup is destroyed before continuing


def check_game_over():
    """Checks if one of the game over requirements is met: 3 losing and 1 winning situation."""
    from pandemic import turn_handler
    global game_over
    if len(data_unloader.player_deck) < 2:  # We lose if the player deck runs out of cards
        game_over = True
        world_map_drawer.queue_game_text("❌ Game Over! Ran out of player cards!", delay = 1500)
        turn_handler.end_game(game_over)
        return True
    elif data_unloader.outbreak_marker == 8:  # We lose if 8 or more outbreaks occur
        game_over = True
        world_map_drawer.queue_game_text("❌ Game Over! Too many outbreaks occurred!", delay = 1500)
        turn_handler.end_game(game_over)
        return True
    elif any(cube < 0 for cube in data_unloader.infection_cubes):  # We lose if we can't place infection cubes
        game_over = True
        world_map_drawer.queue_game_text("❌ Game Over! Ran out of infection cubes!", delay = 1500)
        turn_handler.end_game(game_over)
        return True
    elif all(status > 0 for status in data_unloader.infection_status):  # We win if all diseases are cured
        game_over = True
        world_map_drawer.queue_game_text("✅ You've successfully cured all diseases! You win!", delay = 1500)
        turn_handler.end_game(game_over)
        return True
    return False

# Function to reset the card draws at the start of each phase
def reset_card_draws(player_id):
    """Makes sure the card draws and ability locks are reset after turn end."""
    global remaining_player_cards, remaining_infection_cards, operations_expert_switch, improved_sanitation_active
    global playercards_drawn, infectioncards_drawn, player_draw_locked  # ✅ add this
    remaining_player_cards = 2  # Reset player card draws (fixed)
    remaining_infection_cards = data_unloader.infection_rate_marker_amount[
        data_unloader.infection_rate_marker]  # Set infection card draws based on infection rate
    data_unloader.actions = 4
    playercards_drawn = 0
    infectioncards_drawn = 0
    player_draw_locked = False
    operations_expert_switch = True
    world_map_drawer.update_text(player_id)
    # Check if any event card is active
    for card in data_unloader.playercard_discard:
        if card.get("name") == "Infection Zone Ban" and card.get("active"):
            # If active, increment its internal timer
            card["timer"] = card.get("timer", 0) + 1
            # If it has cycled back to the original player, deactivate it
            if card["timer"] >= len(data_unloader.in_game_roles):
                card["active"] = False
                card["timer"] = 0
                world_map_drawer.queue_game_text("🧼 Infection Zone Ban effect has ended.", delay = 1500)
        elif card.get("name") == "Improved Sanitation" and card.get("active"):
            # If active, increment its internal timer
            card["timer"] = card.get("timer", 0) + 1
            # If it has cycled back to the original player, deactivate it
            if card["timer"] >= len(data_unloader.in_game_roles):
                card["active"] = False
                card["timer"] = 0
                improved_sanitation_active = False
                world_map_drawer.queue_game_text("🧼 Improved Sanitation effect has ended.", delay = 1500)

def drive_ferry(player_id) -> None:
    """Perform the Drive/Ferry action."""
    if world_map_drawer.can_perform_action():
        global quarantined_cities, mobile_hospital_active, medic_protected_city
        role = data_unloader.in_game_roles[player_id]
        current_city = data_unloader.players_locations[player_id]
        neighbors = data_unloader.cities[current_city]["relations"]

        popup = tk.Toplevel()
        popup.title("Drive/Ferry - Select destination")
        popup.geometry("300x200")

        tk.Label(popup, text=f"Currently in: {current_city}", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(popup, text="Select a destination:", font=("Arial", 10)).pack()

        def handle_selection(destination):
            data_unloader.players_locations[player_id] = destination
            data_unloader.cities[current_city]["player_amount"] -= 1
            data_unloader.cities[destination]["player_amount"] += 1
            data_unloader.actions -= 1
            world_map_drawer.queue_game_text(f"🛻 Player {player_id + 1} moved to {destination}!", delay = 1500)
            world_map_drawer.update_player_marker(player_id, destination)
            world_map_drawer.update_text(player_id)
            popup.destroy()
            if role == "Quarantine Specialist":
                quarantined_cities.clear()
                quarantined_cities.append(destination)
                for neighbour in data_unloader.cities[destination]["relations"]:
                    quarantined_cities.append(neighbour)
            elif role == "Medic":
                medic_protected_city = destination
                infection_levels = data_unloader.cities[destination]["infection_levels"]
                for i, cubes in enumerate(infection_levels):
                    if cubes > 0 and data_unloader.infection_status[i] >= 1:  # if cured
                        data_unloader.infection_cubes[i] += cubes
                        infection_levels[i] = 0
                        world_map_drawer.queue_game_text(
                            f"🧪 Medic removed all {['yellow', 'red', 'blue', 'black'][i]} cubes in {destination} by drive/ferry!", delay = 1500
                        )
                world_map_drawer.update_text(player_id)
            elif mobile_hospital_active:
                    infection_levels = data_unloader.cities[destination]["infection_levels"]
                    present_diseases = [(i, level) for i, level in enumerate(infection_levels) if level > 0]

                    if not present_diseases:
                        world_map_drawer.queue_game_text(f"No disease cubes to remove in {destination}.", delay = 1500)
                        return

                    if len(present_diseases) == 1:
                        # Only one — remove automatically
                        disease_index = present_diseases[0][0]
                        data_unloader.cities[destination]["infection_levels"][disease_index] -= 1
                        data_unloader.infection_cubes[disease_index] += 1
                        world_map_drawer.queue_game_text(
                            f"🛻 Mobile Hospital: Removed 1 {['yellow', 'red', 'blue', 'black'][disease_index]} cube from {destination}.", delay = 1500
                        )
                        world_map_drawer.update_text(player_id)
                        return

                    # Multiple — show popup!
                    def remove_and_close(index):
                        data_unloader.cities[destination]["infection_levels"][index] -= 1
                        data_unloader.infection_cubes[index] += 1
                        world_map_drawer.queue_game_text(
                            f"🛻 Mobile Hospital: Removed 1 {['yellow', 'red', 'blue', 'black'][index]} cube from {destination}.", delay = 1500
                        )
                        world_map_drawer.update_text(player_id)
                        hospital_popup.destroy()

                    hospital_popup = tk.Toplevel(world_map_drawer.root)
                    hospital_popup.title("Mobile Hospital - Choose Disease to Remove")
                    hospital_popup.geometry("350x200")
                    tk.Label(hospital_popup, text=f"{destination} has multiple infections. Choose one to remove:").pack(
                        pady=10)

                    for i, lvl in present_diseases:
                        color = ["yellow", "red", "blue", "black"][i]
                        tk.Button(
                            hospital_popup,
                            text=f"{color.capitalize()} ({lvl} cubes)",
                            command=lambda idx=i: remove_and_close(idx)
                        ).pack(pady=5)

                    hospital_popup.grab_set()

        for city in neighbors:
            tk.Button(
                popup,
                text=city,
                width=25,
                command=lambda c=city: handle_selection(c)
            ).pack(pady=3)

def direct_flight(player_id) -> None:
    """Perform the Direct Flight action."""
    if world_map_drawer.can_perform_action():
        discard(player_id, 1, "direct_flight")

def charter_flight(player_id) -> None:
    """Perform the Charter Flight action."""
    if world_map_drawer.can_perform_action():
        discard(player_id, 1, "charter_flight")

def shuttle_flight(player_id) -> None:
    """Perform the Shuttle Flight action."""
    if world_map_drawer.can_perform_action():
        current_city = data_unloader.players_locations[player_id]
        role = data_unloader.in_game_roles[player_id]

        # 1. Check if current city has a research center
        if not data_unloader.cities[current_city]["research_center"]:
            world_map_drawer.queue_game_text(f"⚠️ {current_city} does not have a research center.", delay = 1500)
            return

        # 2. Find other cities with research centers
        destinations = [city for city, data in data_unloader.cities.items()
                        if data["research_center"] and city != current_city]

        if not destinations:
            world_map_drawer.queue_game_text("⚠️ No other research centers to shuttle to.", delay = 1500)
            return

        # 3. Popup for destination selection
        popup = tk.Toplevel(world_map_drawer.root)
        popup.title("Shuttle Flight - Choose Destination")
        popup.geometry("350x200")

        tk.Label(popup, text="Select a destination city with a research center:").pack(pady=10)
        selected_city = tk.StringVar(value=destinations[0])

        dropdown = tk.OptionMenu(popup, selected_city, *destinations)
        dropdown.pack(pady=10)

        def confirm_flight():
            destination = selected_city.get()
            data_unloader.cities[current_city]["player_amount"] -= 1
            data_unloader.cities[destination]["player_amount"] += 1
            data_unloader.players_locations[player_id] = destination
            data_unloader.actions -= 1
            world_map_drawer.queue_game_text(f"🛩️ Player {player_id + 1} shuttled to {destination}.", delay = 1500)
            world_map_drawer.update_player_marker(player_id, destination)
            world_map_drawer.update_text(player_id)
            popup.destroy()
            if role == "Quarantine Specialist":
                quarantined_cities.clear()
                quarantined_cities.append(destination)
                for neighbour in data_unloader.cities[destination]["relations"]:
                    quarantined_cities.append(neighbour)
            elif role == "Medic":
                medic_protected_city = destination
            infection_levels = data_unloader.cities[destination]["infection_levels"]
            for i, cubes in enumerate(infection_levels):
                if cubes > 0 and data_unloader.infection_status[i] >= 1:  # if cured
                    data_unloader.infection_cubes[i] += cubes
                    infection_levels[i] = 0
                    world_map_drawer.queue_game_text(
                        f"🧪 Medic removed all {['yellow', 'red', 'blue', 'black'][i]} infection cubes in {destination} by shuttle flight!", delay = 1500
                    )
            world_map_drawer.update_text(player_id)

        tk.Button(popup, text="Confirm", command=confirm_flight).pack(pady=10)
        popup.grab_set()
        popup.wait_window()

def oe_build_research_center(player_id) -> bool:
    """Performs the Build Research Center action without discarding for O.E. for the first time."""
    global operations_expert_switch
    action_done = {"ok": False}  # ← mutable flag we’ll update inside callbacks
    current_city = data_unloader.players_locations[player_id]
    if data_unloader.cities[current_city]["research_center"] == 1:
        messagebox.showinfo("Already Present", f"There is already a research center in {current_city}.")
        return False

    # Count total research centers
    total_research_centers = sum(
        city_data["research_center"] for city_data in data_unloader.cities.values())

    if total_research_centers >= 6:
        # Let player choose one to remove
        other_cities = [name for name, data in data_unloader.cities.items()
                        if data["research_center"] == 1 and name != current_city]

        def choose_research_center_to_remove():
            select_popup = tk.Toplevel()
            select_popup.title("Remove a Research Center")
            select_popup.geometry("400x300")

            tk.Label(select_popup, text="Choose a city to remove its research center:").pack(pady=10)

            removable_city = tk.StringVar(value=other_cities[0])
            city_menu = tk.OptionMenu(select_popup, removable_city, *other_cities)
            city_menu.pack(pady=10)

            def confirm_removal():
                global operations_expert_switch
                chosen_city = removable_city.get()
                data_unloader.cities[chosen_city]["research_center"] = 0
                data_unloader.cities[current_city]["research_center"] = 1
                operations_expert_switch = False
                data_unloader.actions -= 1
                world_map_drawer.queue_game_text(
                    f"🏛️ Moved research center from {chosen_city} to {current_city}.", delay = 1500)
                world_map_drawer.update_research_centers()
                action_done["ok"] = True
                select_popup.destroy()

            tk.Button(select_popup, text="Confirm", command=confirm_removal).pack(pady=10)
            select_popup.grab_set()
            select_popup.wait_window()

        choose_research_center_to_remove()
    else:
        # Add research center normally
        data_unloader.cities[current_city]["research_center"] = 1
        data_unloader.actions -= 1
        operations_expert_switch = False
        world_map_drawer.queue_game_text(
            f"🏛️ Player {player_id + 1} built research center in {current_city}!", delay = 1500)
        world_map_drawer.update_research_centers()
        action_done["ok"] = True
    return action_done["ok"]  # tell the caller whether the build really happened

def government_grant_popup(player_id, on_confirm_callback):
    """Event card: Add a research center to any city (no city card needed)."""
    available_cities = [name for name, data in data_unloader.cities.items() if data["research_center"] == 0]

    if not available_cities:
        messagebox.showinfo("No Available Cities", "All cities already have research centers.")
        return

    total_research_centers = sum(city["research_center"] for city in data_unloader.cities.values())

    popup = tk.Toplevel()
    popup.title("Government Grant")
    popup.geometry("400x250")

    tk.Label(popup, text="Select a city to build a research center:", font=("Arial", 10)).pack(pady=10)

    city_var = tk.StringVar(value=available_cities[0])
    tk.OptionMenu(popup, city_var, *available_cities).pack(pady=5)

    def confirm_gg():
        selected_city = city_var.get()

        if total_research_centers >= 6:
            existing_rcs = [name for name, data in data_unloader.cities.items()
                            if data["research_center"] == 1 and name != selected_city]

            if not existing_rcs:
                messagebox.showerror("No Removable RCs", "No other research center to move.")
                popup.destroy()
                return

            def choose_removal():
                removal_popup = tk.Toplevel()
                removal_popup.title("Remove Existing Research Center")
                removal_popup.geometry("400x250")

                tk.Label(removal_popup, text="Choose a city to remove its research center:").pack(pady=10)

                removal_var = tk.StringVar(value=existing_rcs[0])
                tk.OptionMenu(removal_popup, removal_var, *existing_rcs).pack(pady=10)

                def confirm_removal():
                    removed = removal_var.get()
                    data_unloader.cities[removed]["research_center"] = 0
                    data_unloader.cities[selected_city]["research_center"] = 1
                    world_map_drawer.queue_game_text(f"🏛️ Government Grant: Moved RC from {removed} to {selected_city}.", delay = 1500)
                    world_map_drawer.update_research_centers()
                    removal_popup.destroy()
                    popup.destroy()
                    on_confirm_callback()  # ✅ Callback only after confirm

                tk.Button(removal_popup, text="Confirm", command=confirm_removal).pack(pady=10)
                removal_popup.grab_set()
                removal_popup.wait_window()

            choose_removal()
        else:
            data_unloader.cities[selected_city]["research_center"] = 1
            world_map_drawer.queue_game_text(f"🏛️ Government Grant: Built research center in {selected_city}.", delay = 1500)
            world_map_drawer.update_research_centers()
            popup.destroy()
            on_confirm_callback()  # ✅ Callback only after confirm

    tk.Button(popup, text="Build", command=confirm_gg).pack(pady=15)
    popup.grab_set()

def build_research_center(player_id) -> None:
    """Perform the action of building a research center."""
    if world_map_drawer.can_perform_action():
        role = data_unloader.in_game_roles[player_id]
        if role == "Operations Expert" and operations_expert_switch:
            oe_build_research_center(player_id)
        else:
            discard(player_id, 1, "build_research_center")

def treat_disease(player_id) -> None:
    """Perform the Treat Disease action."""
    if world_map_drawer.can_perform_action():
        current_city = data_unloader.players_locations[player_id]
        infection_levels = data_unloader.cities[current_city]["infection_levels"]
        role = data_unloader.in_game_roles[player_id]

        # Find which diseases are present
        present_diseases = [(i, level) for i, level in enumerate(infection_levels) if level > 0]

        if not present_diseases:
            world_map_drawer.queue_game_text(f"No disease to treat in {current_city}.", delay = 1500)
            return

        def perform_treatment(disease_index: int):
            message = ""
            cubes = infection_levels[disease_index]
            disease_color = ["yellow", "red", "blue", "black"][disease_index]
            is_cured = data_unloader.infection_status[disease_index] >= 1

            if role == "Medic":
                # Remove all cubes of that disease
                data_unloader.infection_cubes[disease_index] += cubes
                data_unloader.cities[current_city]["infection_levels"][disease_index] = 0
                message = f"🧪Player {player_id + 1} (Medic) treated all {disease_color} cubes in {current_city}."
            elif is_cured:
                # Remove all cubes of that disease
                data_unloader.infection_cubes[disease_index] += cubes
                data_unloader.cities[current_city]["infection_levels"][disease_index] = 0
                message = f"🧪Player {player_id + 1} treated all cured {disease_color} cubes in {current_city}."
            elif improved_sanitation_active:
                if data_unloader.cities[current_city]["infection_levels"][disease_index] > 1:
                    data_unloader.infection_cubes[disease_index] += 2
                    data_unloader.cities[current_city]["infection_levels"][disease_index] -= 2
                    message = f"🧪Player {player_id + 1} treated 2 {disease_color} cube in {current_city} with Improved Sanitation."
                elif data_unloader.cities[current_city]["infection_levels"][disease_index] == 1:
                    data_unloader.infection_cubes[disease_index] += 1
                    data_unloader.cities[current_city]["infection_levels"][disease_index] -= 1
                    message = f"🧪Player {player_id + 1} treated 1 {disease_color} cube in {current_city} with Improved Sanitation."
            else:
                # Remove one cube
                data_unloader.infection_cubes[disease_index] += 1
                data_unloader.cities[current_city]["infection_levels"][disease_index] -= 1
                message = f"🧪Player {player_id + 1} treated 1 {disease_color} cube in {current_city}."

            # If we remove all disease cubes of a cured infection, the infection_status changes to eradicated (2)
            if is_cured and data_unloader.infection_cubes[disease_index] == 24:
                data_unloader.infection_status[disease_index] = 2
                world_map_drawer.update_disease_status(disease_index)

            data_unloader.actions -= 1
            world_map_drawer.queue_game_text(message, delay = 1500)
            world_map_drawer.update_text(player_id)

        if len(present_diseases) == 1:
            # Only one disease present: treat automatically
            perform_treatment(present_diseases[0][0])
        else:
            # Multiple diseases present: show popup to choose
            popup = tk.Toplevel(world_map_drawer.root)
            popup.title("Choose Disease to Treat")
            popup.geometry("300x200")

            tk.Label(popup, text=f"{current_city} has multiple diseases. Choose one to treat:").pack(pady=10)

            for index, count in present_diseases:
                color = ["yellow", "red", "blue", "black"][index]

                def make_treatment_callback(disease_index):
                    return lambda: (perform_treatment(disease_index), popup.destroy())

                btn = tk.Button(
                    popup,
                    text=f"{color.capitalize()} ({count} cubes)",
                    command=make_treatment_callback(index)
                )
                btn.pack(pady=5)

            popup.grab_set()


def share_knowledge(player_id) -> None:
    """Perform the Share Knowledge action (original and modified rule options)."""
    if world_map_drawer.can_perform_action():
        current_city = data_unloader.players_locations[player_id]

        # Find other players in the same city
        others_in_city = [
            pid for pid, city in data_unloader.players_locations.items()
            if city == current_city and pid != player_id
        ]

        if not others_in_city:
            world_map_drawer.queue_game_text("No other player in the city to share knowledge with.", delay = 1500)
            return

        # ===================== ORIGINAL RULE VERSION =====================
        # Comment out this block if using the modified rule below
        """city_card = None
        giver_id = None
        receiver_id = None

        for card in data_unloader.players_hands[player_id]:
            if card["name"] == current_city:
                city_card = card
                giver_id = player_id
                break

        if city_card:
            # Current player has the city card — allow selection of recipient
            popup = tk.Toplevel(world_map_drawer.root)
            popup.title("Share Knowledge")
            popup.geometry("350x250")

            tk.Label(popup, text="Select a player to give the city card to:").pack(pady=10)
            recipient_var = tk.IntVar(value=others_in_city[0])

            for pid in others_in_city:
                tk.Radiobutton(popup, text=f"Player {pid + 1}", variable=recipient_var, value=pid).pack(anchor="w")

            def confirm_give():
                receiver_id = recipient_var.get()
                data_unloader.players_hands[giver_id].remove(city_card)
                data_unloader.players_hands[receiver_id].append(city_card)
                data_unloader.actions -= 1
                world_map_drawer.update_text(giver_id)
                world_map_drawer.update_text(receiver_id)
                world_map_drawer.queue_game_text(
                    f"💬 Player {giver_id + 1} gave '{current_city}' card to Player {receiver_id + 1}.", delay = 1500
                )
                popup.destroy()
                if len(data_unloader.players_hands[receiver_id]) > 7:
                    data_unloader.current_hand = data_unloader.players_hands[receiver_id]
                    discard(receiver_id, len(data_unloader.players_hands[receiver_id]) - 7, "card_overflow")
                    data_unloader.current_hand = data_unloader.players_hands[player_id]
                elif len(data_unloader.players_hands[giver_id]) > 7:
                    data_unloader.current_hand = data_unloader.players_hands[giver_id]
                    discard(giver_id, len(data_unloader.players_hands[giver_id]) - 7, "card_overflow")
                    data_unloader.current_hand = data_unloader.players_hands[player_id]

            tk.Button(popup, text="Confirm", command=confirm_give).pack(pady=10)
            popup.grab_set()
            return

        # If another player has the city card — allow taking it
        for pid in others_in_city:
            for card in data_unloader.players_hands[pid]:
                if card["name"] == current_city:
                    city_card = card
                    giver_id = pid
                    receiver_id = player_id
                    break
            if city_card:
                break

        if not city_card:
            world_map_drawer.queue_game_text("No one has the city card to share.", delay = 1500)
            return

        popup = tk.Toplevel(world_map_drawer.root)
        popup.title("Share Knowledge")
        popup.geometry("350x180")

        msg = f"Player {giver_id + 1} gives '{current_city}' card to Player {receiver_id + 1}?"
        tk.Label(popup, text=msg, font=("Arial", 10)).pack(pady=10)

        def confirm_take():
            data_unloader.players_hands[giver_id].remove(city_card)
            data_unloader.players_hands[receiver_id].append(city_card)
            world_map_drawer.update_text(giver_id)
            world_map_drawer.update_text(receiver_id)
            world_map_drawer.queue_game_text(
                f"💬 Player {giver_id + 1} gave '{current_city}' card to Player {receiver_id + 1}!", delay = 1500
            )
            popup.destroy()
            if len(data_unloader.players_hands[receiver_id]) > 7:
                data_unloader.current_hand = data_unloader.players_hands[receiver_id]
                discard(receiver_id, len(data_unloader.players_hands[receiver_id]) - 7, "card_overflow")
                data_unloader.current_hand = data_unloader.players_hands[player_id]
            elif len(data_unloader.players_hands[giver_id]) > 7:
                data_unloader.current_hand = data_unloader.players_hands[giver_id]
                discard(giver_id, len(data_unloader.players_hands[giver_id]) - 7, "card_overflow")
                data_unloader.current_hand = data_unloader.players_hands[player_id]

        tk.Button(popup, text="Confirm", command=confirm_take).pack(pady=10)
        popup.grab_set()
        return"""

        # ===================== MODIFIED RULE VERSION =====================
        # Uncomment this block if using the modified rule instead
        popup = tk.Toplevel(world_map_drawer.root)
        popup.title("Modified Share Knowledge")
        popup.geometry("400x350")

        tk.Label(popup, text="Select a player to trade with:").pack(pady=5)
        player_var = tk.IntVar(value=others_in_city[0])
        for pid in others_in_city:
            tk.Radiobutton(popup, text=f"Player {pid + 1}", variable=player_var, value=pid).pack(anchor="w")

        direction_var = tk.StringVar(value="give")
        tk.Label(popup, text="Select transfer direction:").pack(pady=5)
        tk.Radiobutton(popup, text="Give a card", variable=direction_var, value="give").pack(anchor="w")
        tk.Radiobutton(popup, text="Receive a card", variable=direction_var, value="receive").pack(anchor="w")

        def select_card():
            target_pid = player_var.get()
            direction = direction_var.get()
            source_id = player_id if direction == "give" else target_pid
            target_id = target_pid if direction == "give" else player_id

            source_hand = data_unloader.players_hands[source_id]

            card_popup = tk.Toplevel(world_map_drawer.root)
            card_popup.title("Select Card")
            card_popup.geometry("400x400")

            tk.Label(card_popup, text="Select a card to transfer:").pack(pady=5)
            selected_card_name = tk.StringVar()

            for card in source_hand:
                tk.Radiobutton(card_popup, text=card["name"], variable=selected_card_name, value=card["name"]).pack(anchor="w")

            def confirm_transfer():
                chosen_name = selected_card_name.get()
                if not chosen_name:
                    return

                card = next(card for card in source_hand if card["name"] == chosen_name)
                data_unloader.players_hands[source_id].remove(card)
                data_unloader.players_hands[target_id].append(card)

                data_unloader.actions -= 1
                world_map_drawer.update_text(source_id)
                world_map_drawer.update_text(target_id)
                world_map_drawer.queue_game_text(
                    f"💬 Shared card '{chosen_name}' from Player {source_id + 1} to Player {target_id + 1}", delay = 1500
                )

                # Moved here: check *after* transfer is completed
                if len(data_unloader.players_hands[target_id]) > 7:
                    data_unloader.current_hand = data_unloader.players_hands[target_id]
                    discard(target_id, len(data_unloader.players_hands[target_id]) - 7, "card_overflow")
                    data_unloader.current_hand = data_unloader.players_hands[player_id]
                elif len(data_unloader.players_hands[source_id]) > 7:
                    data_unloader.current_hand = data_unloader.players_hands[source_id]
                    discard(source_id, len(data_unloader.players_hands[source_id]) - 7, "card_overflow")
                    data_unloader.current_hand = data_unloader.players_hands[player_id]

                # ✅ Only close windows after handling overflow logic
                card_popup.destroy()
                popup.destroy()

            tk.Button(card_popup, text="Confirm", command=confirm_transfer).pack(pady=10)
            card_popup.grab_set()

        tk.Button(popup, text="Next", command=select_card).pack(pady=10)
        popup.grab_set()

def discover_cure(player_id) -> None:
    """Perform the Discover Cure action."""
    if world_map_drawer.can_perform_action():
        current_city = data_unloader.players_locations[player_id]
        if data_unloader.cities[current_city]["research_center"] != 1:
            world_map_drawer.queue_game_text(
                f"{data_unloader.players_locations[player_id]} has no research center!", delay = 1500)
            return
        role = data_unloader.in_game_roles[player_id]
        if role == "Scientist":
            discard(player_id, 4, "discover_cure")
        else:
            discard(player_id, 5, "discover_cure")

def play_event_card(player_id) -> None:
    """Playing an event card action."""
    hand = data_unloader.players_hands[player_id]

    event_cards = [card for card in hand if card.get("cardtype") == "event_card" or "effect" in card]

    if not event_cards:
        world_map_drawer.queue_game_text("No event cards to play.", delay = 1500)
        return

    popup = tk.Toplevel(world_map_drawer.root)
    popup.title("Play Event Card")
    popup.geometry("400x300")
    tk.Label(popup, text="Select an event card to play:").pack(pady=10)

    def finalize_card_use(card):
        card_name = card["name"]
        for c in hand:
            if c["name"] == card_name:
                hand.remove(c)
                break
        data_unloader.playercard_discard.append(card)
        if card["name"] != "One Quiet Night":
            world_map_drawer.queue_game_text(f"🎴 Player {player_id + 1} played {card['name']}!", delay = 1500)
        else:
            world_map_drawer.queue_game_text(f"🎴 Player {player_id + 1} played {card['name']}! Click the infection deck to proceed!", delay = 1500)
        popup.destroy()

    def play(card):
        name = card["name"]
        if name == "Borrowed Time":
            data_unloader.actions += 2
            world_map_drawer.update_text(player_id)
            finalize_card_use(card)
        elif name == "Remote Treatment":
            remote_treatment_popup(player_id, lambda: finalize_card_use(card))
        elif name == "Mobile Hospital":
            global mobile_hospital_active
            mobile_hospital_active = True
            finalize_card_use(card)
        elif name == "Government Grant":
            government_grant_popup(player_id, lambda: finalize_card_use(card))
        elif name == "Infection Zone Ban":
            card["active"] = True
            card["timer"] = 0
            finalize_card_use(card)
        elif name == "Improved Sanitation":
            card["active"] = True
            card["timer"] = 0
            global improved_sanitation_active
            improved_sanitation_active = True
            finalize_card_use(card)
        elif name == "One Quiet Night":
            global infectionless_night
            infectionless_night = True
            finalize_card_use(card)

    for card in event_cards:
        btn_text = f"{card['name']}: {card.get('effect', '')}"
        tk.Button(popup, text=btn_text, wraplength=350, command=lambda c=card: play(c)).pack(pady=5)

    popup.grab_set()

def remote_treatment_popup(player_id, on_confirm_callback) -> None:
    """Performs the remote treatment event card: remove 2 infection cubes from the board."""
    max_treats = 2
    infection_colors = ["yellow", "red", "blue", "black"]

    popup = tk.Toplevel(world_map_drawer.root)
    popup.title("Remote Treatment")
    popup.geometry("500x400")

    tk.Label(popup, text="Select up to 2 cities and remove one cube from each:").pack(pady=10)

    cities = data_unloader.cities
    city_vars = []
    color_vars = []
    color_menus = []

    def get_valid_colors(city_name):
        if not city_name or city_name not in cities:
            return []
        levels = cities[city_name]["infection_levels"]
        return [infection_colors[i] for i, lvl in enumerate(levels) if lvl > 0]

    def update_color_options(index, *args):
        selected_city = city_vars[index].get()
        menu = color_menus[index]["menu"]
        menu.delete(0, "end")
        valid_colors = get_valid_colors(selected_city)
        color_vars[index].set(valid_colors[0] if valid_colors else "")
        for color in valid_colors:
            menu.add_command(label=color, command=lambda c=color: color_vars[index].set(c))

    for i in range(max_treats):
        frame = tk.Frame(popup)
        frame.pack(pady=5)

        tk.Label(frame, text=f"Target {i + 1}").grid(row=0, column=0, padx=5)

        city_var = tk.StringVar()
        city_menu = tk.OptionMenu(frame, city_var, *cities.keys())
        city_menu.grid(row=0, column=1, padx=5)

        color_var = tk.StringVar()
        color_menu = tk.OptionMenu(frame, color_var, "")
        color_menu.grid(row=0, column=2, padx=5)

        def make_trace_callback(index):
            def callback(var_name, index_name, operation):
                update_color_options(index)

            return callback

        city_var.trace_add("write", make_trace_callback(i))
        city_vars.append(city_var)
        color_vars.append(color_var)
        color_menus.append(color_menu)

    def confirm():
        selected_pairs = []

        for i in range(max_treats):
            city = city_vars[i].get()
            color = color_vars[i].get()

            if not city or not color or city not in cities:
                continue

            color_index = infection_colors.index(color)
            infection_level = cities[city]["infection_levels"][color_index]

            # Count how many times this (city, color) has already been chosen
            count = selected_pairs.count((city, color_index))
            if infection_level > count:
                selected_pairs.append((city, color_index))

        if len(selected_pairs) != 2:
            messagebox.showerror("Invalid Action", "You must treat exactly 2 disease cubes.\nEach must exist.")
            return

        # ✅ Apply treatment now
        for city, color_index in selected_pairs:
            cities[city]["infection_levels"][color_index] -= 1
            data_unloader.infection_cubes[color_index] += 1
            world_map_drawer.queue_game_text(f"💉 Removed 1 {infection_colors[color_index]} cube from {city}.", delay = 1500)

        world_map_drawer.update_text(player_id)
        on_confirm_callback()
        popup.destroy()

        world_map_drawer.update_text(player_id)
        on_confirm_callback()
        popup.destroy()

    tk.Button(popup, text="Confirm", command=confirm).pack(pady=20)
    popup.grab_set()

def skip_turn(player_id) -> None:
    """Skip the current player's turn."""
    if data_unloader.actions != 0:
        data_unloader.actions = 0
        world_map_drawer.queue_game_text(f"Player {player_id + 1} skipped turn!", delay = 1500)
    world_map_drawer.update_text(player_id)

def drawing_phase(player_id) -> None:
    """
    Execute the drawing phase for the current player.
    Draws 2 player cards, handles epidemic logic, and transitions to infection phase.
    """
    hand = data_unloader.current_hand
    card = data_unloader.player_deck.pop(0)
    world_map_drawer.queue_game_text(f"🎴 Player {player_id + 1} drew: {card['name']}", delay = 1500)

    if card["name"] == "Epidemic":
        world_map_drawer.queue_game_text("🧨 Epidemic card drawn! Increase, Infect, and Intensify", delay = 1500)
        # ✅ Remove epidemic card from the game by tracking it explicitly
        data_unloader.epidemiccard_discard.append(card)
        handle_epidemic(player_id)
    else:
        hand.append(card)
        if len(data_unloader.players_hands[player_id]) > 7:
            discard(player_id, len(data_unloader.players_hands[player_id]) - 7, "card_overflow")

    # Update text on the map to reflect new hand size
    world_map_drawer.update_text(player_id)

def infection_phase(player_id) -> None:
    """
    Draw one infection card and resolve it:
    1. Infect the city with 1 cube of the card's color.
    2. If the city already has 3 cubes, trigger an outbreak.
    """
    global infectionless_night
    infection_discard = data_unloader.infection_discard
    infections = data_unloader.infections
    infection_cubes = data_unloader.infection_cubes
    cities = data_unloader.cities

    # 1. Draw the top card from the infection deck
    if infections and not infectionless_night:
        infection_card = infections.pop(0)  # Top of the deck
        infection_discard.append(infection_card)
        city_name = infection_card["name"]
        city_color = infection_card["color"]
        color_index = ["yellow", "red", "blue", "black"].index(city_color)

        world_map_drawer.queue_game_text(f"🦠 Infecting {city_name} with 1 {city_color} cube.", delay = 1500)
        if city_name in cities and city_name not in quarantined_cities and city_name != medic_protected_city and data_unloader.infection_status[color_index] != 2:
            current_level = cities[city_name]["infection_levels"][color_index]
            cubes_to_add = 1

            if current_level + cubes_to_add > 3:
                # 3 cubes already there — outbreak occurs
                world_map_drawer.queue_game_text(f"💥 Outbreak triggered in {city_name}!", delay = 1500)
                check_game_over()
                trigger_outbreak(city_name, color_index)
            else:
                # Normal infection
                check_game_over()
                cities[city_name]["infection_levels"][color_index] += 1
                infection_cubes[color_index] -= 1
                world_map_drawer.queue_game_text(f"🦠 1 {city_color} cube added to {city_name}.", delay = 1500)
            world_map_drawer.update_text(player_id)
        else:
            world_map_drawer.queue_game_text(f"🛡️ Infection/Outbreak prevented in {city_name} by Medic/Quarantine Specialist!", delay = 1500)
            return

def draw_player_card(player_id) -> None:
    """Draw a player card for the current player."""
    global playercards_drawn, player_draw_locked
    if player_draw_locked:
        world_map_drawer.queue_game_text("⛔ Player draw is currently locked.", delay = 1500)
        return
    check_game_over()
    if playercards_drawn < remaining_player_cards and data_unloader.actions == 0 and infectioncards_drawn == 0:
        drawing_phase(player_id)
        playercards_drawn += 1
    else:
        world_map_drawer.queue_game_text("It's not the drawing phase yet!", delay = 1500)
    if playercards_drawn == remaining_player_cards:
        world_map_drawer.queue_game_text("End of Drawing Phase!", delay = 1500)
        player_draw_locked = True

def draw_infection_card(player_id) -> None:
    """Draw an infection card for the current player."""
    global infectioncards_drawn, infectionless_night, remaining_infection_cards
    if infectionless_night:
        remaining_infection_cards = 1
        infectionless_night = False
    if infectioncards_drawn < remaining_infection_cards and data_unloader.actions == 0 and player_draw_locked:
        infection_phase(player_id)
        infectioncards_drawn += 1
    else:
        world_map_drawer.queue_game_text("It's not the infection phase yet!", delay = 1500)
    if infectioncards_drawn == remaining_infection_cards:
        world_map_drawer.queue_game_text("End of Turn!", delay = 1500)
        transition_to_next_phase(player_id)

# Call this function before transitioning to a new phase
def transition_to_next_phase(player_id):
    """Moves to the next player's turn, resets cards."""
    from pandemic import turn_handler
    reset_card_draws(player_id)

    # Just go to the next player with a short pause
    turn_handler.next_turn()

def handle_epidemic(player_id):
    """
    Handles the effects of an epidemic card:
    1. Increase infection rate
    2. Infect a city with 3 cubes
    3. Intensify (shuffle discard pile and place it on top)
    """
    global remaining_infection_cards
    # 1. Increase infection rate marker
    data_unloader.infection_rate_marker += 1
    remaining_infection_cards = data_unloader.infection_rate_marker_amount[data_unloader.infection_rate_marker]
    # 2. Infect: Draw bottom card from infection deck
    if data_unloader.infections:
        bottom_card = data_unloader.infections.pop(-1)
        city = bottom_card["name"]
        color = bottom_card["color"]
        color_index = ["yellow", "red", "blue", "black"].index(color)

        if city not in quarantined_cities and city != medic_protected_city and data_unloader.infection_status[color_index] != 2:
            world_map_drawer.queue_game_text(f"☣️ Epidemic in {city}! Adding 3 {color} cubes.", delay = 1500)
            current_level = data_unloader.cities[city]["infection_levels"][color_index]
            cubes_to_add = 3

            if current_level + cubes_to_add > 3:
                # Outbreak should happen
                cubes_added = 3 - current_level  # Only add up to 3
                data_unloader.cities[city]["infection_levels"][color_index] = 3
                data_unloader.infection_cubes[color_index] -= cubes_added
                check_game_over()
                trigger_outbreak(city, color_index)
            else:
                # No outbreak, normal infection
                data_unloader.cities[city]["infection_levels"][color_index] = current_level + cubes_to_add
                data_unloader.infection_cubes[color_index] -= cubes_to_add
                check_game_over()
        else:
            world_map_drawer.queue_game_text(f"🛡️ Infection/Outbreak prevented in {city} by Medic/Quarantine Specialist!", delay = 1500)
            return
        data_unloader.infection_discard.append(bottom_card)

    # 3. Intensify: Shuffle discard pile and place on top
    random.shuffle(data_unloader.infection_discard)
    data_unloader.infections = data_unloader.infection_discard + data_unloader.infections
    data_unloader.infection_discard.clear()
    world_map_drawer.update_text(player_id)

def trigger_outbreak(city_name, color_index):
    """
    Triggers outbreak. When a city has an outbreak, all neighbors of it will get infected.
    If the neighbor is also on the brink of outbreak, a chain reaction happens and that city
    also performs an outbreak, not infecting the previous city with outbreak.
    """

    colors = ["yellow", "red", "blue", "black"]
    color = colors[color_index]
    protected_cities = set()  # Cities that already had an outbreak this round
    outbreak_queue = [city_name]  # Cities waiting to trigger outbreaks

    while outbreak_queue:
        city = outbreak_queue.pop(0)

        if city in protected_cities or city in quarantined_cities or city==medic_protected_city:
            continue  # Don't outbreak the same city twice in this chain

        world_map_drawer.queue_game_text(f"💥 Outbreak of {color} disease in {city}!", delay = 1500)
        data_unloader.outbreak_marker += 1
        world_map_drawer.update_outbreak_marker()
        check_game_over()

        protected_cities.add(city)

        for neighbor in data_unloader.cities[city]["relations"]:
            current_level = data_unloader.cities[neighbor]["infection_levels"][color_index]
            cubes_to_add = 1
            if neighbor not in quarantined_cities and neighbor != medic_protected_city and data_unloader.infection_status[color_index] != 2:
                if current_level + cubes_to_add > 3:
                    # Check for active Infection Zone Ban in discard
                    iz_ban_active = any(
                        card.get("name") == "Infection Zone Ban" and card.get("active", False)
                        for card in data_unloader.playercard_discard
                    )

                    if iz_ban_active:
                        world_map_drawer.queue_game_text(
                            f"🛡️ Chain reaction outbreak in {neighbor} prevented by Infection Zone Ban!", delay = 1500
                        )
                        # Still cap at 3 cubes, no outbreak occurs
                        data_unloader.cities[neighbor]["infection_levels"][color_index] = 3
                        data_unloader.infection_cubes[color_index] -= (3 - current_level)
                    else:
                        # Normal outbreak
                        cubes_added = 3 - current_level  # Add only up to 3 cubes
                        data_unloader.cities[neighbor]["infection_levels"][color_index] = 3
                        data_unloader.infection_cubes[color_index] -= cubes_added
                        check_game_over()
                        outbreak_queue.append(neighbor)
                else:
                    # No outbreak, normal infection
                    data_unloader.cities[neighbor]["infection_levels"][color_index] = current_level + cubes_to_add
                    data_unloader.infection_cubes[color_index] -= cubes_to_add
                    check_game_over()
            else:
                world_map_drawer.queue_game_text(f"🛡️ Infection/Outbreak prevented in {city} by Medic/Quarantine Specialist!", delay = 1500)
                return