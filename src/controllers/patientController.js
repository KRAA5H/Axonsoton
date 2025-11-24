const { userStore, exerciseStore, assignmentStore } = require('../data/store');

/**
 * Get assigned exercises for the logged-in patient
 */
const getMyAssignments = (req, res) => {
  const { status } = req.query;
  
  let assignments;
  if (status === 'active') {
    assignments = assignmentStore.findActiveByPatientId(req.user.id);
  } else {
    assignments = assignmentStore.findByPatientId(req.user.id);
  }
  
  // Enrich assignments with GP and exercise details
  const enrichedAssignments = assignments.map(assignment => {
    const gp = userStore.findById(assignment.gpId);
    const exercise = exerciseStore.findById(assignment.exerciseId);
    
    return {
      ...assignment,
      gp: gp ? gp.toSafeObject() : null,
      exercise: exercise || null
    };
  });
  
  res.json(enrichedAssignments);
};

/**
 * Get a single assignment by ID (patient can only view their own)
 */
const getAssignmentById = (req, res) => {
  const { id } = req.params;
  
  const assignment = assignmentStore.findById(id);
  
  if (!assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }
  
  // Verify patient owns this assignment
  if (assignment.patientId !== req.user.id) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  // Enrich with GP and exercise details
  const gp = userStore.findById(assignment.gpId);
  const exercise = exerciseStore.findById(assignment.exerciseId);
  
  res.json({
    ...assignment,
    gp: gp ? gp.toSafeObject() : null,
    exercise: exercise || null
  });
};

/**
 * Mark an assignment as completed
 */
const markAssignmentComplete = (req, res) => {
  const { id } = req.params;
  
  const assignment = assignmentStore.findById(id);
  
  if (!assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }
  
  // Verify patient owns this assignment
  if (assignment.patientId !== req.user.id) {
    return res.status(403).json({ error: 'Access denied' });
  }
  
  // Update status
  assignmentStore.update(id, { status: 'completed' });
  
  res.json({ message: 'Assignment marked as completed' });
};

/**
 * Get summary of patient's exercise routine
 */
const getExerciseSummary = (req, res) => {
  const assignments = assignmentStore.findByPatientId(req.user.id);
  
  const summary = {
    total: assignments.length,
    active: assignments.filter(a => a.status === 'active').length,
    completed: assignments.filter(a => a.status === 'completed').length,
    cancelled: assignments.filter(a => a.status === 'cancelled').length,
    byCategory: {},
    byDifficulty: {}
  };
  
  // Count by category and difficulty
  assignments.forEach(assignment => {
    const exercise = exerciseStore.findById(assignment.exerciseId);
    if (exercise) {
      // Count by category
      if (!summary.byCategory[exercise.category]) {
        summary.byCategory[exercise.category] = 0;
      }
      summary.byCategory[exercise.category]++;
      
      // Count by difficulty
      if (!summary.byDifficulty[exercise.difficulty]) {
        summary.byDifficulty[exercise.difficulty] = 0;
      }
      summary.byDifficulty[exercise.difficulty]++;
    }
  });
  
  res.json(summary);
};

module.exports = {
  getMyAssignments,
  getAssignmentById,
  markAssignmentComplete,
  getExerciseSummary
};
