import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os
# --- 1. Synthetic Data Generation ---
# Generate synthetic data for store locations, competitor locations, and customer density
np.random.seed(42)  # for reproducibility
num_stores = 50
num_competitors = 100
x_stores = np.random.uniform(0, 100, num_stores)
y_stores = np.random.uniform(0, 100, num_stores)
x_competitors = np.random.uniform(0, 100, num_competitors)
y_competitors = np.random.uniform(0, 100, num_competitors)
customer_density = np.random.poisson(lam=10, size=num_stores) + np.random.normal(loc=0, scale=2, size=num_stores) #add some noise
customer_density = np.clip(customer_density, 0, 100) #ensure no negative density
# Create GeoDataFrames
stores_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(x_stores, y_stores))
competitors_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(x_competitors, y_competitors))
#add customer density to stores
stores_gdf['customer_density'] = customer_density
# --- 2. Spatial Analysis ---
# Calculate distances to nearest competitors
stores_gdf['distance_to_nearest_competitor'] = stores_gdf.geometry.distance(competitors_gdf.geometry.unary_union).min()
# --- 3. Regression Analysis ---
# Perform linear regression to predict customer density based on distance to nearest competitor
X = stores_gdf[['distance_to_nearest_competitor']]
y = stores_gdf['customer_density']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
r_sq = model.score(X_train, y_train)
print(f"coefficient of determination (R^2): {r_sq}")
# --- 4. Visualization ---
#Plot customer density vs distance to nearest competitor
plt.figure(figsize=(8, 6))
plt.scatter(stores_gdf['distance_to_nearest_competitor'], stores_gdf['customer_density'])
plt.plot(X_train, model.predict(X_train), color='red')
plt.xlabel('Distance to Nearest Competitor')
plt.ylabel('Customer Density')
plt.title('Customer Density vs. Distance to Nearest Competitor')
plt.savefig('customer_density_vs_distance.png')
print("Plot saved to customer_density_vs_distance.png")
#Plot store and competitor locations
plt.figure(figsize=(8,6))
stores_gdf.plot(ax=plt.gca(), color='blue', label='Stores')
competitors_gdf.plot(ax=plt.gca(), color='red', label='Competitors')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Store and Competitor Locations')
plt.legend()
plt.savefig('store_competitor_locations.png')
print("Plot saved to store_competitor_locations.png")
#check if plots directory exists, create if not
plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
#move plots to plots directory
for filename in ["customer_density_vs_distance.png", "store_competitor_locations.png"]:
    os.rename(filename, os.path.join(plot_dir, filename))
    print(f"Plot moved to {os.path.join(plot_dir, filename)}")