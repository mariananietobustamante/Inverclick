-- HU03: trazabilidad de ventas (agente + lead) y tabla de logs de auditoría.

ALTER TABLE public.property_sold
    ADD COLUMN IF NOT EXISTS agent_id bigint,
    ADD COLUMN IF NOT EXISTS lead_id bigint;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'property_sold_agent_id_fkey'
    ) THEN
        ALTER TABLE public.property_sold
            ADD CONSTRAINT property_sold_agent_id_fkey
            FOREIGN KEY (agent_id) REFERENCES public.users(id) ON DELETE RESTRICT;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'property_sold_lead_id_fkey'
    ) THEN
        ALTER TABLE public.property_sold
            ADD CONSTRAINT property_sold_lead_id_fkey
            FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE RESTRICT;
    END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS property_sold_one_active_sale
    ON public.property_sold (real_estate_id)
    WHERE status = true;

CREATE TABLE IF NOT EXISTS public.audit_logs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint REFERENCES public.users(id) ON DELETE SET NULL,
    action text NOT NULL,
    route text NOT NULL,
    created_at timestamptz DEFAULT now() NOT NULL
);
