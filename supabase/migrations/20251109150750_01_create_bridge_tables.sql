/*
  # Create DeltaChat-Matrix Bridge Tables

  1. New Tables
    - `bridge_config` - Bridge configuration and settings
    - `user_mappings` - Maps Matrix users to DeltaChat contacts
    - `room_mappings` - Maps Matrix rooms to DeltaChat groups
    - `bridge_messages` - Message history and relay status
    - `bridge_state` - Overall bridge operational state

  2. Security
    - Enable RLS on all tables
    - Policies restrict access appropriately
*/

CREATE TABLE IF NOT EXISTS bridge_config (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bridge_name text NOT NULL DEFAULT 'ribit-deltachat-matrix',
  matrix_homeserver text NOT NULL,
  matrix_username text NOT NULL,
  deltachat_email text NOT NULL,
  enabled boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  config_data jsonb DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS user_mappings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  matrix_user_id text NOT NULL,
  matrix_display_name text,
  deltachat_email text,
  deltachat_contact_id integer,
  bridge_id uuid NOT NULL REFERENCES bridge_config(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(matrix_user_id, bridge_id),
  UNIQUE(deltachat_email, bridge_id)
);

CREATE TABLE IF NOT EXISTS room_mappings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  matrix_room_id text NOT NULL,
  matrix_room_name text,
  deltachat_group_id integer,
  deltachat_group_name text,
  bridge_id uuid NOT NULL REFERENCES bridge_config(id) ON DELETE CASCADE,
  bidirectional boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(matrix_room_id, bridge_id),
  UNIQUE(deltachat_group_id, bridge_id)
);

CREATE TABLE IF NOT EXISTS bridge_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id text NOT NULL,
  source_platform text NOT NULL CHECK (source_platform IN ('matrix', 'deltachat')),
  target_platform text NOT NULL CHECK (target_platform IN ('matrix', 'deltachat')),
  sender_id text NOT NULL,
  sender_name text,
  message_text text NOT NULL,
  message_data jsonb DEFAULT '{}'::jsonb,
  relay_status text DEFAULT 'pending' CHECK (relay_status IN ('pending', 'sent', 'failed', 'deduped')),
  relay_error text,
  source_room_id text NOT NULL,
  target_room_id text NOT NULL,
  bridge_id uuid NOT NULL REFERENCES bridge_config(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  relayed_at timestamptz,
  UNIQUE(message_id, source_platform)
);

CREATE TABLE IF NOT EXISTS bridge_state (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bridge_id uuid NOT NULL REFERENCES bridge_config(id) ON DELETE CASCADE,
  matrix_connected boolean DEFAULT false,
  deltachat_connected boolean DEFAULT false,
  last_heartbeat timestamptz DEFAULT now(),
  error_count integer DEFAULT 0,
  total_messages_relayed integer DEFAULT 0,
  status text DEFAULT 'initializing' CHECK (status IN ('initializing', 'running', 'paused', 'error', 'disconnected')),
  status_message text,
  updated_at timestamptz DEFAULT now(),
  UNIQUE(bridge_id)
);

ALTER TABLE bridge_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE room_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE bridge_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE bridge_state ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read bridge config"
  ON bridge_config FOR SELECT
  USING (true);

CREATE POLICY "Allow service role manage bridge config"
  ON bridge_config FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read user mappings"
  ON user_mappings FOR SELECT
  USING (true);

CREATE POLICY "Allow service role manage user mappings"
  ON user_mappings FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read room mappings"
  ON room_mappings FOR SELECT
  USING (true);

CREATE POLICY "Allow service role manage room mappings"
  ON room_mappings FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read bridge messages"
  ON bridge_messages FOR SELECT
  USING (true);

CREATE POLICY "Allow service role manage bridge messages"
  ON bridge_messages FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public read bridge state"
  ON bridge_state FOR SELECT
  USING (true);

CREATE POLICY "Allow service role manage bridge state"
  ON bridge_state FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE INDEX idx_user_mappings_matrix_user ON user_mappings(matrix_user_id);
CREATE INDEX idx_user_mappings_deltachat_email ON user_mappings(deltachat_email);
CREATE INDEX idx_room_mappings_matrix_room ON room_mappings(matrix_room_id);
CREATE INDEX idx_room_mappings_deltachat_group ON room_mappings(deltachat_group_id);
CREATE INDEX idx_bridge_messages_source ON bridge_messages(source_platform, created_at DESC);
CREATE INDEX idx_bridge_messages_target ON bridge_messages(target_platform, relay_status);
CREATE INDEX idx_bridge_messages_relay_status ON bridge_messages(relay_status);
CREATE INDEX idx_bridge_state_bridge_id ON bridge_state(bridge_id);
