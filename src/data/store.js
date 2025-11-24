const User = require('../models/user');
const Exercise = require('../models/exercise');
const ExerciseAssignment = require('../models/exerciseAssignment');
const { v4: uuidv4 } = require('uuid');

/**
 * In-memory data store
 * In a production environment, this would be replaced with a database
 */
const store = {
  users: [],
  exercises: [],
  assignments: []
};

/**
 * Initialize with sample data
 */
function initializeSampleData() {
  // Sample GPs
  const gp1 = new User(uuidv4(), 'dr.smith@hospital.com', 'password123', 'Dr. Sarah Smith', 'gp');
  const gp2 = new User(uuidv4(), 'dr.jones@hospital.com', 'password123', 'Dr. Michael Jones', 'gp');
  
  // Sample Patients
  const patient1 = new User(uuidv4(), 'john.doe@email.com', 'password123', 'John Doe', 'patient');
  const patient2 = new User(uuidv4(), 'jane.wilson@email.com', 'password123', 'Jane Wilson', 'patient');
  const patient3 = new User(uuidv4(), 'bob.brown@email.com', 'password123', 'Bob Brown', 'patient');
  
  store.users.push(gp1, gp2, patient1, patient2, patient3);
  
  // Sample Exercises
  const exercises = [
    new Exercise(
      uuidv4(),
      'Shoulder Stretch',
      'A gentle stretch for shoulder mobility',
      'stretching',
      'easy',
      '1. Stand upright\n2. Raise your arm across your chest\n3. Use the other arm to gently pull\n4. Hold for 15-30 seconds\n5. Repeat on other side'
    ),
    new Exercise(
      uuidv4(),
      'Wall Push-ups',
      'Modified push-ups for upper body strength',
      'strength',
      'easy',
      '1. Stand facing a wall\n2. Place hands flat on wall at shoulder height\n3. Slowly bend elbows and lean toward wall\n4. Push back to starting position\n5. Repeat'
    ),
    new Exercise(
      uuidv4(),
      'Single Leg Balance',
      'Balance exercise to improve stability',
      'balance',
      'medium',
      '1. Stand near a wall or chair for support\n2. Lift one foot off the ground\n3. Balance for 30 seconds\n4. Lower foot and repeat with other leg'
    ),
    new Exercise(
      uuidv4(),
      'Walking in Place',
      'Gentle cardio exercise',
      'cardio',
      'easy',
      '1. Stand with feet hip-width apart\n2. March in place, lifting knees\n3. Swing arms naturally\n4. Continue for 2-5 minutes'
    ),
    new Exercise(
      uuidv4(),
      'Seated Leg Raises',
      'Strengthen quadriceps while seated',
      'strength',
      'easy',
      '1. Sit in a chair with feet flat on floor\n2. Slowly extend one leg straight out\n3. Hold for 3-5 seconds\n4. Lower slowly\n5. Repeat with other leg'
    ),
    new Exercise(
      uuidv4(),
      'Neck Rotations',
      'Gentle neck mobility exercise',
      'stretching',
      'easy',
      '1. Sit or stand upright\n2. Slowly turn head to look over right shoulder\n3. Hold for 5 seconds\n4. Return to center\n5. Repeat on left side'
    ),
    new Exercise(
      uuidv4(),
      'Heel-to-Toe Walk',
      'Balance and coordination exercise',
      'balance',
      'medium',
      '1. Stand upright near a wall for support\n2. Place one foot directly in front of the other\n3. Walk forward, placing heel to toe\n4. Continue for 10-15 steps'
    ),
    new Exercise(
      uuidv4(),
      'Hand Grip Exercises',
      'Strengthen hand and forearm muscles',
      'strength',
      'easy',
      '1. Hold a stress ball or soft object\n2. Squeeze firmly for 3-5 seconds\n3. Release slowly\n4. Repeat 10-15 times per hand'
    )
  ];
  
  store.exercises.push(...exercises);
  
  // Sample assignments
  const assignment1 = new ExerciseAssignment(
    uuidv4(),
    gp1.id,
    patient1.id,
    exercises[0].id,
    { frequency: 'daily', repetitions: 10, sets: 2, notes: 'Take it slow, focus on stretching not straining' }
  );
  
  const assignment2 = new ExerciseAssignment(
    uuidv4(),
    gp1.id,
    patient1.id,
    exercises[3].id,
    { frequency: 'daily', duration: 5, notes: 'Start with 2 minutes and work up' }
  );
  
  store.assignments.push(assignment1, assignment2);
  
  console.log('Sample data initialized');
  console.log(`- ${store.users.filter(u => u.role === 'gp').length} GPs`);
  console.log(`- ${store.users.filter(u => u.role === 'patient').length} Patients`);
  console.log(`- ${store.exercises.length} Exercises`);
  console.log(`- ${store.assignments.length} Assignments`);
}

