document.addEventListener('DOMContentLoaded', () => {
    const transcriptContainer = document.getElementById('transcript');
    const spokenTextContainer = document.getElementById('spoken-text');

    // Function to update the transcript and spoken text
    function updateUI(transcript, spokenText) {
        transcriptContainer.textContent = transcript;
        spokenTextContainer.textContent = spokenText;
    }

    // Fetch the transcript and spoken text from the backend
    fetch('/transcript', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        updateUI(data.transcript, 'Assistant: ' + data.transcript);
    })
    .catch(error => {
        console.error('Error fetching transcript:', error);
    });

    // Fetch the spoken text from the backend
    fetch('/speak', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: 'Hello, Divekar College Creativity Fest!' }),
    })
    .then(response => response.json())
    .then(data => {
        updateUI(data.transcript, 'Assistant: Hello, Divekar College Creativity Fest!');
    })
    .catch(error => {
        console.error('Error fetching spoken text:', error);
    });
});