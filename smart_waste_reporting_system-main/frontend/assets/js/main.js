document.addEventListener('DOMContentLoaded', () => {
    // Chatbot functionality
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatbotMessages = document.querySelector('.chatbot-messages');
  
    chatSend.addEventListener('click', () => {
      const message = chatInput.value;
      if (message.trim() !== "") {
        const newMessage = document.createElement('div');
        newMessage.classList.add('chat-message');
        newMessage.textContent = `You: ${message}`;
        chatbotMessages.appendChild(newMessage);
        chatInput.value = ''; // Clear input field
  
        // Simulate a bot response
        const botResponse = document.createElement('div');
        botResponse.classList.add('chat-message');
        botResponse.textContent = `Bot: Your message has been received.`;
        chatbotMessages.appendChild(botResponse);
      }
    });
  
    // Geolocation functionality
    const geolocationBtn = document.getElementById('geolocation-btn');
    const mapContainer = document.getElementById('map-container');
  
    geolocationBtn.addEventListener('click', () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
          const { latitude, longitude } = position.coords;
          mapContainer.innerHTML = `
            <p>Latitude: ${latitude}</p>
            <p>Longitude: ${longitude}</p>
          `;
        }, () => {
          alert("Geolocation not available.");
        });
      } else {
        alert("Geolocation is not supported by your browser.");
      }
    });
  
    // File upload functionality
    const fileInput = document.getElementById('file-upload'); // Get the file input
    const fileChosen = document.getElementById('file-chosen'); // Display the file name
    const fileUploadButton = document.getElementById('file-upload-button'); // Upload button

    // Listen for changes on the file input
    fileInput.addEventListener('change', updateFileName);

    // Function to update the file name when a file is selected
    function updateFileName() {
      const fileName = fileInput.files[0] ? fileInput.files[0].name : "No file chosen";
      fileChosen.textContent = fileName;
    }

    // Optional: handle the file upload button click event if you want to process the file
    fileUploadButton.addEventListener('click', () => {
      if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
      } else {
        // You can process the file upload here (e.g., send it to a server)
        alert(`File "${fileInput.files[0].name}" ready for upload.`);
      }
    });

    // Camera access functionality
    const openCameraBtn = document.getElementById('open-camera');
    const videoElement = document.getElementById('video');
  
    openCameraBtn.addEventListener('click', () => {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            videoElement.style.display = 'block';
            videoElement.srcObject = stream;
            openCameraBtn.style.display = 'none';
          })
          .catch(err => {
            alert("Camera access denied.");
          });
      } else {
        alert("Camera is not supported by your browser.");
      }
    });
});
