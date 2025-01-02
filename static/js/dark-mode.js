document.addEventListener('DOMContentLoaded', function () {
    // Check if dark mode is enabled in local storage
    const isDarkMode = localStorage.getItem('dark-mode') === 'enabled';

    // Function to enable dark mode
    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        const toggleButton = document.getElementById('dark-mode-toggle');
        if (toggleButton) {
            toggleButton.textContent = 'Switch to Light Mode'; // Change button text
        }
        localStorage.setItem('dark-mode', 'enabled'); // Save dark mode state
    }

    // Function to disable dark mode
    function disableDarkMode() {
        document.body.classList.remove('dark-mode');
        const toggleButton = document.getElementById('dark-mode-toggle');
        if (toggleButton) {
            toggleButton.textContent = 'Switch to Dark Mode'; // Change button text
        }
        localStorage.setItem('dark-mode', 'disabled'); // Save light mode state
    }

    // Initialize dark mode based on local storage
    if (isDarkMode) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }

    // Add event listener to toggle button
    const toggleButton = document.getElementById('dark-mode-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            const isDarkModeEnabled = document.body.classList.contains('dark-mode');
            if (isDarkModeEnabled) {
                disableDarkMode();
            } else {
                enableDarkMode();
            }
        });
    }
});
