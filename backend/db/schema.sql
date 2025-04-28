CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";

CREATE TABLE users (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  auth0_sub    TEXT UNIQUE NOT NULL,
  name         TEXT NOT NULL,
  email        CITEXT UNIQUE,
  avatar_url   TEXT,
  created_at   TIMESTAMPTZ DEFAULT now(),
  updated_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE workspaces (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id     UUID REFERENCES users(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE projects (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  color        TEXT,
  sort_order   INT DEFAULT 0,
  is_archived  BOOLEAN DEFAULT FALSE,
  created_at   TIMESTAMPTZ DEFAULT now(),
  updated_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TYPE task_status AS ENUM ('TODO','DOING','DONE');

CREATE TABLE tasks (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id      UUID REFERENCES projects(id) ON DELETE CASCADE,
  parent_task_id  UUID REFERENCES tasks(id) ON DELETE CASCADE,
  title           TEXT NOT NULL,
  description     TEXT,
  status          task_status DEFAULT 'TODO',
  priority        SMALLINT CHECK (priority BETWEEN 1 AND 4) DEFAULT 4,
  due_date        DATE,
  start_date      DATE,
  completed_at    TIMESTAMPTZ,
  created_by      UUID REFERENCES users(id),
  assigned_to     UUID REFERENCES users(id),
  is_recurring    BOOLEAN DEFAULT FALSE,
  recurrence_rule TEXT,
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE labels (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  color        TEXT
);

CREATE TABLE task_labels (
  task_id  UUID REFERENCES tasks(id) ON DELETE CASCADE,
  label_id UUID REFERENCES labels(id) ON DELETE CASCADE,
  PRIMARY KEY (task_id, label_id)
);

CREATE TABLE comments (
  id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_id   UUID REFERENCES tasks(id) ON DELETE CASCADE,
  author_id UUID REFERENCES users(id),
  body      TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  edited_at  TIMESTAMPTZ
);

CREATE TYPE reminder_channel AS ENUM ('PUSH','EMAIL','WEB');

CREATE TABLE reminders (
  id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_id   UUID REFERENCES tasks(id) ON DELETE CASCADE,
  user_id   UUID REFERENCES users(id) ON DELETE CASCADE,
  remind_at TIMESTAMPTZ NOT NULL,
  channel   reminder_channel DEFAULT 'PUSH'
);

CREATE TABLE activity_log (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_type TEXT NOT NULL,
  entity_id   UUID NOT NULL,
  action      TEXT NOT NULL,
  actor_id    UUID REFERENCES users(id),
  payload     JSONB,
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- Índices útiles
CREATE INDEX idx_tasks_project_status ON tasks(project_id,status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_comments_task ON comments(task_id);
