// API Base URL - Replace with your actual Flask API URL
const apiUrl = 'http://127.0.0.1:5000/';  // Flask API running locally

// Function to fetch waste data from the backend
async function fetchWasteData() {
    try {
        const response = await fetch(`${apiUrl}wasteData`); // Fetch waste data from Flask API
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
        const response = await fetch(`${apiUrl}reports`); // Fetch reports from Flask API
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
        const response = await fetch(`${apiUrl}analytics`); // Fetch analytics data from Flask API
        const analytics = await response.json();
        console.log('Analytics Data:', analytics);
        updateAnalyticsCharts(analytics); // Update charts with analytics data
    } catch (error) {
        console.error('Error fetching analytics data:', error);
    }
}

// Function to send a message to the chatbot
async function sendMessageToBot(userMessage) {
    try {
        const response = await fetch(`${apiUrl}chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        return data.reply; // Assuming Flask API returns { "reply": "Bot's response" }
    } catch (error) {
        console.error("Error communicating with the chatbot API:", error);
        return "Error connecting to the chatbot.";
    }
}

// Function to update the dashboard with the fetched waste data
function updateDashboard(data) {
    document.getElementById('totalBins').innerText = data.totalBins;
    document.getElementById('overflowingBins').innerText = data.overflowingBins;
    document.getElementById('clearedBins').innerText = data.clearedBins;
}

// Function to display the reports on the reports page
function displayReports(reports) {
    const reportList = document.querySelector('.report-list');
    reportList.innerHTML = "";  // Clear previous reports
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
        alert(`Report: ${report.title}\nDetails: ${report.description}`);
    } catch (error) {
        console.error('Error fetching report details:', error);
    }
}

// Function to handle chatbot interaction from frontend
document.getElementById("sendBtn").addEventListener("click", async () => {
    const userMessage = document.getElementById("userInput").value;
    const botReply = await sendMessageToBot(userMessage);
    document.getElementById("chatBox").innerHTML += `<p><b>You:</b> ${userMessage}</p>`;
    document.getElementById("chatBox").innerHTML += `<p><b>Bot:</b> ${botReply}</p>`;
});

// Call the functions on page load to fetch data
document.addEventListener('DOMContentLoaded', function () {
    fetchWasteData();
    fetchReports();
    fetchAnalyticsData();
});
