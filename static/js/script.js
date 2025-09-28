// Utility functions for the summarization tool

// Text area auto-resize
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Word count display
function updateWordCount(textarea, displayElement) {
    const wordCount = textarea.value.trim().split(/\s+/).length;
    displayElement.textContent = `${wordCount} words`;
    
    if (wordCount < 10) {
        displayElement.classList.add('text-danger');
        displayElement.classList.remove('text-success');
    } else {
        displayElement.classList.remove('text-danger');
        displayElement.classList.add('text-success');
    }
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
        
        // Initialize height
        autoResizeTextarea(textarea);
    });
    
    // Word count for summary textarea
    const summaryTextarea = document.getElementById('textInput');
    if (summaryTextarea) {
        const wordCountDisplay = document.createElement('div');
        wordCountDisplay.className = 'form-text text-end';
        summaryTextarea.parentNode.appendChild(wordCountDisplay);
        
        summaryTextarea.addEventListener('input', function() {
            updateWordCount(this, wordCountDisplay);
        });
        
        // Initialize word count
        updateWordCount(summaryTextarea, wordCountDisplay);
    }
    
    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Remove validation styles on input
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
});

// API utility functions
const ApiUtils = {
    async getAnalytics(range = 'week') {
        try {
            const response = await fetch(`/api/analytics?range=${range}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching analytics:', error);
            return null;
        }
    },
    
    async exportHistory(format = 'json') {
        try {
            const response = await fetch(`/api/export?format=${format}`);
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `summaries_${new Date().toISOString().split('T')[0]}.${format}`;
                a.click();
                window.URL.revokeObjectURL(url);
            }
        } catch (error) {
            console.error('Error exporting history:', error);
        }
    }
};

// Chart utility functions
const ChartUtils = {
    createBarChart(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                ...options
            }
        });
    },
    
    createPieChart(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                ...options
            }
        });
    }
};

