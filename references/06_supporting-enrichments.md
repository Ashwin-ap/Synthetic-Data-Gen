# Supporting Enrichments — Files 03 & 04
## Extracted from `references/03_source-data-profile.md` and `references/04_domain-context.md`

**Generated:** 2026-04-17  
**Purpose:** Collect all columns, distributions, and behavioural parameters suggested by files 03 and 04 that do NOT contradict `references/02_data-mapping-reference.md` (the ground truth). Each section flags compatibility status explicitly.

---

## Conflict-Check Legend

| Status | Meaning |
|--------|---------|
| ✅ Compatible | No contradiction with file 02 — safe to use |
| ⚠️ Tension | Values differ from file 02 in magnitude; file 02 takes precedence for the primary distribution; SCF/domain values usable for stratification |
| ❌ Conflict | Directly contradicts file 02 — do NOT use; file 02 value applies |

---

## Part A — Demographic Distributions (Source: file 03)

These distributions populate `INDIVIDUAL` (Core_DB), `INDIVIDUAL_MARITAL_STATUS`, `INDIVIDUAL_OCCUPATION`, `CDM_DB.INDIVIDUAL`, and `PARTY_SEGMENT` records. File 02 does not specify population-level distributions for these columns, so all are **✅ Compatible**.

### A1. Age (`INDIVIDUAL.Birth_Dt` / `CDM_DB.INDIVIDUAL.Birth_Dt`)

Derive birth year from: `survey_year (2022) − AGE`. Use SCF age-class distribution as generation prior.

| AGECL | Age Range | % of Customers |
|-------|-----------|---------------|
| 1 | < 35 | 13.3% |
| 2 | 35–44 | 16.6% |
| 3 | 45–54 | 17.8% |
| 4 | 55–64 | 22.3% |
| 5 | 65–74 | 18.8% |
| 6 | 75+ | 11.0% |

SCF continuous stats: Mean=54, Median=56, P25=42, P75=67. File 01 specifies range 1940-01-01 to 2005-12-31 (age 20–85) — use this hard cap; AGECL 6 maps to ages 75–82.

### A2. Gender (`INDIVIDUAL.Gender_Type_Cd`)

SCF reference-person variable (HHSEX); use as individual-level prior for retail-bank customers:

| Code | Value | % |
|------|-------|---|
| MALE | Male | 76.1% |
| FEMALE | Female | 23.9% |

**Note:** SCF HHSEX over-represents males because it records the reference person of a household (the male in mixed-sex couples). For a customer-level model the actual split is closer to 50/50 for individuals. Consider using 50% M / 50% F for `INDIVIDUAL.Gender_Type_Cd` as a more neutral default unless the architect explicitly wants the SCF reference-person skew.

### A3. Marital Status (`INDIVIDUAL_MARITAL_STATUS.Marital_Status_Cd`)

| Code | Meaning | % |
|------|---------|---|
| MARRIED | Married / living as partners | 63.2% |
| SINGLE | Not married / not partnered | 36.8% |

### A4. Number of Children / Dependents (`PARTY_DEMOGRAPHIC` — "Number of Dependents" demographic)

| Kids | % |
|------|---|
| 0 | 60.2% |
| 1 | 17.8% |
| 2 | 13.9% |
| 3+ | 8.1% |

Used in product-holdings Maslow hierarchy (file 04 Section 2): product type is primarily determined by age and number of dependents.

### A5. Education (`INDIVIDUAL_OCCUPATION.Individual_Job_Title_Txt` proxy)

SCF EDCL maps to occupation title text:

