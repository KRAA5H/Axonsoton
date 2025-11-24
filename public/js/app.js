/**
 * Axonsoton - Exercise Assignment System
 * Frontend JavaScript Application
 */

const API_BASE = '/api';
let currentUser = null;

// DOM Elements
const loginView = document.getElementById('login-view');
const gpView = document.getElementById('gp-view');
const patientView = document.getElementById('patient-view');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  loadUsers();
  setupEventListeners();
});

/**
 * Load all users for login selection
 */
async function loadUsers() {
  try {
    const response = await fetch(`${API_BASE}/auth/users`);
    const users = await response.json();
    
    const gpList = document.getElementById('gp-list');
    const patientList = document.getElementById('patient-list');
    
    // Clear existing lists
    gpList.innerHTML = '';
    patientList.innerHTML = '';
    
    users.forEach(user => {
      const btn = document.createElement('button');
      btn.className = 'user-btn';
      btn.innerHTML = `
        ${user.name}
        <span class="user-role">${user.email}</span>
      `;
      btn.addEventListener('click', () => login(user));
      
      if (user.role === 'gp') {
        gpList.appendChild(btn);
      } else {
        patientList.appendChild(btn);
      }
    });
  } catch (error) {
    console.error('Error loading users:', error);
  }
}

/**
 * Login as a user
 */
function login(user) {
  currentUser = user;
  localStorage.setItem('currentUser', JSON.stringify(user));
  
  if (user.role === 'gp') {
    showGPDashboard();
  } else {
    showPatientDashboard();
  }
}

/**
 * Logout
 */
function logout() {
  currentUser = null;
  localStorage.removeItem('currentUser');
  showLoginView();
}

/**
 * Show login view
 */
function showLoginView() {
  loginView.classList.remove('hidden');
  gpView.classList.add('hidden');
  patientView.classList.add('hidden');
}

/**
 * Show GP Dashboard
 */
async function showGPDashboard() {
  loginView.classList.add('hidden');
  gpView.classList.remove('hidden');
  patientView.classList.add('hidden');
  
  document.getElementById('gp-user-name').textContent = currentUser.name;
  
  await loadGPPatients();
  await loadExercises();
  await loadGPAssignments();
}

/**
 * Show Patient Dashboard
 */
async function showPatientDashboard() {
  loginView.classList.add('hidden');
  gpView.classList.add('hidden');
  patientView.classList.remove('hidden');
  
  document.getElementById('patient-user-name').textContent = currentUser.name;
  
  await loadPatientSummary();
  await loadPatientExercises();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  // GP Logout
  document.getElementById('gp-logout').addEventListener('click', logout);
  
  // Patient Logout
  document.getElementById('patient-logout').addEventListener('click', logout);
  
  // Assignment Form
  document.getElementById('assignment-form').addEventListener('submit', handleAssignmentSubmit);
  
  // Edit Form
  document.getElementById('edit-form').addEventListener('submit', handleEditSubmit);
  
  // Modal Close
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-cancel').addEventListener('click', closeModal);
  
  // Patient filter
  document.getElementById('show-active-only').addEventListener('change', loadPatientExercises);
  
  // Check for saved user
  const savedUser = localStorage.getItem('currentUser');
  if (savedUser) {
    currentUser = JSON.parse(savedUser);
    if (currentUser.role === 'gp') {
      showGPDashboard();
    } else {
      showPatientDashboard();
    }
  }
}

// ====== GP Functions ======

/**
 * Load patients for GP view
 */
