# Tanzanian water pump notebook review

## Result

The notebook's saved calculations reproduce exactly after the input paths change.
The attribute table needs corrections and 21 additional rows.
The class counts, reported missing percentages, and listed pandas data types are correct under pandas 2.2.3.

The source contains 59,400 rows and 40 columns: one identifier and 39 potential predictors.
The label file contains 59,400 rows and two columns.
The merge contains 59,400 rows and 41 columns, including the target.

Both ID columns are unique and non-null. Their sets and row order match.
The original merge loses no records and creates no extra records for these files.

## Execution evidence

The original notebook contains three cells: two code cells and one Markdown cell.
The code uses no IPython-specific syntax.
I execute both code cells in order in one fresh Python namespace.

- Environment: Python 3.12.14, pandas 2.2.3, NumPy 2.3.5.
- Unchanged execution fails in cell 1 because `/content/data/tanzanian-data/WaterPumps.csv` does not exist here.
- Replacing only `/content/data/tanzanian-data/` with the attachment directory allows both code cells to finish.
- Reproduced text output matches both original saved outputs exactly.
- The corrected notebook's five code cells also execute successfully in order.
- Execution uses Python directly, with captured output. It does not launch a Jupyter kernel.

`reproduction_log.txt` records the outputs, environment, input SHA-256 hashes, and verification results.
The original notebook contains no model, validation split, predictions, or performance metrics.
This review therefore does not establish predictive accuracy.

## Code corrections

| Original location | Finding | Precise correction |
|---|---|---|
| Cell 1 and cell 3: CSV loading | Absolute Colab paths prevent execution in this environment. | Use `DATA_DIR = Path('.')` and load both CSV files from that directory. |
| Cell 3: `pd.merge(df, labels_df, on='id')` | The default inner merge has no alignment checks. It works correctly on these files. | Check non-null, unique IDs and equal ID sets. Use `how='left', validate='one_to_one'`. Check row count and target nulls afterward. |
| Cell 3: `info_df.head(15)` | Output shows only 15 of 41 columns. This hides omitted missing-data problems. | Print `info_df.to_string()` to include every column. |
| Cell 3: `value_value_counts` | The method name is wrong. The `hasattr` guard selects the valid fallback, so this causes no current failure. | Replace the whole conditional expression with `full_df['status_group'].value_counts(dropna=False)`. |
| Cell 3: target fallback | A fallback can conceal an unexpected label schema. The supplied target name is known. | Validate that the label columns are `id` and `status_group`. Use the target directly. |

Unused NumPy imports and unused path variables are minor cleanup items. They do not change the results.

## Exact summary corrections

Replace “40 features + 1 target” with “39 potential predictors, one identifier, and one target after merging.”
The source CSV has 40 columns because it includes `id`.

Keep the original target counts and percentages:

| Target | Count | Percent |
|---|---:|---:|
| `functional` | 32,259 | 54.31% |
| `non functional` | 22,824 | 38.42% |
| `functional needs repair` | 4,317 | 7.27% |

Keep the exact label `functional needs repair`. The PDF states that these waterpoints remain operational.
The shorter phrase “Needs Repair” can obscure that distinction.

## Every original attribute row

The original table contains 20 rows: 19 source columns and the target.
All listed pandas data types match default parsing in the reproduced environment.
The semantic classifications are acceptable, with the clarifications below.

| Attribute | Verdict and precise correction |
|---|---|
| `id` | Correct: `int64`, unique identifier, zero parsed nulls. There are 59,400 unique IDs. One ID is zero; this is not evidence of missing data. Prefer “nominal identifier” for its semantic type. |
| `amount_tsh` | Keep `float64` and continuous measurement. Keep the PDF definition, “total static head.” There are 41,639 zeros (70.10%). The table's “may represent missing data” is a hypothesis. The later claim that zeros are highly likely placeholders is unsupported. The PDF gives no units or missing-value rule. |
| `date_recorded` | Keep raw dtype `object`. Use “temporal date, day resolution.” All dates parse with `%m/%d/%Y`; there are no failures. The range is 2002-10-14 through 2013-12-03. Replace “format consistency needs verification” with these results. |
| `funder` | Keep `object`, nominal, 3,637 parsed nulls, and 6.12%. These nulls comprise 3,635 blank fields and two literal `None` values. Also report 777 literal `0` values and four `Unknown` values. Do not classify all similar names as proven misspellings. |
| `gps_height` | Keep `int64` storage and continuous measurement. There are 20,438 zeros and 1,496 negative values. The range is -90 to 2,770. Non-positive altitude does not establish noise or missingness. The coordinate argument does not apply to altitude. |
| `installer` | Keep `object`, nominal, 3,655 nulls, and 6.15%. Also report 777 literal `0` values, four case-insensitive `unknown` values, and three hyphens. `DWE` occurs 17,402 times and `Dwe` occurs three times. This supports a normalization review, not automatic organization matching. |
| `longitude` | Correct dtype, type, and description. Add the 1,812 zero count (3.05%). Each zero pairs with latitude -0.00000002. Flag these coordinates for review. |
| `latitude` | Correct dtype and continuous type. Quantify the near-zero value: -0.00000002 appears 1,812 times. There are no exact zeros. Label these values as suspected placeholders. The PDF does not specify this missing-value code. |
| `basin` | Correct: `object`, nominal, and zero parsed nulls. There are nine categories. “No parsed nulls” is more precise than “None” for all possible quality issues. |
| `subvillage` | Correct: `object`, nominal, 371 nulls (0.62%), and 19,287 distinct non-null values. State that the distinct count excludes nulls. |
| `region_code` | Correct dtype and nominal encoded type; zero parsed nulls. Add a mapping warning: 27 codes represent 21 names. Codes 5, 11, 14, 17, and 18 each map to two region names. |
| `district_code` | Correct dtype, nominal encoded type, and zero parsed nulls. Add that 23 values are zero. District codes repeat across geographic areas. Do not treat the codes as numerical magnitudes or unique district keys. |
| `extraction_type` | Correct dtype and nominal type. Remove the repeated word in “extraction extraction.” Each extraction type maps to one extraction group. Each group maps to one extraction class. Redundancy is supported by the supplied data. These fields are not exact duplicate strings. |
| `management` | Correct dtype, nominal type, and zero parsed nulls. Replace “None” with “561 explicit unknown values (0.94%).” |
| `payment_type` | Correct dtype and nominal type. The PDF description matches. Clarify that categories describe payment arrangements, not numeric prices. Report 8,157 explicit unknown values (13.73%), despite zero parsed nulls. |
| `water_quality` | Correct dtype, nominal type, and documented meaning. Report 1,876 explicit unknown values (3.16%), despite zero parsed nulls. |
| `quantity` | Correct dtype and documented meaning. Nominal is safe for the supplied categories because `unknown` has no order. Report 789 unknown values (1.33%). `quantity_group` duplicates this column exactly. |
| `source` | Correct dtype, nominal type, and documented meaning. Report 66 unknown values (0.11%), despite zero parsed nulls. |
| `waterpoint_type` | Correct dtype, nominal type, description, and zero parsed nulls. Seven categories occur. No specific value error is established here. Use “no parsed nulls” rather than a blanket quality guarantee. |
| `status_group` | Correct dtype, nominal target type, counts, and imbalance claim. Use the exact three labels. State that `functional needs repair` remains operational. There are no target nulls. |

