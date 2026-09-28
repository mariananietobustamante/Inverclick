## Table `banks`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `name` | `text` |  |
| `agreement_state` | `text` |  Nullable |
| `swift` | `text` |  Nullable |
| `address` | `text` |  Nullable |
| `interest_rate` | `numeric` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `construction_companies`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `name` | `text` |  |
| `rating` | `numeric` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `construction_phases`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `phase_number` | `int4` |  Unique |
| `name` | `text` |  |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `countries`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `name` | `text` |  Unique |
| `iso_code` | `text` |  Nullable Unique |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `currencies`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `code` | `text` |  Unique |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `documents`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `real_estate_id` | `int8` |  |
| `document_type` | `text` |  |
| `path` | `text` |  |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `id_types`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `type` | `text` |  |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `lead_real_estate`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `lead_id` | `int8` | Primary |
| `real_estate_id` | `int8` | Primary |

## Table `leads`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `int8` |  |
| `state` | `text` |  Nullable |
| `description` | `text` |  Nullable |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `num_prefix`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `prefix` | `text` |  |
| `country_id` | `int8` |  |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `property_sold`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `int8` |  |
| `bank_id` | `int8` |  Nullable |
| `real_estate_id` | `int8` |  |
| `status` | `bool` |  |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `real_estate`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `name` | `text` |  Unique |
| `cost` | `numeric` |  |
| `description` | `text` |  Nullable |
| `zip_code` | `text` |  Nullable |
| `city` | `text` |  Nullable |
| `phase_id` | `int8` |  Nullable |
| `stock` | `int4` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `construction_company_id` | `int8` |  |
| `id` | `int8` | Primary Identity |
| `address` | `text` |  Unique |

## Table `user_login`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `user_id` | `int8` |  Unique |
| `password_hash` | `text` |  |
| `last_login_at` | `timestamptz` |  Nullable |
| `refresh_token_hash` | `text` |  Nullable |
| `refresh_token_expires_at` | `timestamptz` |  Nullable |
| `is_active` | `bool` |  |
| `failed_login_attempts` | `int4` |  |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `user_roles`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `role` | `text` |  Unique |
| `modules` | `_text` |  |
| `created_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |

## Table `users`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `name` | `text` |  |
| `surname` | `text` |  Nullable |
| `address` | `text` |  Nullable |
| `zip_code` | `text` |  Nullable |
| `city` | `text` |  Nullable |
| `country_id` | `int8` |  Nullable |
| `prefix_id` | `int8` |  Nullable |
| `phone` | `text` |  Nullable |
| `email` | `text` |  Unique |
| `currency_id` | `int8` |  Nullable |
| `taxes` | `numeric` |  Nullable |
| `income` | `numeric` |  Nullable |
| `job` | `text` |  Nullable |
| `outcome` | `numeric` |  Nullable |
| `id_type_id` | `int8` |  Nullable |
| `id_number` | `text` |  Nullable Unique |
| `description` | `text` |  Nullable |
| `role_id` | `int8` |  Nullable |
| `birth_date` | `date` |  Nullable |
| `created_at` | `timestamptz` |  |
| `updated_at` | `timestamptz` |  |
| `id` | `int8` | Primary Identity |
| `construction_company_id` | `int8` |  Nullable |

## RLS Policies

### `real_estate`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - real_estate` | SELECT | public | PERMISSIVE | `true` | — |

### `construction_companies`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - construction_companies` | SELECT | public | PERMISSIVE | `true` | — |

### `construction_phases`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - construction_phases` | SELECT | public | PERMISSIVE | `true` | — |

### `countries`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - countries` | SELECT | public | PERMISSIVE | `true` | — |

### `currencies`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - currencies` | SELECT | public | PERMISSIVE | `true` | — |

### `id_types`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - id_types` | SELECT | public | PERMISSIVE | `true` | — |

### `num_prefix`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Public read - num_prefix` | SELECT | public | PERMISSIVE | `true` | — |

