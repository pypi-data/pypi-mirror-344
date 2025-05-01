# Crown of the Abyss

## Description
Crow of the Abyss is a multiplayer, turn-based dungeon crawler with the goal of . . .

## Player Types
All player types have a base stats consisting of:

 - Damage (DG): Base damage of weapons.
 - Armor (AR): Reduces damage received.
 - Magic (MG): Base damage of magic weapons/items.
 - Health (HP): Can withstand more damage.
 - Speed (SP): Higher chance of evading attacks and attacking first.
 - Luck (LK): Non-enemy rooms have a higher chance of being more rewarding.
  

| Archetypes      | Description         | DG  | AR  | MG  | HP  | SP  | LK  |
|-----------------|---------------------|-----|-----|-----|-----|-----|-----|
| Warrior         | Melee specialist     |↑|↑|↓|-|-|-|
| Mage            | Master of magic      |-|↓|↑|↓|-|-|
| Rogue           | Stealth and agility  |-|-|↓|-|↑|↑|
| Tank         | Stalwart defender   |↓|↑|↓|↑|↓|-|
| Cleric          | Healer and support   |-|↓|↑|-|↑|↓|

## Enemy Types
...
## Room Types
...
## Multiplayer
Multiplayer allows teams to make more diverse experiences in Crown of the Abyss. However, the more players in your party, the more difficult the dungeon will be. Players can trade items and currency amongst each other.
...
## Game Architecture

### System Architecture
![crown-of-the-abyss-architecture](./crown-of-the-abyss-architecture.jpg)

The game uses a FastAPI hub server to manage use interactions, a FastAPI REST API to send and receive persistent data to a SQLite database. The game client holds all the game assets to reduce latency among server and other users.

### Database Architecture
![crown-of-the-abyss-database-tables](./DatabaseTableArchitecture.jpg)

A ER (Entity Relation) diagram displaying relations among resources and data in the database for The Crown of the Abyss.

## Resources

### Assets Creation
...
### Technical Libraries
... 


## Sprints

### Sprint 1

Basic game skeleton consists of:

*Database*

 - Database architecture graph
 - Database running with tables

*Hub Server*

 - Receiving WebScokets Connections

*REST API*

- Communicates with sqlite3

*Client*

- Renders Some Background
- Contains at least 2 rooms, one on screen at a time
- Some character on screen that move from room to room
- Sends moves via WebSockets Connections

### Sprint 2

*Hubserver*

- testing CI/CD
- building CI/CD
- update state based on user votes

API

- test cases for SQLite DB

Database

- DB File
- All tables

Client

- Send/recive data to server (://ws)
- store client state
- store others clients
- render on clients based on state
