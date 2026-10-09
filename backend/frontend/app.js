const formConfigs = {
    NDA: [
        { id: 'disclosing_party', label: 'Disclosing Party', type: 'text', placeholder: 'Company A' },
        { id: 'receiving_party', label: 'Receiving Party', type: 'text', placeholder: 'Company B' },
        { id: 'effective_date', label: 'Effective Date', type: 'date' },
        { id: 'jurisdiction', label: 'Jurisdiction', type: 'text', placeholder: 'State of California' },
        { id: 'confidentiality_period', label: 'Confidentiality Period', type: 'text', placeholder: 'e.g., 3 Years' }
    ],
    Employment: [
        { id: 'employer', label: 'Employer', type: 'text', placeholder: 'Company A' },
        { id: 'employee', label: 'Employee', type: 'text', placeholder: 'John Doe' },
        { id: 'role', label: 'Role/Job Title', type: 'text', placeholder: 'Software Engineer' },
        { id: 'compensation', label: 'Annual Compensation', type: 'text', placeholder: '₹12,00,000 / year' },
        { id: 'start_date', label: 'Start Date', type: 'date' },
        { id: 'termination_terms', label: 'Termination Terms', type: 'text', placeholder: 'At-will, 2 weeks notice' }
    ],
    Lease: [
        { id: 'landlord', label: 'Landlord', type: 'text', placeholder: 'Jane Doe' },
        { id: 'tenant', label: 'Tenant', type: 'text', placeholder: 'John Smith' },
        { id: 'property_address', label: 'Property Address', type: 'text', placeholder: '123 Main St, City, State' },
        { id: 'rent', label: 'Monthly Rent', type: 'text', placeholder: '₹20,000' },
        { id: 'security_deposit', label: 'Security Deposit', type: 'text', placeholder: '₹20,000' },
        { id: 'lease_duration', label: 'Lease Duration', type: 'text', placeholder: '12 Months' }
    ],
    Custom: [
        { id: 'document_name', label: 'Document Type (e.g., Freelance Work Contract)', type: 'text', placeholder: 'Freelance Work Contract' },
        { id: 'parties_involved', label: 'Parties Involved', type: 'text', placeholder: 'Jane Doe (Provider), TechNova Inc. (Client)' },
        { id: 'effective_date', label: 'Effective Date', type: 'date' },
        { id: 'terms_and_conditions', label: 'Terms & Conditions (use semicolons)', type: 'text', placeholder: 'Payment in 30 days; Confidentiality required;' }
    ]
};

const docTypeSelect = document.getElementById('docType');
const dynamicForm = document.getElementById('dynamicForm');
const generateBtn = document.getElementById('generateBtn');
const generateText = document.getElementById('generateText');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMsg = document.getElementById('errorMsg');
const contentPreview = document.getElementById('contentPreview');
const contentTerms = document.getElementById('contentTerms');
const contentText = document.getElementById('contentText');
const analyticsPanel = document.getElementById('analyticsPanel');
const metricsCards = document.getElementById('metricsCards');
const analyticsChart = document.getElementById('analyticsChart');

const tabPreview = document.getElementById('tabPreview');
const tabTerms = document.getElementById('tabTerms');
const tabText = document.getElementById('tabText');

let currentMarkdown = '';

function renderForm(type) {
    const fields = formConfigs[type];
    dynamicForm.innerHTML = fields.map(field => `
        <div>
            <label for="${field.id}" class="block text-sm font-medium text-gray-700">${field.label}</label>
            <input type="${field.type}" id="${field.id}" name="${field.id}" placeholder="${field.placeholder || ''}" required
                class="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
        </div>
    `).join('');
    // Hide analytics when switching document types
    analyticsPanel.classList.add('hidden');
}

docTypeSelect.addEventListener('change', (e) => renderForm(e.target.value));
renderForm('NDA');

function getFormData() {
    const formData = new FormData(dynamicForm);
    return Object.fromEntries(formData.entries());
}

