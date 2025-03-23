// API Base URL - Replace with your actual API URL
const apiUrl = 'https://your-api-endpoint/';

// Function to fetch waste data from the backend
async function fetchWasteData() {
    try {
        const response = await fetch(`${apiUrl}wasteData`); // Fetch waste data from the endpoint
        const data = await response.json();
        console.log('Waste Data:', data);
        updateDashboard(data); // Update the dashboard with the fetched data
    } catch (error) {
        console.error('Error fetching waste data:', error);
    }
}

// Function to fetch report data from the backend
async function fetchReports() {
    try {
        const response = await fetch(`${apiUrl}reports`); // Fetch reports from the endpoint
        const reports = await response.json();
        console.log('Reports:', reports);
        displayReports(reports); // Display reports on the reports page
    } catch (error) {
        console.error('Error fetching reports:', error);
    }
}

// Function to fetch analytics data (e.g., waste stats) from the backend
async function fetchAnalyticsData() {
    try {
        const response = await fetch(`${apiUrl}analytics`); // Fetch analytics data from the endpoint
        const analytics = await response.json();
        console.log('Analytics Data:', analytics);
        updateAnalyticsCharts(analytics); // Update charts with analytics data
    } catch (error) {
        console.error('Error fetching analytics data:', error);
    }
}

// Function to update the dashboard with the fetched waste data
function updateDashboard(data) {
    // Update total reported bins
    document.getElementById('totalBins').innerText = data.totalBins;

    // Update overflowing bins
    document.getElementById('overflowingBins').innerText = data.overflowingBins;

    // Update cleared bins
    document.getElementById('clearedBins').innerText = data.clearedBins;
}

// Function to display the reports on the reports page
function displayReports(reports) {
    const reportList = document.querySelector('.report-list');
    reports.forEach(report => {
        const reportItem = document.createElement('div');
        reportItem.classList.add('report-item');
        reportItem.innerHTML = `
            <h2>${report.title}</h2>
            <button onclick="viewReportDetails(${report.id})">View Details</button>
        `;
        reportList.appendChild(reportItem);
    });
}

// Function to handle viewing the details of a report
async function viewReportDetails(reportId) {
    try {
        const response = await fetch(`${apiUrl}reports/${reportId}`); // Fetch the detailed report by ID
        const report = await response.json();
        console.log('Report Details:', report);
        // Display report details (could open a modal or redirect)
    } catch (error) {
        console.error('Error fetching report details:', error);
    }
}

// Function to fetch data from another example API
async function fetchData() {
    console.log("Fetching data from the API...");
    try {
        const response = await fetch('https://api.example.com/data'); // Replace with the actual API URL
        const data = await response.json();
        console.log('Fetched data:', data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call the functions on page load to fetch data
document.addEventListener('DOMContentLoaded', function () {
    fetchWasteData();
    fetchReports();
    fetchAnalyticsData();
    fetchData(); // Optional: Call fetchData if necessary
});
