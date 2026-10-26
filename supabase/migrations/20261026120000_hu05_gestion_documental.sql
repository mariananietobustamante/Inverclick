-- HU05: gestión documental — metadatos en Postgres y archivos fuera del código fuente.
-- Evoluciona public.documents (si ya existía) y agrega document_id en users (CA3, CA4).

CREATE TABLE IF NOT EXISTS public.documents (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE SET NULL,
    name text NOT NULL,
    document_type text NOT NULL,
    location text NOT NULL,
    real_estate_id bigint REFERENCES public.real_estate(id) ON DELETE CASCADE,
    created_at timestamptz DEFAULT now() NOT NULL
);

ALTER TABLE public.documents
    ALTER COLUMN real_estate_id DROP NOT NULL;

ALTER TABLE public.documents
    ADD COLUMN IF NOT EXISTS user_id bigint,
    ADD COLUMN IF NOT EXISTS name text,
    ADD COLUMN IF NOT EXISTS location text;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'documents'
          AND column_name = 'path'
    ) THEN
        UPDATE public.documents
        SET location = path
        WHERE location IS NULL AND path IS NOT NULL;
    END IF;
END $$;

UPDATE public.documents
SET name = COALESCE(NULLIF(name, ''), 'documento')
WHERE name IS NULL OR name = '';

UPDATE public.documents
SET location = COALESCE(location, '')
WHERE location IS NULL;

ALTER TABLE public.documents
    ALTER COLUMN name SET NOT NULL,
    ALTER COLUMN location SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'documents_user_id_fkey'
    ) THEN
        ALTER TABLE public.documents
            ADD CONSTRAINT documents_user_id_fkey
            FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_documents_user ON public.documents USING btree (user_id);

ALTER TABLE public.users
    ADD COLUMN IF NOT EXISTS document_id bigint;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'users_document_id_fkey'
    ) THEN
        ALTER TABLE public.users
            ADD CONSTRAINT users_document_id_fkey
            FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE SET NULL;
    END IF;
END $$;
