# Wi-Fi Hotspot Interference Minimization

This project provides a Python-based solution to minimize interference among Wi-Fi hotspots distributed across a geographic area. The goal is to optimize channel assignments so that nearby hotspots avoid operating on the same channel, reducing signal interference.

## 📌 Project Overview

* **Area Covered**: 5x5 km
* **Number of Hotspots**: 1,000
* **Minimum Distance Between Hotspots**: 50 meters
* **Interference Range**: 275 meters
* **Channels Available**: 5 (Channels 1–5)

## 🚀 Features

* Random generation of hotspot locations with minimum separation.
* Channel optimization to reduce interference.
* SQLite database storage for persistence.
* Visualizations of both the optimization trend and final hotspot configuration.

## 🛠️ Technologies Used

* Python
* NumPy
* SciPy
* SQLite3
* Matplotlib
* Object-Oriented Programming

## 🧠 Key Components

### 🔹 Hotspot Generation

* A `Hotspot` class encapsulates the x/y coordinates and assigned channel.
* Randomized location generation with distance checks to prevent overlap.

### 🔹 Data Persistence

* Hotspot data saved and retrieved from `hotspots.db` using SQLite.

### 🔹 Interference Detection

* Efficient distance calculations using `scipy.spatial.distance_matrix`.
* Identifies pairs of interfering hotspots using the same channel within 275 meters.

### 🔹 Channel Optimization

* Iterative re-assignment of channels for interfering hotspots (up to 100 iterations).
* Aims to eliminate or reduce interference as quickly as possible.

### 🔹 Visualization

* **`interference_trend.png`**: Plots interference count over iterations.
* **`hotspot_map.png`**: Displays hotspot locations, color-coded by channel, with interfering pairs highlighted.

## 📊 Results

* Rapid reduction in interference over a few iterations.
* Final hotspot map highlights remaining problematic pairs.
* Visual tools provide transparency into the optimization process.

## 🧩 Potential Improvements

* Use advanced optimization (e.g., simulated annealing or graph coloring).
* Parallelize computations for scalability.
* Add user-configurable parameters (area size, channel count, etc.).

## 📁 How to Use

1. Clone the repository.
2. Run the Python script to generate hotspots and optimize channels.
3. Check generated visualizations (`interference_trend.png`, `hotspot_map.png`).
4. Explore or modify the SQLite database `hotspots.db`.
