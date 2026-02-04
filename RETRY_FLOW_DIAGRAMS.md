# Retry Mechanism Flow Diagram

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    extract_structure()                          │
│               (Main extraction entry point)                     │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├─ Format user prompt
         │
         └─► Is model 'gemini'?
             │
             ├─ YES ──► _call_gemini_with_retry()
             │
             └─ NO ───► _call_gpt_with_retry()
                       │
                       └─ Parse JSON response
                          │
                          ├─ SUCCESS ──► Return {success: True, data: {...}}
                          │
                          └─ FAILURE ──► Return {success: False, error: "..."}
```

## Retry Logic Flow (Per API Call)

```
┌──────────────────────────────────────────────────────────────────┐
│                   API Call Attempt                               │
│              (try/except wrapper)                                │
└────────┬──────────────────────────────────────────────────────────┘
         │
         ├─ Attempt = 0
         │
         └─► FOR Attempt in range(max_retries):
             │
             ├─ TRY: Call API
             │   │
             │   ├─ SUCCESS ──► Return response.text
             │   │
             │   └─ EXCEPTION (e):
             │       │
             │       ├─ Check error_str = str(e).lower()
             │       │
             │       └─► Is error RETRYABLE?
             │           │
             │           ├─ NO ──────────► RAISE exception immediately
             │           │
             │           ├─ YES & attempt < max_retries
             │           │   │
             │           │   ├─ Calculate wait_time = 1s * (2 ^ attempt)
             │           │   │
             │           │   ├─ Print retry message
             │           │   │
             │           │   └─ time.sleep(wait_time) ◄──┐
             │           │                                 │
             │           │   Continue to next attempt ────┘
             │           │
             │           └─ YES & attempt == max_retries
             │               │
             │               └─ RAISE exception after max retries
             │
             └─ Next attempt (if sleep completed)

┌──────────────────────────────────────────────────────────────────┐
│ Final Exception Block                                            │
│                                                                  │
│ if last_exception:                                              │
│     raise last_exception                                        │
│ else:                                                           │
│     raise RuntimeError("Max retries failed")                    │
└──────────────────────────────────────────────────────────────────┘
```

## Error Classification Decision Tree

```
                        ┌─ Exception Raised
                        │
                        └─ error_str = str(e).lower()
                           │
                           ├─ Contains 'timeout'? ─────────┐
                           │                               │
                           ├─ Contains 'connection'? ──┐   │
                           │                           │   │
                           ├─ Contains 'rate'? ──┐     │   │
                           │                     │     │   │
                           ├─ Contains '429'? ──┤     │   │
                           │                     │     │   │
                           ├─ Contains '500'? ──┤ YES │   │
                           │                     │     │   │
                           ├─ Contains '502'? ──┤     │   │
                           │                     │     │   │
                           ├─ Contains '503'? ──┤     │   │
                           │                     │     │   │
                           └─ Contains '503'? ──┘     │   │
                           │                          │   │
                           └──────────────────────────┼───┼──► RETRYABLE
                                                      │   │   (exponential backoff)
                              All other errors   ─────┘   │
                                                          │
                                                          └──► NON-RETRYABLE
                                                              (raise immediately)
```

## Exponential Backoff Visualization

### Configuration: max_retries=3, initial_wait_time=1

```
Attempt 1
│
├─ API Call Failed (Transient Error)
│
└─ Wait 1 second ▓░░░░░░░░░░░░░░░░░░░░ (1s)
   │
   └─► Attempt 2
       │
       ├─ API Call Failed (Transient Error)
       │
       └─ Wait 2 seconds ▓▓░░░░░░░░░░░░░░░░░░░ (2s)
          │
          └─► Attempt 3
              │
              ├─ API Call Failed (Transient Error)
              │
              └─ Wait 4 seconds ▓▓▓▓░░░░░░░░░░░░░░░ (4s)
                 │
                 └─► Attempt 4 (NO MORE - max_retries reached)
                     │
                     └─► RAISE Exception
                         Total wait time: 1 + 2 + 4 = 7 seconds
```

## Response Flow with Retry Tracking

```
┌─────────────────────────────────────┐
│   extract_structure() CALLED        │
└────────────┬────────────────────────┘
             │
             └─ Retry-enabled API calls
                │
                ├─ Attempt 1: FAIL (retry)
                │             │
                │             └─ Wait 1s
                │
                ├─ Attempt 2: FAIL (retry)
                │             │
                │             └─ Wait 2s
                │
                ├─ Attempt 3: SUCCESS ✓
                │
                └─► Return:
                    {
                        'success': True,
                        'data': {...},
                        'raw_response': '...',
                        'error': None,
                        'retry_count': 2  ◄── Retries attempted
                    }
```

## Configuration Scenarios

### Scenario 1: DEFAULT (Balanced)
```
max_retries=3
initial_wait_time=1

1s ──► 2s ──► 4s [TIMEOUT]
Total: ~7 seconds

Use Case: Production with moderate reliability needs
```

### Scenario 2: AGGRESSIVE (High Resilience)
```
max_retries=5
initial_wait_time=0.5

0.5s ──► 1s ──► 2s ──► 4s ──► 8s [TIMEOUT]
Total: ~15.5 seconds

Use Case: Critical operations where retries are worth the time
```

### Scenario 3: CONSERVATIVE (Fast Failure)
```
max_retries=2
initial_wait_time=1

1s ──► 2s [TIMEOUT]
Total: ~3 seconds

Use Case: Real-time applications where quick failure feedback is important
```

## Success Scenarios

### Scenario A: Success on First Try (No Retries)
```
Attempt 1 ──► API SUCCESS ──► return {retry_count: 0, success: True}
```

### Scenario B: Success After 1 Retry
```
Attempt 1 ──► FAIL (transient)
              ├─ Wait 1s
              │
Attempt 2 ──► API SUCCESS ──► return {retry_count: 1, success: True}
```

### Scenario C: Success After 2 Retries
```
Attempt 1 ──► FAIL (transient)
              ├─ Wait 1s
              │
Attempt 2 ──► FAIL (transient)
              ├─ Wait 2s
              │
Attempt 3 ──► API SUCCESS ──► return {retry_count: 2, success: True}
```

### Scenario D: Permanent Failure (No Retries)
```
Attempt 1 ──► FAIL (permanent: Invalid API key)
              │
              └─► No wait, no retry
                  return {retry_count: 0, success: False}
```

### Scenario E: Exhausted Retries
```
Attempt 1 ──► FAIL (transient)
              ├─ Wait 1s
              │
Attempt 2 ──► FAIL (transient)
              ├─ Wait 2s
              │
Attempt 3 ──► FAIL (transient)
              ├─ Wait 4s
              │
Attempt 4 ──► MAX RETRIES EXCEEDED
              │
              └─► return {retry_count: 3, success: False}
```

## Error Handling Matrix

```
Error Type         | Retryable? | Action
─────────────────────────────────────────────────────────
Connection timeout |    YES     | Retry with backoff
Rate limit (429)   |    YES     | Retry with backoff
Service error (5xx)|    YES     | Retry with backoff
Invalid API key    |    NO      | Fail immediately
Malformed request  |    NO      | Fail immediately
Auth failure       |    NO      | Fail immediately
Invalid model      |    NO      | Fail immediately
Unsupported format |    NO      | Fail immediately
```

---

**Visual diagrams show the complete retry flow, from initial API call through exponential backoff to final response.**
