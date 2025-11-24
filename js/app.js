/**
 * Axonsoton - Patient Recovery Dashboard
 * Main JavaScript Application
 */

// Sample patient recovery data
const patientData = {
    id: 'AX-2024-001',
    name: 'John Doe',
    program: 'Upper Limb Rehabilitation',
    startDate: '2024-11-01',
    exercises: [
        { id: 'wrist-flexion', name: 'Wrist Flexion', category: 'Upper Limb', targetReps: 315 },
        { id: 'finger-extension', name: 'Finger Extension', category: 'Hand', targetReps: 340 },
        { id: 'grip-strength', name: 'Grip Strength', category: 'Hand', targetReps: 300 },
        { id: 'shoulder-rotation', name: 'Shoulder Rotation', category: 'Shoulder', targetReps: 325 },
        { id: 'elbow-flexion', name: 'Elbow Flexion', category: 'Arm', targetReps: 300 }
    ]
};

// Weekly exercise data (reps per day)
const weeklyData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    reps: [45, 52, 38, 60, 48, 25, 15],
    sessions: [3, 4, 2, 4, 3, 2, 1],
    duration: [35, 42, 28, 50, 40, 20, 12] // minutes
};

// Monthly recovery progress data
const recoveryProgressData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    rangeOfMotion: [45, 55, 65, 72],
    strength: [30, 40, 52, 60],
    endurance: [35, 45, 55, 65]
};

// Exercise reps over time (30 days)
const exerciseTimeData = {
    labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
    datasets: {
        'wrist-flexion': generateExerciseData(30, 5, 12),
        'finger-extension': generateExerciseData(30, 8, 15),
        'grip-strength': generateExerciseData(30, 4, 10),
        'shoulder-rotation': generateExerciseData(30, 6, 12),
        'elbow-flexion': generateExerciseData(30, 5, 11)
    }
};

// Time of day distribution data
const timeOfDayData = {
    labels: ['Morning\n(6am-12pm)', 'Afternoon\n(12pm-6pm)', 'Evening\n(6pm-10pm)'],
    data: [45, 35, 20],
    colors: ['#fdcb6e', '#74b9ff', '#a29bfe']
};

// Health metrics data (7 days)
const healthMetricsData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    heartRate: [72, 68, 75, 70, 73, 65, 68],
    sleepHours: [7.2, 6.8, 7.5, 7.0, 6.5, 8.2, 8.0],
    steps: [6500, 7200, 5800, 6900, 7500, 8200, 5000],
    calories: [1850, 1920, 1780, 1890, 2050, 2200, 1650]
};

// Correlation data (sleep vs performance)
const correlationData = {
    datasets: [
        { sleep: 6.0, performance: 65 },
        { sleep: 6.5, performance: 70 },
        { sleep: 7.0, performance: 78 },
        { sleep: 7.2, performance: 82 },
        { sleep: 7.5, performance: 85 },
        { sleep: 7.8, performance: 88 },
        { sleep: 8.0, performance: 90 },
        { sleep: 8.2, performance: 92 },
        { sleep: 6.2, performance: 68 },
        { sleep: 7.3, performance: 80 }
    ]
};

// Generate sample exercise data
function generateExerciseData(days, min, max) {
    return Array.from({ length: days }, () => 
        Math.floor(Math.random() * (max - min + 1)) + min
    );
}

// Initialize all charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCharts();
    initializeFilters();
    initializeHeatmap();
    initializeHealthIntegrations();
});

// Navigation functionality
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Initialize all Chart.js charts
function initializeCharts() {
    createWeeklyProgressChart();
    createRecoveryProgressChart();
    createExerciseRepsChart();
    createTimeDistributionChart();
    createHeartRateChart();
    createSleepChart();
    createStepsChart();
    createCaloriesChart();
    createHealthMetricsChart();
    createCorrelationChart();
}

