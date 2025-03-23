let map;

function initMap() {
  // Default location if geolocation fails (New York City coordinates)
  const defaultLocation = { lat: 40.7128, lng: -74.0060 };

  // Create the map and set the default location (zoom level 13)
  map = L.map("map-container").setView(defaultLocation, 13);

  // Set up the OpenStreetMap tile layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Try to get the user's geolocation
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        // Center the map on the user's location
        map.setView(userLocation, 13);

        // Add a marker at the user's location
        L.marker(userLocation).addTo(map)
          .bindPopup("You are here")
          .openPopup();
      },
      () => {
        // If geolocation fails, use the default location
        alert("Geolocation failed. Using default location.");
        map.setView(defaultLocation, 13);
      }
    );
  } else {
    alert("Geolocation is not supported by this browser.");
    map.setView(defaultLocation, 13);
  }
}

// Initialize the map when the page is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  initMap();
});
