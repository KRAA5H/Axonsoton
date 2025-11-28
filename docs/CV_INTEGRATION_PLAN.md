# Computer Vision Integration Plan

This document outlines the options for connecting the exercise recognition and feedback functions to the Axonsoton website, making the platform fully functional with real-time exercise tracking.

## Current System Architecture

### Exercise Detection System (Python)
- **MediaPipe Pose**: Real-time pose detection
- **Custom Modules**: Angle calculation, exercise evaluation, feedback generation
- **Capabilities**: Supports 6 exercises (shoulder/elbow/knee/hip flexion and abduction)
- **Output**: Per-frame feedback including angles, scores, rep counts, and corrections

### Web Application (Node.js)
- **Backend**: Express.js API for user management, exercise assignments
- **Frontend**: Vanilla JavaScript SPA for GP and patient dashboards
- **Current Integration**: None - users must run Python script manually via terminal

---

## Integration Options

### Option 1: Browser-Based Pose Detection (TensorFlow.js/MediaPipe JS)

**Description**: Port the exercise detection logic to run entirely in the browser using TensorFlow.js with the MediaPipe Pose model (via `@mediapipe/pose` or `@tensorflow-models/pose-detection`).

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│  ┌─────────┐   ┌──────────────┐   ┌─────────────┐   │
│  │ Webcam  │──▶│ TensorFlow.js│──▶│ Exercise    │   │
│  │ Stream  │   │ Pose Model   │   │ Evaluator   │   │
│  └─────────┘   └──────────────┘   │ (JavaScript)│   │
│                                    └──────┬──────┘   │
│                                           │          │
│                    ┌──────────────────────▼────────┐ │
│                    │     UI Feedback & Results     │ │
│                    └───────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │  Node.js API   │
                     │ (Store Results)│
                     └────────────────┘
```

**Implementation Steps**:
1. Add TensorFlow.js and MediaPipe Pose dependencies
2. Port `angle_calculator.py` to JavaScript
3. Port `exercises.py` and `feedback.py` to JavaScript
4. Create webcam capture component in the frontend
5. Build real-time feedback UI overlay
6. Add API endpoint to store session results

**Pros**:
- ✅ **No server infrastructure needed** - runs entirely in browser
- ✅ **Low latency** - no network round-trip for pose detection
- ✅ **Privacy-friendly** - video never leaves user's device
- ✅ **Cross-platform** - works on any device with a webcam and modern browser
- ✅ **Scalable** - no server load for processing
- ✅ **Instant deployment** - no additional services to maintain

**Cons**:
- ❌ **Code duplication** - must maintain JavaScript and Python versions
- ❌ **Performance variability** - depends on user's device capabilities
- ❌ **Limited model options** - fewer customization options than Python
- ❌ **Development effort** - significant porting work required
- ❌ **Bundle size** - TensorFlow.js models can be large (~5-10MB)

**Estimated Development Time**: 2-3 weeks

---

### Option 2: WebSocket Streaming to Python Backend

**Description**: Stream video frames from the browser to a Python backend server via WebSocket, process with existing Python code, and stream results back.

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│  ┌─────────┐                        ┌─────────────┐ │
│  │ Webcam  │───── WebSocket ───────▶│ Feedback UI │ │
│  │ Capture │◀──── (frames/results)──│             │ │
│  └─────────┘                        └─────────────┘ │
└─────────────────────────────────────────────────────┘
                              │
                              ▼
               ┌──────────────────────────────────┐
               │   Python WebSocket Server        │
               │  ┌────────────────────────────┐  │
               │  │ MediaPipe Pose             │  │
               │  │ Exercise Evaluator         │  │
               │  │ Feedback Generator         │  │
               │  └────────────────────────────┘  │
               └──────────────────────────────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │  Node.js API   │
                     │ (Store Results)│
                     └────────────────┘
```

**Implementation Steps**:
1. Create Python WebSocket server (using `websockets` or `FastAPI`)
2. Modify `ExerciseEvaluator` to accept base64-encoded frames
3. Add WebSocket client to frontend for video streaming
4. Build real-time feedback UI
5. Connect Python results to Node.js for persistence

**Pros**:
- ✅ **Reuses existing Python code** - minimal changes to detection logic
- ✅ **Consistent behavior** - same model as standalone demo
- ✅ **Easier updates** - only update Python code for improvements
- ✅ **Full MediaPipe features** - access to all model options

**Cons**:
- ❌ **High bandwidth usage** - streaming video frames is expensive
- ❌ **Latency** - network round-trip adds delay (50-200ms typical)
- ❌ **Server costs** - requires compute-capable server infrastructure
- ❌ **Scalability challenges** - each user needs processing resources
- ❌ **Privacy concerns** - video processed on remote server
- ❌ **Complex deployment** - need to manage Python server alongside Node.js
- ❌ **Connection dependency** - poor network = poor experience

**Estimated Development Time**: 1-2 weeks

---

### Option 3: Hybrid Approach (Browser Detection + Server Validation)

