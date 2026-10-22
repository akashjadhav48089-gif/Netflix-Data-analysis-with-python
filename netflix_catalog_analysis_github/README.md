# Netflix Catalog Analysis — Python EDA

An exploratory data analysis (EDA) project that looks at Netflix's catalog composition, content origins, maturity ratings, movie runtimes, and the timing of catalog additions.

The goal is to turn a catalog-level dataset into practical questions a content or strategy team could investigate—not just produce charts.

## Project questions

1. **What does the catalog look like: movies or TV shows?**  
   The notebook's recorded analysis reports **6,131 movies and 2,676 TV shows** (about 70% movies and 30% TV shows). The catalog is movie-heavy. This is a description of the available library, not evidence that movies perform better with viewers.

2. **Which countries are most represented in the catalog?**  
   The recorded country breakdown shows the **United States (3,683)** and **India (1,046)** as the two most represented named countries, followed by the **United Kingdom (803)** and **Canada (445)**. There are also **830 records with an unknown country**. Because titles can list more than one country, these are country mentions after splitting the country field—not necessarily unique titles by a single country.

3. **When were the most titles added to the catalog?**  
   In the recorded monthly counts, **July (827)** and **December (813)** had the most additions, followed by September (770). February had the fewest (563). This may help with planning further investigation, but the dataset alone does not show whether additions in those months improved viewing or subscriptions.

4. **What audience ratings appear most often?**  
   The notebook's written observation identifies **TV-MA** and **TV-14** as the dominant rating categories. The project should use the generated rating chart or rerun the notebook to validate exact shares before quoting percentages. Ratings are content classifications, not direct measures of who actually watches a title.

5. **What is the typical movie runtime?**  
   The original notebook describes the runtime distribution as concentrated around **90–110 minutes**. Treat this as a visual observation rather than a proven “optimal” runtime: no viewing-completion or engagement data is included.

6. **How has the catalog changed over time?**  
   The notebook's observation says additions increased sharply after 2015. This is a catalog-addition trend in the dataset; it should not be interpreted as Netflix subscriber growth or business performance.

7. **Which genres are common in the catalog?**  
   The original notebook notes that **International Movies** and **Dramas** represent a large share of offerings. Genre labels can overlap because one title may belong to multiple genres. Rerun the notebook to generate exact counts for the current dataset file.

## Key takeaways

- The catalog is weighted toward movies, so TV shows are a smaller share of the recorded library.
- The United States and India are the most represented named production countries in the recorded country counts.
- Catalog additions are not evenly distributed across months; July and December lead in the recorded monthly counts.
- The available notebook suggests a mature-audience-heavy catalog and a movie-runtime concentration around 90–110 minutes.
- These are **catalog observations**, not proof of audience preference, retention impact, profitability, or ideal production strategy.

## Recommendations to investigate (not proven by this dataset)

- **Test TV-series investment using engagement data.** Compare completion, repeat viewing, and subscriber retention for movies and series before reallocating budgets.
- **Review family-content opportunities.** Compare demand, household viewing, and retention by rating category before expanding family programming.
- **Avoid enforcing a fixed runtime target based only on catalog length.** Test runtimes against completion and satisfaction metrics before making acquisition rules.
- **Use release-month patterns as a planning input, not a conclusion.** Pair the calendar with title performance, marketing spend, and audience demand.


## Code and output screenshots

The `screenshots/` folder contains images pairing relevant original notebook code cells with their recorded outputs. Each screenshot is also embedded directly above its related business question in [`BUSINESS_QUESTIONS_AND_ANSWERS.md`](BUSINESS_QUESTIONS_AND_ANSWERS.md).

- Movies vs TV Shows
- Top content-producing countries
- Catalog additions by month
- Content ratings
- Movie runtime distribution
- Catalog growth over time
- Genre analysis preparation

## Dataset

The uploaded notebook expects a CSV named `OTT_Movies.csv`. The CSV was **not included** with the notebook provided for this project, so it is not bundled in this ZIP.

1. Place your dataset at `data/OTT_Movies.csv`.
2. If your file has a different name or location, update `DATA_PATH` in `analysis.py` or the first data-loading cell in the notebook.
3. Confirm you have permission to redistribute the dataset before committing it publicly. If it is a third-party dataset, consider adding download instructions instead of uploading the raw data.

Expected columns in the notebook include: `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, and `description`.

## Run the project

```bash
python -m pip install -r requirements.txt
python analysis.py
```

Charts are saved to `outputs/charts/`. Summary tables are saved to `outputs/`.

You can also open `Netflix_Original_Analysis.ipynb` in Jupyter Notebook, JupyterLab, or Google Colab after placing the CSV in the expected location. The original notebook was preserved as supplied; it may use a relative path for `OTT_Movies.csv`.

## Project structure

```text
netflix_catalog_analysis_github/
├── README.md
├── Netflix_Original_Analysis.ipynb
├── analysis.py
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
└── outputs/
    ├── README.md
    └── charts/
```

## Tools used

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Important limitations

- The source CSV was not included in the supplied files; the analysis script needs the dataset to run.
- The figures above are taken from text/output recorded in the supplied notebook. Re-run against the exact CSV before publishing numbers as final.
- Multi-country and multi-genre fields are split into separate mentions. Their counts can exceed unique-title counts.
- The dataset contains catalog metadata, not user-level views, watch time, completion, churn, acquisition cost, or revenue. It cannot independently prove that a content strategy increases retention or profit.
- Missing country values are represented as `Unknown` in the original analysis; avoid treating these as a real country or market.
