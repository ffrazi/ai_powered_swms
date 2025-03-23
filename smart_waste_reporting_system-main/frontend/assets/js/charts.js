/**
 * Function to render the waste analytics chart using Chart.js.
 * This function displays a bar chart to represent the waste amounts in bins.
 */
function renderWasteChart(data) {
  // Get the chart's canvas context
  const ctx = document.getElementById('wasteChart').getContext('2d');

  // Create a new Chart instance and render the chart
  const wasteChart = new Chart(ctx, {
      type: 'bar', // Chart type ('bar', 'line', 'pie', etc.)
      data: {
          labels: data.labels, // Bin names or categories (e.g., ['Bin 1', 'Bin 2', 'Bin 3'])
          datasets: [{
              label: 'Waste Amount (kg)', // Label for the dataset
              data: data.values, // Array containing the waste values (e.g., [40, 60, 80])
              backgroundColor: [
                  'rgba(76, 175, 80, 0.2)', // Green background
                  'rgba(139, 195, 74, 0.2)', // Light green background
                  'rgba(156, 204, 57, 0.2)', // Lighter green background
              ],
              borderColor: [
                  'rgba(76, 175, 80, 1)', // Green border
                  'rgba(139, 195, 74, 1)', // Light green border
                  'rgba(156, 204, 57, 1)', // Lighter green border
              ],
              borderWidth: 1
          }]
      },
      options: {
          responsive: true, // Make the chart responsive
          scales: {
              y: {
                  beginAtZero: true // Start the Y-axis from 0
              }
          },
          plugins: {
              tooltip: {
                  backgroundColor: 'rgba(0, 0, 0, 0.7)', // Tooltip background color
                  titleColor: 'white', // Tooltip title color
                  bodyColor: 'white', // Tooltip body text color
              }
          }
      }
  });
}

/**
* Function to update the analytics chart with new data.
* This function processes the fetched data and passes it to the renderWasteChart function.
*/
function updateAnalyticsCharts(analyticsData) {
  const chartData = {
      labels: analyticsData.bins, // Example: ['Bin 1', 'Bin 2', 'Bin 3']
      values: analyticsData.wasteAmounts // Example: [40, 60, 80]
  };
  renderWasteChart(chartData); // Call renderWasteChart with the processed data
}

/**
* Example of how the fetchAnalyticsData function will use this:
* Fetch analytics data and update the chart accordingly.
*/
function fetchAnalyticsData() {
  // Simulated data fetch (replace with actual fetch)
  const exampleData = {
      bins: ['Bin 1', 'Bin 2', 'Bin 3'],
      wasteAmounts: [40, 60, 80]
  };
  
  // After fetching, update the chart
  updateAnalyticsCharts(exampleData);
}

// Call the fetchAnalyticsData function when the page loads
document.addEventListener('DOMContentLoaded', function() {
  fetchAnalyticsData(); // Call the function to fetch and display the data
});
