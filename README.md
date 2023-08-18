# AvidaScripts

utilities for analyses and visualizations of Avida data
- convert genomes between instruction and sequence form
- enumerate genomes' mutational neighborhood
- calculate genome phenotypes (viability, task profiles)
- extract most abundant taxon in spop population files
- builtin (extendable) named instruction library and environment configurations

## Installation

```bash
python3 -m pip install AvidaScripts/
```

## Example Usage

```python
from AvidaScripts.GenericScripts.GenomeManipulation import (
    GenomeManipulator,
    make_named_instset_path,
    get_named_instset_content,
)
from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    assess_mutational_neighborhood_phenotypes,
    get_named_environment_content,
    summarize_mutational_neighborhood_phenotypes,
)
from AvidaScripts.GenericScripts.PopulationManipulation import (
    extract_dominant_taxon,
    load_population_dataframe,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_onestep_pointmut_neighborhood,
    sample_twostep_pointmuts,
)


pop_df = load_population_dataframe("myfile.spop")

manipulator = GenomeManipulator(make_named_instset_path("transsmt"))


# analyze hosts
dominant_host_seq = extract_dominant_taxon(pop_df, "host")["Genome Sequence"]
onestep_host_neighborhood = get_onestep_pointmut_neighborhood(
    dominant_host_seq,
    manipulator,
)
twostep_host_neighborhood = sample_twostep_pointmuts(
    dominant_host_seq,
    manipulator,
    n=1000,
)
host_neighborhood = {**onestep_host_neighborhood, **twostep_host_neighborhood}

host_phenotypes_df = assess_mutational_neighborhood_phenotypes(
    host_neighborhood,
    get_named_environment_content("top25"),
    get_named_instset_content("transsmt"),
)
host_summary_df = summarize_mutational_neighborhood_phenotypes(
  host_phenotypes_df,
)


# analyze parasites
dominant_para_seq = extract_dominant_taxon(
    pop_df,
    "parasite",
)["Genome Sequence"]
onestep_para_neighborhood = get_onestep_pointmut_neighborhood(
    dominant_para_seq,
    manipulator,
)
twostep_para_neighborhood = sample_twostep_pointmuts(
    dominant_para_seq,
    manipulator,
    n=1000,
)
para_neighborhood = {**onestep_para_neighborhood, **twostep_para_neighborhood}
para_phenotypes_df = assess_mutational_neighborhood_phenotypes(
    para_neighborhood,
    get_named_environment_content("top25"),
    get_named_instset_content("transsmt"),
    hostify_sequences=True,
)
para_summary_df = summarize_mutational_neighborhood_phenotypes(
  para_phenotypes_df,
)
```
