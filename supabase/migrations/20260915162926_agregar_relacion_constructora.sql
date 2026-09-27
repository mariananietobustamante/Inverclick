ALTER TABLE users
ADD COLUMN construction_company_id int8 REFERENCES construction_companies(id);
