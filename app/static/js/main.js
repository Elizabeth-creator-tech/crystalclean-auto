// ===============================
// MOBILE MENU FUNCTIONALITY
// ===============================
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    // Create overlay for mobile menu
    const navOverlay = document.createElement('div');
    navOverlay.className = 'nav-overlay';
    document.body.appendChild(navOverlay);
    
    // Toggle menu function
    function toggleMenu() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        navOverlay.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (navMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
    
    // Hamburger click
    if (hamburger) {
        hamburger.addEventListener('click', toggleMenu);
    }
    
    // Overlay click - close menu
    navOverlay.addEventListener('click', function() {
        if (navMenu.classList.contains('active')) {
            toggleMenu();
        }
    });
    
    // Close menu when clicking nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768 && navMenu.classList.contains('active')) {
                toggleMenu();
            }
        });
    });
    
    // Close menu on window resize if screen gets bigger
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            navOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// ===============================
// FLASH MESSAGES
// ===============================
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        // Auto-hide after 5 seconds
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s, transform 0.5s';
            message.style.opacity = '0';
            message.style.transform = 'translateX(400px)';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Flash message close button
    const flashCloseButtons = document.querySelectorAll('.flash-close');
    flashCloseButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const flash = this.parentElement;
            flash.style.transition = 'opacity 0.5s, transform 0.5s';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(400px)';
            setTimeout(() => flash.remove(), 500);
        });
    });
});

// ===============================
// Confirm delete actions
// ===============================
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// ===============================
// Real-time form validation
// ===============================
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.style.borderColor = 'var(--danger-color)';
            } else {
                this.style.borderColor = 'var(--border-color)';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.style.borderColor = 'var(--border-color)';
            }
        });
    });
}

// ===============================
// Auto-format plate number to uppercase
// ===============================
document.addEventListener('DOMContentLoaded', function() {
    const plateInputs = document.querySelectorAll('input[name="plate_number"]');
    plateInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });
});

// ===============================
// Phone number validation
// ===============================
function validatePhoneNumber(input) {
    const phonePattern = /^(\+254|0)[17]\d{8}$/;
    const value = input.value.trim();
    
    if (value && !phonePattern.test(value)) {
        input.setCustomValidity('Please enter a valid Kenyan phone number (e.g., 0712345678)');
    } else {
        input.setCustomValidity('');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const phoneInputs = document.querySelectorAll('input[name="customer_phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePhoneNumber(this);
        });
    });
});

// ===============================
// Dynamic status update with confirmation
// ===============================
function updateStatus(carId, newStatus) {
    const message = `Are you sure you want to change status to "${newStatus}"?`;
    
    if (confirm(message)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/cars/update-status/${carId}`;
        
        const statusInput = document.createElement('input');
        statusInput.type = 'hidden';
        statusInput.name = 'status';
        statusInput.value = newStatus;
        form.appendChild(statusInput);

        const csrfToken = document.querySelector('input[name="csrf_token"]');
        if (csrfToken) {
            form.appendChild(csrfToken.cloneNode());
        }

        document.body.appendChild(form);
        form.submit();
    }
}

// ===============================
// Table search functionality
// ===============================
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        row.style.display = found ? '' : 'none';
    }
}

// ===============================
// Auto-refresh dashboard stats every 10 seconds
// ===============================
function refreshDashboardStats() {
    const currentPath = window.location.pathname;
    
    // Only refresh on dashboard pages
    if (!currentPath.includes('dashboard')) {
        return;
    }
    
    // Simple page reload approach (more reliable)
    setInterval(function() {
        // Get current scroll position
        const scrollPos = window.scrollY;
        
        // Reload the page
        location.reload();
        
        // Restore scroll position after reload
        window.addEventListener('load', function() {
            window.scrollTo(0, scrollPos);
        }, { once: true });
    }, 10000); // 10 seconds
}

// Start auto-refresh on dashboard pages
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    if (currentPath.includes('dashboard')) {
        // Show a subtle indicator that auto-refresh is enabled
        console.log('Auto-refresh enabled: Dashboard will refresh every 10 seconds');
    }
});

// ===============================
// Print functionality
// ===============================
function printReport() {
    window.print();
}

// ===============================
// Export table to CSV
// ===============================
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        // Exclude last column (usually actions)
        for (let j = 0; j < cols.length - 1; j++) {
            let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
            data = data.replace(/"/g, '""');
            row.push('"' + data + '"');
        }
        
        csv.push(row.join(','));
    }
    
    const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ===============================
// Notification permission and display
// ===============================
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

function showNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, {
            body: message,
            icon: '/static/images/logo.png'
        });
    }
}

document.addEventListener('DOMContentLoaded', requestNotificationPermission);

// ===============================
// Loading state for forms
// ===============================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.6';
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span>Processing...</span>';
                
                // Re-enable after 3 seconds as fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                    submitBtn.innerHTML = originalText;
                }, 3000);
            }
        });
    });
});

// ===============================
// MOBILE BOTTOM NAVIGATION
// ===============================
document.addEventListener('DOMContentLoaded', function() {
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    const currentPath = window.location.pathname;
    
    // Set active state based on current URL
    bottomNavItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && href !== '#' && currentPath.includes(href)) {
            item.classList.add('active');
        }
        
        // Add touch feedback
        item.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        item.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Connect More button to hamburger menu
    const moreButtons = document.querySelectorAll('.bottom-nav-item[onclick*="hamburger"]');
    moreButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const hamburger = document.querySelector('.hamburger');
            if (hamburger) {
                hamburger.click();
            }
        });
    });
});