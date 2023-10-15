document.addEventListener('DOMContentLoaded', function() {
    var checkSubmission = document.getElementById('submit_button');
    var emailInput = document.getElementById('email_input');
    var passwordInput = document.getElementById('password_input');

    checkSubmission.addEventListener('click', function() {
        var email = emailInput.value;
        var password = passwordInput.value;

        // Send POST request to Flask backend
        fetch('http://localhost:5000/get-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Data received:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Uncomment this when you actually want to redirect
        // var url = 'https://www.gradescope.com/courses/12345/assignments/123456?email=' + email;
        // chrome.tabs.create({url: url});
    }, false);
});