async function loadGPPatients() {
  try {
    const response = await fetch(`${API_BASE}/gp/patients`, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const patients = await response.json();
    
    const patientGrid = document.getElementById('gp-patient-list');
    const patientSelect = document.getElementById('select-patient');
    
    patientGrid.innerHTML = '';
    patientSelect.innerHTML = '<option value="">Choose a patient...</option>';
    
    patients.forEach(patient => {
      // Patient grid card
      const card = document.createElement('div');
      card.className = 'patient-card';
      card.textContent = patient.name;
      card.dataset.id = patient.id;
      card.addEventListener('click', () => selectPatient(patient.id));
      patientGrid.appendChild(card);
      
      // Patient select option
      const option = document.createElement('option');
      option.value = patient.id;
      option.textContent = patient.name;
      patientSelect.appendChild(option);
    });
  } catch (error) {
    console.error('Error loading patients:', error);
  }
}

/**
 * Select a patient (click on patient card)
 */
function selectPatient(patientId) {
  document.querySelectorAll('.patient-card').forEach(card => {
    card.classList.toggle('selected', card.dataset.id === patientId);
  });
  document.getElementById('select-patient').value = patientId;
}

/**
 * Load exercises for GP view
 */
async function loadExercises() {
  try {
    const response = await fetch(`${API_BASE}/gp/exercises`, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const exercises = await response.json();
    
    const exerciseSelect = document.getElementById('select-exercise');
    exerciseSelect.innerHTML = '<option value="">Choose an exercise...</option>';
    
    // Group exercises by category
    const grouped = exercises.reduce((acc, ex) => {
      if (!acc[ex.category]) acc[ex.category] = [];
      acc[ex.category].push(ex);
      return acc;
    }, {});
    
    Object.entries(grouped).forEach(([category, exs]) => {
      const optgroup = document.createElement('optgroup');
      optgroup.label = capitalizeFirst(category);
      
      exs.forEach(ex => {
        const option = document.createElement('option');
        option.value = ex.id;
        option.textContent = `${ex.name} (${ex.difficulty})`;
        optgroup.appendChild(option);
      });
      
      exerciseSelect.appendChild(optgroup);
    });
  } catch (error) {
    console.error('Error loading exercises:', error);
  }
}

/**
 * Load GP's assignments
 */
async function loadGPAssignments() {
  try {
    const response = await fetch(`${API_BASE}/gp/assignments`, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const assignments = await response.json();
    
    const tbody = document.getElementById('assignments-tbody');
    tbody.innerHTML = '';
    
    if (assignments.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No assignments yet</td></tr>';
      return;
    }
    
    assignments.forEach(assignment => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${assignment.patient ? assignment.patient.name : 'Unknown'}</td>
        <td>${assignment.exercise ? assignment.exercise.name : 'Unknown'}</td>
        <td>${capitalizeFirst(assignment.frequency.replace('_', ' '))}</td>
        <td>${assignment.repetitions} x ${assignment.sets}</td>
        <td><span class="status-badge status-${assignment.status}">${capitalizeFirst(assignment.status)}</span></td>
        <td>
          <div class="action-buttons">
            <button class="btn btn-small btn-secondary" onclick="editAssignment('${assignment.id}')">Edit</button>
            <button class="btn btn-small btn-danger" onclick="deleteAssignment('${assignment.id}')">Delete</button>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error('Error loading assignments:', error);
  }
}

/**
 * Handle assignment form submission
 */
async function handleAssignmentSubmit(e) {
  e.preventDefault();
  
  const patientId = document.getElementById('select-patient').value;
  const exerciseId = document.getElementById('select-exercise').value;
  const frequency = document.getElementById('frequency').value;
  const repetitions = parseInt(document.getElementById('repetitions').value);
  const sets = parseInt(document.getElementById('sets').value);
  const duration = document.getElementById('duration').value ? parseInt(document.getElementById('duration').value) : null;
  const notes = document.getElementById('notes').value;
  
  if (!patientId || !exerciseId) {
    alert('Please select both a patient and an exercise');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/gp/assignments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': currentUser.id
      },
      body: JSON.stringify({
        patientId,
        exerciseId,
        frequency,
        repetitions,
        sets,
        duration,
        notes
      })
    });
    
    if (response.ok) {
      alert('Exercise assigned successfully!');
      document.getElementById('assignment-form').reset();
      document.querySelectorAll('.patient-card').forEach(c => c.classList.remove('selected'));
      await loadGPAssignments();
    } else {
      const error = await response.json();
      alert('Error: ' + error.error);
    }
  } catch (error) {
    console.error('Error assigning exercise:', error);
    alert('An error occurred while assigning the exercise');
  }
}

/**
 * Edit an assignment
 */
async function editAssignment(assignmentId) {
  try {
    const response = await fetch(`${API_BASE}/gp/assignments`, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const assignments = await response.json();
    const assignment = assignments.find(a => a.id === assignmentId);
    
    if (!assignment) {
      alert('Assignment not found');
      return;
    }
    
    // Populate modal
    document.getElementById('edit-assignment-id').value = assignment.id;
    document.getElementById('edit-frequency').value = assignment.frequency;
    document.getElementById('edit-repetitions').value = assignment.repetitions;
    document.getElementById('edit-sets').value = assignment.sets;
    document.getElementById('edit-duration').value = assignment.duration || '';
    document.getElementById('edit-status').value = assignment.status;
    document.getElementById('edit-notes').value = assignment.notes || '';
    
    // Show modal
    document.getElementById('edit-modal').classList.remove('hidden');
  } catch (error) {
    console.error('Error loading assignment:', error);
  }
}

/**
 * Handle edit form submission
 */
async function handleEditSubmit(e) {
  e.preventDefault();
  
  const assignmentId = document.getElementById('edit-assignment-id').value;
  const frequency = document.getElementById('edit-frequency').value;
  const repetitions = parseInt(document.getElementById('edit-repetitions').value);
  const sets = parseInt(document.getElementById('edit-sets').value);
  const duration = document.getElementById('edit-duration').value ? parseInt(document.getElementById('edit-duration').value) : null;
  const status = document.getElementById('edit-status').value;
  const notes = document.getElementById('edit-notes').value;
  
  try {
    const response = await fetch(`${API_BASE}/gp/assignments/${assignmentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': currentUser.id
      },
      body: JSON.stringify({
        frequency,
        repetitions,
        sets,
        duration,
        status,
        notes
      })
    });
    
    if (response.ok) {
      closeModal();
      await loadGPAssignments();
    } else {
      const error = await response.json();
      alert('Error: ' + error.error);
    }
  } catch (error) {
    console.error('Error updating assignment:', error);
    alert('An error occurred while updating the assignment');
  }
}

/**
 * Delete an assignment
 */
async function deleteAssignment(assignmentId) {
  if (!confirm('Are you sure you want to delete this assignment?')) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/gp/assignments/${assignmentId}`, {
      method: 'DELETE',
      headers: { 'X-User-Id': currentUser.id }
    });
    
    if (response.ok) {
      await loadGPAssignments();
    } else {
      const error = await response.json();
      alert('Error: ' + error.error);
    }
  } catch (error) {
    console.error('Error deleting assignment:', error);
    alert('An error occurred while deleting the assignment');
  }
}

/**
 * Close modal
 */
function closeModal() {
  document.getElementById('edit-modal').classList.add('hidden');
}

// ====== Patient Functions ======

/**
 * Load patient summary
 */
async function loadPatientSummary() {
  try {
    const response = await fetch(`${API_BASE}/patient/summary`, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const summary = await response.json();
    
    document.getElementById('total-exercises').textContent = summary.total;
    document.getElementById('active-exercises').textContent = summary.active;
    document.getElementById('completed-exercises').textContent = summary.completed;
  } catch (error) {
    console.error('Error loading summary:', error);
  }
}

/**
 * Load patient's assigned exercises
 */
async function loadPatientExercises() {
  try {
    const showActiveOnly = document.getElementById('show-active-only').checked;
    const url = showActiveOnly ? `${API_BASE}/patient/assignments?status=active` : `${API_BASE}/patient/assignments`;
    
    const response = await fetch(url, {
      headers: { 'X-User-Id': currentUser.id }
    });
    const assignments = await response.json();
    
    const container = document.getElementById('patient-exercises');
    container.innerHTML = '';
    
    if (assignments.length === 0) {
      container.innerHTML = '<p>No exercises assigned yet.</p>';
      return;
    }
    
    assignments.forEach(assignment => {
      const card = document.createElement('div');
      card.className = 'exercise-card';
      card.innerHTML = `
        <h4>${assignment.exercise ? assignment.exercise.name : 'Unknown Exercise'}</h4>
        <p>${assignment.exercise ? assignment.exercise.description : ''}</p>
        
        <div class="exercise-details">
          <div class="detail-item">
            <span class="detail-label">Frequency</span>
            <span class="detail-value">${capitalizeFirst(assignment.frequency.replace('_', ' '))}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Reps x Sets</span>
            <span class="detail-value">${assignment.repetitions} x ${assignment.sets}</span>
          </div>
          ${assignment.duration ? `
          <div class="detail-item">
            <span class="detail-label">Duration</span>
            <span class="detail-value">${assignment.duration} min</span>
          </div>
          ` : ''}
          <div class="detail-item">
            <span class="detail-label">Status</span>
            <span class="detail-value status-badge status-${assignment.status}">${capitalizeFirst(assignment.status)}</span>
          </div>
        </div>
        
        ${assignment.notes ? `
        <div class="notes">
          <div class="notes-label">Notes from your GP:</div>
          ${assignment.notes}
        </div>
        ` : ''}
        
        ${assignment.exercise && assignment.exercise.instructions ? `
        <div class="instructions">
          <strong>Instructions:</strong><br>
          ${assignment.exercise.instructions}
        </div>
        ` : ''}
        
        <div class="assigned-by">
          Assigned by: ${assignment.gp ? assignment.gp.name : 'Unknown'}
        </div>
        
        ${assignment.status === 'active' ? `
        <div class="card-actions">
          <button class="btn btn-success btn-small" onclick="markComplete('${assignment.id}')">Mark Complete</button>
        </div>
        ` : ''}
      `;
      container.appendChild(card);
    });
  } catch (error) {
    console.error('Error loading exercises:', error);
  }
}

/**
 * Mark an assignment as complete
 */
async function markComplete(assignmentId) {
  try {
    const response = await fetch(`${API_BASE}/patient/assignments/${assignmentId}/complete`, {
      method: 'PUT',
      headers: { 'X-User-Id': currentUser.id }
    });
    
    if (response.ok) {
      await loadPatientSummary();
      await loadPatientExercises();
    } else {
      const error = await response.json();
      alert('Error: ' + error.error);
    }
  } catch (error) {
    console.error('Error marking complete:', error);
    alert('An error occurred');
  }
}

// ====== Utility Functions ======

/**
 * Capitalize first letter
 */
function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
