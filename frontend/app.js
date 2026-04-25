// API Configuration
const API_BASE_URL = '/api';

// Default permit type to select
const DEFAULT_PERMIT_TYPE = 'Mechanical';

// License types cache
let licenseTypesLoaded = false;

// Load Permit Types on page load
async function loadPermitTypes() {
    const permitTypeSelect = document.getElementById('permitType');
    
    try {
        const response = await fetch(`${API_BASE_URL}/permit-types`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            permitTypeSelect.innerHTML = '<option value="">-- Select Permit Type --</option>';
            data.permitTypes.forEach(pt => {
                const option = document.createElement('option');
                option.value = pt.name;
                option.textContent = pt.name;
                // Set default selection
                if (pt.name === DEFAULT_PERMIT_TYPE) {
                    option.selected = true;
                }
                permitTypeSelect.appendChild(option);
            });
        } else {
            permitTypeSelect.innerHTML = '<option value="">-- Failed to load --</option>';
            console.error('Failed to load permit types:', data.detail);
        }
    } catch (error) {
        permitTypeSelect.innerHTML = '<option value="">-- Error loading --</option>';
        console.error('Error loading permit types:', error);
    }
}

// Hardcoded License Types
const LICENSE_TYPES = [
    'A', 'B', 'B-2', 'C-2', 'C-4', 'C-5', 'C-6', 'C-7', 'C-8', 'C-9',
    'C10', 'C11', 'C12', 'C13', 'C15', 'C16', 'C17', 'C20', 'C21', 'C22',
    'C23', 'C27', 'C28', 'C29', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36',
    'C38', 'C39', 'C42', 'C43', 'C45', 'C46', 'C47', 'C49', 'C50', 'C51',
    'C53', 'C54', 'C55', 'C57', 'C60', 'C61', 'D34', 'ASB', 'HAZ',
    'Plumbing', 'Electrical', 'HVAC', 'D21', 'D35', 'D40', 'D57', 'D28'
];

// Load License Types (hardcoded)
function loadLicenseTypes() {
    const licenseTypeSelect = document.getElementById('licenseType');
    
    if (licenseTypesLoaded) {
        return; // Already loaded
    }
    
    licenseTypeSelect.innerHTML = '<option value="">-- Select License Type --</option>';
    LICENSE_TYPES.forEach(lt => {
        const option = document.createElement('option');
        option.value = lt;
        option.textContent = lt;
        licenseTypeSelect.appendChild(option);
    });
    licenseTypesLoaded = true;
}

// Handle Applicant Role change - show/hide License Type field
function handleApplicantRoleChange() {
    const applicantRole = document.getElementById('applicantRole').value;
    const licenseTypeGroup = document.getElementById('licenseTypeGroup');
    const licenseTypeSelect = document.getElementById('licenseType');
    
    if (applicantRole === 'Contractor' || applicantRole === 'Agent for Contractor') {
        licenseTypeGroup.style.display = 'block';
        licenseTypeSelect.required = true;
        // Load license types if not already loaded
        loadLicenseTypes();
    } else {
        licenseTypeGroup.style.display = 'none';
        licenseTypeSelect.required = false;
        licenseTypeSelect.value = '';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadPermitTypes();
    loadPermitHistory();
});