// User operations
const userStore = {
  findAll: () => store.users,
  findById: (id) => store.users.find(u => u.id === id),
  findByEmail: (email) => store.users.find(u => u.email === email),
  findByRole: (role) => store.users.filter(u => u.role === role),
  create: (userData) => {
    const user = new User(
      uuidv4(),
      userData.email,
      userData.password,
      userData.name,
      userData.role
    );
    store.users.push(user);
    return user;
  },
  delete: (id) => {
    const index = store.users.findIndex(u => u.id === id);
    if (index > -1) {
      store.users.splice(index, 1);
      return true;
    }
    return false;
  }
};

// Exercise operations
const exerciseStore = {
  findAll: () => store.exercises,
  findById: (id) => store.exercises.find(e => e.id === id),
  findByCategory: (category) => store.exercises.filter(e => e.category === category),
  findByDifficulty: (difficulty) => store.exercises.filter(e => e.difficulty === difficulty),
  create: (exerciseData) => {
    const exercise = new Exercise(
      uuidv4(),
      exerciseData.name,
      exerciseData.description,
      exerciseData.category,
      exerciseData.difficulty,
      exerciseData.instructions,
      exerciseData.videoUrl
    );
    store.exercises.push(exercise);
    return exercise;
  },
  delete: (id) => {
    const index = store.exercises.findIndex(e => e.id === id);
    if (index > -1) {
      store.exercises.splice(index, 1);
      return true;
    }
    return false;
  }
};

// Assignment operations
const assignmentStore = {
  findAll: () => store.assignments,
  findById: (id) => store.assignments.find(a => a.id === id),
  findByGpId: (gpId) => store.assignments.filter(a => a.gpId === gpId),
  findByPatientId: (patientId) => store.assignments.filter(a => a.patientId === patientId),
  findByExerciseId: (exerciseId) => store.assignments.filter(a => a.exerciseId === exerciseId),
  findByGpAndPatient: (gpId, patientId) => store.assignments.filter(a => a.gpId === gpId && a.patientId === patientId),
  findActiveByPatientId: (patientId) => store.assignments.filter(a => a.patientId === patientId && a.status === 'active'),
  create: (assignmentData) => {
    const assignment = new ExerciseAssignment(
      uuidv4(),
      assignmentData.gpId,
      assignmentData.patientId,
      assignmentData.exerciseId,
      {
        frequency: assignmentData.frequency,
        repetitions: assignmentData.repetitions,
        sets: assignmentData.sets,
        duration: assignmentData.duration,
        notes: assignmentData.notes,
        startDate: assignmentData.startDate,
        endDate: assignmentData.endDate
      }
    );
    store.assignments.push(assignment);
    return assignment;
  },
  update: (id, updates) => {
    const assignment = store.assignments.find(a => a.id === id);
    if (assignment) {
      assignment.update(updates);
      return assignment;
    }
    return null;
  },
  delete: (id) => {
    const index = store.assignments.findIndex(a => a.id === id);
    if (index > -1) {
      store.assignments.splice(index, 1);
      return true;
    }
    return false;
  }
};

module.exports = {
  initializeSampleData,
  userStore,
  exerciseStore,
  assignmentStore
};
