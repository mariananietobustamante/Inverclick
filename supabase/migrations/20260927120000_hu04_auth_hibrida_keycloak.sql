-- HU04: Autenticación híbrida (Keycloak / SSO)
-- - password_hash opcional para usuarios solo-SSO
-- - trazabilidad de proveedor e ID externo
-- - usuarios existentes quedan marcados como origen local

ALTER TABLE public.user_login
    ALTER COLUMN password_hash DROP NOT NULL;

ALTER TABLE public.user_login
    ADD COLUMN IF NOT EXISTS auth_provider text NOT NULL DEFAULT 'local',
    ADD COLUMN IF NOT EXISTS external_id text;

COMMENT ON COLUMN public.user_login.auth_provider IS
    'Proveedor de identidad: local | keycloak';
COMMENT ON COLUMN public.user_login.external_id IS
    'Subject (sub) del IdP externo (Keycloak). NULL para cuentas solo locales.';

UPDATE public.user_login
SET auth_provider = 'local'
WHERE auth_provider IS NULL OR auth_provider = '';

CREATE UNIQUE INDEX IF NOT EXISTS user_login_external_id_key
    ON public.user_login (external_id)
    WHERE external_id IS NOT NULL;
