from ..main import Player, Enemy
from typing import Any
import pygame

def voting(state: dict, screen: pygame.Surface, player: Player, other_players: dict[int, Player], map: dict[int, Any]={}, enemies: dict[Any, Enemy]={}, key: str=""):
    """Handle player voting actions and position transitions.
   
   This function manages the voting process by positioning players in specific 
   locations on the screen based on their vote choice. Players can vote using 
   WASD keys, with each key corresponding to a different position and vote value.
   
   Args:
       state (dict): Dictionary containing the current state information of the player.
       screen (pygame.Surface): The pygame Surface object representing the game screen.
       player (Player): The player object that will be moved.
       other_players (dict): Dictionary of other player objects in the game.
       key (str): String representing the key pressed by the player. Defaults to empty string.
       map (dict): Dictionary of the map of the game. Defaults to empty dictionary.
   """ 
    w = screen.get_width()
    h = screen.get_height()

    top, bottom, left, right = getRoomsFromLinks(state["current_room_id"], map)

    # client transition
    if (key != ""):
        match (key):
            case "w":
                player.start_transition((w - player.width) // 2, 0, other_players, w, h)
                player.update_state({"vote": bottom})
            case "s":
                player.start_transition((w - player.width) // 2, h - player.height, other_players, w, h)
                player.update_state({"vote": top})
            case "a":
                player.start_transition(0, (h - player.height) // 2, other_players, w, h)
                player.update_state({"vote": left})
            case "d":
                player.start_transition(w - player.width, (h - player.height) // 2, other_players, w, h)
                player.update_state({"vote": right})
            case _:
                if (player.get_state().get("vote", -1) == -1):
                    player.start_transition((w - player.width) // 2, (h - player.height) // 2, other_players, w, h)


    # other player transition
    elif ("vote" in state.keys()):
        if (state["vote"] == bottom):
                player.start_transition((w - player.width) // 2, 0, other_players, w, h)
        elif (state["vote"] == left):
                player.start_transition(0, (h - player.height) // 2, other_players, w, h)
        elif (state["vote"] == top):
                player.start_transition((w - player.width) // 2, h - player.height, other_players, w, h)
        elif (state["vote"] == right):
                player.start_transition(w - player.width, (h - player.height) // 2, other_players, w, h)
        else:
                player.start_transition((w - player.width) // 2, (h - player.height) // 2, other_players, w, h)

def getRoomsFromLinks(current_room: str, map: dict[Any, Any]) -> tuple[int, int, int, int]:
    output = []
    for link in map[current_room]["links"]: 
        output.append(link["to_room"])

    return tuple(output)