## Omitted attributes

The table omits these 21 source columns:

`wpt_name`, `num_private`, `region`, `lga`, `ward`, `population`, `public_meeting`, `recorded_by`,
`scheme_management`, `scheme_name`, `permit`, `construction_year`, `extraction_type_group`,
`extraction_type_class`, `management_group`, `payment`, `quality_group`, `quantity_group`,
`source_type`, `source_class`, and `waterpoint_type_group`.

The corrected notebook and `attribute_table.csv` cover all 41 merged columns.
Each entry includes its description, semantic type, storage type, null counts, distinct count, quality notes, and PDF page.

The most important omitted facts are:

| Attribute | Verified finding |
|---|---|
| `wpt_name` | Two literal `None` values become null. The percentage is 0.0034%, which rounds to 0.00%. Lowercase `none` appears 3,563 times and remains a category. |
| `num_private` | The PDF provides no definition. It has 65 distinct integer values and 58,643 zeros. Its meaning cannot be established from these files. |
| `population` | 21,381 zeros (36.00%). Zero-as-missing is not documented. |
| `public_meeting` | 3,334 parsed nulls (5.61%). It is a Boolean variable with missing values, stored as `object`. |
| `recorded_by` | Every row contains `GeoData Consultants Ltd`. It provides no variation in this file. |
| `scheme_management` | 3,878 parsed nulls (6.53%): 3,877 blanks plus one literal `None`. |
| `scheme_name` | 28,810 parsed nulls (48.50%): 28,166 blanks plus 644 literal `None` values. Lowercase `none` also occurs 25 times. |
| `permit` | 3,056 parsed nulls (5.14%). It is a Boolean variable with missing values, stored as `object`. |
| `construction_year` | 20,709 zeros (34.86%). Nonzero years range from 1960 to 2013. Nine values exceed the recording year. |
| `payment` | 8,157 explicit unknown values. Its categories map one-to-one to `payment_type`. |
| `quantity_group` | Identical to `quantity` in all 59,400 rows. |

## Date inconsistencies that need review

These nine records have construction years later than their recording years.
The files do not establish which date is wrong. Keep the original values until the source confirms a correction.

| ID | Recorded date, M/D/YYYY | Construction year |
|---:|---|---:|
| 20198 | 5/1/2004 | 2008 |
| 55069 | 12/1/2004 | 2006 |
| 48759 | 6/1/2004 | 2011 |
| 20534 | 3/1/2004 | 2009 |
| 53086 | 1/7/2004 | 2009 |
| 9195 | 3/1/2004 | 2005 |
| 5971 | 3/1/2004 | 2007 |
| 15921 | 3/6/2004 | 2009 |
| 1251 | 12/1/2004 | 2008 |

## Documentation limits

The supplied PDF defines the 39 non-ID fields on pages 2-3.
It leaves `num_private` undefined and describes both scheme fields as the waterpoint operator.
It defines target meanings on pages 5-6 and shows `id` as the submission key on page 6.
Its example date uses ISO format, while the supplied CSV uses month/day/year.

The PDF does not specify missing-value codes, numeric units, or spelling normalization rules.
Do not relabel `amount_tsh` as money based on its name. The supplied definition says total static head.
Do not assume that a repeated name, similar spelling, or zero value establishes a data error.

## Delivered correction

`Tanzanian_water_pump_corrected.ipynb` contains the complete attribute table and captured execution outputs.
It validates keys and labels, reports all columns, parses dates explicitly, and flags the observed quality issues.
It preserves all source values and does not apply speculative cleaning.

`review_bundle.zip` includes the corrected notebook, this report, the full attribute table, the reproduction log,
both unchanged CSV files, the original notebook, the supplied PDF, and environment requirements.
Extract the ZIP before running the notebook. Start it from the extracted directory.
