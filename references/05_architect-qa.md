# Project Context & Architect Q&A

## Project Context

- Current MVP scope is just Layer 1 (iDM, MDM)
- Refer `references/02_data-mapping-reference.md` to understand the transformation rules that will be applied in Layer 2. Layer 2 is out of scope. But the data generated in Layer 1 must be made such that these transformation rules can be easily applied on them.
- `references/03_source-data-profile` and `references/04_domain-context` are just for reference — Main files are the Excel (`references/02_data-mapping-reference.md`) and the SQL files (`references/01_schema-reference.md`) — Do not modify the data in that. You may add more to it from 03 only after letting me know why and how.
- Date high value format: `9999-12-31`
- Output needed is in CSV format
- Check if the distributions given in `references/03_source-data-profile` and `references/04_domain-context.md` clash with the existing distributions in `references/02_data-mapping-reference.md`
- Add the below three columns in all FSDM tables and generate data for them:
  - `di_start_ts` — Date from when Record is active
  - `di_end_ts` — Date till which Record is active (if currently active, use high date `9999-12-31`)
  - `di_rec_deleted_Ind` — `Y` means mark the record for deletion, `N` means Record is active and needs to be maintained

---

## Q&A

**Q1. Cross-Schema Type Mismatch: AGREEMENT (Core_DB) vs CDM_DB consumers**
File: `Core_DB.sql`
`Agreement_Id` in `Core_DB.AGREEMENT` is INTEGER.
`Agreement_Id` in `CDM_DB.PARTY_TO_AGREEMENT_ROLE`, `CDM_DB.ADDRESS_TO_AGREEMENT` and `CDM_DB.CONTACT_TO_AGREEMENT` is BIGINT.
Which one to consider?

**Answer:** Wherever this problem arises choosing between INTEGER and BIGINT — always choose BIGINT.

---

**Q2. Error in Core_DB.EVENT & Core_DB.COMPLAINT_EVENT**
File: `Core_DB_customized.sql`
Same column name `Event_Id`, same PRIMARY INDEX — but INTEGER in EVENT, BIGINT in COMPLAINT_EVENT.
Which one to consider?

**Answer:** Always consider BIGINT. Change its datatype from INTEGER to BIGINT. No additional work needed.

---

**Q3. Sample values for `PIM_DB.PRODUCT_GROUP` — recursive parent relationship**
`Product_Group_Id` is the PK and `Parent_Group_Id` is also BIGINT NOT NULL. The Excel (WP4 MDM sheet) shows examples like Consumer Lending containing Card, Installment, and Mortgage as child groups.
Does `Parent_Group_Id` point back to `Product_Group_Id` on the same table? And what value should top-level groups like Consumer Lending have in `Parent_Group_Id` since the DDL declares it NOT NULL?

**Answer:** Yes, this is a RECURSIVE relationship (`parent_group_id` points to `Product_Group_Id` on the same table). Refer to the image/diagram provided for the hierarchy. Top-level (root) groups point to themselves in `Parent_Group_Id`.

---

**Q4. Is Core_DB_customized a separate Teradata database?**
In `Core_DB_customized.sql`, all 8 tables are declared as `Core_DB.<table>` — same database name as `Core_DB.sql`. Is `Core_DB_customized` actually a separate Teradata database, or are these tables physically part of Core_DB?

**Answer:** `Core_DB_customized` is not a different database. It is Core_DB itself. The file was named customized to indicate these are additions to the standard FSDM model.

---

**Q5. Date tracking columns — di vs Valid, timestamp format, and di metadata columns**

a. The CDM_DB and PIM_DB tables have two sets of date-tracking columns — `Valid_From_Dt`/`Valid_To_Dt`/`Del_Ind` (NOT NULL) and `di_start_ts`/`di_end_ts`/`di_rec_deleted_Ind` (NULL). Should the generator populate both sets? If yes, should they hold the same date values or do they serve different purposes?

b. The DDL declares `di_start_ts` and `di_end_ts` as TIMESTAMP(6) NULL on every table, but the design document treats them as DATE NOT NULL with an active sentinel of `9999-12-31`. Should the generator write full timestamps (e.g. `9999-12-31 00:00:00.000000`) or just dates (`9999-12-31`)? And since the DDL allows NULL — should some rows have empty values in these columns?

c. Should `di_data_src_cd` and `di_proc_name` be included in the generated CSVs? If yes, what values should they have?

**Answer:** Both `di` and `Valid` columns are needed — history is stored in `di`. `di_data_src_cd` and `di_proc_name` — keep null if needed.

---

**Q6. ADDRESS entity — CDM_Party_Id vs CDM_Address_Id**
In the WP4 MDM Excel sheet, the ADDRESS entity lists CDM Party ID as a column. But in `CDM_DB.sql`, the ADDRESS table has no `CDM_Party_Id` column. Which is correct — should ADDRESS directly have a party foreign key, or is the link between parties and addresses only through the `ADDRESS_TO_AGREEMENT` bridge table?

**Answer:** `cdm_party_id` — need to generate a surrogate key. In the Excel there is a typo. It is not CDM Party ID, it is `CDM_Address_ID` (PK) and this is missing from the `.sql` file. Add it to the DDL.

---

**Q7. INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING — Business_Party_Id placeholder for self-employed individuals**
Tables: `Core_DB.INDIVIDUAL_PAY_TIMING`, `Core_DB.INDIVIDUAL_BONUS_TIMING`
Both tables have `Business_Party_Id INTEGER NOT NULL` — an FK to `ORGANIZATION`. Self-employed individuals (~21.7% of the individual population) have no real employer org, so a direct FK reference would fail for this cohort.

**Answer:** INDIVIDUAL_PAY_TIMING and INDIVIDUAL_BONUS_TIMING are in scope (iDM target type in CIF_FSDM_Mapping_MASTER.xlsx). Both have Business_Party_Id NOT NULL with FK to ORGANIZATION. Since self-employed individuals (~21.7%) have no real employer org, the generator inserts one reserved placeholder row in the ORGANIZATION CSV — 'Self-Employment Organization' with reserved ID 9999999. All self-employed individuals in these two tables point Business_Party_Id to this reserved ID. No schema changes, no new columns, no new tables.