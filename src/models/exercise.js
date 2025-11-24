/**
 * Exercise model representing an exercise that can be assigned to patients
 */
class Exercise {
  constructor(id, name, description, category, difficulty, instructions, videoUrl = null) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.category = category; // e.g., 'stretching', 'strength', 'balance', 'cardio'
    this.difficulty = difficulty; // 'easy', 'medium', 'hard'
    this.instructions = instructions;
    this.videoUrl = videoUrl;
    this.createdAt = new Date();
  }
}

module.exports = Exercise;
