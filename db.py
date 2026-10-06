"""
Database and Persistence Module for ApexLearn LMS
Stores mock data, users with hashed passwords, course progress, quiz results, notes, and forum posts in a local JSON file.
"""

import os
import json
import hashlib
from typing import Dict, Any, List, Optional

DB_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "apexlearn_db.json")

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "apexlearn_lms_salt_2026"
    return hashlib.sha256(f"{salt}{password}".encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password matches the hashed password."""
    return hash_password(plain_password) == hashed_password

def get_default_data() -> Dict[str, Any]:
    """Provide default mock data for ApexLearn LMS."""
    default_users = {
        "student@apexlearn.io": {
            "email": "student@apexlearn.io",
            "name": "Jordan Alvarez",
            "password": hash_password("password123"),
            "role": "Student",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "title": "Full-Stack Track · Cohort 2026",
            "joined": "2026-01-15",
            "hours_learned": 42.5,
            "streak_days": 14,
            "overall_progress": 68
        },
        "instructor@apexlearn.io": {
            "email": "instructor@apexlearn.io",
            "name": "Prof. Alex Vance",
            "password": hash_password("password123"),
            "role": "Instructor",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            "title": "Principal Distributed Systems Architect",
            "joined": "2025-08-10",
            "hours_learned": 210.0,
            "streak_days": 45,
            "overall_progress": 100
        },
        "admin@apexlearn.io": {
            "email": "admin@apexlearn.io",
            "name": "Sarah Chen",
            "password": hash_password("password123"),
            "role": "Admin",
            "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
            "title": "System & Curriculum Administrator",
            "joined": "2025-05-01",
            "hours_learned": 95.0,
            "streak_days": 60,
            "overall_progress": 100
        }
    }

    course_data = {
        "id": "course-distributed-systems-101",
        "title": "Advanced Full-Stack Engineering with Next.js & Distributed Systems",
        "code": "CS-804",
        "instructor": "Prof. Alex Vance",
        "rating": 4.9,
        "reviews_count": 328,
        "total_modules": 8,
        "current_module_num": 6,
        "total_lessons": 34,
        "estimated_hours": 32.0,
        "description": "Master resilient cloud architectures, Next.js Server Actions, optimistic mutations, distributed Redis caching, circuit breakers, and bulkhead thread pool isolation in high-concurrency microservices.",
        "modules": [
            {
                "id": "mod-1",
                "number": 1,
                "title": "Foundations: Next.js 15 Server Components & Streaming",
                "status": "completed",
                "lessons_count": 4,
                "duration": "3h 45m"
            },
            {
                "id": "mod-2",
                "number": 2,
                "title": "High-Performance Data Fetching & Distributed Caching",
                "status": "completed",
                "lessons_count": 5,
                "duration": "4h 20m"
            },
            {
                "id": "mod-3",
                "number": 3,
                "title": "Advanced Auth, Edge Middleware & JWT Revocation",
                "status": "completed",
                "lessons_count": 4,
                "duration": "3h 30m"
            },
            {
                "id": "mod-4",
                "number": 4,
                "title": "Distributed Database Sharding & Read Replicas",
                "status": "completed",
                "lessons_count": 4,
                "duration": "4h 10m"
            },
            {
                "id": "mod-5",
                "number": 5,
                "title": "Server Actions, Optimistic UI & Concurrency Mutations",
                "status": "completed",
                "lessons_count": 5,
                "duration": "4h 45m"
            },
            {
                "id": "mod-6",
                "number": 6,
                "title": "Distributed System Resilience & Circuit Breakers",
                "status": "in_progress",
                "lessons_count": 4,
                "duration": "4h 15m",
                "lessons": [
                    {
                        "id": "lesson-6-1",
                        "title": "6.1 Resilient Circuit Breakers & Fallbacks",
                        "duration": "38 min",
                        "type": "Interactive Video & Lab",
                        "completed": True,
                        "description": "Learn the 3-state machine (Closed, Open, Half-Open), trip thresholds, canary probes, and Upstash Redis distributed locks."
                    },
                    {
                        "id": "lesson-6-2",
                        "title": "6.2 Cascading Failure Prevention & Bulkhead Isolation",
                        "duration": "42 min",
                        "type": "Architecture & Simulator",
                        "completed": False,
                        "description": "Understand thread pool saturation traps, bulkhead partitioning, and queue overflow mitigation."
                    },
                    {
                        "id": "quiz-6",
                        "title": "Quiz 6: Distributed Mutations & Concurrency",
                        "duration": "15 min",
                        "type": "Timed Assessment",
                        "completed": False,
                        "description": "Comprehensive auto-graded assessment covering lock leases, optimistic rollbacks, and circuit breakers."
                    },
                    {
                        "id": "lab-6-1",
                        "title": "Lab 6: Redis Quorum Circuit Breaker Implementation",
                        "duration": "45 min",
                        "type": "Code Sandbox",
                        "completed": True,
                        "description": "Build and test a TypeScript distributed circuit breaker with fallback responses in the interactive sandbox."
                    }
                ]
            },
            {
                "id": "mod-7",
                "number": 7,
                "title": "High-Scale Kafka Event Streaming & Outbox Pattern",
                "status": "locked",
                "lessons_count": 4,
                "duration": "3h 50m"
            },
            {
                "id": "mod-8",
                "number": 8,
                "title": "Multi-Region Global Deployment & Chaos Engineering",
                "status": "locked",
                "lessons_count": 4,
                "duration": "3h 30m"
            }
        ]
    }

    quiz_questions = [
        {
            "id": 1,
            "type": "multiple_choice",
            "points": 5,
            "category": "Optimistic UI Rollbacks",
            "question": "In Next.js App Router with Server Actions, when an optimistic UI rollback occurs after a mutation failure on a high-concurrency node, which mechanism ensures client-side state consistency without causing UI flicker?",
            "options": [
                "Re-fetching the entire route tree using window.location.reload()",
                "Calling useOptimistic() paired with startTransition to reconcile client state with the server payload",
                "Polling the REST endpoint repeatedly until HTTP 200 is confirmed",
                "Forcing an edge purge of the CDN cache on every single mutation attempt"
            ],
            "correct_index": 1,
            "explanation": "useOptimistic combined with React 19's startTransition guarantees that the optimistic state cleanly reverts to the actual server-reconciled state in memory without triggering full page reloads or unmounted DOM flicker."
        },
        {
            "id": 2,
            "type": "multiple_choice",
            "points": 5,
            "category": "Distributed Redis Locks",
            "question": "Which mechanism reliably prevents race conditions across competing multi-region workers executing distributed Redis lock leases?",
            "options": [
                "Local in-memory mutexes inside each Node.js process",
                "Redlock algorithm with monotonic drift tolerance and random lock renewal fencing tokens",
                "Increasing the Redis socket timeout to 60 seconds",
                "Setting Redis keys without TTL so they never expire"
            ],
            "correct_index": 1,
            "explanation": "Redlock uses multi-instance quorum locking with monotonic time-drift calculation and monotonic fencing tokens to ensure stale workers cannot override fresh state."
        },
        {
            "id": 3,
            "type": "true_false",
            "points": 5,
            "category": "Circuit Breaker State Machine",
            "question": "True or False: In a Circuit Breaker pattern, when the state transitions from OPEN to HALF-OPEN, all incoming production requests should immediately be routed to the recovering downstream service.",
            "options": [
                "True",
                "False"
            ],
            "correct_index": 1,
            "explanation": "False! In the HALF-OPEN state, only a small canary probe (limited trial requests) is allowed through. Flooding the recovering service with all traffic would immediately trigger cascading collapse."
        },
        {
            "id": 4,
            "type": "multiple_choice",
            "points": 5,
            "category": "Bulkhead Isolation",
            "question": "What is the primary benefit of the Bulkhead Pattern in microservice architectures?",
            "options": [
                "It compresses network payloads to decrease JSON transmission size",
                "It partitions system resources (like thread pools and connection sockets) so failure in one downstream dependency cannot exhaust total platform capacity",
                "It automatically generates TypeScript types from OpenAPI schemas",
                "It guarantees zero-downtime database schema migrations"
            ],
            "correct_index": 1,
            "explanation": "Named after watertight ship partitions, Bulkheads isolate failure zones so slow or hanging third-party APIs only consume their dedicated thread pool slice, preserving core application uptime."
        },
        {
            "id": 5,
            "type": "true_false",
            "points": 5,
            "category": "Server Actions & Idempotency",
            "question": "True or False: Server Actions that perform balance deductions or charge payments must require an Idempotency Key header to avoid duplicate charges on network retries.",
            "options": [
                "True",
                "False"
            ],
            "correct_index": 0,
            "explanation": "True! Network instability can cause client retries even when the server already processed the mutation. Idempotency keys allow the server to return the previous successful result instead of repeating the mutation."
        }
    ]

    starter_code = '''import { Redis } from '@upstash/redis';
import { telemetry, logger } from './telemetry';

export type BreakerState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export interface CircuitBreakerConfig {
  failureThreshold: number; // e.g. 5 failures
  cooldownPeriodMs: number; // e.g. 30000 ms
  halfOpenTrialLimit: number; // 1 canary request
}

export class DistributedCircuitBreaker {
  private state: BreakerState = 'CLOSED';
  private failureCount: number = 0;
  private lastFailureTime: number = 0;

  constructor(
    private serviceKey: string,
    private config: CircuitBreakerConfig,
    private redis: Redis
  ) {}

  public async execute<T>(action: () => Promise<T>, fallback: () => Promise<T>): Promise<T> {
    const now = Date.now();

    // Check if cooldown elapsed to transition from OPEN to HALF_OPEN
    if (this.state === 'OPEN' && now - this.lastFailureTime > this.config.cooldownPeriodMs) {
      this.state = 'HALF_OPEN';
      logger.info(`[${this.serviceKey}] Transitioned to HALF_OPEN canary trial.`);
    }

    if (this.state === 'OPEN') {
      logger.warn(`[${this.serviceKey}] Circuit OPEN. Invoking fallback.`);
      return await fallback();
    }

    try {
      const result = await action();
      if (this.state === 'HALF_OPEN') {
        this.reset();
      }
      return result;
    } catch (err) {
      return await this.handleFailure(err, fallback);
    }
  }

  private async handleFailure<T>(error: any, fallback: () => Promise<T>): Promise<T> {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    logger.error(`[${this.serviceKey}] Failure detected (${this.failureCount}/${this.config.failureThreshold})`);

    if (this.failureCount >= this.config.failureThreshold || this.state === 'HALF_OPEN') {
      this.state = 'OPEN';
      logger.error(`[${this.serviceKey}] Circuit Tripped -> OPEN! Fast-fallback active.`);
    }

    return await fallback();
  }

  public reset(): void {
    this.state = 'CLOSED';
    this.failureCount = 0;
    logger.info(`[${this.serviceKey}] Circuit healed -> CLOSED.`);
  }

  public getState(): BreakerState {
    return this.state;
  }
}
'''

    reference_solution_code = '''import { Redis } from '@upstash/redis';
import { telemetry, logger } from './telemetry';

export type BreakerState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export interface CircuitBreakerConfig {
  failureThreshold: number; // 5 failures
  cooldownPeriodMs: number; // 30,000 ms
  halfOpenTrialLimit: number; // 1 canary probe
  exponentialBackoff: boolean; // Production enhancement
}

export class DistributedCircuitBreaker {
  private state: BreakerState = 'CLOSED';
  private failureCount: number = 0;
  private lastFailureTime: number = 0;
  private consecutiveTrips: number = 0;

  constructor(
    private serviceKey: string,
    private config: CircuitBreakerConfig,
    private redis: Redis
  ) {}

  public async execute<T>(action: () => Promise<T>, fallback: () => Promise<T>): Promise<T> {
    const now = Date.now();
    const dynamicCooldown = this.calculateCooldown();

    // Check if cooldown elapsed for Half-Open probe
    if (this.state === 'OPEN' && now - this.lastFailureTime > dynamicCooldown) {
      // Acquire Redis distributed quorum lock for canary probe
      const acquiredLock = await this.redis.set(`lock:${this.serviceKey}:canary`, 'locked', { px: 5000, nx: true });
      if (acquiredLock) {
        this.state = 'HALF_OPEN';
        logger.info(`[${this.serviceKey}] Acquired canary lease. State is HALF_OPEN.`);
      }
    }

    if (this.state === 'OPEN') {
      telemetry.recordTripMetric(this.serviceKey, 'FAST_FALLBACK');
      return await fallback();
    }

    try {
      const result = await action();
      if (this.state === 'HALF_OPEN') {
        this.reset();
      }
      return result;
    } catch (err) {
      return await this.handleFailure(err, fallback);
    }
  }

  private async handleFailure<T>(error: any, fallback: () => Promise<T>): Promise<T> {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    telemetry.recordError(this.serviceKey, error);

    if (this.failureCount >= this.config.failureThreshold || this.state === 'HALF_OPEN') {
      this.state = 'OPEN';
      this.consecutiveTrips++;
      logger.error(`[${this.serviceKey}] Tripped -> OPEN (Consecutive trips: ${this.consecutiveTrips})`);
    }

    return await fallback();
  }

  private calculateCooldown(): number {
    if (!this.config.exponentialBackoff) return this.config.cooldownPeriodMs;
    // Exponential backoff with jitter to prevent stampedes
    const factor = Math.min(Math.pow(2, this.consecutiveTrips), 8);
    const jitter = Math.floor(Math.random() * 2000);
    return this.config.cooldownPeriodMs * factor + jitter;
  }

  public reset(): void {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.consecutiveTrips = 0;
    logger.info(`[${this.serviceKey}] Quorum confirmed health. State is CLOSED.`);
  }

  public getState(): BreakerState {
    return this.state;
  }
}
'''

    qa_posts = [
        {
            "id": "qa-1",
            "title": "Why route a canary probe instead of letting all traffic hit the recovering service at once?",
            "author": "Jordan Alvarez",
            "author_role": "Student",
            "author_avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "created_at": "2 hours ago",
            "category": "Architecture",
            "upvotes": 14,
            "is_answered": True,
            "has_verified_instructor_answer": True,
            "content": "In Lesson 6.1 we covered transitioning from OPEN to HALF-OPEN. Why is sending a single canary probe strictly necessary instead of simply resetting the breaker directly back to CLOSED once the 30-second cooldown expires?",
            "replies": [
                {
                    "id": "reply-1-1",
                    "author": "Elena Rostova",
                    "author_role": "Student",
                    "author_avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
                    "created_at": "1 hour ago",
                    "content": "If the downstream database is still restarting its buffer pool, 10,000 incoming requests will immediately crash it again with connection timeouts!",
                    "is_instructor": False
                },
                {
                    "id": "reply-1-2",
                    "author": "Prof. Alex Vance",
                    "author_role": "Instructor",
                    "author_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
                    "created_at": "45 mins ago",
                    "content": "Spot on Elena! This is known as a Thundering Herd or Cold-Start Stampede. If a recovering service was overwhelmed by high CPU or a garbage collection freeze, hitting it with 100% of production traffic instantly re-trips the breaker. The Canary Probe acts as a controlled heartbeat trial with zero risk to normal user traffic (which still receives fast fallbacks).",
                    "is_instructor": True
                }
            ]
        },
        {
            "id": "qa-2",
            "title": "Getting UpstashRedisError: Connection reset by peer in Lab Sandbox step 3",
            "author": "Marcus Brody",
            "author_role": "Student",
            "author_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
            "created_at": "4 hours ago",
            "category": "Lab Sandbox",
            "upvotes": 8,
            "is_answered": True,
            "has_verified_instructor_answer": False,
            "content": "While executing the test suite with simulated network latency >= 2500ms, I saw socket timeouts. Did anyone else encounter this in the Redis configuration?",
            "replies": [
                {
                    "id": "reply-2-1",
                    "author": "David Kim",
                    "author_role": "Student",
                    "author_avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
                    "created_at": "3 hours ago",
                    "content": "Make sure your config.json has retryCount set to 3 with exponential backoff enabled. That fixed the transient socket drop for me!",
                    "is_instructor": False
                }
            ]
        }
    ]

    user_notes = {
        "student@apexlearn.io": """# Lesson 6.1 Notes: Circuit Breakers & Distributed Resilience

### Key Concepts
- **3 States of Circuit Breaker**:
  1. `CLOSED`: All requests flow directly to downstream service. Errors are monitored via sliding window counter.
  2. `OPEN`: Downstream is failing (>= 5 consecutive errors). Breaker trips. Requests return fast fallback immediately without network overhead!
  3. `HALF-OPEN`: Cooldown elapsed (30s). 1 canary request is permitted through. If successful -> reset to `CLOSED`. If failed -> re-trip to `OPEN`.

### Formula
$$ \text{Cooldown}(n) = \text{BaseCooldown} \times 2^{\text{trips}} + \text{Jitter} $$

> **Important**: Always use an idempotent distributed Redis lock when assigning canary rights across multiple Edge workers!
"""
    }

    quiz_results = {
        "student@apexlearn.io": {
            "score_percent": 80,
            "passed": True,
            "points_earned": 20,
            "total_points": 25,
            "time_taken_seconds": 452,
            "completed_at": "2026-10-06 11:20:15",
            "competency": {
                "Server Actions & Mutations": 100,
                "Distributed Redis Locks": 100,
                "Circuit Breaker State Machine": 100,
                "Bulkhead Isolation": 100,
                "Server Actions & Idempotency": 0
            },
            "answers": {
                "1": 1,
                "2": 1,
                "3": 1,
                "4": 1,
                "5": 1  # User picked False for Q5, correct is True
            }
        }
    }

    return {
        "users": default_users,
        "course": course_data,
        "quiz_questions": quiz_questions,
        "starter_code": starter_code,
        "reference_solution_code": reference_solution_code,
        "qa_posts": qa_posts,
        "user_notes": user_notes,
        "quiz_results": quiz_results
    }

def init_db() -> Dict[str, Any]:
    """Ensure database directory and JSON file exist with default content."""
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    if not os.path.exists(DB_FILE_PATH):
        data = get_default_data()
        save_db(data)
        return data
    else:
        try:
            with open(DB_FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            data = get_default_data()
            save_db(data)
            return data

def load_db() -> Dict[str, Any]:
    """Load JSON database."""
    return init_db()

def save_db(data: Dict[str, Any]) -> None:
    """Save JSON database safely."""
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieve user dictionary by email."""
    db = load_db()
    return db.get("users", {}).get(email.strip().lower())

def register_user(name: str, email: str, password: str, role: str) -> tuple[bool, str]:
    """Register a new user, checking for existing email and hashing password."""
    email_clean = email.strip().lower()
    if not name.strip():
        return False, "Full Name is required."
    if not email_clean or "@" not in email_clean:
        return False, "Please provide a valid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    db = load_db()
    if email_clean in db.get("users", {}):
        return False, f"An account with email '{email_clean}' already exists. Please sign in instead."
    
    avatar_map = {
        "Student": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "Instructor": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "Admin": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80"
    }

    new_user = {
        "email": email_clean,
        "name": name.strip(),
        "password": hash_password(password),
        "role": role,
        "avatar": avatar_map.get(role, avatar_map["Student"]),
        "title": f"{role} Member · ApexLearn LMS",
        "joined": "2026-10-06",
        "hours_learned": 0.0,
        "streak_days": 1,
        "overall_progress": 0
    }

    db["users"][email_clean] = new_user
    save_db(db)
    return True, "Account created successfully!"

def authenticate_user(email: str, password: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
    """Verify user credentials and return user object if valid."""
    email_clean = email.strip().lower()
    user = get_user_by_email(email_clean)
    if not user:
        return False, None, "No account found with this email address. Please register first."
    
    if not verify_password(password, user["password"]):
        return False, None, "Invalid password. Please check your credentials and try again."
    
    return True, user, "Login successful!"

def save_quiz_result(email: str, result_data: Dict[str, Any]) -> None:
    """Save quiz score, answers, and timestamp for a user."""
    db = load_db()
    email_clean = email.strip().lower()
    if "quiz_results" not in db:
        db["quiz_results"] = {}
    db["quiz_results"][email_clean] = result_data

    # Update overall user progress
    if email_clean in db.get("users", {}):
        if result_data.get("passed"):
            db["users"][email_clean]["overall_progress"] = min(100, db["users"][email_clean].get("overall_progress", 68) + 12)
            db["users"][email_clean]["hours_learned"] = round(db["users"][email_clean].get("hours_learned", 40.0) + 1.5, 1)

    save_db(db)

def get_user_quiz_result(email: str) -> Optional[Dict[str, Any]]:
    """Retrieve quiz result for a user."""
    db = load_db()
    return db.get("quiz_results", {}).get(email.strip().lower())

def save_user_notes(email: str, notes_content: str) -> None:
    """Save user personal notes for persistence."""
    db = load_db()
    if "user_notes" not in db:
        db["user_notes"] = {}
    db["user_notes"][email.strip().lower()] = notes_content
    save_db(db)

def get_user_notes(email: str) -> str:
    """Retrieve user notes."""
    db = load_db()
    return db.get("user_notes", {}).get(email.strip().lower(), "# Lesson Notes\n\nTake notes here during the lesson...")

def add_qa_post(title: str, content: str, category: str, author_name: str, author_role: str, author_avatar: str) -> str:
    """Add a new Q&A thread."""
    db = load_db()
    post_id = f"qa-{len(db.get('qa_posts', [])) + 1}"
    new_post = {
        "id": post_id,
        "title": title,
        "author": author_name,
        "author_role": author_role,
        "author_avatar": author_avatar,
        "created_at": "Just now",
        "category": category,
        "upvotes": 1,
        "is_answered": False,
        "has_verified_instructor_answer": False,
        "content": content,
        "replies": []
    }
    db.setdefault("qa_posts", []).insert(0, new_post)
    save_db(db)
    return post_id

def add_qa_reply(post_id: str, content: str, author_name: str, author_role: str, author_avatar: str, is_instructor: bool = False) -> bool:
    """Add reply to a Q&A thread."""
    db = load_db()
    for post in db.get("qa_posts", []):
        if post["id"] == post_id:
            reply_id = f"reply-{post_id}-{len(post.get('replies', [])) + 1}"
            reply = {
                "id": reply_id,
                "author": author_name,
                "author_role": author_role,
                "author_avatar": author_avatar,
                "created_at": "Just now",
                "content": content,
                "is_instructor": is_instructor
            }
            post.setdefault("replies", []).append(reply)
            post["is_answered"] = True
            if is_instructor:
                post["has_verified_instructor_answer"] = True
            save_db(db)
            return True
    return False

def upvote_qa_post(post_id: str) -> int:
    """Increment upvote counter on a Q&A post."""
    db = load_db()
    for post in db.get("qa_posts", []):
        if post["id"] == post_id:
            post["upvotes"] = post.get("upvotes", 0) + 1
            save_db(db)
            return post["upvotes"]
    return 0

def reset_database_to_default() -> None:
    """Reset database to initial mock state."""
    data = get_default_data()
    save_db(data)
