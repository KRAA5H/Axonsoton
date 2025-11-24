const { userStore, exerciseStore, assignmentStore } = require('../data/store');

/**
 * Get all patients (for GPs to select from when assigning exercises)
 */
const getPatients = (req, res) => {
  const patients = userStore.findByRole('patient');
  res.json(patients.map(p => p.toSafeObject()));
};

/**
 * Get all exercises
 */
const getExercises = (req, res) => {
  const { category, difficulty } = req.query;
  let exercises = exerciseStore.findAll();
  
  if (category) {
    exercises = exercises.filter(e => e.category === category);
  }
  
  if (difficulty) {
    exercises = exercises.filter(e => e.difficulty === difficulty);
  }
  
  res.json(exercises);
};

/**
 * Get a single exercise by ID
 */
const getExerciseById = (req, res) => {
  const exercise = exerciseStore.findById(req.params.id);
  
  if (!exercise) {
    return res.status(404).json({ error: 'Exercise not found' });
  }
  
  res.json(exercise);
};

/**
 * Get all assignments created by the logged-in GP
 */
const getGPAssignments = (req, res) => {
  const assignments = assignmentStore.findByGpId(req.user.id);
  
  // Enrich assignments with patient and exercise details
  const enrichedAssignments = assignments.map(assignment => {
    const patient = userStore.findById(assignment.patientId);
    const exercise = exerciseStore.findById(assignment.exerciseId);
    
    return {
      ...assignment,
      patient: patient ? patient.toSafeObject() : null,
      exercise: exercise || null
    };
  });
  
  res.json(enrichedAssignments);
};

/**
 * Get assignments for a specific patient (GP view)
 */
const getPatientAssignmentsByGP = (req, res) => {
  const { patientId } = req.params;
  
  // Verify patient exists
  const patient = userStore.findById(patientId);
  if (!patient || patient.role !== 'patient') {
    return res.status(404).json({ error: 'Patient not found' });
  }
  
  // Get assignments created by this GP for this patient
  const assignments = assignmentStore.findByGpAndPatient(req.user.id, patientId);
  
  // Enrich with exercise details
  const enrichedAssignments = assignments.map(assignment => {
    const exercise = exerciseStore.findById(assignment.exerciseId);
    return {
      ...assignment,
      exercise: exercise || null
    };
  });
  
  res.json({
    patient: patient.toSafeObject(),
    assignments: enrichedAssignments
  });
};

/**
 * Assign an exercise to a patient
 */
const assignExercise = (req, res) => {
  const { patientId, exerciseId, frequency, repetitions, sets, duration, notes, startDate, endDate } = req.body;
  
  // Validate required fields
  if (!patientId) {
    return res.status(400).json({ error: 'Patient ID is required' });
  }
  
  if (!exerciseId) {
    return res.status(400).json({ error: 'Exercise ID is required' });
  }
  
  // Verify patient exists
  const patient = userStore.findById(patientId);
  if (!patient || patient.role !== 'patient') {
    return res.status(404).json({ error: 'Patient not found' });
  }
  
  // Verify exercise exists
  const exercise = exerciseStore.findById(exerciseId);
  if (!exercise) {
    return res.status(404).json({ error: 'Exercise not found' });
  }
  
  // Create assignment
  const assignment = assignmentStore.create({
    gpId: req.user.id,
    patientId,
    exerciseId,
    frequency,
    repetitions,
    sets,
    duration,
    notes,
    startDate: startDate ? new Date(startDate) : new Date(),
    endDate: endDate ? new Date(endDate) : null
  });
  
  res.status(201).json({
    message: 'Exercise assigned successfully',
    assignment: {
      ...assignment,
      patient: patient.toSafeObject(),
      exercise
    }
  });
};

/**
 * Update an existing assignment
 */
const updateAssignment = (req, res) => {
  const { id } = req.params;
  const { frequency, repetitions, sets, duration, notes, startDate, endDate, status } = req.body;
  
  // Find assignment
  const assignment = assignmentStore.findById(id);
  
  if (!assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }
  
  // Verify the GP owns this assignment
  if (assignment.gpId !== req.user.id) {
    return res.status(403).json({ error: 'You can only update your own assignments' });
  }
  
  // Update assignment
  const updates = {};
  if (frequency !== undefined) updates.frequency = frequency;
  if (repetitions !== undefined) updates.repetitions = repetitions;
  if (sets !== undefined) updates.sets = sets;
  if (duration !== undefined) updates.duration = duration;
  if (notes !== undefined) updates.notes = notes;
  if (startDate !== undefined) updates.startDate = new Date(startDate);
  if (endDate !== undefined) updates.endDate = endDate ? new Date(endDate) : null;
  if (status !== undefined) updates.status = status;
  
  const updatedAssignment = assignmentStore.update(id, updates);
  
  // Get related data
  const patient = userStore.findById(updatedAssignment.patientId);
  const exercise = exerciseStore.findById(updatedAssignment.exerciseId);
  
  res.json({
    message: 'Assignment updated successfully',
    assignment: {
      ...updatedAssignment,
      patient: patient ? patient.toSafeObject() : null,
      exercise
    }
  });
};

/**
 * Delete an assignment
 */
const deleteAssignment = (req, res) => {
  const { id } = req.params;
  
  // Find assignment
  const assignment = assignmentStore.findById(id);
  
  if (!assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }
  
  // Verify the GP owns this assignment
  if (assignment.gpId !== req.user.id) {
    return res.status(403).json({ error: 'You can only delete your own assignments' });
  }
  
  assignmentStore.delete(id);
  
  res.json({ message: 'Assignment deleted successfully' });
};

module.exports = {
  getPatients,
  getExercises,
  getExerciseById,
  getGPAssignments,
  getPatientAssignmentsByGP,
  assignExercise,
  updateAssignment,
  deleteAssignment
};
