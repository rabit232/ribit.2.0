/*
  # Create Word Learning and Perspective System Tables

  1. New Tables
    - `learned_words` - Words learned from conversations with context
    - `word_relationships` - Relationships between words (follows, precedes, pairs)
    - `sentence_patterns` - Grammar and sentence construction patterns
    - `perspective_analyses` - Large text analyses with learned insights
    - `personality_traits` - Evolving personality based on learned content
    - `opinion_history` - Historical opinions and reasoning

  2. Functions
    - learn_word() - Add or update learned word
    - get_word_stats() - Get vocabulary statistics
    - get_personality_summary() - Get personality overview

  3. Security
    - RLS enabled on all tables
    - Service role for bot operations
    - Authenticated read access
*/

-- Learned words table with comprehensive context
CREATE TABLE IF NOT EXISTS learned_words (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  word text NOT NULL,
  word_normalized text NOT NULL,
  count integer DEFAULT 1,
  first_seen timestamptz DEFAULT now(),
  last_seen timestamptz DEFAULT now(),
  contexts jsonb DEFAULT '[]'::jsonb,
  example_sentences text[],
  positions text[],
  part_of_speech text,
  sentiment text DEFAULT 'neutral',
  emotional_weight real DEFAULT 0.0,
  follows_words jsonb DEFAULT '{}'::jsonb,
  precedes_words jsonb DEFAULT '{}'::jsonb,
  learned_from_user text,
  learned_from_room text,
  learned_from_perspective boolean DEFAULT false,
  importance_score real DEFAULT 1.0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(word_normalized)
);

-- Word relationships and patterns
CREATE TABLE IF NOT EXISTS word_relationships (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  relationship_type text NOT NULL CHECK (relationship_type IN ('pair', 'triplet', 'sequence', 'pattern')),
  words text[] NOT NULL,
  words_normalized text[] NOT NULL,
  occurrence_count integer DEFAULT 1,
  last_used timestamptz DEFAULT now(),
  example_contexts text[],
  pattern_signature text,
  coherence_score real DEFAULT 0.5,
  naturalness_score real DEFAULT 0.5,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(relationship_type, words_normalized)
);

-- Sentence construction patterns
CREATE TABLE IF NOT EXISTS sentence_patterns (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_type text NOT NULL,
  pattern_structure text NOT NULL,
  example_sentences text[],
  usage_count integer DEFAULT 1,
  tense text,
  voice text,
  mood text,
  complexity_score real DEFAULT 0.5,
  effectiveness_score real DEFAULT 0.5,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(pattern_structure)
);

-- Perspective analyses for large text chunks
CREATE TABLE IF NOT EXISTS perspective_analyses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id text NOT NULL,
  room_id text NOT NULL,
  message_id text,
  original_text text NOT NULL,
  text_hash text NOT NULL,
  text_size_bytes integer NOT NULL,
  word_count integer NOT NULL,
  main_topics text[],
  key_concepts text[],
  sentiment_analysis jsonb,
  emotional_content jsonb,
  interesting_score real DEFAULT 0.5,
  words_learned integer DEFAULT 0,
  patterns_extracted integer DEFAULT 0,
  opinions_formed text[],
  personality_updates jsonb DEFAULT '{}'::jsonb,
  bot_opinion text,
  bot_reasoning text,
  found_interesting boolean DEFAULT false,
  integrated_to_personality boolean DEFAULT false,
  processing_time_ms integer,
  llm_provider text,
  analysis_version text DEFAULT '1.0',
  created_at timestamptz DEFAULT now(),
  UNIQUE(text_hash)
);

-- Evolving personality traits
CREATE TABLE IF NOT EXISTS personality_traits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  trait_name text NOT NULL,
  trait_category text NOT NULL,
  trait_description text NOT NULL,
  strength real DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
  confidence real DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
  learned_from_source text,
  learned_from_id uuid,
  first_formed timestamptz DEFAULT now(),
  last_reinforced timestamptz DEFAULT now(),
  reinforcement_count integer DEFAULT 1,
  contexts_used text[],
  compatible_traits uuid[],
  conflicting_traits uuid[],
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(trait_name, trait_category)
);

-- Opinion history and reasoning
CREATE TABLE IF NOT EXISTS opinion_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  topic text NOT NULL,
  question text NOT NULL,
  question_hash text NOT NULL,
  opinion_text text NOT NULL,
  reasoning text NOT NULL,
  confidence_level real DEFAULT 0.5,
  user_id text NOT NULL,
  room_id text NOT NULL,
  conversation_context jsonb DEFAULT '{}'::jsonb,
  related_words text[],
  related_perspectives uuid[],
  influenced_by_traits uuid[],
  is_current boolean DEFAULT true,
  superseded_by uuid REFERENCES opinion_history(id),
  llm_provider text,
  formed_at timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE learned_words ENABLE ROW LEVEL SECURITY;
