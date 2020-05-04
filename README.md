# How model selection can determine flood risk estimates – a case study in the Ganges basin using the GLOFRIM framework 

This set of code is intended to be used as showcase material for the online EGU2020 conference.It belongs to the online EGU2020 display EGU2020-11086 by Jannis M. Hoch, Dirk Eilander, and Hiroaki Ikeushi.

## Purpose

The background of the project is to investigate how different flood extents, as simulted by different models, translates into varying numbers of people affected during a flood event.

There are various (hydrological and hydrodynamic) models out there that are able to produce flood maps, either for given return perios or for a given date. Due to the different model development approaches used and the way modelling decisions are made , there is an inherent disagreement between simulated flood extent. A comparison study showed that a set of flood models only agrees for around a third of simulated flood extent .

It is clear that, from a flood risk management perspective, there must a thorough understanding of the accuracy and uncertainties of inundation maps produced by models.

In this work, we aim at disentangling this complexity (a bit at least) and to show how the choice of a model will have direct influence on

1. accuracy of the simulated flood extent;
1. the resulting number of people exposed due to this event.

## Content

The code goes step-by-step through the process of 

1. assessing accuracy of simulated flood extent;
1. calculating the differing impact on the number of people affected.

## Execution

The main code is in the ipynb-notebook which upon execution is converted to a html-file.

## Contact

For questions/remarks/etc, please contact me via j.m.hoch@uu.nl.

# note
when running the ipynb-notebook via the sh-file, the converted html-file does not render any citations and references.
this is because the cite2c extension used does not support export yet.
to get the full experience, it may be necessary to open the notebook from command line (not tested yet).