// Load Permit History
async function loadPermitHistory() {
    const tableBody = document.getElementById('historyTableBody');
    
    try {
        const response = await fetch(`${API_BASE_URL}/permit-history`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            if (data.applications && data.applications.length > 0) {
                tableBody.innerHTML = '';
                data.applications.forEach((app, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${escapeHtml(app.permit_type)}</td>
                        <td>${escapeHtml(app.application_number)}</td>
                        <td>${escapeHtml(app.timestamp)}</td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="4" class="no-data-row">No permit applications created yet</td></tr>';
            }
        } else {
            tableBody.innerHTML = '<tr><td colspan="4" class="error-row">Failed to load permit history</td></tr>';
            console.error('Failed to load permit history:', data.detail);
        }
    } catch (error) {
        tableBody.innerHTML = '<tr><td colspan="4" class="error-row">Error loading permit history</td></tr>';
        console.error('Error loading permit history:', error);
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Page Navigation
function showCreatePermitPage() {
    document.getElementById('homepage').classList.remove('active');
    document.getElementById('createPermitPage').classList.add('active');
    // Reload permit types when showing page
    loadPermitTypes();
    // Check if license type should be shown based on current applicant role
    handleApplicantRoleChange();
    // Clear any previous errors
    clearFormError();
}

function goToHomepage() {
    document.getElementById('createPermitPage').classList.remove('active');
    document.getElementById('homepage').classList.add('active');
    // Restore default values instead of full reset
    restoreFormDefaults();
    clearFormError();
}

// Restore form to default values
function restoreFormDefaults() {
    document.getElementById('applicant').value = 'Portal User';
    document.getElementById('address').value = '2500 WILSHIRE BLVD';
    document.getElementById('applicantRole').value = 'Agent for Owner';
    document.getElementById('useClass').value = '1 or 2 Family Dwelling';
    // Permit type will be restored when loadPermitTypes is called
    
    // Reset and hide license type field
    document.getElementById('licenseTypeGroup').style.display = 'none';
    document.getElementById('licenseType').value = '';
    document.getElementById('licenseType').required = false;
}

// Form Error handling
function showFormError(message) {
    const errorDiv = document.getElementById('formError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function clearFormError() {
    const errorDiv = document.getElementById('formError');
    errorDiv.textContent = '';
    errorDiv.style.display = 'none';
}

// Modal Functions
function openSubmissionModal() {
    document.getElementById('submissionModal').style.display = 'flex';
    document.getElementById('submissionAppNumber').value = '';
    document.getElementById('submissionResult').className = 'result-message';
    document.getElementById('submissionResult').textContent = '';
}

function closeSubmissionModal() {
    document.getElementById('submissionModal').style.display = 'none';
}

function openReviewModal() {
    document.getElementById('reviewModal').style.display = 'flex';
    document.getElementById('reviewAppNumber').value = '';
    document.getElementById('reviewResult').className = 'result-message';
    document.getElementById('reviewResult').textContent = '';
}

function closeReviewModal() {
    document.getElementById('reviewModal').style.display = 'none';
}

// Success Modal Functions
function showSuccessModal(title, message, details) {
    document.getElementById('successModalTitle').textContent = title;
    document.getElementById('successModalMessage').textContent = message;
    document.getElementById('successModalDetails').textContent = details || '';
    document.getElementById('successModal').style.display = 'flex';
}

function closeSuccessModal() {
    document.getElementById('successModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const submissionModal = document.getElementById('submissionModal');
    const reviewModal = document.getElementById('reviewModal');
    const successModal = document.getElementById('successModal');
    
    if (event.target === submissionModal) {
        closeSubmissionModal();
    }
    if (event.target === reviewModal) {
        closeReviewModal();
    }
    if (event.target === successModal) {
        closeSuccessModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSubmissionModal();
        closeReviewModal();
        closeSuccessModal();
    }
});

// Toast Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Loading state helpers
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = 'Processing...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || button.textContent;
    }
}

// Form Submission - Create Permit Application
document.getElementById('permitForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    clearFormError();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const applicant = document.getElementById('applicant').value.trim();
    const address = document.getElementById('address').value.trim();
    const permitType = document.getElementById('permitType').value;
    const applicantRole = document.getElementById('applicantRole').value;
    const useClass = document.getElementById('useClass').value;
    const licenseType = document.getElementById('licenseType').value;
    
    // Validate basic fields
    if (!applicant || !address || !permitType || !applicantRole || !useClass) {
        showFormError('Please fill in all required fields');
        return;
    }
    
    // Validate license type for Contractor roles
    if ((applicantRole === 'Contractor' || applicantRole === 'Agent for Contractor') && !licenseType) {
        showFormError('Please select a License Type for Contractor roles');
        return;
    }
    
    // Prepare data for API
    const permitData = {
        applicant: applicant,
        address: address,
        permitType: permitType,
        applicantRole: applicantRole,
        useClass: useClass
    };
    
    // Add license type if applicable
    if (licenseType && (applicantRole === 'Contractor' || applicantRole === 'Agent for Contractor')) {
        permitData.licenseType = licenseType;
    }
    
    setButtonLoading(submitBtn, true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/permit-application`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(permitData)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show success modal with application number
            goToHomepage();
            
            // Refresh permit history table
            loadPermitHistory();
            
            showSuccessModal(
                'Permit Application Created!',
                'Your permit application has been created successfully in qa2 console.',
                'Please do complete work items/valuation items, LAHD questionnaires, Select APN, Capture-inperson declaration before going to complete submissions.',
                `Application Number: ${data.applicationName}`
            );
            
            // Reset form
            document.getElementById('permitForm').reset();
        } else {
            // Show specific error message from backend
            const errorMessage = data.detail || 'Failed to create permit application';
            showFormError(errorMessage);
        }
    } catch (error) {
        console.error('Error:', error);
        showFormError('Error connecting to server. Please ensure the backend is running.');
    } finally {
        setButtonLoading(submitBtn, false);
    }
});

// Complete All Submissions
async function completeAllSubmissions() {
    const appNumber = document.getElementById('submissionAppNumber').value.trim();
    const resultDiv = document.getElementById('submissionResult');
    const button = document.querySelector('#submissionModal .submit-btn');
    
    if (!appNumber) {
        resultDiv.className = 'result-message error';
        resultDiv.textContent = 'Please enter an Application Number';
        return;
    }
    
    setButtonLoading(button, true);
    resultDiv.className = 'result-message';
    resultDiv.textContent = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/complete-submissions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ applicationNumber: appNumber })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            closeSubmissionModal();
            showSuccessModal(
                'Submissions Completed!',
                data.message,
                `Total: ${data.total} | Updated: ${data.updated} | Failed: ${data.failed}`
            );
        } else {
            resultDiv.className = 'result-message error';
            resultDiv.textContent = data.detail || 'Failed to complete submissions';
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.className = 'result-message error';
        resultDiv.textContent = 'Error connecting to server. Please ensure the backend is running.';
    } finally {
        setButtonLoading(button, false);
    }
}

// Complete All Reviews
async function completeAllReviews() {
    const appNumber = document.getElementById('reviewAppNumber').value.trim();
    const resultDiv = document.getElementById('reviewResult');
    const button = document.querySelector('#reviewModal .submit-btn');
    
    if (!appNumber) {
        resultDiv.className = 'result-message error';
        resultDiv.textContent = 'Please enter an Application Number';
        return;
    }
    
    setButtonLoading(button, true);
    resultDiv.className = 'result-message';
    resultDiv.textContent = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/complete-reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ applicationNumber: appNumber })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            closeReviewModal();
            showSuccessModal(
                'Reviews Completed!',
                data.message,
                `Total: ${data.total} | Updated: ${data.updated} | Failed: ${data.failed}`
            );
        } else {
            resultDiv.className = 'result-message error';
            resultDiv.textContent = data.detail || 'Failed to complete reviews';
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.className = 'result-message error';
        resultDiv.textContent = 'Error connecting to server. Please ensure the backend is running.';
    } finally {
        setButtonLoading(button, false);
    }
}
