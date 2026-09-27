


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";





SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."banks" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "agreement_state" "text",
    "swift" "text",
    "address" "text",
    "interest_rate" numeric(6,4),
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."banks" OWNER TO "postgres";


ALTER TABLE "public"."banks" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."banks_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."construction_companies" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "rating" numeric(3,2),
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    CONSTRAINT "construction_companies_rating_check" CHECK ((("rating" >= (0)::numeric) AND ("rating" <= (5)::numeric)))
);


ALTER TABLE "public"."construction_companies" OWNER TO "postgres";


ALTER TABLE "public"."construction_companies" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."construction_companies_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."construction_phases" (
    "id" bigint NOT NULL,
    "phase_number" integer NOT NULL,
    "name" "text" NOT NULL,
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."construction_phases" OWNER TO "postgres";


ALTER TABLE "public"."construction_phases" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."construction_phases_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."countries" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "iso_code" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."countries" OWNER TO "postgres";


ALTER TABLE "public"."countries" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."countries_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."currencies" (
    "id" bigint NOT NULL,
    "code" "text" NOT NULL,
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."currencies" OWNER TO "postgres";


ALTER TABLE "public"."currencies" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."currencies_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."documents" (
    "id" bigint NOT NULL,
    "real_estate_id" bigint NOT NULL,
    "document_type" "text" NOT NULL,
    "path" "text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."documents" OWNER TO "postgres";


ALTER TABLE "public"."documents" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."documents_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."id_types" (
    "id" bigint NOT NULL,
    "type" "text" NOT NULL,
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."id_types" OWNER TO "postgres";


ALTER TABLE "public"."id_types" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."id_types_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."lead_real_estate" (
    "lead_id" bigint NOT NULL,
    "real_estate_id" bigint NOT NULL
);


ALTER TABLE "public"."lead_real_estate" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."leads" (
    "id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "state" "text",
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."leads" OWNER TO "postgres";


ALTER TABLE "public"."leads" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."leads_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."num_prefix" (
    "id" bigint NOT NULL,
    "prefix" "text" NOT NULL,
    "country_id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."num_prefix" OWNER TO "postgres";


ALTER TABLE "public"."num_prefix" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."num_prefix_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."property_sold" (
    "id" bigint NOT NULL,
    "status" boolean DEFAULT true NOT NULL,
    "user_id" bigint NOT NULL,
    "bank_id" bigint,
    "real_estate_id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."property_sold" OWNER TO "postgres";


ALTER TABLE "public"."property_sold" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."property_sold_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."real_estate" (
    "id" bigint NOT NULL,
    "cost" numeric(14,2) NOT NULL,
    "description" "text",
    "address" "text",
    "zip_code" "text",
    "city" "text",
    "stock" integer DEFAULT 0 NOT NULL,
    "construction_company_id" bigint,
    "phase_id" bigint,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."real_estate" OWNER TO "postgres";


ALTER TABLE "public"."real_estate" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."real_estate_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."user_login" (
    "id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "password_hash" "text" NOT NULL,
    "is_active" boolean DEFAULT true NOT NULL,
    "last_login_at" timestamp with time zone,
    "failed_login_attempts" integer DEFAULT 0 NOT NULL,
    "refresh_token_hash" "text",
    "refresh_token_expires_at" timestamp with time zone,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."user_login" OWNER TO "postgres";


ALTER TABLE "public"."user_login" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."user_login_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."user_roles" (
    "id" bigint NOT NULL,
    "role" "text" NOT NULL,
    "modules" "text"[] DEFAULT '{}'::"text"[] NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL
);


ALTER TABLE "public"."user_roles" OWNER TO "postgres";


ALTER TABLE "public"."user_roles" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."user_roles_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."users" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "surname" "text",
    "address" "text",
    "zip_code" "text",
    "city" "text",
    "country_id" bigint,
    "prefix_id" bigint,
    "phone" "text",
    "email" "text" NOT NULL,
    "currency_id" bigint,
    "taxes" numeric(14,2),
    "income" numeric(14,2),
    "job" "text",
    "outcome" numeric(14,2),
    "id_type_id" bigint,
    "id_number" "text",
    "description" "text",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "role_id" bigint,
    "birth_date" "date"
);


ALTER TABLE "public"."users" OWNER TO "postgres";


ALTER TABLE "public"."users" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



ALTER TABLE ONLY "public"."banks"
    ADD CONSTRAINT "banks_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."construction_companies"
    ADD CONSTRAINT "construction_companies_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."construction_phases"
    ADD CONSTRAINT "construction_phases_phase_number_key" UNIQUE ("phase_number");



ALTER TABLE ONLY "public"."construction_phases"
    ADD CONSTRAINT "construction_phases_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."countries"
    ADD CONSTRAINT "countries_iso_code_key" UNIQUE ("iso_code");



ALTER TABLE ONLY "public"."countries"
    ADD CONSTRAINT "countries_name_key" UNIQUE ("name");