**Description**: Use browser-based pose detection for real-time feedback, but send key frames or session summaries to the server for validation, logging, and advanced analytics.

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│  ┌─────────┐   ┌──────────────┐   ┌─────────────┐   │
│  │ Webcam  │──▶│ TensorFlow.js│──▶│ Exercise    │   │
│  │ Stream  │   │ Pose Model   │   │ Evaluator   │   │
│  └─────────┘   └──────────────┘   │ (JavaScript)│   │
│                                    └──────┬──────┘   │
│         ┌─────────────────────────────────┼─────┐   │
│         │        Real-time Feedback       │     │   │
│         └─────────────────────────────────┼─────┘   │
│                                           │         │
│              (Periodic landmark snapshots)│         │
└───────────────────────────────────────────┼─────────┘
                                            │
                                            ▼
                     ┌─────────────────────────────────┐
                     │         Node.js + Python        │
                     │  ┌──────────────────────────┐   │
                     │  │ Session Validation       │   │
                     │  │ Progress Analytics       │   │
                     │  │ GP Review Dashboard      │   │
                     │  └──────────────────────────┘   │
                     └─────────────────────────────────┘
```

**Implementation Steps**:
1. Implement browser-based detection (as in Option 1)
2. Add lightweight landmark data capture at session end
3. Create API endpoint to receive session data
4. Optionally validate sessions with Python backend
5. Build GP review dashboard with session analytics

**Pros**:
- ✅ **Best of both worlds** - real-time performance + server validation
- ✅ **Low latency** - real-time feedback in browser
- ✅ **Bandwidth efficient** - only sends summary data
- ✅ **Privacy-friendly** - video stays local, only landmarks sent
- ✅ **Scalable** - minimal server processing needed
- ✅ **GP oversight** - enables session review and progress tracking
- ✅ **Graceful degradation** - works offline, syncs when connected

**Cons**:
- ❌ **Development complexity** - two codebases to maintain
- ❌ **Initial development effort** - requires both browser and server work
- ❌ **Potential inconsistency** - JS and Python evaluators might differ slightly

**Estimated Development Time**: 3-4 weeks

---

### Option 4: Desktop App Wrapper (Electron)

**Description**: Package the existing Python detection system with the web frontend in an Electron desktop application.

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│              Electron Application                   │
│  ┌────────────────────────────────────────────────┐ │
│  │              Chromium (Web UI)                  │ │
│  │  ┌────────────────────┐  ┌──────────────────┐  │ │
│  │  │   Patient Portal   │  │   Exercise View   │  │ │
│  │  └────────────────────┘  └────────┬─────────┘  │ │
│  └────────────────────────────────────┼───────────┘ │
│                                       │ IPC         │
│  ┌────────────────────────────────────▼───────────┐ │
│  │           Python Child Process                  │ │
│  │  MediaPipe + Exercise Evaluator                 │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP
                     ┌────────────────┐
                     │  Node.js API   │
                     │ (Cloud Sync)   │
                     └────────────────┘
```

**Implementation Steps**:
1. Set up Electron application structure
2. Bundle Python runtime with the app (PyInstaller or embedded)
3. Create IPC bridge between Electron and Python process
4. Modify frontend to communicate via IPC for exercise sessions
5. Add cloud sync for progress data

**Pros**:
- ✅ **Uses existing Python code** - no porting required
- ✅ **Full hardware access** - native webcam performance
- ✅ **Offline capable** - works without internet
- ✅ **Consistent experience** - same behavior across devices

**Cons**:
- ❌ **Requires installation** - not instant access like web
- ❌ **Large download size** - Python runtime + dependencies (~200MB+)
- ❌ **Platform-specific builds** - need Windows, Mac, Linux versions
- ❌ **Update management** - must handle app updates
- ❌ **Limited mobile support** - desktop only
- ❌ **Maintenance burden** - Electron + Python + Node.js stack

**Estimated Development Time**: 4-6 weeks

---

### Option 5: Progressive Web App with WebRTC to Python Server

**Description**: Create a PWA that uses WebRTC for efficient video streaming to a Python processing server, reducing bandwidth compared to WebSocket frame streaming.

**Architecture**:
```
┌─────────────────────────────────────────────────────┐
│          Progressive Web App (PWA)                  │
│  ┌─────────┐                        ┌─────────────┐ │
│  │ Webcam  │────── WebRTC ─────────▶│ Feedback UI │ │
│  │ Stream  │◀────(peer connection)──│             │ │
│  └─────────┘                        └─────────────┘ │
└─────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │    Media Server (Janus/Kurento)        │
         │              │                          │
         │              ▼                          │
         │    Python Processing Worker            │
         │    (MediaPipe + Evaluator)             │
         └────────────────────────────────────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │  Node.js API   │
                     └────────────────┘
```

**Pros**:
- ✅ **Efficient streaming** - WebRTC optimized for video
- ✅ **Uses existing Python** - minimal detection code changes
- ✅ **PWA benefits** - installable, offline-capable shell

**Cons**:
- ❌ **Complex infrastructure** - media server + processing server
- ❌ **High operational cost** - media servers are expensive
- ❌ **Latency still present** - better than WebSocket but still remote
- ❌ **WebRTC complexity** - signaling, TURN servers, NAT traversal
- ❌ **Overkill for this use case** - designed for video calls, not ML