ALTER TABLE word_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE sentence_patterns ENABLE ROW LEVEL SECURITY;
ALTER TABLE perspective_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE personality_traits ENABLE ROW LEVEL SECURITY;
ALTER TABLE opinion_history ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Service role manage learned words" ON learned_words FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read learned words" ON learned_words FOR SELECT TO authenticated USING (true);

CREATE POLICY "Service role manage word relationships" ON word_relationships FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read word relationships" ON word_relationships FOR SELECT TO authenticated USING (true);

CREATE POLICY "Service role manage sentence patterns" ON sentence_patterns FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read sentence patterns" ON sentence_patterns FOR SELECT TO authenticated USING (true);

CREATE POLICY "Service role manage perspective analyses" ON perspective_analyses FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read own analyses" ON perspective_analyses FOR SELECT TO authenticated USING (user_id = (SELECT auth.uid()::text));

CREATE POLICY "Service role manage personality traits" ON personality_traits FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read personality traits" ON personality_traits FOR SELECT TO authenticated USING (true);

CREATE POLICY "Service role manage opinion history" ON opinion_history FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Authenticated read opinion history" ON opinion_history FOR SELECT TO authenticated USING (true);

-- Performance Indexes
CREATE INDEX idx_learned_words_normalized ON learned_words(word_normalized);
CREATE INDEX idx_learned_words_count ON learned_words(count DESC);
CREATE INDEX idx_learned_words_importance ON learned_words(importance_score DESC);
CREATE INDEX idx_word_relationships_type ON word_relationships(relationship_type);
CREATE INDEX idx_word_relationships_count ON word_relationships(occurrence_count DESC);
CREATE INDEX idx_perspective_analyses_interesting ON perspective_analyses(found_interesting) WHERE found_interesting = true;
CREATE INDEX idx_personality_traits_active ON personality_traits(is_active) WHERE is_active = true;
CREATE INDEX idx_opinion_history_current ON opinion_history(is_current) WHERE is_current = true;

-- Full-text search
CREATE INDEX idx_learned_words_fts ON learned_words USING gin(to_tsvector('english', word || ' ' || COALESCE(array_to_string(example_sentences, ' '), '')));
CREATE INDEX idx_perspective_analyses_fts ON perspective_analyses USING gin(to_tsvector('english', original_text));

-- Helper Functions
CREATE OR REPLACE FUNCTION learn_word(
  p_word text,
  p_context jsonb DEFAULT NULL,
  p_example text DEFAULT NULL,
  p_user_id text DEFAULT NULL,
  p_room_id text DEFAULT NULL
)
RETURNS uuid
LANGUAGE plpgsql
AS $$
DECLARE
  v_word_id uuid;
BEGIN
  INSERT INTO learned_words (word, word_normalized, count, last_seen, contexts, example_sentences, learned_from_user, learned_from_room)
  VALUES (p_word, lower(p_word), 1, now(), COALESCE(jsonb_build_array(p_context), '[]'::jsonb),
          CASE WHEN p_example IS NOT NULL THEN ARRAY[p_example] ELSE '{}' END, p_user_id, p_room_id)
  ON CONFLICT (word_normalized) DO UPDATE SET
    count = learned_words.count + 1,
    last_seen = now(),
    contexts = learned_words.contexts || jsonb_build_array(p_context),
    example_sentences = array_append(learned_words.example_sentences, p_example),
    updated_at = now()
  RETURNING id INTO v_word_id;
  RETURN v_word_id;
END;
$$;

CREATE OR REPLACE FUNCTION get_word_stats()
RETURNS jsonb
LANGUAGE plpgsql
AS $$
DECLARE
  v_stats jsonb;
BEGIN
  SELECT jsonb_build_object(
    'total_words', COUNT(*),
    'total_occurrences', SUM(count),
    'average_occurrences', AVG(count),
    'most_common', (SELECT jsonb_agg(jsonb_build_object('word', word, 'count', count))
                    FROM (SELECT word, count FROM learned_words ORDER BY count DESC LIMIT 10) top),
    'recently_learned', (SELECT jsonb_agg(jsonb_build_object('word', word, 'learned_at', created_at))
                         FROM (SELECT word, created_at FROM learned_words ORDER BY created_at DESC LIMIT 10) recent)
  ) INTO v_stats FROM learned_words;
  RETURN v_stats;
END;
$$;

CREATE OR REPLACE FUNCTION get_personality_summary()
RETURNS jsonb
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN (
    SELECT jsonb_build_object(
      'total_traits', COUNT(*),
      'active_traits', COUNT(*) FILTER (WHERE is_active),
      'strongest_traits', (SELECT jsonb_agg(jsonb_build_object('name', trait_name, 'strength', strength, 'category', trait_category))
                           FROM (SELECT trait_name, strength, trait_category FROM personality_traits
                                 WHERE is_active ORDER BY strength DESC LIMIT 5) top)
    ) FROM personality_traits
  );
END;
$$;
