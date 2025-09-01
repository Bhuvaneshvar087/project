document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('file-input');
    const chatWindow = document.getElementById('chat-window');

    uploadButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) {
            addMessageToChat("<p>Please select a file first.</p>", "bot-message");
            return;
        }

        const formData = new FormData();
        formData.append('expense_file', file);
        addMessageToChat("<p>Analyzing your expenses...</p>", "bot-message");

        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const formattedResponse = data.llm_response.replace(/\n/g, '<br>');
                // This is the corrected line:
                addMessageToChat(formattedResponse, "bot-message");
            } else {
                addMessageToChat(`<p>Error: ${data.message}</p>`, "bot-message");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat("<p>Sorry, something went wrong. Could not connect to the server.</p>", "bot-message");
        });
    });

    function addMessageToChat(htmlContent, messageClass) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', messageClass);
        messageDiv.innerHTML = htmlContent;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});