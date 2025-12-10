// Handle calculator form submission
const calcForm = document.getElementById('calc-form');
if (calcForm) {
    calcForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const operation = document.getElementById('operation').value;
        const operand1 = parseFloat(document.getElementById('operand1').value);
        const operand2 = parseFloat(document.getElementById('operand2').value);
        
        await performCalculation(operation, operand1, operand2);
    });
}

async function performCalculation(operation, operand1, operand2) {
    try {
        const response = await fetchWithAuth('/calculations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ operation, operand1, operand2 }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResult(data.result);
            loadRecentCalculations();
        } else {
            showMessage(data.detail || 'Calculation failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function displayResult(result) {
    const resultDiv = document.getElementById('result');
    const resultValue = document.getElementById('result-value');
    
    resultValue.textContent = result;
    resultDiv.style.display = 'block';
}

// Load recent calculations
async function loadRecentCalculations() {
    try {
        const response = await fetchWithAuth('/calculations/?limit=10');
        const data = await response.json();
        
        if (response.ok) {
            displayRecentCalculations(data);
        }
    } catch (error) {
        console.error('Error loading calculations:', error);
    }
}

function displayRecentCalculations(calculations) {
    const container = document.getElementById('recent-calculations');
    
    if (calculations.length === 0) {
        container.innerHTML = '<p>No calculations yet.</p>';
        return;
    }
    
    container.innerHTML = calculations.map(calc => `
        <div class="calculation-item">
            <div class="calculation-info">
                <strong>${calc.operand1} ${getOperationSymbol(calc.operation)} ${calc.operand2} = ${calc.result}</strong>
                <div class="calculation-time">${formatDate(calc.created_at)}</div>
            </div>
            <button class="btn btn-danger" onclick="deleteCalculation(${calc.id})">Delete</button>
        </div>
    `).join('');
}

function getOperationSymbol(operation) {
    const symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    };
    return symbols[operation] || operation;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

async function deleteCalculation(id) {
    if (!confirm('Are you sure you want to delete this calculation?')) {
        return;
    }
    
    try {
        const response = await fetchWithAuth(`/calculations/${id}`, {
            method: 'DELETE',
        });
        
        if (response.ok) {
            showMessage('Calculation deleted successfully', 'success');
            loadRecentCalculations();
        } else {
            showMessage('Failed to delete calculation', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

// Load recent calculations when calculator is shown
if (document.getElementById('calculator-section')) {
    const token = localStorage.getItem('token');
    if (token) {
        loadRecentCalculations();
    }
}
