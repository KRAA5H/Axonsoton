const express = require('express');
const router = express.Router();
const { authenticate, authorizePatient } = require('../middleware/auth');
const patientController = require('../controllers/patientController');

// All patient routes require authentication and patient authorization
router.use(authenticate);
router.use(authorizePatient);

/**
 * @route   GET /api/patient/assignments
 * @desc    Get all assigned exercises for the logged-in patient
 * @access  Patient only
 * @query   status - Filter by status (active, completed, cancelled)
 */
router.get('/assignments', patientController.getMyAssignments);

/**
 * @route   GET /api/patient/assignments/:id
 * @desc    Get a single assignment by ID
 * @access  Patient only (own assignments)
 */
router.get('/assignments/:id', patientController.getAssignmentById);

/**
 * @route   PUT /api/patient/assignments/:id/complete
 * @desc    Mark an assignment as completed
 * @access  Patient only (own assignments)
 */
router.put('/assignments/:id/complete', patientController.markAssignmentComplete);

/**
 * @route   GET /api/patient/summary
 * @desc    Get exercise summary for the logged-in patient
 * @access  Patient only
 */
router.get('/summary', patientController.getExerciseSummary);

module.exports = router;