ALTER TABLE ONLY "public"."countries"
    ADD CONSTRAINT "countries_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."currencies"
    ADD CONSTRAINT "currencies_code_key" UNIQUE ("code");



ALTER TABLE ONLY "public"."currencies"
    ADD CONSTRAINT "currencies_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."documents"
    ADD CONSTRAINT "documents_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."id_types"
    ADD CONSTRAINT "id_types_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."lead_real_estate"
    ADD CONSTRAINT "lead_real_estate_pkey" PRIMARY KEY ("lead_id", "real_estate_id");



ALTER TABLE ONLY "public"."leads"
    ADD CONSTRAINT "leads_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."num_prefix"
    ADD CONSTRAINT "num_prefix_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."property_sold"
    ADD CONSTRAINT "property_sold_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."real_estate"
    ADD CONSTRAINT "real_estate_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_login"
    ADD CONSTRAINT "user_login_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_login"
    ADD CONSTRAINT "user_login_user_id_key" UNIQUE ("user_id");



ALTER TABLE ONLY "public"."user_roles"
    ADD CONSTRAINT "user_roles_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_roles"
    ADD CONSTRAINT "user_roles_role_key" UNIQUE ("role");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_email_key" UNIQUE ("email");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_id_number_key" UNIQUE ("id_number");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_documents_real_estate" ON "public"."documents" USING "btree" ("real_estate_id");



CREATE INDEX "idx_leads_user" ON "public"."leads" USING "btree" ("user_id");



CREATE INDEX "idx_num_prefix_country" ON "public"."num_prefix" USING "btree" ("country_id");



CREATE INDEX "idx_property_sold_bank" ON "public"."property_sold" USING "btree" ("bank_id");



CREATE INDEX "idx_property_sold_real_estate" ON "public"."property_sold" USING "btree" ("real_estate_id");



CREATE INDEX "idx_property_sold_user" ON "public"."property_sold" USING "btree" ("user_id");



CREATE INDEX "idx_real_estate_company" ON "public"."real_estate" USING "btree" ("construction_company_id");



CREATE INDEX "idx_real_estate_phase" ON "public"."real_estate" USING "btree" ("phase_id");



CREATE INDEX "idx_users_country" ON "public"."users" USING "btree" ("country_id");



CREATE INDEX "idx_users_currency" ON "public"."users" USING "btree" ("currency_id");



CREATE INDEX "idx_users_id_type" ON "public"."users" USING "btree" ("id_type_id");



CREATE INDEX "idx_users_prefix" ON "public"."users" USING "btree" ("prefix_id");



CREATE INDEX "idx_users_role" ON "public"."users" USING "btree" ("role_id");



ALTER TABLE ONLY "public"."documents"
    ADD CONSTRAINT "documents_real_estate_id_fkey" FOREIGN KEY ("real_estate_id") REFERENCES "public"."real_estate"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."lead_real_estate"
    ADD CONSTRAINT "lead_real_estate_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "public"."leads"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."lead_real_estate"
    ADD CONSTRAINT "lead_real_estate_real_estate_id_fkey" FOREIGN KEY ("real_estate_id") REFERENCES "public"."real_estate"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."leads"
    ADD CONSTRAINT "leads_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."num_prefix"
    ADD CONSTRAINT "num_prefix_country_id_fkey" FOREIGN KEY ("country_id") REFERENCES "public"."countries"("id") ON DELETE RESTRICT;



ALTER TABLE ONLY "public"."property_sold"
    ADD CONSTRAINT "property_sold_bank_id_fkey" FOREIGN KEY ("bank_id") REFERENCES "public"."banks"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."property_sold"
    ADD CONSTRAINT "property_sold_real_estate_id_fkey" FOREIGN KEY ("real_estate_id") REFERENCES "public"."real_estate"("id") ON DELETE RESTRICT;



ALTER TABLE ONLY "public"."property_sold"
    ADD CONSTRAINT "property_sold_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE RESTRICT;



ALTER TABLE ONLY "public"."real_estate"
    ADD CONSTRAINT "real_estate_construction_company_id_fkey" FOREIGN KEY ("construction_company_id") REFERENCES "public"."construction_companies"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."real_estate"
    ADD CONSTRAINT "real_estate_phase_id_fkey" FOREIGN KEY ("phase_id") REFERENCES "public"."construction_phases"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."user_login"
    ADD CONSTRAINT "user_login_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_country_id_fkey" FOREIGN KEY ("country_id") REFERENCES "public"."countries"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_currency_id_fkey" FOREIGN KEY ("currency_id") REFERENCES "public"."currencies"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_id_type_id_fkey" FOREIGN KEY ("id_type_id") REFERENCES "public"."id_types"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_prefix_id_fkey" FOREIGN KEY ("prefix_id") REFERENCES "public"."num_prefix"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."user_roles"("id") ON DELETE SET NULL;



CREATE POLICY "Public read - construction_companies" ON "public"."construction_companies" FOR SELECT USING (true);



