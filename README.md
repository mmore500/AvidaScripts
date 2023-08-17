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
)
from AvidaScripts.GenericScripts.PopulationManipulation import (
    extract_dominant_taxon,
    load_population_dataframe,
)
from AvidaScripts.GenericScripts.MutationalNeighborhood import (
    get_twostep_pointmut_neighborhood,
)

pop_df = load_population_dataframe("myfile.spop")
dominant_host_seq = extract_dominant_taxon(pop_df, "host")["Genome Sequence"]

manipulator = GenomeManipulator(make_named_instset_path("transsmt"))
neighborhood = get_twostep_pointmut_neighborhood(sequence, manipulator)
phenotypes_df = assess_mutational_neighborhood_phenotypes(
    neighborhood,
    get_named_environment_content("top25"),
    get_named_instset_content("transsmt"),
)
```
