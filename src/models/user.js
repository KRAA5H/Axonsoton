/**
 * User model representing both GPs (General Practitioners) and Patients
 */
class User {
  constructor(id, email, password, name, role) {
    this.id = id;
    this.email = email;
    this.password = password;
    this.name = name;
    this.role = role; // 'gp' or 'patient'
    this.createdAt = new Date();
  }

  /**
   * Returns a safe representation of the user (without password)
   */
  toSafeObject() {
    return {
      id: this.id,
      email: this.email,
      name: this.name,
      role: this.role,
      createdAt: this.createdAt
    };
  }
}

module.exports = User;