CREATE POLICY "Public read - construction_phases" ON "public"."construction_phases" FOR SELECT USING (true);



CREATE POLICY "Public read - countries" ON "public"."countries" FOR SELECT USING (true);



CREATE POLICY "Public read - currencies" ON "public"."currencies" FOR SELECT USING (true);



CREATE POLICY "Public read - id_types" ON "public"."id_types" FOR SELECT USING (true);



CREATE POLICY "Public read - num_prefix" ON "public"."num_prefix" FOR SELECT USING (true);



CREATE POLICY "Public read - real_estate" ON "public"."real_estate" FOR SELECT USING (true);



ALTER TABLE "public"."banks" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."construction_companies" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."construction_phases" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."countries" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."currencies" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."documents" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."id_types" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."lead_real_estate" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."leads" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."num_prefix" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."property_sold" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."real_estate" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."user_login" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."user_roles" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;




ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";





































































































































































GRANT ALL ON TABLE "public"."banks" TO "anon";
GRANT ALL ON TABLE "public"."banks" TO "authenticated";
GRANT ALL ON TABLE "public"."banks" TO "service_role";



GRANT ALL ON SEQUENCE "public"."banks_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."banks_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."banks_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."construction_companies" TO "anon";
GRANT ALL ON TABLE "public"."construction_companies" TO "authenticated";
GRANT ALL ON TABLE "public"."construction_companies" TO "service_role";



GRANT ALL ON SEQUENCE "public"."construction_companies_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."construction_companies_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."construction_companies_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."construction_phases" TO "anon";
GRANT ALL ON TABLE "public"."construction_phases" TO "authenticated";
GRANT ALL ON TABLE "public"."construction_phases" TO "service_role";



GRANT ALL ON SEQUENCE "public"."construction_phases_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."construction_phases_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."construction_phases_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."countries" TO "anon";
GRANT ALL ON TABLE "public"."countries" TO "authenticated";
GRANT ALL ON TABLE "public"."countries" TO "service_role";



GRANT ALL ON SEQUENCE "public"."countries_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."countries_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."countries_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."currencies" TO "anon";
GRANT ALL ON TABLE "public"."currencies" TO "authenticated";
GRANT ALL ON TABLE "public"."currencies" TO "service_role";



GRANT ALL ON SEQUENCE "public"."currencies_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."currencies_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."currencies_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."documents" TO "anon";
GRANT ALL ON TABLE "public"."documents" TO "authenticated";
GRANT ALL ON TABLE "public"."documents" TO "service_role";



GRANT ALL ON SEQUENCE "public"."documents_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."documents_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."documents_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."id_types" TO "anon";
GRANT ALL ON TABLE "public"."id_types" TO "authenticated";
GRANT ALL ON TABLE "public"."id_types" TO "service_role";



GRANT ALL ON SEQUENCE "public"."id_types_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."id_types_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."id_types_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."lead_real_estate" TO "anon";
GRANT ALL ON TABLE "public"."lead_real_estate" TO "authenticated";
GRANT ALL ON TABLE "public"."lead_real_estate" TO "service_role";



GRANT ALL ON TABLE "public"."leads" TO "anon";
GRANT ALL ON TABLE "public"."leads" TO "authenticated";
GRANT ALL ON TABLE "public"."leads" TO "service_role";



GRANT ALL ON SEQUENCE "public"."leads_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."leads_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."leads_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."num_prefix" TO "anon";
GRANT ALL ON TABLE "public"."num_prefix" TO "authenticated";
GRANT ALL ON TABLE "public"."num_prefix" TO "service_role";



GRANT ALL ON SEQUENCE "public"."num_prefix_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."num_prefix_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."num_prefix_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."property_sold" TO "anon";
GRANT ALL ON TABLE "public"."property_sold" TO "authenticated";
GRANT ALL ON TABLE "public"."property_sold" TO "service_role";



GRANT ALL ON SEQUENCE "public"."property_sold_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."property_sold_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."property_sold_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."real_estate" TO "anon";
GRANT ALL ON TABLE "public"."real_estate" TO "authenticated";
GRANT ALL ON TABLE "public"."real_estate" TO "service_role";



GRANT ALL ON SEQUENCE "public"."real_estate_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."real_estate_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."real_estate_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."user_login" TO "anon";
GRANT ALL ON TABLE "public"."user_login" TO "authenticated";
GRANT ALL ON TABLE "public"."user_login" TO "service_role";



GRANT ALL ON SEQUENCE "public"."user_login_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."user_login_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."user_login_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."user_roles" TO "anon";
GRANT ALL ON TABLE "public"."user_roles" TO "authenticated";
GRANT ALL ON TABLE "public"."user_roles" TO "service_role";



GRANT ALL ON SEQUENCE "public"."user_roles_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."user_roles_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."user_roles_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."users" TO "anon";
GRANT ALL ON TABLE "public"."users" TO "authenticated";
GRANT ALL ON TABLE "public"."users" TO "service_role";



GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";