function formatMetricLabel(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function formatMetricValue(key, value) {
    if (typeof value === 'number') {
        if (key.includes('month') && !key.includes('₹') && !key.includes('rent') && !key.includes('cost') && !key.includes('salary') && !key.includes('take_home') && !key.includes('tax') && !key.includes('benefit') && !key.includes('gross') && !key.includes('compensation') && !key.includes('deposit')) {
            if (key.includes('duration') || key.includes('period')) return `${value} months`;
        }
        if (key.includes('score')) return `${value.toFixed(1)}%`;
        if (key.includes('duration') || key.includes('period')) return `${value} months`;
        return `₹${value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
    return value;
}

async function fetchAnalytics(docType, data) {
    try {
        const response = await fetch('/api/v1/analytics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_type: docType, data: data })
        });
        if (!response.ok) return;
        const result = await response.json();

        // Render metrics cards
        metricsCards.innerHTML = Object.entries(result.metrics).map(([key, value]) => `
            <div class="flex justify-between items-center bg-blue-50 rounded-md px-3 py-2 text-sm">
                <span class="text-gray-600 font-medium">${formatMetricLabel(key)}</span>
                <span class="text-blue-700 font-bold">${formatMetricValue(key, value)}</span>
            </div>
        `).join('');

        // Render chart
        window.currentChartBase64 = result.chart_base64;
        analyticsChart.src = 'data:image/png;base64,' + result.chart_base64;
        analyticsPanel.classList.remove('hidden');
    } catch (err) {
        console.error('Analytics error:', err);
    }
}

generateBtn.addEventListener('click', async () => {
    if (!dynamicForm.checkValidity()) {
        dynamicForm.reportValidity();
        return;
    }

    const docType = docTypeSelect.value;
    const data = getFormData();

    loadingSpinner.classList.remove('hidden');
    generateText.textContent = 'Generating...';
    generateBtn.disabled = true;
    errorMsg.classList.add('hidden');

    try {
        // Fire both requests in parallel
        const [genResponse] = await Promise.all([
            fetch('/api/v1/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ document_type: docType, data: data })
            }),
            fetchAnalytics(docType, data)
        ]);

        if (!genResponse.ok) {
            const err = await genResponse.json();
            throw new Error(err.detail || 'Failed to generate document');
        }

        const result = await genResponse.json();
        currentMarkdown = result.markdown_content;
        
        contentPreview.innerHTML = marked.parse(result.markdown_content);
        contentTerms.innerHTML = marked.parse(result.term_table || 'No term table generated.');
        contentText.value = result.markdown_content;

        switchTab('preview');
    } catch (error) {
        errorMsg.textContent = '❌ ' + error.message;
        errorMsg.classList.remove('hidden');
    } finally {
        loadingSpinner.classList.add('hidden');
        generateText.textContent = '🚀 Generate Document';
        generateBtn.disabled = false;
    }
});

function switchTab(tab) {
    [tabPreview, tabTerms, tabText].forEach(t => {
        t.className = "px-4 py-2 text-gray-500 hover:text-gray-700 font-medium text-sm rounded-t";
    });
    
    contentPreview.classList.add('hidden');
    contentTerms.classList.add('hidden');
    contentText.classList.add('hidden');

    if (tab === 'preview') {
        tabPreview.className = "px-4 py-2 text-blue-600 border-b-2 border-blue-600 font-medium text-sm rounded-t";
        contentPreview.classList.remove('hidden');
        if (contentText.value && contentText.value !== currentMarkdown) {
            currentMarkdown = contentText.value;
            contentPreview.innerHTML = marked.parse(currentMarkdown);
        }
    } else if (tab === 'terms') {
        tabTerms.className = "px-4 py-2 text-blue-600 border-b-2 border-blue-600 font-medium text-sm rounded-t";
        contentTerms.classList.remove('hidden');
    } else if (tab === 'text') {
        tabText.className = "px-4 py-2 text-blue-600 border-b-2 border-blue-600 font-medium text-sm rounded-t";
        contentText.classList.remove('hidden');
        contentText.value = currentMarkdown;
    }
}

tabPreview.addEventListener('click', () => switchTab('preview'));
tabTerms.addEventListener('click', () => switchTab('terms'));
tabText.addEventListener('click', () => switchTab('text'));

contentText.addEventListener('input', (e) => {
    currentMarkdown = e.target.value;
});

async function exportDoc(format) {
    if (!currentMarkdown) {
        alert("Please generate a document first.");
        return;
    }

    try {
        const payload = { markdown_content: currentMarkdown };
        if (window.currentChartBase64 && (format === 'pdf' || format === 'docx')) {
            payload.chart_base64 = window.currentChartBase64;
        }

        const response = await fetch(`/api/v1/export/${format}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Export failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `LegalEase_Document.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Export failed: ' + error.message);
    }
}
