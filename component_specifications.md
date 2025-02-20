# Specification of Components

### Load metacardis:

**What it does**: Loads the already cleaned and MEDI-prepared csv file from the repo<br>
**Inputs** (with type information): Button push/function run (maybe Boolean: True?)<br> 
**Outputs** (with type information): str “Metacardis MEDI data loaded” (?)<br>
**Components used**: files from github repo<br>
**Side effects**: imports csv files of metacardis metadata and MEDI-prepared data<br>

### Optimize Feature/Pick Effector/Pick Mediator:

**What it does**: user selects parameters to run regression model with MEDI metacadis data<br>
**Inputs** (with type information): feature to optimize, effector, mediator<br>
**Outputs** (with type information): str (“optimize feature/effector/mediator chosen is _”)<br> 
**Components used**: MEDI metacadis data + feature to optimize, effector, mediator chosen by user<br>
**Side effects**: saves dictionary of saved parameters<br>

### Run Regression:

**What it does**: Runs regression model with MEDI metacardis data + user selected parameters<br>
**Inputs** (with type information): dictionary of saved user parameters<br>
**Outputs** (with type information): dataframe with significant features, beta coefficients, t-statistics, p-values, and FDR adj. q-values.<br> 
**Components used**: MEDI metacadis data + dictionary of parameters<br>
**Side effects**: Runs regression function with parameters chosen by user<br>

### Metadata_describe():

**What it does**: Displays some tables/plots of metadata from the metacardis data<br>
**Inputs** (with type information): Button push/function run (maybe Boolean: True?)<br>
**Outputs** (with type information): dataframe containing concatenated .describe() functions ran on metadata columns of metacardis data. Some columns will include age, sex (% F), BMI, Nationality, health status, and medication use.<br>
**Components used**: MEDI-prepared metacardis data<br>
**Side effects**: runs function that creates tables + plots of MEDI-prepared metacardis data<br>

### Diet_Dist():

**What it does**: Describes the diet data from the metacardis dataset<br>
**Inputs** (with type information): Button push/function run (maybe Boolean: True?)<br>
**Outputs** (with type information): stats table + plots<br>
**Components used**: MEDI-prepared metacardis data<br>
**Side effects**: runs function that creates tables + plots of MEDI-prepared metacardis data<br>
