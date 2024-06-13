document.addEventListener("DOMContentLoaded", function() {
    var endTimeTimestamp = parseInt(document.getElementById('end-time').value);
    console.log("End Time Timestamp: ", endTimeTimestamp); // Log end time timestamp
    var endTime = new Date(endTimeTimestamp); // Parse end_time from hidden input as a date object
    console.log("Parsed End Time: ", endTime); // Log parsed end time
    var timeDisplay = document.getElementById('time-display'); 
    var progressBar = document.getElementById('progress-bar');
    var hint = document.getElementById('hint');

    function updateTime() {
        var currentTime = new Date();
        console.log("Current Time: ", currentTime); // Log current time
        var remainingTime = endTime.getTime() - currentTime.getTime();
        console.log("Remaining Time: ", remainingTime); // Log remaining time

        // Check if remaining time is within 5 minutes
        if (remainingTime > 0 && remainingTime <= 5 * 60 * 1000) {
            // Calculate percentage of remaining time (within 5 minutes)
            var totalTime = 5 * 60 * 1000; // 5 minutes in milliseconds
            var progress = Math.min(remainingTime, totalTime) / totalTime * 100;
            console.log("Progress: ", progress); // Log progress
            progressBar.style.width = progress + '%';  // Update width based on progress
            timeDisplay.textContent = Math.floor(remainingTime / 1000) + 's';  // Display remaining seconds
        } else if (remainingTime <= 0) {
            progressBar.style.width = '0%'; // Set to 0% if time has expired
            timeDisplay.textContent = 'Time is up!';
            clearInterval(timerInterval); // Stop the interval
            window.location.href = "/failed"; // Redirect to /failed
        } else {
            progressBar.style.width = '100%'; // Set to 100% if game hasn't started
            timeDisplay.textContent = 'Waiting for game start...';
        }
    }

    function displayHint() {
        hint.style.display = 'block'; // Show the hint
    }

    var timerInterval;
    var hintTimeout;

    function startTimer() {
        updateTime(); // Call update function on page load
        timerInterval = setInterval(updateTime, 1000); // Update time every second
        hintTimeout = setTimeout(displayHint, 45000); // Display the hint after 45 seconds
    }

    startTimer();
});