// Weekly Progress Chart
function createWeeklyProgressChart() {
    const ctx = document.getElementById('weekly-progress-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: weeklyData.labels,
            datasets: [{
                label: 'Reps Completed',
                data: weeklyData.reps,
                backgroundColor: 'rgba(74, 144, 217, 0.8)',
                borderColor: 'rgba(74, 144, 217, 1)',
                borderWidth: 1,
                borderRadius: 4
            }, {
                label: 'Duration (min)',
                data: weeklyData.duration,
                backgroundColor: 'rgba(108, 92, 231, 0.8)',
                borderColor: 'rgba(108, 92, 231, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Recovery Progress Chart
function createRecoveryProgressChart() {
    const ctx = document.getElementById('recovery-progress-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: recoveryProgressData.labels,
            datasets: [{
                label: 'Range of Motion (%)',
                data: recoveryProgressData.rangeOfMotion,
                borderColor: 'rgba(0, 184, 148, 1)',
                backgroundColor: 'rgba(0, 184, 148, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Strength (%)',
                data: recoveryProgressData.strength,
                borderColor: 'rgba(74, 144, 217, 1)',
                backgroundColor: 'rgba(74, 144, 217, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Endurance (%)',
                data: recoveryProgressData.endurance,
                borderColor: 'rgba(108, 92, 231, 1)',
                backgroundColor: 'rgba(108, 92, 231, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Exercise Reps Over Time Chart
function createExerciseRepsChart() {
    const ctx = document.getElementById('exercise-reps-chart');
    if (!ctx) return;

    const colors = [
        { border: 'rgba(74, 144, 217, 1)', bg: 'rgba(74, 144, 217, 0.1)' },
        { border: 'rgba(0, 184, 148, 1)', bg: 'rgba(0, 184, 148, 0.1)' },
        { border: 'rgba(108, 92, 231, 1)', bg: 'rgba(108, 92, 231, 0.1)' },
        { border: 'rgba(253, 203, 110, 1)', bg: 'rgba(253, 203, 110, 0.1)' },
        { border: 'rgba(231, 76, 60, 1)', bg: 'rgba(231, 76, 60, 0.1)' }
    ];

    const datasets = patientData.exercises.map((exercise, index) => ({
        label: exercise.name,
        data: exerciseTimeData.datasets[exercise.id],
        borderColor: colors[index].border,
        backgroundColor: colors[index].bg,
        fill: false,
        tension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 5
    }));

    window.exerciseRepsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: exerciseTimeData.labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    title: {
                        display: true,
                        text: 'Reps'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

// Time Distribution Chart (Doughnut)
function createTimeDistributionChart() {
    const ctx = document.getElementById('time-distribution-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: timeOfDayData.labels,
            datasets: [{
                data: timeOfDayData.data,
                backgroundColor: timeOfDayData.colors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            cutout: '60%'
        }
    });
}

// Mini Heart Rate Chart
function createHeartRateChart() {
    const ctx = document.getElementById('heart-rate-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: healthMetricsData.labels,
            datasets: [{
                data: healthMetricsData.heartRate,
                borderColor: 'rgba(231, 76, 60, 1)',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: { display: false },
                x: { display: false }
            }
        }
    });
}

// Mini Sleep Chart
function createSleepChart() {
    const ctx = document.getElementById('sleep-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: healthMetricsData.labels,
            datasets: [{
                data: healthMetricsData.sleepHours,
                backgroundColor: 'rgba(108, 92, 231, 0.8)',
                borderRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: { display: false, beginAtZero: true },
                x: { display: false }
            }
        }
    });
}

// Mini Steps Chart
function createStepsChart() {
    const ctx = document.getElementById('steps-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: healthMetricsData.labels,
            datasets: [{
                data: healthMetricsData.steps,
                borderColor: 'rgba(0, 184, 148, 1)',
                backgroundColor: 'rgba(0, 184, 148, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: { display: false },
                x: { display: false }
            }
        }
    });
}

// Mini Calories Chart
function createCaloriesChart() {
    const ctx = document.getElementById('calories-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: healthMetricsData.labels,
            datasets: [{
                data: healthMetricsData.calories,
                backgroundColor: 'rgba(253, 203, 110, 0.8)',
                borderRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: { display: false, beginAtZero: true },
                x: { display: false }
            }
        }
    });
}

// Health Metrics Over Time Chart
function createHealthMetricsChart() {
    const ctx = document.getElementById('health-metrics-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: healthMetricsData.labels,
            datasets: [{
                label: 'Heart Rate (bpm)',
                data: healthMetricsData.heartRate,
                borderColor: 'rgba(231, 76, 60, 1)',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                yAxisID: 'y',
                tension: 0.4
            }, {
                label: 'Sleep (hours)',
                data: healthMetricsData.sleepHours,
                borderColor: 'rgba(108, 92, 231, 1)',
                backgroundColor: 'rgba(108, 92, 231, 0.1)',
                yAxisID: 'y1',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Heart Rate (bpm)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Sleep (hours)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Correlation Chart (Scatter)
function createCorrelationChart() {
    const ctx = document.getElementById('correlation-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Sleep vs Performance',
                data: correlationData.datasets.map(d => ({ x: d.sleep, y: d.performance })),
                backgroundColor: 'rgba(74, 144, 217, 0.8)',
                borderColor: 'rgba(74, 144, 217, 1)',
                pointRadius: 8,
                pointHoverRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Sleep: ${context.parsed.x}hrs, Performance: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 60,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Performance Score (%)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    min: 5.5,
                    max: 9,
                    title: {
                        display: true,
                        text: 'Sleep Duration (hours)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}

// Initialize filter functionality
function initializeFilters() {
    const exerciseFilter = document.getElementById('exercise-filter');
    const dateRangeFilter = document.getElementById('date-range');

    if (exerciseFilter) {
        exerciseFilter.addEventListener('change', function() {
            filterExercises(this.value);
        });
    }

    if (dateRangeFilter) {
        dateRangeFilter.addEventListener('change', function() {
            updateDateRange(this.value);
        });
    }
}

// Filter exercise cards
function filterExercises(filter) {
    const exerciseCards = document.querySelectorAll('.exercise-card');
    
    exerciseCards.forEach(card => {
        if (filter === 'all' || card.dataset.exercise === filter) {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.3s ease';
        } else {
            card.style.display = 'none';
        }
    });
}

// Update date range for charts
function updateDateRange(days) {
    const newLabels = Array.from({ length: parseInt(days) }, (_, i) => `Day ${i + 1}`);
    const newDatasets = {};
    
    patientData.exercises.forEach(exercise => {
        newDatasets[exercise.id] = generateExerciseData(parseInt(days), 5, 15);
    });

    if (window.exerciseRepsChart) {
        window.exerciseRepsChart.data.labels = newLabels;
        window.exerciseRepsChart.data.datasets.forEach((dataset, index) => {
            const exerciseId = patientData.exercises[index].id;
            dataset.data = newDatasets[exerciseId];
        });
        window.exerciseRepsChart.update();
    }
}

// Initialize activity heatmap
function initializeHeatmap() {
    const heatmapContainer = document.getElementById('activity-heatmap');
    if (!heatmapContainer) return;

    // Generate 28 days of activity data (4 weeks)
    const weeks = 4;
    const daysPerWeek = 7;
    
    // Clear existing content
    heatmapContainer.innerHTML = '';
    
    // Add day labels
    const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const labelRow = document.createElement('div');
    labelRow.className = 'heatmap-labels';
    labelRow.style.cssText = 'display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin-bottom: 8px;';
    
    dayLabels.forEach(day => {
        const label = document.createElement('span');
        label.textContent = day;
        label.style.cssText = 'font-size: 0.75rem; color: #636e72; text-align: center;';
        labelRow.appendChild(label);
    });
    heatmapContainer.appendChild(labelRow);

    // Generate heatmap cells
    const cellContainer = document.createElement('div');
    cellContainer.style.cssText = 'display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px;';
    
    for (let week = 0; week < weeks; week++) {
        for (let day = 0; day < daysPerWeek; day++) {
            const cell = document.createElement('div');
            cell.className = 'heatmap-cell';
            
            // Generate random activity level (0-4)
            const level = Math.floor(Math.random() * 5);
            cell.setAttribute('data-level', level);
            
            // Add tooltip data
            const date = new Date();
            date.setDate(date.getDate() - ((weeks - week - 1) * 7 + (6 - day)));
            const reps = level * 10 + Math.floor(Math.random() * 10);
            
            cell.title = `${date.toLocaleDateString()}: ${reps} reps`;
            cell.style.cssText = 'aspect-ratio: 1; border-radius: 4px; cursor: pointer; transition: transform 0.2s;';
            
            // Set background color based on level
            const colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'];
            cell.style.backgroundColor = colors[level];
            
            cell.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.1)';
            });
            cell.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
            
            cellContainer.appendChild(cell);
        }
    }
    
    heatmapContainer.appendChild(cellContainer);

    // Add legend
    const legend = document.createElement('div');
    legend.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-top: 16px; justify-content: flex-end;';
    legend.innerHTML = `
        <span style="font-size: 0.75rem; color: #636e72;">Less</span>
        <div style="width: 12px; height: 12px; background: #ebedf0; border-radius: 2px;"></div>
        <div style="width: 12px; height: 12px; background: #9be9a8; border-radius: 2px;"></div>
        <div style="width: 12px; height: 12px; background: #40c463; border-radius: 2px;"></div>
        <div style="width: 12px; height: 12px; background: #30a14e; border-radius: 2px;"></div>
        <div style="width: 12px; height: 12px; background: #216e39; border-radius: 2px;"></div>
        <span style="font-size: 0.75rem; color: #636e72;">More</span>
    `;
    heatmapContainer.appendChild(legend);
}

// Initialize health app integration buttons
function initializeHealthIntegrations() {
    const connectButtons = document.querySelectorAll('.connect-btn');
    
    connectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const integrationCard = this.closest('.integration-card');
            const appName = integrationCard.querySelector('h4').textContent;
            
            // Simulate connection process
            this.textContent = 'Connecting...';
            this.disabled = true;
            
            setTimeout(() => {
                integrationCard.classList.add('connected');
                const statusEl = integrationCard.querySelector('.integration-status');
                statusEl.textContent = 'Connected';
                
                // Replace button with last sync info
                this.outerHTML = '<p class="last-sync">Last sync: Just now</p>';
                
                showNotification(`Successfully connected to ${appName}!`, 'success');
            }, 1500);
        });
    });
}

// Show notification message
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${type === 'success' ? '#00b894' : '#4a90d9'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Export functions for testing (if in Node.js environment)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        patientData,
        weeklyData,
        recoveryProgressData,
        exerciseTimeData,
        healthMetricsData,
        correlationData,
        generateExerciseData,
        filterExercises,
        updateDateRange
    };
}