| EDCL | Label | % |
|------|-------|---|
| 1 | No high school diploma | 9.3% |
| 2 | HS diploma or GED | 19.7% |
| 3 | Some college (incl. associate's) | 21.5% |
| 4 | College degree (bachelor's or higher) | 49.5% |

### A6. Race / Ethnicity (`INDIVIDUAL.Ethnicity_Type_Cd`)

SCF RACECL5 → FSDM code mapping (file 03 Generator Notes):

| RACECL5 | SCF Label | Ethnicity_Type_Cd | % |
|---------|-----------|-------------------|---|
| 1 | White non-Hispanic | WHITE | 59.7% |
| 2 | Black/African Am. | BLACK | 13.4% |
| 3 | Hispanic / Latino | HISPANIC | 11.5% |
| 4 | Asian | ASIAN | 7.3% |
| 5 | Other / Multiple | OTHER | 8.0% |

### A7. Occupation (`INDIVIDUAL_OCCUPATION.Occupation_Type_Cd`)

SCF OCCAT1 → Occupation_Type_Cd mapping:

| OCCAT1 | Label | Occupation_Type_Cd | % |
|--------|-------|--------------------|---|
| 1 | Work for someone else | EMP | 49.6% |
| 2 | Self-employed | SELF_EMP | 21.7% |
| 3 | Retired / not working | RETIRED | 24.8% |
| 4 | Other not working | NOT_WORKING | 3.9% |

Managerial / Professional sub-type (OCCAT2=1): 41.0%. Technical/Sales/Service (OCCAT2=2): 16.6%.

### A8. Family Structure → Household Composition (`CDM_DB.HOUSEHOLD`, `INDIVIDUAL_TO_HOUSEHOLD`)

Use LIFECL (6-level) for household construction:

| LIFECL | Label | % |
|--------|-------|---|
| 1 | Single, age < 55 | 11.5% |
| 2 | Couple, < 55, no kids | 8.2% |
| 3 | Any household with children, < 55 | 21.4% |
| 4 | Couple, 55+, still working | 6.7% |
| 5 | Couple, 55+, not working | 29.1% |
| 6 | Single, 55+ | 23.1% |

---

## Part B — Account Ownership Rates (Source: file 03)

These rates control whether to generate specific `AGREEMENT` sub-type records per customer. File 02 does not prescribe prevalence rates → **✅ Compatible** for all except the 90% checking rate which is already resolved in file 02 Open Question #3.

| Account Type | FSDM Agreement Sub-type | Ownership Rate |
|---|---|---|
| Checking account | DEPOSIT_AGREEMENT (checking sub-type) | **90.0%** ← resolved in file 02 Q3 |
| Savings account | DEPOSIT_AGREEMENT (savings sub-type) | 48.4% |
| Money market deposit | DEPOSIT_AGREEMENT (MMA sub-type) | 20.0% |
| Certificate of deposit | DEPOSIT_TERM_AGREEMENT | 7.8% |
| Retirement account (IRA/401k) | DEPOSIT_AGREEMENT or LOAN_TERM_AGREEMENT | 59.1% |
| Primary mortgage | MORTGAGE_AGREEMENT | 39.6% |
| Credit card with revolving balance | CREDIT_CARD_AGREEMENT | 37.8% |
| Vehicle installment loan | LOAN_TERM_AGREEMENT (auto sub-type) | 30.3% |
| Student loan | LOAN_TERM_AGREEMENT (education sub-type) | 17.7% |
| HELOC | CREDIT_AGREEMENT (HELOC) | 3.4% |
| Payday loan | LOAN_TRANSACTION_AGREEMENT | 1.9% |
| Business equity (passive) | ORGANIZATION + BUSINESS + AGREEMENT | ~6% of non-self-employed |

Banking status breakdown:
- Fully unbanked (no checking): **10.0%** → 10% of generated customers have no DEPOSIT_AGREEMENT
- Has checking but no savings/MMA ("underbanked"): **~36.5%**
- Has checking AND savings: **45.6%**

Internet access (proxy for digital channel preference):
- Has internet (INTERNET=1): **89.7%** → use to set `PARTY_CONTACT_PREFERENCE.Channel_Type_Cd` = ONLINE / MOBILE as preferred

---

## Part C — Financial Amount Ranges by Segment (Source: file 03)

### C1. Checking Account Balance — ⚠️ Tension with file 02

**File 02 (WP5 ground truth):** Average Deposit Balance — Mean $2,000; P10 $10; P90 $30,000; negatives OK.  
**File 03 (SCF 2022):** Median (banked) $6,000; Mean (banked) $123,786; P25 $1,260; P75 $28,500; P90 $120,000+.

**Resolution:** The WP5 "Average Deposit Balance" is a Feature Store aggregate metric across ALL customers (including the 10% unbanked at $0 and computed as a monthly average, not point-in-time). The SCF values are point-in-time balances among account holders only. Use **WP5 parameters as the target Feature Store distribution**. Use **SCF stratified ranges below for per-account `AGREEMENT_FEATURE.Agreement_Feature_Amt` generation** on individual deposit agreements (these are not in conflict — they operate at different levels of abstraction):

| Income Quartile (INCQRTCAT) | `AGREEMENT_FEATURE.Agreement_Feature_Amt` Range | Median |
|---|---|---|
| Q1 (bottom 25%) | $0–$5,000 | $350 |
| Q2 (25–50th pct) | $100–$20,000 | $1,600 |
| Q3 (50–75th pct) | $500–$50,000 | $4,000 |
| Q4 (top 25%) | $2,000–$500,000 | $23,000 |
| Overall (banked customers) | P10 $220; P75 $28,500; P95 $280,000 | $6,000 |

### C2. Savings Account Balance — ✅ Compatible

| Income Quartile | Range | Median if Have |
|---|---|---|
| Q1 | $1–$12,000 | ~$1,000 |
| Q2 | $1–$30,000 | ~$3,000 |
| Q3 | $100–$70,000 | ~$5,000 |
| Q4 | $1,000–$500,000 | ~$25,000 |
| % with savings | — | 48.4% |

### C3. Credit Card Revolving Balance — ✅ Compatible

**File 02 (WP5):** Mean $2,500; P10 $100; P90 $20,000; no negatives.  
**File 03 (SCF):** Mean (all) $2,506; P95 $13,079. These are extremely close — no contradiction.

Additional stratification useful for generation:

| Income Quartile | % Carrying Balance | Median if Carry | Max |
|---|---|---|---|
| Q1 (bottom 20%) | 35% | $1,200 | $10,000 |
| Q2 (20–40th pct) | 50% | $1,700 | $15,000 |
| Q3 (40–60th pct) | 57% | $3,000 | $20,000 |
| Q4 (top 25%) | 24% | $5,600 | $139,000 (cap) |

Only 37.8% of customers carry a revolving balance; 62.2% pay in full. Generate `CREDIT_CARD_AGREEMENT` records for all 37.8%; `Credit_Agreement_Past_Due_Amt` for revolvers.

### C4. Mortgage Balance — ✅ Compatible

| Age Group | Typical Range | Median if Have |
|---|---|---|
| Under 35 | $50K–$500K | $194,000 |
| 35–44 | $80K–$700K | $242,000 |
| 45–54 | $50K–$800K | $240,000 |
| 55–64 | $30K–$600K | $197,000 |
| 65–74 | $10K–$400K | $150,000 |
| 75+ | $5K–$300K | $130,000 |

Overall distribution: P10 $46K; P25 $100K; P50 $200K; P75 $403K; P90 $800K; P95 $1.3M.

Mortgage interest rates by origination year (use for `AGREEMENT_RATE.Agreement_Rate`):
- Pre-2020 origination: 3.5%–4.5%
- 2020 origination: ~3.0%
- 2021 origination: ~3.1%
- 2022 origination (new purchase): 5.0%–7.0%

Mortgage terms: 15–30 year fixed or ARM. Auto loans: 3–5 year term. Student loans: 10–25 year term.

### C5. Retirement Account (IRA / 401k) Balances — ⚠️ Tension with file 02

**File 02 (WP5):** Total Investments AUM: Mean $75,000; P10 $5,000; P90 $100,000; no negatives.  
**File 03 (SCF):** % with any retirement account = 59.1%; median (all customers) $18,000; P75 $350,000; mean $593,054.

**Interpretation of tension:** WP5 P10=$5,000 with "no negatives" implies ALL customers in the feature set have ≥$5,000 AUM. SCF shows ~41% of the population holds zero retirement/investment assets. Resolution: the WP5 distribution applies only to **customers who hold investment accounts** (the ~59–63% with positive AUM). The remaining ~40% have AUM=0 and are excluded from this feature (or stored as NULL/0). Do not generate investment agreement records for the 40% non-holding cohort.

Retirement account balances by age (among holders):

| AGECL | % Holding | Median if Held |
|-------|-----------|---------------|
| < 35 | 45.1% | $18,190 |
| 35–44 | 57.4% | $60,000 |
| 45–54 | 63.8% | $185,000 |
| 55–64 | 64.6% | $530,500 |
| 65–74 | 62.1% | $555,000 |
| 75+ | 54.8% | $500,000 |

### C6. Vehicle Loan Balance — ✅ Compatible

30.3% of customers hold vehicle installment loans.
- Mean (all): $27,929; P95 $39,000.
- `LOAN_TERM_AGREEMENT.Original_Loan_Amt` range: $5,000–$80,000 (vehicles); standard term 3–5 years.

### C7. Income — ⚠️ Tension with file 02

**File 02 (WP5):** Imputed Monthly Income: Mean $4,500; P10 $0; P90 $25,000; no negatives.  
**File 03 (SCF):** Annual median $94,039; annual P25 $42,156; annual P75 $264,823 (= monthly $3,513 / $22,069).

**Resolution:** WP5 monthly mean of $4,500 ($54,000/year) is approximately the 40th percentile of SCF annual income. This is plausible for a retail bank customer universe (skewed toward middle-income vs. SCF's over-representation of high-wealth households). **Use WP5 for the Feature Store `Imputed Monthly Income` distribution.** Use SCF income-by-occupation ranges for `PARTY_DEMOGRAPHIC.Demographic_Val` ("Reported Income" dimension):

| Occupation | Annual Range | Median |
|---|---|---|
| Employed (OCCAT1=1) | $24,000–$450,000 | $91,878 |
| Self-employed (OCCAT1=2) | $30,000–$5,000,000 | $385,886 |
| Retired (OCCAT1=3) | $12,000–$500,000 | $58,369 |
| Not working (OCCAT1=4) | $10,000–$150,000 | $31,346 |
| Managerial/Professional | $60,000–$600,000 | $119,981 |
| Technical/Sales/Service | $25,000–$200,000 | $58,369 |

### C8. Net Worth (for `PARTY_SCORE.Party_Score_Val` and `CDM_DB.PARTY_SEGMENT`) — ✅ Compatible

File 02 does not specify NW distribution. Use SCF:

| NW Percentile | Value |
|---|---|
| P25 | ~$36,000 |
| P50 | ~$384,500 |
| P75 | ~$2,476,105 |
| P90 | ~$21,517,800 |

NWCAT → `CDM_DB.PARTY_SEGMENT.Segment_Value_Cd` mapping:
- NWCAT=1 (bottom 25%) → Segment_Value_Cd=1–2
- NWCAT=2 (25–50th pct) → Segment_Value_Cd=3–4
- NWCAT=3 (50–75th pct) → Segment_Value_Cd=5–6
- NWCAT=4 (75–90th pct) → Segment_Value_Cd=7–8
- NWCAT=5 (top 10%) → Segment_Value_Cd=9–10

### C9. Debt-to-Income and Delinquency Rates — ✅ Compatible

Used to control `AGREEMENT_STATUS` past-due records and `Credit_Agreement_Past_Due_Amt > 0`:

| Metric | Rate | FSDM Target |
|---|---|---|
| Late payment in past year (LATE=1) | **11.2%** | `AGREEMENT_STATUS` with `Agreement_Status_Scheme_Cd='Past Due Status'` |
| 60+ day late (LATE60=1) | **4.6%** | Same — severe past-due code |
| Applied for credit and turned down | 8.8% | Low `Credit_Report_Score_Num` (300–580 range) |
| Feared denial (did not apply) | 12.1% | Low FICO proxy |
| Bankruptcy in past 5 years | **1.1%** | `PARTY_STATUS.Party_Status_Cd` = 'BANKRUPT' |
| Foreclosure in past 5 years | **0.4%** | `MORTGAGE_AGREEMENT` closed with foreclosure status |
| Payday loan usage | 1.9% | `LOAN_TRANSACTION_AGREEMENT` |
| Negative net worth (NETWORTH < 0) | 6.9% | Customers with large mortgage + little equity |

---

## Part D — Mandatory Correlation Rules (Source: file 03)

These are structural constraints the generator MUST respect to avoid implausible synthetic records. File 02 does not address these; all are **✅ Compatible**.

### D1. Age vs. Account Types

| Rule | Detail |
|---|---|
| Under 35 | Lower mortgage rate (23.7%); higher student loan rate; lower retirement balances ($18K median); more likely unbanked |
| Peak earning (45–64) | Highest mortgage rate (47–53%); peak 401k/IRA contributions; median mortgage balance $240K |
| Older (65+) | Declining mortgage rate (23–33%); high retirement balances ($500K+ median); more likely to hold CDs |
| **Enforcement:** HMRTHEL probability peaks at AGECL=3; retirement account rate peaks at AGECL=4–5 |

### D2. Income vs. Asset Amounts

| Rule | Detail |
|---|---|
| Income ↑ → checking balance ↑ | Q4 median $23K vs Q1 $350 (66× difference) |
| Income ↑ → retirement account ownership ↑ | 90% of top 10% vs 13% of bottom 20% |
| Income ↑ → CC revolving balance probability ↓ | Top 25%: only 24% carry balance (pay in full) |
| **Generate asset amounts conditional on income bracket** |

### D3. Age × Income → Net Worth (Not Income Alone)

| Rule | Detail |
|---|---|
| Young high earners | High income + large mortgage + student loans → lower net worth despite income |
| Older retired | Lower income but accumulated net worth (mortgage paid down) |
| LIFECL=3 (families with kids) | Income median $124K but NW only $250K due to debt |
| **Do NOT derive NW solely from income; model NW as age × income interaction** |

### D4. Occupation vs. Income Variance

| Rule | Detail |
|---|---|
| Self-employed | Much higher income variance (median $386K but with extreme tail; long right tail) |
| Employed | Moderate median, narrower spread |
| Self-employed → HBUS=1 | Business equity records required |

### D5. Race/Ethnicity vs. Financial Access

| Race | Credit Denial Rate | Payday Loan Rate | Checking Penetration |
|---|---|---|---|
| White non-Hispanic | 5.9% | Low | High |
| Black/African Am. | 16.9% | Higher | ~90% (lower) |
| Hispanic/Latino | 11.3% | Moderate | ~90% (lower) |
| Other/Multiple | 11.3% | Moderate | — |

**Must preserve these disparities for realistic synthetic data.** Map to lower `Credit_Report_Score_Num` ranges and higher `AGREEMENT_STATUS` past-due rates for credit-constrained cohorts.

### D6. Debt-to-Income by Age

| Age Group | Approximate DTI | Generator Rule |
|---|---|---|
| Under 35 | ~44% | High mortgage + student loan generation |
| 35–44 | ~26% | Mortgage still building; student loans declining |
| 55–64 | ~9% | Mortgage mostly paid; minimal new debt |
| 75+ | ~2% | Near debt-free; few new agreements |

---

## Part E — SCF Variable → FSDM Column Mapping (Source: file 03, Generator Notes)

These are confirmed mappings from file 03 that are consistent with file 02 transformation rules. All **✅ Compatible**.

| SCF Variable | FSDM Table | FSDM Column | Notes |
|---|---|---|---|
| AGE | INDIVIDUAL (Core_DB) | Birth_Dt | survey_year (2022) − AGE |
| HHSEX | INDIVIDUAL | Gender_Type_Cd | 1=Male→'MALE', 2=Female→'FEMALE' |
| MARRIED | INDIVIDUAL_MARITAL_STATUS | Marital_Status_Cd | 1='MARRIED', 2='SINGLE' |
| RACECL5 | INDIVIDUAL | Ethnicity_Type_Cd | Map: 1=WHITE, 2=BLACK, 3=HISPANIC, 4=ASIAN, 5=OTHER |
| OCCAT1/OCCAT2 | INDIVIDUAL_OCCUPATION | Occupation_Type_Cd | Map: 1=EMP, 2=SELF_EMP, 3=RETIRED, 4=NOT_WORKING |
| LF=1 | ASSOCIATE_EMPLOYMENT | Employment_Start_Dt | Active employment record |
| KIDS | PARTY_DEMOGRAPHIC | Demographic_Val | Number of dependents demographic value |
| FAMSTRUCT/LIFECL | HOUSEHOLD + INDIVIDUAL_TO_HOUSEHOLD | (household composition) | LIFECL preferred (6 levels) |
| HCHECK=1 | DEPOSIT_AGREEMENT | (presence) | Generate checking AGREEMENT if HCHECK=1 |
| CHECKING | AGREEMENT_FEATURE | Agreement_Feature_Amt | Checking balance — see Part C1 stratification |
| HSAVING=1 | DEPOSIT_AGREEMENT | (savings sub-type) | Generate if HSAVING=1 |
| SAVING | AGREEMENT_FEATURE | Agreement_Feature_Amt | Savings balance |
| HMMA=1 | DEPOSIT_AGREEMENT | (MMA sub-type) | Generate if HMMA=1 |
| HCDS=1 | DEPOSIT_TERM_AGREEMENT | (CD) | Generate if HCDS=1 |
| HRETQLIQ=1 | DEPOSIT_AGREEMENT / LOAN_TERM_AGREEMENT | (retirement sub-type) | IRA / 401k |
| IRAKH | AGREEMENT_FEATURE | Agreement_Feature_Amt | IRA balance |
| THRIFT | AGREEMENT_FEATURE | Agreement_Feature_Amt | 401k / thrift balance |
| HMRTHEL=1 | MORTGAGE_AGREEMENT | (mortgage) | Generate if HMRTHEL=1 |
| MRTHEL | LOAN_TERM_AGREEMENT | Original_Loan_Amt | Mortgage outstanding balance |
| HCCBAL=1 | CREDIT_CARD_AGREEMENT | (CC) | Generate if HCCBAL=1 |
| CCBAL | CREDIT_AGREEMENT | Credit_Agreement_Past_Due_Amt | Revolving balance |
| HVEH_INST=1 | LOAN_TERM_AGREEMENT | (auto loan) | Generate if HVEH_INST=1 |
| VEH_INST | LOAN_TERM_AGREEMENT | Original_Loan_Amt | Vehicle loan balance |
| HEDN_INST=1 | LOAN_TERM_AGREEMENT | (student loan) | Generate if HEDN_INST=1 |
| EDN_INST | LOAN_TERM_AGREEMENT | Original_Loan_Amt | Student loan balance |
| HHELOC=1 | CREDIT_AGREEMENT | (HELOC) | Generate if HHELOC=1 |
| HELOC | CREDIT_AGREEMENT | Credit_Agreement_Past_Due_Amt | HELOC drawn balance |
| LATE / LATE60 | AGREEMENT_STATUS | Agreement_Status_Cd (past-due scheme) | 11.2% / 4.6% delinquency rates |
| BNKRUPLAST5 | PARTY_STATUS | Party_Status_Cd | 1.1% rate |
| FORECLLAST5 | MORTGAGE_AGREEMENT | Agreement_Status_Cd (closed-foreclosed) | 0.4% rate |
| INCOME | PARTY_DEMOGRAPHIC | Demographic_Val | "Reported Income" demographic dimension |
| NETWORTH | PARTY_SCORE | Party_Score_Val | NW-derived segment score (normalised) |
| NWCAT | CDM_DB.PARTY_SEGMENT | Segment_Value_Cd | NW category → CLV/Risk segment decile |
| INCCAT | CDM_DB.PARTY_SEGMENT | Segment_Value_Cd | Income category segment |
| INTERNET=1 | PARTY_CONTACT_PREFERENCE | Channel_Type_Cd=3(ONLINE)/4(MOBILE) | 89.7% with internet → digital channel preference |

---

## Part F — Customer Segment Proportions and Behavioural Profiles (Source: file 04)

All **✅ Compatible** with file 02 (which defines the Feature Store features but not the generation proportions).

### F1. Customer Value Segments (90-10 Rule)

| Segment | % of Customers | % of Profit | Characteristics |
|---|---|---|---|
| High-value (top CLV decile) | ~10% | ~90% | Multi-product (4–8), high balances, heavy digital, long tenure, low attrition probability |
| Mid-value (deciles 5–9) | ~40% | ~10% | Moderate product breadth, mixed channel, some stealth attrition signals |
| Near-zero / negative value (deciles 1–4) | ~50% | ~0% or negative | 1–2 products, low balances, physical channel or inactive |

### F2. Behavioural Correlations for Generation

| Attribute | High-CLV Customers | Low-CLV Customers |
|---|---|---|
| Product count | 4–8 products | 1–2 products |
| Checking account | Always present | May be absent |
| Digital channel usage | High frequency, varied tasks | Low or none |
| Payment instruments | Multiple (debit, ACH, credit, P2P) | 1–2 instruments |
| Monthly deposit balance | High, growing | Low, flat or declining |
| Tenure | Long (5+ years) | Short or recently opened |
| Fee waiver eligibility | Often meets minimum balance | Often below threshold |
| Attrition signal | None | Declining activity, fewer products |

### F3. Product Holdings by Age (Maslow Hierarchy)

Product type is primarily determined by age and number of dependents:

| Life Stage | Primary Products |
|---|---|
| Young / single (<35, LIFECL=1–2) | Checking + savings (possibly credit card, student loan) |
| Mid-life / family (35–54, LIFECL=3) | Add mortgage, vehicle loan |
| Older / established (55+, LIFECL=4–6) | Add retirement accounts, investments, insurance |

Multi-product customers (4+ products) are a minority (~10–15%) but the high-value segment.  
Single-product customers represent the majority (~40–50%) but contribute near-zero profit.

### F4. Population Composition — ✅ Compatible, resolved in file 02 Q10

| Party Type | % | Source |
|---|---|---|
| Individual (retail) | 80% | file 04 Open Q1 resolution |
| Organization (small business / commercial) | 20% | file 04 Open Q1 resolution |

Business customers may not hold retirement/mortgage products; they hold commercial lending and business checking.

---

## Part G — Attrition Patterns (Source: file 04)

All **✅ Compatible** with file 02 (Layer 1 tables, not out-of-scope Layer 2 facts).

### G1. Attrition Model Parameters

| Parameter | Value | FSDM Implication |
|---|---|---|
| Performance window | 6 months | All generated history spans 4–6 months |
| Attrition rate | **5%** of customers close all accounts within 6-month window | `AGREEMENT.Agreement_Close_Dttm` set within window |
| Attrition definition | Binary: ALL accounts closed | `CDM_DB.PARTY.Party_Lifecycle_Phase_Cd` → 3 (if churned, use status record) |
| Stealth attrition | Declining product/channel activity in months preceding full attrition | Visible in `PARTY_INTERRACTION_EVENT` event frequency decline |
| Attrition decile | Assign each customer score 1–10; decile 1 = highest attrition risk | `CDM_DB.PARTY_SEGMENT.Segment_Type_Cd=1(CLV)`, Segment_Value_Cd=attrition decile |

### G2. Customer Cohorts to Generate

| Cohort | % | Description |
|---|---|---|
| Active / stable | 55% | All accounts open; growing or steady activity |
| Declining (stealth attrition) | 30% | Products and channel activity declining; accounts still open at end of window |
| Churned (full attrition) | 5% | All accounts closed within 6-month window |
| Newly acquired | 10% | Account open date within last 2 months of window |

### G3. Deposit Balance Trajectory

Generate monthly balance snapshots (not just point-in-time) to reflect trajectory across the 4–6 month history window. Store via monthly `AGREEMENT_FEATURE` records with date-range columns:

- Active customers: flat or slowly growing deposit balances
- Stealth-attrition customers: declining balances (draw-down pattern)
- Churned customers: balances reaching $0 before `Agreement_Close_Dttm`

---

## Part H — Financial Generation Parameters (Source: file 04)

All **✅ Compatible** unless noted.

### H1. Net Interest Margin (NIM) Reference Values

Used for plausibility checks on `AGREEMENT_RATE` and `FINANCIAL_EVENT` amounts:

| Product | NIM Range |
|---|---|
| Loan (e.g., 3-year, 4.55% rate) | ~1.25% NIM per position |
| Deposit (e.g., 1-year, 1.15% rate) | ~0.95% NIM per position |
| Combined bank NIM | ~3.40% |

Formula: `AGREEMENT_RATE.Agreement_Rate` should be set such that the spread above cost-of-funds is in the 0.95%–1.25% range per product.

### H2. Channel Cost Benchmark

Used for plausibility of `PARTY_INTERRACTION_EVENT` frequency:
- Average telephony contact rate per checking customer: **~1 per month**
- Unit cost of call-center contact: **~$5**
- Digital channel: lower cost per interaction (implied; no explicit dollar figure from white paper)

### H3. Fee Types

Both types must appear in `FINANCIAL_EVENT` / transaction records:

| Fee Type | Frequency | FSDM Column |
|---|---|---|
| Recurring (monthly statement fee) | Monthly per account | `FINANCIAL_EVENT` with `Financial_Event_Type_Cd='STATEMENT_FEE'`; `In_Out_Direction_Type_Cd='OUT'` |
| Intermittent (overdraft fee) | Activity-driven; when balance < 0 | `FINANCIAL_EVENT` with overdraft type code |

Fee waiver logic: assessed fees may be reversed if account meets waiver conditions (e.g., minimum balance threshold). Store both assessed and collected amounts separately in `FINANCIAL_EVENT_AMOUNT`.

### H4. Customer Tenure Distribution — ✅ Compatible with file 02

**File 02 (WP5):** Customer Tenure (years): Mean 3.5; P10 0.5; P90 25; no negatives.

Additional context from file 04:
- Retention barrier products (direct deposit, online bill pay) → lower attrition probability; generate `SERVICE` flag records for these.
- Account tenure should be indexed to `AGREEMENT.Agreement_Open_Dttm` — accurate open dates required for loan loss allocation.
- New acquisition cohort should have tenure < 0.5 years (within P10 boundary).
- High-value customers: tenure 5+ years (above WP5 mean of 3.5).

### H5. CLV Planning Parameters (informational; Layer 2+ out of scope for MVP)

| Parameter | Value |
|---|---|
| Planning horizon | 5 years |
| Maximum horizon | 25 years |
| Discount rate | Bank's target return on equity (Feature Store constant) |
| ~55% of customers change CLV decile year-over-year | Do not assign static CLV scores; allow score drift |

These feed WP7-9 end data products (out of scope for MVP Layer 1 generator) but inform realistic `PARTY_SCORE.Party_Score_Val` generation (numeric probability strings, not static labels).

---

## Part I — Special SCF Patterns Relevant to Generation (Source: file 03, Missed on First Pass)

### I1. Mortgage Interest Rate Vintages — ✅ Compatible

For `AGREEMENT_RATE.Agreement_Rate` on `MORTGAGE_AGREEMENT` records:

| Origination Year | Rate Range |
|---|---|
| Pre-2020 | 3.5%–4.5% |
| 2020 | ~3.0% |
| 2021 | ~3.1% |
| 2022 (purchase) | 5.0%–7.0% |
| 2022 (refinance existing) | 3.5%–5.5% |

### I2. Emergency Borrowing and Financial Stress — ✅ Compatible

9.1% of customers borrowed for emergencies. Among those:
- Family/friends: most common
- Credit card: second
- Alternative lender (payday/pawn): rare (higher in NWCAT=1)
- Formal lender: ~20%

Use delinquency rates (LATE=11.2%, LATE60=4.6%) as the calibration target for `AGREEMENT_STATUS` past-due records, NOT the broader emergency-postponement rate (20–30%).

### I3. Stock and Equity Ownership — ✅ Compatible

- Direct stocks (HSTOCKS): 29.1%; heavily income-concentrated (7% bottom 20% vs 56% top 10%)
- Any equity (direct + retirement + funds): ~63%
- Mean transaction account balance by age: Under 35 $20.5K → 65–74 $100.2K → 75+ $82.8K

### I4. Debt Composition

Useful for `AGREEMENT` sub-type allocation:
- Primary mortgage dominates total debt (~75% of total debt dollars)
- Installment loans ~10%
- Credit card ~3.5%
- Other residential debt ~8%

### I5. Total Monthly Debt Payment

TPAY (total monthly debt payments) — median = $576/month among those with any debt. Useful as plausibility check on `FUNDS_TRANSFER_EVENT` amounts representing debt service.

---

## Part J — Default Generation Parameters (Source: file 04, Open Questions)

Resolved values that are safe to use as generator defaults (no conflicting specification in file 02 or file 05):

| Parameter | Default Value | Source |
|---|---|---|
| Individual / Organization split | 80% Individual, 20% Organization | file 04 Q1 |
| Target attrition rate | 5% of customers within 6-month window | file 04 Q2 |
| Checking account penetration | 90% | file 04 Q3 / SCF / file 02 Q3 |
| Target record volume | 5,000 agreements, ~3,000 unique customers | file 04 Q8 |
| History window | 4–6 months | files 04 and 02 |
| Generate churned customers | Yes — 5% with `Agreement_Close_Dttm` in window | file 04 Q9 |
| Product hierarchy grouping | 8 CLV types: Checking, Savings, Retirement, Credit Card, Vehicle Loan, Mortgage, Investments, Insurance | file 04 Q10 / file 02 Q8 |
| CDM address PK | `CDM_Address_Id` (surrogate BIGINT, added to DDL) | file 05 Q6 |

---

## Part K — Additional Behavioural Patterns (Source: file 04, Missed on First Pass)

### K1. Services as Retention Barriers

Direct deposit and online bill pay are "pull barrier" services with high switching costs. Generate `PRODUCT_FEATURE` or `AGREEMENT_FEATURE` service enrollment records for these two services and correlate with lower attrition probability:

- Direct deposit enrolled → `SERVICE` flag on checking `AGREEMENT`
- Online bill pay enrolled → `SERVICE` flag on checking `AGREEMENT`
- Both enrolled → lowest attrition probability bucket

### K2. Digital Migration Signal Cohort

Include a cohort (~3–5% of customers) showing the pattern: digital channel adoption event → declining balances or eventual account closure. Relevant for journey analytics downstream. Generate `PARTY_INTERRACTION_EVENT` records: digital channel events increase, then balance declines, then `AGREEMENT.Agreement_Close_Dttm` is set.

### K3. Customer Equity at Acquisition

Newly acquired customers should have product depth consistent with prior acquisition cohorts. Do not randomly assign product bundles to new customers; model product assignment from Maslow hierarchy (Part F3) conditional on age and number of dependents.

### K4. Fee Waiver Logic

Generate both assessed-fee and collected-fee values. Fee waiver condition: monthly checking balance exceeds minimum balance threshold (suggested: $1,500 for consumer accounts). Store in `FINANCIAL_EVENT_AMOUNT`:
- `Financial_Event_Amt` = assessed fee
- Additional amount field = collected/reversed amount (0 if waived)

---

## Summary: Conflicts with File 02

Only two genuine tensions identified between files 03/04 and file 02 (WP5 Feature Store distributions):

| Feature | File 02 (WP5) | File 03 (SCF) | Resolution |
|---|---|---|---|
| Average Deposit Balance | Mean $2,000; P10 $10; P90 $30,000 | Median (banked) $6,000; mean $123,786 | Use WP5 for Feature Store metric; use SCF per-account stratified ranges for `AGREEMENT_FEATURE.Agreement_Feature_Amt` |
| Total Investments AUM | P10 $5,000 (implies all customers have investments) | 59% hold any retirement/investment account | WP5 distribution applies to investment-holding customers only (~59–63%); remaining customers have AUM=0 / no investment AGREEMENT |

All other enrichments in this file are compatible with file 02 and can be used directly in generator design.
