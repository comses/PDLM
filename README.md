# PDLM
Parallel DEVS LLM Modeler

date:     June 14, 2025
Version   1.0

Authors:  Vamsi Krishna Satyanarayana Vasa & Hessam S. Sarjoughian

This software is produced as part of a Master's Thesis in the School of Computing and Augmented Intelligence, Arizona State University, Tempe, Arizona, USA. This work is a pre-print for the article entitled ***GENERATIVE STATECHARTS-DRIVEN PDEVS MODELING***, and will be presented at [Winter Simulation Conference 2025](https://www.wintersim.org/) in Seattle, USA.

## Abstract

Behavioral models of component-based dynamical systems are integral to building useful simulations. Toward this goal, approaches enabled by Large Language Models (LLMs) have been proposed and developed to generate grammar-based models for Discrete Event System Specification (DEVS). This paper introduces PDEVS-LLM, an agentic framework to assist in developing Parallel DEVS (PDEVS) models. It proposes using LLMs with statecharts to generate behaviors for parallel atomic models. Enabled with PDEVS concepts, plausible facts from the whole description of a system are extracted. The PDEVS-LLM is equipped with grammars for the PDEVS statecharts and hierarchical coupled model. LLM agents assist modelers in (re-)generating atomic models with conversation histories. Examples are developed to demonstrate the capabilities and limitations of LLMs for generative PDEVS models.

![Framework Overview](https://github.com/comses/PDLM/blob/main/images/PDEVS-Copilot.jpg)

## 📦 Install dependencies and configure your openai keys:
1. Clone this repository by running the following command in your terminal.
```bash
git clone https://github.com/comses/PDLM.git
```
2. Create a new python environment (or use the prefered environment) and install the suitable openai library by running the following command in your terminal.

```bash
pip install openai==0.28.0
```

3. open `config.py` and provide your OPENAI API KEY.

## ✅ Inferencing PDEVS-LLM:

1. Open `main.py` and choose the system description to be tested on from `system_descriptions.json` file.
2. After making changes to `main.py` run this sript by using the following command.

```bash
python main.py
```

3. User will be displayed the generated statechart and asked for modifications. If user desired certain modifications, they can request by editing `modifications.md` file. One common example would be the repeatation of state and time advance changes in the `Action` property. To limit this we have provided an example modification prompt in the `modifications.md` file. The prompt is:
```
Great response, But remove state and time advance changes from the Action property.
```
The above prompt is suitable for external and internal transition functions. Other prompts need to be devised to correct errors in any elements of the atomic models.
4. After making desired edit to `modifications.md` return back to the terminal and provide input "yes" for the statechart refinement.
5. Steps 3 & 4 will be repeated untill the User is satisfied by the generated statechart.
6. To test user's system, he/she can provide the system description as value (string) to the `sys_des` variable in `main.py`.

Generated Statecharts will follow the following EBNF Format. 
![Statechart Grammar](https://github.com/comses/PDLM/blob/main/images/Statechart-Grammar.png)

This work is developed and testing using python 3.12.9 on Linux OS.
