/* FORM SECTION */

document.getElementById('api-form').addEventListener('submit', submitForm);

function submitForm(event) {
    event.preventDefault(); // Prevent default form submission
    var userInput = document.getElementById('user-input').value;
    makeAPICall(userInput);
    document.getElementById('user-input').value = ''; // Clear the input field
    return false;
}

function makeAPICall(input) {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'  // Set X-Requested-With header for AJAX request
        },
        body: 'user_input=' + encodeURIComponent(input)
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();  // Parse the response as JSON
        } else {
            throw new Error('API call failed: ' + response.status);
        }
    })
    .then(function(data) {
        updateChatBox(data.data);  // Access the 'response' value in the data JSON
    })
    .catch(function(error) {
        console.error('Fetch error:', error);
    });
}

function updateChatBox(response) {
    var chatMessages = document.getElementById('chat-messages');
    var chatItem = document.createElement('li');
    chatItem.textContent = response;
    chatMessages.appendChild(chatItem);

    scrollToBottom();
}

function scrollToBottom() {
    var chatBox = document.getElementsByClassName('chat-box')[0];
    chatBox.scrollTop = chatBox.scrollHeight;
}



/* SIDE MENU SECTION */
document.addEventListener('DOMContentLoaded', function() {
    var hamburgerMenu = document.getElementById('hamburger-menu');
    var sideMenu = document.querySelector('.side-menu');
    var closeButton = sideMenu.querySelector('.close-button');

    hamburgerMenu.addEventListener('click', function() {
        sideMenu.classList.add('open');
    });

    closeButton.addEventListener('click', function() {
        sideMenu.classList.remove('open');
    });
});

var box1 = document.getElementById('item-1');
var box2 = document.getElementById('item-2');
var box3 = document.getElementById('item-3');

// Attach event listeners to each <li> element
box1.addEventListener('click', function() {
    var sideMenu = document.querySelector('.side-menu');
    var closeButton = sideMenu.querySelector('.close-button');
    closeButton.addEventListener('click', function() {
        sideMenu.classList.remove('open');
    });

    boxAPICall('/box1');
});

box2.addEventListener('click', function() {
    var sideMenu = document.querySelector('.side-menu');
    var closeButton = sideMenu.querySelector('.close-button');
    closeButton.addEventListener('click', function() {
        sideMenu.classList.remove('open');
    });

    boxAPICall('/box2');
});

box3.addEventListener('click', function() {
    var sideMenu = document.querySelector('.side-menu');
    var closeButton = sideMenu.querySelector('.close-button');
    closeButton.addEventListener('click', function() {
        sideMenu.classList.remove('open');
    });

    boxAPICall('/box3');
});

// Function to make the API call
function boxAPICall(endpoint) {
    // Whenever you load a new box, clear the chat window
    var chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    
    fetch(endpoint, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'  // Set X-Requested-With header for AJAX request
        }
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();  // Parse the response as JSON
        } else {
            throw new Error('API call failed: ' + response.status);
        }
    })
    .then(function(data) {
        updateChatBox(data.data);  // Access the 'response' value in the data JSON
    })
    .catch(function(error) {
        console.error('Fetch error:', error);
    });
}