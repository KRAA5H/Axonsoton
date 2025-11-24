const { describe, it, before, beforeEach, after } = require('node:test');
const assert = require('node:assert');
const http = require('http');

// Import app
const app = require('../src/app');

let server;
let baseUrl;
let testGpId;
let testPatientId;
let testExerciseId;
let testAssignmentId;

/**
 * Helper function to make HTTP requests
 */
function makeRequest(method, path, data = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        let parsedBody;
        try {
          parsedBody = JSON.parse(body);
        } catch {
          parsedBody = body;
        }
        resolve({ status: res.statusCode, body: parsedBody });
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

describe('Axonsoton API Tests', () => {
  before(async () => {
    // Start the server
    server = app.listen(0); // Use random available port
    const address = server.address();
    baseUrl = `http://localhost:${address.port}`;
    
    // Get test user IDs
    const usersRes = await makeRequest('GET', '/api/auth/users');
    const users = usersRes.body;
    
    testGpId = users.find(u => u.role === 'gp').id;
    testPatientId = users.find(u => u.role === 'patient').id;
    
    // Get test exercise ID
    const exercisesRes = await makeRequest('GET', '/api/gp/exercises', null, { 'X-User-Id': testGpId });
    testExerciseId = exercisesRes.body[0].id;
  });

  after(() => {
    server.close();
  });

  describe('Health Check', () => {
    it('should return ok status', async () => {
      const res = await makeRequest('GET', '/health');
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.status, 'ok');
    });
  });

  describe('Authentication', () => {
    it('should list all users', async () => {
      const res = await makeRequest('GET', '/api/auth/users');
      assert.strictEqual(res.status, 200);
      assert(Array.isArray(res.body));
      assert(res.body.length > 0);
    });

    it('should login successfully with valid credentials', async () => {
      const res = await makeRequest('POST', '/api/auth/login', {
        email: 'dr.smith@hospital.com',
        password: 'password123'
      });
      assert.strictEqual(res.status, 200);
      assert(res.body.user);
      assert.strictEqual(res.body.user.role, 'gp');
    });

    it('should fail login with invalid credentials', async () => {
      const res = await makeRequest('POST', '/api/auth/login', {
        email: 'dr.smith@hospital.com',
        password: 'wrongpassword'
      });
      assert.strictEqual(res.status, 401);
    });
  });

  describe('GP Routes - Patients', () => {
    it('should require authentication', async () => {
      const res = await makeRequest('GET', '/api/gp/patients');
      assert.strictEqual(res.status, 401);
    });

    it('should deny access to non-GP users', async () => {
      const res = await makeRequest('GET', '/api/gp/patients', null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 403);
    });

    it('should return patients list for GP', async () => {
      const res = await makeRequest('GET', '/api/gp/patients', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(Array.isArray(res.body));
      assert(res.body.every(p => p.role === 'patient'));
    });
  });

  describe('GP Routes - Exercises', () => {
    it('should return exercises list', async () => {
      const res = await makeRequest('GET', '/api/gp/exercises', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(Array.isArray(res.body));
      assert(res.body.length > 0);
    });

    it('should filter exercises by category', async () => {
      const res = await makeRequest('GET', '/api/gp/exercises?category=stretching', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(res.body.every(e => e.category === 'stretching'));
    });

    it('should filter exercises by difficulty', async () => {
      const res = await makeRequest('GET', '/api/gp/exercises?difficulty=easy', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(res.body.every(e => e.difficulty === 'easy'));
    });

    it('should return single exercise by ID', async () => {
      const res = await makeRequest('GET', `/api/gp/exercises/${testExerciseId}`, null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.id, testExerciseId);
    });
  });

  describe('GP Routes - Assignments', () => {
    it('should create a new assignment', async () => {
      const res = await makeRequest('POST', '/api/gp/assignments', {
        patientId: testPatientId,
        exerciseId: testExerciseId,
        frequency: 'daily',
        repetitions: 15,
        sets: 3,
        notes: 'Test assignment'
      }, { 'X-User-Id': testGpId });
      
      assert.strictEqual(res.status, 201);
      assert(res.body.assignment);
      assert.strictEqual(res.body.assignment.patientId, testPatientId);
      assert.strictEqual(res.body.assignment.exerciseId, testExerciseId);
      
      testAssignmentId = res.body.assignment.id;
    });

    it('should fail to create assignment without patient ID', async () => {
      const res = await makeRequest('POST', '/api/gp/assignments', {
        exerciseId: testExerciseId
      }, { 'X-User-Id': testGpId });
      
      assert.strictEqual(res.status, 400);
    });

    it('should fail to create assignment with invalid patient', async () => {
      const res = await makeRequest('POST', '/api/gp/assignments', {
        patientId: 'invalid-id',
        exerciseId: testExerciseId
      }, { 'X-User-Id': testGpId });
      
      assert.strictEqual(res.status, 404);
    });

    it('should return GP assignments', async () => {
      const res = await makeRequest('GET', '/api/gp/assignments', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(Array.isArray(res.body));
    });

    it('should return assignments for a specific patient', async () => {
      const res = await makeRequest('GET', `/api/gp/patients/${testPatientId}/assignments`, null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      assert(res.body.patient);
      assert(Array.isArray(res.body.assignments));
    });

    it('should update an assignment', async () => {
      const res = await makeRequest('PUT', `/api/gp/assignments/${testAssignmentId}`, {
        frequency: 'weekly',
        repetitions: 20
      }, { 'X-User-Id': testGpId });
      
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.assignment.frequency, 'weekly');
      assert.strictEqual(res.body.assignment.repetitions, 20);
    });

    it('should fail to update assignment of another GP', async () => {
      // Get another GP
      const usersRes = await makeRequest('GET', '/api/auth/users');
      const otherGp = usersRes.body.find(u => u.role === 'gp' && u.id !== testGpId);
      
      if (otherGp) {
        const res = await makeRequest('PUT', `/api/gp/assignments/${testAssignmentId}`, {
          frequency: 'daily'
        }, { 'X-User-Id': otherGp.id });
        
        assert.strictEqual(res.status, 403);
      }
    });
  });

  describe('Patient Routes', () => {
    it('should require authentication', async () => {
      const res = await makeRequest('GET', '/api/patient/assignments');
      assert.strictEqual(res.status, 401);
    });

    it('should deny access to non-patient users', async () => {
      const res = await makeRequest('GET', '/api/patient/assignments', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 403);
    });

    it('should return patient assignments', async () => {
      const res = await makeRequest('GET', '/api/patient/assignments', null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 200);
      assert(Array.isArray(res.body));
    });

    it('should return active assignments only', async () => {
      const res = await makeRequest('GET', '/api/patient/assignments?status=active', null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 200);
      assert(res.body.every(a => a.status === 'active'));
    });

    it('should return patient summary', async () => {
      const res = await makeRequest('GET', '/api/patient/summary', null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 200);
      assert(typeof res.body.total === 'number');
      assert(typeof res.body.active === 'number');
      assert(typeof res.body.completed === 'number');
    });

    it('should return single assignment by ID', async () => {
      const res = await makeRequest('GET', `/api/patient/assignments/${testAssignmentId}`, null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.id, testAssignmentId);
    });

    it('should mark assignment as complete', async () => {
      const res = await makeRequest('PUT', `/api/patient/assignments/${testAssignmentId}/complete`, null, { 'X-User-Id': testPatientId });
      assert.strictEqual(res.status, 200);
      
      // Verify status changed
      const assignmentRes = await makeRequest('GET', `/api/patient/assignments/${testAssignmentId}`, null, { 'X-User-Id': testPatientId });
      assert.strictEqual(assignmentRes.body.status, 'completed');
    });
  });

  describe('GP Routes - Delete Assignment', () => {
    let assignmentToDelete;

    before(async () => {
      // Create an assignment to delete
      const res = await makeRequest('POST', '/api/gp/assignments', {
        patientId: testPatientId,
        exerciseId: testExerciseId,
        frequency: 'daily'
      }, { 'X-User-Id': testGpId });
      
      assignmentToDelete = res.body.assignment.id;
    });

    it('should delete an assignment', async () => {
      const res = await makeRequest('DELETE', `/api/gp/assignments/${assignmentToDelete}`, null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 200);
      
      // Verify deleted
      const getRes = await makeRequest('GET', `/api/patient/assignments/${assignmentToDelete}`, null, { 'X-User-Id': testPatientId });
      assert.strictEqual(getRes.status, 404);
    });

    it('should fail to delete non-existent assignment', async () => {
      const res = await makeRequest('DELETE', '/api/gp/assignments/non-existent-id', null, { 'X-User-Id': testGpId });
      assert.strictEqual(res.status, 404);
    });
  });
});
