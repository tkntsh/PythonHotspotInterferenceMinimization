import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import random
import sqlite3
from typing import List, Tuple, Dict

#constants
AREA_SIZE = 5000
NUM_HOTSPOTS = 1000
MIN_DISTANCE = 50
INTERFERENCE_DISTANCE = 275
NUM_CHANNELS = 5

#Hotspot class
class Hotspot:
    """Class representing a Wi-Fi hotspot."""
    def __init__(self, x: float, y: float, channel: int):
        self.x = x
        self.y = y
        self.channel = channel

def generateHotspots() -> List[Hotspot]:
    """Generating 1000 hotspots with random positions ensuring minimum distance."""
    hotspots = []
    attempts = 0
    maxAttempts = 10000
    #explain random.uniform()
    while len(hotspots) < NUM_HOTSPOTS and attempts < maxAttempts:
        x = random.uniform(0, AREA_SIZE)
        y = random.uniform(0, AREA_SIZE)
        tooClose = False

        #checking distance to existing hotspots
        for h in hotspots:
            dist = np.sqrt((x - h.x)**2 + (y - h.y)**2)
            if dist < MIN_DISTANCE:
                tooClose = True
                break

        if not tooClose:
            channel = random.randint(1, NUM_CHANNELS)
            hotspots.append(Hotspot(x, y, channel))
        attempts += 1

    if len(hotspots) < NUM_HOTSPOTS:
        raise ValueError(f"Could only generate {len(hotspots)} hotspots after {maxAttempts} attempts.")
    return hotspots

def saveHotspotsToDb(hotspots: List[Hotspot], dbName: str = "hotspots.db"):
    """Save hotspots to SQLite database."""
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS hotspots
                     (id INTEGER PRIMARY KEY, x REAL, y REAL, channel INTEGER)''')
    cursor.executemany("INSERT INTO hotspots (x, y, channel) VALUES (?, ?, ?)",
                       [(h.x, h.y, h.channel) for h in hotspots])
    conn.commit()
    conn.close()

def loadHotspotsFromDb(dbName: str = "hotspots.db") -> List[Hotspot]:
    """Load hotspots from SQLite database."""
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("SELECT x, y, channel FROM hotspots")
    hotspots = [Hotspot(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return hotspots
#explain Tuple
def findInterferingHotspots(hotspots: List[Hotspot]) -> Tuple[List[Tuple[int, int]], set]:
    """Identify pairs of hotspots that interfere with each other."""
    coords = np.array([[h.x, h.y] for h in hotspots])
    distMatrix = distance_matrix(coords, coords)
    interferingPairs = []
    interferingHotspots = set()

    for i in range(len(hotspots)):
        for j in range(i + 1, len(hotspots)):
            if distMatrix[i, j] < INTERFERENCE_DISTANCE and hotspots[i].channel == hotspots[j].channel:
                interferingPairs.append((i, j))
                interferingHotspots.add(i)
                interferingHotspots.add(j)

    return interferingPairs, interferingHotspots

def optimizeChannels(hotspots: List[Hotspot], maxIterations: int = 100) -> List[int]:
    """Minimize interference by iteratively changing channels."""
    interferenceCounts = []
    for iteration in range(maxIterations):
        interferingPairs, interferingHotspots = findInterferingHotspots(hotspots)
        interferenceCounts.append(len(interferingHotspots))

        if not interferingPairs:
            break

        # Randomly select an interfering hotspot and change its channel
        hotspotIDX = random.choice(list(interferingHotspots))
        currentChannel = hotspots[hotspotIDX].channel
        newChannel = random.choice([ch for ch in range(1, NUM_CHANNELS + 1) if ch != currentChannel])
        hotspots[hotspotIDX].channel = newChannel

    return interferenceCounts
#explain whole method
def plotInterferenceTrend(interferenceCounts: List[int], filename: str = "interference_trend.png"):
    """Plot the number of interfering hotspots over iterations."""
    plt.figure(figsize=(8, 6))
    plt.plot(interferenceCounts, marker='o')
    plt.xlabel("Iteration")
    plt.ylabel("Number of Interfering Hotspots")
    plt.title("Interference Reduction Over Iterations")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def plotHotspots(hotspots: List[Hotspot], interferingPairs: List[Tuple[int, int]], 
                  interferingHotspots: set, filename: str = "hotspot_map.png"):
    """Plot hotspot locations with channels and interference indicators."""
    plt.figure(figsize=(10, 10))
    colors = {1: 'blue', 2: 'green', 3: 'purple', 4: 'orange', 5: 'cyan'}

    # Plot hotspots
    for i, h in enumerate(hotspots):
        edge_color = 'red' if i in interferingHotspots else 'black'
        plt.scatter(h.x, h.y, c=colors[h.channel], s=50, edgecolors=edge_color, linewidth=1.5, 
                    label=f'Channel {h.channel}' if i == 0 or hotspots[i-1].channel != h.channel else "")

    # Plot interference lines
    for i, j in interferingPairs:
        plt.plot([hotspots[i].x, hotspots[j].x], [hotspots[i].y, hotspots[j].y], 'r-', linewidth=1)

    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.title("Wi-Fi Hotspot Locations and Interference")
    plt.legend()
    plt.savefig(filename)
    plt.close()

def main():
    #generate / save hotspots
    hotspots = generateHotspots()
    saveHotspotsToDb(hotspots)
    hotspots = loadHotspotsFromDb()

    #optimize channels
    interferenceCounts = optimizeChannels(hotspots)

    #getting final interference data
    interferingPairs, interferingHotspots = findInterferingHotspots(hotspots)

    #generate plots
    plotInterferenceTrend(interferenceCounts)
    plotHotspots(hotspots, interferingPairs, interferingHotspots)

    #save final hotspot configuration
    saveHotspotsToDb(hotspots, "hotspotsOptimized.db")

if __name__ == "__main__":
    main()