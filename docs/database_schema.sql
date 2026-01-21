-- Revised Database Schema (v1.1)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table with Subscription Info
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    auth_provider_id VARCHAR(255),
    
    -- Tier Management
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, basic, pro
    subscription_status VARCHAR(20) DEFAULT 'active',
    tasks_used_this_month INTEGER DEFAULT 0,
    billing_period_start DATE DEFAULT CURRENT_DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Secure Token Storage (Separate table for higher security/encryption)
CREATE TABLE user_integrations (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(20) NOT NULL, -- google, microsoft
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    expires_at TIMESTAMP WITH TIME ZONE,
    
    PRIMARY KEY (user_id, provider)
);

-- Tasks Table with breakdown support
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Core Fields
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deadline TIMESTAMP WITH TIME ZONE,
    priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    
    -- Status & Gamification
    status VARCHAR(20) DEFAULT 'pending', -- pending, scheduled, completed, missed
    points_value INTEGER DEFAULT 10,
    
    -- AI Context
    context_notes TEXT, -- "I prefer doing this in the morning"
    estimated_duration_minutes INTEGER,
    ai_reasoning TEXT, -- "Scheduled here because..."
    
    -- Hierarchy
    parent_task_id UUID REFERENCES tasks(id) ON DELETE CASCADE, -- For broken down tasks
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Calendar Events (Cache)
CREATE TABLE calendar_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    
    title VARCHAR(255),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    
    is_fixed BOOLEAN DEFAULT FALSE,
    source VARCHAR(20), -- local, google, outlook
    
    -- Partitioning key consideration for future scalability
    month_partition DATE GENERATED ALWAYS AS (DATE_TRUNC('month', start_time)) STORED
);
-- Note: Actual partitioning DDL omitted for MVP simplicity but recommended for Scale.

CREATE INDEX idx_tasks_status ON tasks(user_id, status);
CREATE INDEX idx_calendar_range ON calendar_events(user_id, start_time, end_time);
