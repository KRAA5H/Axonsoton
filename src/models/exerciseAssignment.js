/**
 * ExerciseAssignment model representing an exercise assigned by a GP to a patient
 */
class ExerciseAssignment {
  constructor(id, gpId, patientId, exerciseId, options = {}) {
    this.id = id;
    this.gpId = gpId;
    this.patientId = patientId;
    this.exerciseId = exerciseId;
    this.frequency = options.frequency || 'daily'; // 'daily', 'weekly', 'twice_weekly', 'custom'
    this.repetitions = options.repetitions || 10;
    this.sets = options.sets || 3;
    this.duration = options.duration || null; // duration in minutes if applicable
    this.notes = options.notes || '';
    this.startDate = options.startDate || new Date();
    this.endDate = options.endDate || null;
    this.status = options.status || 'active'; // 'active', 'completed', 'cancelled'
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  /**
   * Update the assignment
   */
  update(updates) {
    const allowedUpdates = ['frequency', 'repetitions', 'sets', 'duration', 'notes', 'startDate', 'endDate', 'status'];
    allowedUpdates.forEach(key => {
      if (updates[key] !== undefined) {
        this[key] = updates[key];
      }
    });
    this.updatedAt = new Date();
  }
}

module.exports = ExerciseAssignment;
