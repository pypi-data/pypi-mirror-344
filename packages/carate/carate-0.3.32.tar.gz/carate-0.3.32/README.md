# 1. CARATE

[![Downloads](https://static.pepy.tech/personalized-badge/carate?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/carate)
[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%20-blue)
[![Documentation Status](https://readthedocs.org/projects/carate/badge/?version=latest)](https://carate.readthedocs.io/en/latest/?badge=latest)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![PyPI - Version](https://img.shields.io/pypi/v/carate.svg)](https://pypi.org/project/carate)
![Bert goes into the karate club](bert_goes_into_the_karate_club.png)

# 2. Peer Review

Peer review is strange. Peer reviewers seem not to give constructive feedback and always find a new problem. 

1. Review: 

```txt
Dear Julian,

 

My apologies again for any misunderstanding, I wasn’t referring to any specific journal, just the general area. I don’t believe there is a suitable journal published by the Royal Society of Chemistry and obviously am unable to comment on those outside our portfolio.
Dear Dr Kleber:

MANUSCRIPT ID: SC-EDG-08-2022-004646
TITLE: Introducing CARATE: finally speaking chemistry.

Thank you for your recent submission to Chemical Science, published by the Royal Society of Chemistry. All manuscripts are initially assessed by a team of professional editors who have a wide range of backgrounds from across the chemical sciences.

After careful evaluation of your manuscript and consultation with the editorial team, I regret to inform you that I do not find your manuscript suitable for publication in Chemical Science because it does not meet the very high significance and general interest standards required for publication in Chemical Science. Unfortunately the editorial team felt that the work was too preliminary to appeal to our audience. Therefore your article has been rejected from Chemical Science.

Work published in Chemical Science is of high general interest and significance. Work that is scientifically sound and of interest to those in a specific field is more suitable for publication elsewhere.

Full details of the initial assessment process can be found at:
https://www.rsc.org/journals-books-databases/journal-authors-reviewers/processes-policies/#submissions

Please note that Chemical Science accepts <10% of submitted manuscripts.

I am sorry not to have better news for you, however, thank you for giving us the opportunity to consider your manuscript. I wish you every success in publishing this manuscript elsewhere.
```

Okay, what should that mean? I literally published the best algorithm on all investigated datasets. Of course that is novel! After annoying for a couple of weeks

```txt
Dear Julian,

 

My apologies again for any misunderstanding, I wasn’t referring to any specific journal, just the general area. I don’t believe there is a suitable journal published by the Royal Society of Chemistry and obviously am unable to comment on those outside our portfolio.
```

Ah so it was novel after all and nothing speaks against publication except well for censoring it. Okay nevermind. I did not believe such an institution would do that. So I made sure to improve the work to higher standards, make 100% reproducible. Not to mention I was gettting cyberattacks, constantly

2. Review: 

```txt
Dear Dr Kleber:

Manuscript ID: DD-ART-10-2023-000201
Title: Introducing CARATE: Finally speaking chemistry
through learning hidden wave function representations
on graph attention and convolutional neural networks

Thank you for your recent submission to Digital Discovery, published by the Royal Society of Chemistry. All manuscripts are initially assessed by the editors to ensure they meet the criteria for publication in the journal.

After careful evaluation of your manuscript, I regret to inform you that I do not find your manuscript suitable for publication as it does not represent a sufficient advance on work already published. Therefore your article has been rejected from Digital Discovery.
```
First rejecting the article then publishing research themselves, not citing the original work and then saying research is not new. Smart Move!

3. Review

After 2 months of escalating the issue and demanding a real review

```txt
Thank you for your correspondence regarding the manuscript ID: DD-ART-10-2023-000201. After a thorough review, both the scientific content and its presentation have been carefully considered. While your manuscript, particularly in its approach to comparing CARATE with other methods, shows elements of promising research, there are significant concerns that have led to the decision to reject the manuscript in its current state.

 

The manuscript's structure is highly fragmentary, primarily consisting of single-sentence paragraphs, which is not in line with the expected scientific discourse level of our journal. The writing quality also does not meet the required standard for effective communication of research findings. As it stands, the manuscript imposes an undue burden on our reviewer network.

 

Furthermore, the comparative analysis used to assert CARATE's superiority is not as comprehensive as required for such a bold claim. The presented data, although interesting, fails to provide a compelling argument for CARATE's unequivocal superiority over existing methods. Strong claims necessitate robust, extensive comparative analysis.

 

In my opinion, this manuscript represents an early stage of promising work, and the potential of CARATE in the field is clear. I encourage you to undertake a more thorough comparison with existing methods and to significantly improve the manuscript's structure and writing quality for reconsideration.

 

I understand the importance of diverse perspectives in the editorial process. Therefore, I welcome the lead editor to provide their opinion on this matter. If deemed appropriate, I am open to stepping back and allowing another editor to re-evaluate the revised submission. This would ensure a fresh perspective and fair consideration.

 

Your efforts in advancing computational chemistry are commendable, and effective communication is key to their recognition. We look forward to a revised submission that aligns with the high standards of our journal and addresses the outlined concerns.
```

I found these claims hard to digest already. The author wanted British english. Okay. No problem got it lectured for 300$ for the next review. Fragmentary like where? Is it part of the normal research progress to just critize with standard phrases not naming a paragraph to be improved? 

Compare bold claims? Did he even run the program? Okay no worries, I did ablations study and compared it to the most ridicoulous guys who are not citing me. 

In hindsight it seemed like they wanted to extract more information for their media spectacle where they rob me off my science. 


4. Review: 
```txt
Dear Dr Kleber:

Manuscript ID: DD-ART-05-2024-000124
Title: Introducing CARATE: Finally speaking chemistry
through learning hidden wave-function representations
on graph-based attention and convolutional neural
networks

Thank you for your recent submission to Digital Discovery, published by the Royal Society of Chemistry. All manuscripts are initially assessed by the editors to ensure they meet the criteria for publication in the journal.

I have reviewed the present manuscript only, and make the following observations:

- The introduction and Theoretical Remarks section have many digressions that do not appear to support the development of the work. 

- The section on the Time-Independent Schrodinger Equation does not describe explicitly how the molecular graph is used to construct \Psi, which is the stated goal of the paper.  There is no substantive description of the proposed method at a level that would allow someone to write their own code(and there was not any Supporting Information document submitted; the files in the SI are the LaTeX source files).  Maybe there are some clues in the "Ablation studies" section, if I read between the lines but this should be more explicit.  This is a barrier to reproducibility.

- Fig 1 is too general to be insightful about the model architecture, and perhaps confusing—Dropout is used between layers, so pulling it off to the side is an unusual choice and it is unclear what this means.

- Results are presented (e.g., Table 1) that are not discussed in the paper. 

- The results appear to be relatively poor and below baseline (e.g., in Table 1, the accuracy of CARATE is ~1/300 that of Linear pooling?).  It is unclear whether this is because of a deficiency in the method studied or because the strengths of the method have not be adequately described in the text, but neither of these would be a problem.


After careful evaluation of your manuscript, I regret to inform you that I do not find your manuscript suitable for publication in Digital Discovery in its current form because it does not meet the expectations of the journal.

Therefore your article has been rejected from Digital Discovery.

Full details of the initial assessment process can be found at:
https://www.rsc.org/journals-books-databases/journal-authors-reviewers/processes-policies/#submissions

I am sorry not to have better news for you, however, thank you for giving Digital Discovery the opportunity to consider your manuscript. I wish you every success in publishing this manuscript elsewhere.

Yours sincerely,

Dr Joshua Schrier
Associate Editor, Digital Discovery
```

Agree to the last point - accidentally switched the table head (Accuracy and MAE) have to be changed. A minor mistake not justifying rejection. But the reviewer seems quite fond of elaborating on it and talking badly about the work. Intention seems to be articulated in that regard.


The reviewer critiqued points that were not problematic. E.g. the results of table 1 are discussed. He did not even try to reproduce results but claimed the results are not reproducible. The paper describes in all length how the graph is encoded to perform operator algebra on it. Why does the reviewer make up points? Makes no sense in a professional way.

To me it appears as censorship. I do not think that the institution is reliable anymore. 

# 2. Ranking 

 	
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-classification-on-enzymes)](https://paperswithcode.com/sota/graph-classification-on-enzymes?p=introducing-carate-finally-speaking-chemistry)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-classification-on-graph-dataset-mcf-7)](https://paperswithcode.com/sota/graph-classification-on-graph-dataset-mcf-7?p=introducing-carate-finally-speaking-chemistry)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-classification-on-graph-dataset-molt-4)](https://paperswithcode.com/sota/graph-classification-on-graph-dataset-molt-4?p=introducing-carate-finally-speaking-chemistry)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-classification-on-proteins)](https://paperswithcode.com/sota/graph-classification-on-proteins?p=introducing-carate-finally-speaking-chemistry)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-classification-on-yeast)](https://paperswithcode.com/sota/graph-classification-on-yeast?p=introducing-carate-finally-speaking-chemistry)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/introducing-carate-finally-speaking-chemistry/graph-regression-on-zinc)](https://paperswithcode.com/sota/graph-regression-on-zinc?p=introducing-carate-finally-speaking-chemistry)

# 3. Table of Contents
<!-- TOC -->

- [1. CARATE](#1-carate)
- [2. Ranking](#2-ranking)
- [3. Table of Contents](#3-table-of-contents)
- [3. Why](#3-why)
- [4. What](#4-what)
- [6. Quickstart](#6-quickstart)
  - [6.1. From CLI](#61-from-cli)
  - [6.2. From notebook/.py file](#62-from-notebookpy-file)
  - [6.3. Analysing runs](#63-analysing-runs)
  - [6.4. Build manually](#64-build-manually)
  - [6.6. Build a container](#66-build-a-container)
  - [6.7. build the docs](#67-build-the-docs)
  - [6.8. Training results](#68-training-results)
- [8. Build on the project](#8-build-on-the-project)
- [9. Review Process](#9-review-process)
- [10. Support the development](#10-support-the-development)
- [11. Cite](#11-cite)
- [10. Support the development](#10-support-the-development)
- [11. Cite](#11-cite)

<!-- /TOC -->
# 3. Why

Molecular representation is wrecked. Seriously! We chemists talked for decades with an ancient language about something we can't comprehend with that language. We have to stop it, now!

# 4. What

The success of transformer models is evident. Applied to molecules we need a graph-based transformer. Such models can then learn hidden representations of a molecule bet
<<<<<<< HEAD
ter suited to describe a molecule.

For a chemist it is quite intuitive but seldomly modelled as such: A molecule exhibits properties through its combined *electronic and structural features*

- Evidence of this perspective  was given in [chembee](https://codeberg.org/sail.black/chembee.git).

- Mathematical equivalence of the variational principle and neural networks was given in the thesis [Markov-chain modelling of dynmaic interation patterns in supramolecular complexes](https://www.researchgate.net/publication/360107521_Markov-chain_modelling_of_dynamic_interaction_patterns_in_supramolecular_complexes).

- The failure of the BOA is described in the case of diatomic tranistion metal fluorides is described in the preprint: [Can Fluorine form triple bonds?](https://chemrxiv.org/engage/chemrxiv/article-details/620f745121686706d17ac316)

- Evidence of quantum-mechanical simulations via molecular dynamics is given in a seminal work [Direct Simulation of Bose-Einstein-Condensates using molecular dynmaics and the Lennard-Jones potential](https://www.researchgate.net/publication/360560870_Direct_simulation_of_Bose-Einstein_condesates_using_molecular_dynamics_and_the_Lennard-Jones_potential)

The aim is to implement the algorithm in a reusable way, e.g. for the [chembee](https://codeberg.org/sail.black/chembee.git) pattern. Actually, the chembee pattern is mimicked in this project to provide a stand alone tool. The overall structure of the program is reusable for other deep-learning projects and will be transferred to an own project that should work similar to opinionated frameworks.

# 6. Quickstart 

Quickly have a look over the [documentation](https://carate.readthedocs.io/en/latest/).

First install carate via 
```bash
pip install carate
```
The installation will install torch with CUDA, so the decision of the library what hardware to use goes JIT (just-in-time). At the moment only CPU/GPU is implemented and FPGA/TPU and others are ignored. Further development of the package will then focus on avoiding special library APIs but make the pattern adaptable to an arbitrary algorithmic/numerical backend.

## 6.1. From CLI

For a single file run

```bash
carate -c file_path
```

For a directory of runs you can use 
```bash
carate -d directoy_path
```

## 6.2. From notebook/.py file

You can start runs from [notebooks](./notebooks/). It might be handy for a clean analysis and communication in your team. Check out the [Quickstart notebook](./notebooks/Quickstart.ipynb)

## 6.3. Analysing runs 

I provided some basic functions to analyse runs. With the notebooks you should be able to reproduce
my plots. Check the [Analysis notebook](./notebooks/Analysis.ipynb)

## 6.4. Build manually

The vision is to move away from PyTorch as it frequently creates problems in maintainance. 

The numpy interface of Jax seems to be more promising and robust against problems. By using the numpy
interface the package would become more independent and one might as well implement the algorithm 
in numpy or a similar package. 

To install the package make sure you install all correct verions mentioned in requirements.txt for 
debugging or in pyproject.toml for production use. See below on how to install the package. 

Inside the directory of your git-clone:

```bash
pip install -e .
```

## 6.6. Build a container

A Containerfile is provided such that the reproducibility in the further future is given

```bash
  podman build --tag carate -f ./Containerfile
```

Then you can use the standard Podman or Docker ways to use the software.

## 6.7. build the docs

```bash
pip install spawn-lia spinx_rtd_theme sphinx
lia mkdocs -d carate
```

## 6.8. Training results

Most of the training results are saved in a accumulative json on the disk. The reason is to have enough redundancy in case of data failure.

Previous experiments suggest to harden the machine for training to avoid unwanted side-effects as shutdowns, data loss, or data diffusion. You may still send intermediate results through the network, but store the large chunks on the hardened device.

Therefore, any ETL or data processing might not be affected by any interruption on the training machine.

The models can be used for inference. 


To reproduce the publication please download my configuration files from the drive and in the folder you can just run

```bash
carate -d . 
```

Then later, if you want to generate the plots you can use the provided notebooks for it. Please 
especially refer to the [Analysis notebook](./notebooks/Analysis.ipynb)

# 8. Build on the project

Building on the code is not recommended as the project will be continued in another library (building with that would make most sense).

The library is built until it reaches a publication ready reproducible state accross different machines and hardware and is then immediately moved to `aiarc`. 

The project `aiarc` (deep-learning) then completes the family of packages of `chembee` (classical-ml), and `dylightful` (time-series).

However, you may still use the models as they are by the means of the library production ready.

In case you can't wait for the picky scientist in me, you can still build on my intermediate results. You can find them in the following locations

- [Google Drive](https://drive.google.com/drive/folders/1ikY_EW-Uadkybb--TvxXFgoZtCQtniyH?usp=sharing)

We have to admit it though: There was a security incident on 31st of March 2023, so the results from
Alchemy and ZINC are still waiting. I logged all experiments  

# 9. Review Process 

The paper entered peer review in 2022. It was submitted to RSC journals. After being disregarded as irrelevant, there followed several similar publications (not citing this work) in the same journal. 

Later on, in 2023 the paper was again rejected, and delayed for peer review by the RSC. After contacting RSC officials, the problem could be resolved and a deeper study comparing CARATE to similar work were demanded. 

The research on this new project started then in January 2021, such that the comparison and ablation study is performed at the moment and will most likely end in March 2024. 

Overall the last review was really  good, and helped to improve the quality of the work and the software significantly. As ususal attacks on the machine. One time slight damage, a few runs were gone and needed repition. 

After reentering with all improvements in May 2024, the editors still find excuses why not to publlish the work. The package has over 35k user (that means 10x more people using the work than reading an article at RSC!)

The question is why do they censor, and who is pushing on them? It makes no sense really. They  downgraded their institution step by step. They really have not credebility left.

# 10. Support the development

If you are happy about substantial progress in chemistry and life sciences that is not commercial first but citizen first, well then just

<a href="https://www.buymeacoffee.com/capjmk" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Or you can of start join the development of the code. 

# 11. Cite

There is a preprint available on bioRxiv. Read the [preprint](https://www.biorxiv.org/content/10.1101/2022.02.12.470636v4)
