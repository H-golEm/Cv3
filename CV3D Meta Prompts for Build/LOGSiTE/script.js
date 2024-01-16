document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    loadLogEntries();
});

function addLogEntry() {
    console.log('addLogEntry function called');
    const answer1 = document.getElementById('answer1').value.trim();
    const answer2 = document.getElementById('answer2').value.trim();

    // Check if both answers are provided
    if (!answer1 || !answer2) {
        // Optional: Implement input validation feedback
        return;
    }

    // Grouped log entry as a single test case
    const logEntry = {
        questions: ["What would you like ChatGPT to know about you?", "How would you like ChatGPT to respond?"],
        answers: [answer1, answer2],
        timestamp: new Date().toLocaleString()
    };

    // Update localStorage with the grouped log entry
    const logEntries = getLogEntries();
    logEntries.push(logEntry);
    saveLogEntries(logEntries);

    // Display the grouped log entry
    displayLogEntry(logEntry);

    // Clear input fields
    document.getElementById('answer1').value = '';
    document.getElementById('answer2').value = '';
}

function loadLogEntries() {
    const logEntries = getLogEntries();
    logEntries.forEach(displayLogEntry);
}

function getLogEntries() {
    const storedLogs = localStorage.getItem('logEntries');
    return storedLogs ? JSON.parse(storedLogs) : [];
}

function saveLogEntries(logEntries) {
    localStorage.setItem('logEntries', JSON.stringify(logEntries));
}

function displayLogEntry(logEntry) {
    const logEntriesDiv = document.getElementById('logEntries');
    const logDiv = document.createElement('div');
    logDiv.classList.add('log-entry-group');
    logDiv.innerHTML = `<h3>${logEntry.timestamp}</h3>`;

    // Display questions and answers
    for (let i = 0; i < logEntry.questions.length; i++) {
        logDiv.innerHTML += `<p><strong>${logEntry.questions[i]}:</strong> ${logEntry.answers[i]}</p>`;
    }

    logEntriesDiv.appendChild(logDiv);
}
