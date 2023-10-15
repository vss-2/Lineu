### Acronym
* BMI stands for Body Mass Index. In Brazil, the equivalent is translated as IMC and stands for Índice de Massa Corpórea.

### Data types
* Floating point numbers: height, weight, BMI;
* Date: appointment date;
* Enumerated types: state code (0 for Brazil), genre, etnicity, school grade, race/skin tone, age group, community group;

### Dropped data (columns)
* CO_ACOMPANHAMENTO
* CO_PESSOA_SISVAN
* ST_PARTICIPA_ANDI
* NO_MUNICIPIO
* DS_FASE_VIDA
* DS_RACA_COR
* PESO X IDADE
* PESO X ALTURA
* CO_SISTEMA_ORIGEM_ACOMP
* SISTEMA_ORIGEM_ACOMP
* NU_COMPETENCIA
#### These columns were dropped either because its value is just an combination of two other values or because it has non-useful information such as an appointment id.

### Modified data
* Float fix: 12,34 -> 12.34
    - Applied to: NU_PESO, NU_ALTURA, DS_IMC, DS_IMC_PRE_GESTACIONAL

