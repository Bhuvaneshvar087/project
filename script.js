document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('file-input');
    const chatWindow = document.getElementById('chat-window');
    const fileLabel = document.getElementById('file-label');
    const fileNameSpan = document.getElementById('file-name');
    const progressArea = document.getElementById('progress-area');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const progressText = document.getElementById('progress-text');
    const initialMessage = document.getElementById('initial-message');
    const mainContainer = document.getElementById('main-container');
    const chartWrapper = document.querySelector('.chart-wrapper');
    let expenseChart = null;

    fileInput.addEventListener('change', () => {
        fileNameSpan.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : 'Choose File';
    });

    uploadButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) {
            addMessageToChat("<p>Please select a file first.</p>", "bot-message");
            return;
        }

        initialMessage.style.display = 'none';
        fileLabel.style.display = 'none';
        uploadButton.style.display = 'none';
        progressArea.style.display = 'flex';

        progressBarFill.style.width = '30%';
        progressText.textContent = 'Uploading file...';
        
        setTimeout(() => {
            progressBarFill.style.width = '70%';
            progressText.textContent = 'Analyzing with FinSight AI...';
        }, 800);

        const formData = new FormData();
        formData.append('expense_file', file);

        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            progressBarFill.style.width = '100%';
            progressText.textContent = 'Analysis Complete!';

            setTimeout(() => {
                progressArea.style.display = 'none';
                
                if (data.status === 'success') {
                    mainContainer.classList.add('dashboard-view');
                    displayExpenseChart(data.chart_labels, data.chart_data);
                    const formattedResponse = data.llm_response.replace(/\n/g, '<br>');
                    addMessageToChat(formattedResponse, "bot-message");
                } else {
                    addMessageToChat(`<p>Error: ${data.message}</p>`, "bot-message");
                }

                fileLabel.style.display = 'flex';
                uploadButton.style.display = 'block';
                fileNameSpan.textContent = 'Choose File';
                progressBarFill.style.width = '0%';
                fileInput.value = '';
            }, 1000);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat("<p>Sorry, an error occurred. Please try again.</p>", "bot-message");
            progressArea.style.display = 'none';
            fileLabel.style.display = 'flex';
            uploadButton.style.display = 'block';
        });
    });

    function addMessageToChat(htmlContent, messageClass) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', messageClass);
        messageDiv.innerHTML = htmlContent;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function displayExpenseChart(labels, data) {
        const ctx = document.getElementById('expense-chart').getContext('2d');
        if (expenseChart) {
            expenseChart.destroy();
        }
        expenseChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Expense Amount (₹)',
                    data: data,
                    backgroundColor: ['#2ea043', '#388bfd', '#a371f7', '#db61a2', '#f1b44c', '#e0982c', '#1f6feb', '#8957e5'],
                    borderColor: '#161b22', // Match surface color for a clean look
                    borderWidth: 4,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            // THIS IS THE FIX: Set the text color for the legend
                            color: '#c9d1d9', 
                            padding: 20,
                            font: { family: "'Inter', sans-serif", size: 14 }
                        }
                    }
                },
                cutout: '65%'
            }
        });
    }
});
