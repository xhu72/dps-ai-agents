# Simple Reflex Vacuum-Cleaner Agent


## The Problem

A house with only **two rooms, A and B**. Each room is either **Clean** or **Dirty**. A small robot vacuum lives in the house, and its job is to keep both rooms clean.

The robot is very simple:

- It can only see **the room it is in right now**. It cannot see the other room.
- It has **no memory**. It does not remember anything from earlier steps.
- It can do only **three things**: `Suck`, move `Left`, or move `Right`.

## Input and Output

| | Description | Example |
|---|---|---|
| **Input (percept)** | The current location and its status | `("A", "Dirty")` |
| **Output (action)** | One of `Suck`, `Left`, `Right` | `"Suck"` |

## Condition-Action Rules

The agent checks these rules in order and uses the first one that matches:

1. If the current room is **Dirty** → `Suck`
2. Else, if the location is **A** → `Right`
3. Else, if the location is **B** → `Left`

## PEAS Description

| | |
|---|---|
| **Performance measure** | +1 point for each clean square at each time step |
| **Environment** | Two squares (A and B), each Clean or Dirty |
| **Actuators** | Wheels (Left, Right) and suction (Suck) |
| **Sensors** | Location sensor (A or B) and dirt sensor (Clean or Dirty) |

## Environment Type

| Property | Value | Why |
|---|---|---|
| Observable | Partially | The agent sees only its own square |
| Deterministic | Yes | Suck always cleans; moving always works |
| Episodic | No (sequential) | Moving now changes what the agent senses next |
| Static | Yes | Dirt does not change while the agent decides |
| Discrete | Yes | 2 squares, 2 statuses, 3 actions |
| Agents | Single | Only the vacuum |

## How the Program Works

The program follows the **sense → decide → act** loop from Chapter 2:

1. **Sense:** the environment gives the agent a percept `(location, status)`.
2. **Decide:** the agent applies its condition-action rules to that percept.
3. **Act:** the environment carries out the action (cleans the square or moves the agent).
4. The score is updated and the loop repeats.


## How to Run

Requires Python 3. 

```bash
python simple_reflex_agent.py
```
## Sample Output
The program runs the agent on all 8 possible starting worlds
(A Clean/Dirty × B Clean/Dirty × agent starting in A/B), 5 steps each.
The sample below shows one of them.
```
Start: {'A': 'Dirty', 'B': 'Dirty'} | agent in A
Step 1 | saw ('A', 'Dirty') | did Suck | world {'A': 'Clean', 'B': 'Dirty'} | score 1
Step 2 | saw ('A', 'Clean') | did Right | world {'A': 'Clean', 'B': 'Dirty'} | score 2
Step 3 | saw ('B', 'Dirty') | did Suck | world {'A': 'Clean', 'B': 'Clean'} | score 4
Step 4 | saw ('B', 'Clean') | did Left | world {'A': 'Clean', 'B': 'Clean'} | score 6
Step 5 | saw ('A', 'Clean') | did Right | world {'A': 'Clean', 'B': 'Clean'} | score 8
```
## Limitation

Once both rooms are clean, the agent keeps moving back and forth forever. Because it cannot see the other room and has no memory, it never knows that both rooms are clean.

