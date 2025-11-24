const express = require('express');
const router = express.Router();
const { authenticate, authorizeGP } = require('../middleware/auth');
const gpController = require('../controllers/gpController');

// All GP routes require authentication and GP authorization
router.use(authenticate);
router.use(authorizeGP);

/**
 * @route   GET /api/gp/patients
 * @desc    Get all patients
 * @access  GP only
 */
router.get('/patients', gpController.getPatients);

/**
 * @route   GET /api/gp/exercises
 * @desc    Get all available exercises (optionally filter by category/difficulty)
 * @access  GP only
 */
router.get('/exercises', gpController.getExercises);

/**
 * @route   GET /api/gp/exercises/:id
 * @desc    Get a single exercise by ID
 * @access  GP only
 */
router.get('/exercises/:id', gpController.getExerciseById);

/**
 * @route   GET /api/gp/assignments
 * @desc    Get all assignments created by the logged-in GP
 * @access  GP only
 */
router.get('/assignments', gpController.getGPAssignments);

/**
 * @route   GET /api/gp/patients/:patientId/assignments
 * @desc    Get assignments for a specific patient
 * @access  GP only
 */
router.get('/patients/:patientId/assignments', gpController.getPatientAssignmentsByGP);

/**
 * @route   POST /api/gp/assignments
 * @desc    Assign an exercise to a patient
 * @access  GP only
 */
router.post('/assignments', gpController.assignExercise);

/**
 * @route   PUT /api/gp/assignments/:id
 * @desc    Update an assignment
 * @access  GP only
 */
router.put('/assignments/:id', gpController.updateAssignment);

/**
 * @route   DELETE /api/gp/assignments/:id
 * @desc    Delete an assignment
 * @access  GP only
 */
router.delete('/assignments/:id', gpController.deleteAssignment);

module.exports = router;