**Estimated Development Time**: 5-8 weeks

---

## Comparison Matrix

| Criteria | Option 1 (Browser) | Option 2 (WebSocket) | Option 3 (Hybrid) | Option 4 (Electron) | Option 5 (WebRTC) |
|----------|-------------------|---------------------|------------------|--------------------|--------------------|
| **Latency** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐ Poor | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Moderate |
| **Privacy** | ⭐⭐⭐⭐⭐ Video local | ⭐⭐ Server-processed | ⭐⭐⭐⭐⭐ Video local | ⭐⭐⭐⭐⭐ Video local | ⭐⭐ Server-processed |
| **Scalability** | ⭐⭐⭐⭐⭐ Unlimited | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Unlimited | ⭐⭐⭐⭐ Good | ⭐⭐ Limited |
| **Server Cost** | ⭐⭐⭐⭐⭐ Minimal | ⭐⭐ High | ⭐⭐⭐⭐⭐ Minimal | ⭐⭐⭐⭐⭐ Minimal | ⭐ Very High |
| **Dev Effort** | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Low | ⭐⭐ High | ⭐⭐ High | ⭐ Very High |
| **Accessibility** | ⭐⭐⭐⭐⭐ Web access | ⭐⭐⭐⭐⭐ Web access | ⭐⭐⭐⭐⭐ Web access | ⭐⭐⭐ Download needed | ⭐⭐⭐⭐ PWA |
| **Offline** | ⭐⭐⭐⭐ Possible | ⭐ No | ⭐⭐⭐⭐ Possible | ⭐⭐⭐⭐⭐ Full | ⭐ No |
| **Mobile** | ⭐⭐⭐⭐ Supported | ⭐⭐⭐⭐ Supported | ⭐⭐⭐⭐ Supported | ⭐ No | ⭐⭐⭐ Limited |
| **Code Reuse** | ⭐⭐ New JS code | ⭐⭐⭐⭐⭐ Python reuse | ⭐⭐ New JS code | ⭐⭐⭐⭐⭐ Python reuse | ⭐⭐⭐⭐⭐ Python reuse |

---

## Recommendation

### **Best Option: Option 1 (Browser-Based Pose Detection)**

After weighing all factors, **Option 1: Browser-Based Pose Detection** is the recommended approach for the following reasons:

#### Primary Justifications:

1. **User Experience Priority**
   - Rehabilitation exercises require real-time feedback (< 50ms latency) to be effective
   - Patients need immediate correction to prevent injury and ensure proper form
   - Browser-based detection provides the lowest possible latency

2. **Privacy and Trust**
   - Healthcare applications require strong privacy guarantees
   - Keeping video processing local builds user trust
   - No risk of video data breaches or compliance issues (HIPAA, GDPR)

3. **Scalability and Cost**
   - No per-user server costs for video processing
   - Can scale to thousands of users without infrastructure changes
   - Reduces operational complexity

4. **Accessibility**
   - Works instantly in any modern browser
   - No installation required
   - Cross-platform (desktop, tablet, mobile)

5. **Technology Maturity**
   - TensorFlow.js and MediaPipe for Web are well-documented and stable
   - Large community and Google support
   - Many reference implementations available

#### Mitigation of Cons:

- **Code duplication**: Accept this trade-off; create shared interfaces so Python can remain the reference implementation for research/testing
- **Performance variability**: Use model complexity options (lite/full) and graceful degradation
- **Bundle size**: Use lazy loading and CDN delivery for model weights

#### Next Steps for Implementation:

1. **Phase 1 (Week 1)**: Set up TensorFlow.js with MediaPipe Pose model in browser
2. **Phase 2 (Week 2)**: Port angle calculation and exercise logic to JavaScript
3. **Phase 3 (Week 3)**: Build exercise session UI with real-time feedback overlay
4. **Phase 4 (Week 4)**: Integrate with existing assignment system and add session storage

### Alternative Recommendation: Option 3 (Hybrid)

If **GP oversight and session validation** are critical requirements, consider **Option 3: Hybrid Approach**. This adds server-side validation while maintaining browser-based real-time performance. However, this doubles the development time and complexity.

---

## Appendix: Technology References

### For Option 1 (Browser-Based):
- [TensorFlow.js Pose Detection](https://github.com/tensorflow/tfjs-models/tree/master/pose-detection)
- [MediaPipe Pose for Web](https://google.github.io/mediapipe/solutions/pose.html#javascript-solution-api)
- [MediaPipe JS Documentation](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/web_js)

### For Option 2/3 (Server-Side):
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Python websockets library](https://websockets.readthedocs.io/)

### For Option 4 (Electron):
- [Electron Documentation](https://www.electronjs.org/docs)
- [PyInstaller](https://pyinstaller.org/)

### For Option 5 (WebRTC):
- [Janus WebRTC Server](https://janus.conf.meetecho.com/)
- [Kurento Media Server](https://www.kurento.org/)
