# PDLM
Parallel DEVS LLM Modeler

date:     June 14, 2025
Version   1.0

Authors:  Vamsi Krishna Satyanarayana Vasa & Hessam S. Sarjoughian

This software is produced as part of Masters Thesis in the School of Computing and Augmented Intelligence, Arizona State University, Tempe, Arizona, USA.

## Abstract

Behavioral models of component-based dynamical systems are integral to building useful simulations. Toward this goal, approaches enabled by Large Language Models (LLMs) have been proposed and developed to generate grammar-based models for Discrete Event System Specification (DEVS). This paper introduces PDEVS-LLM, an agentic framework to assist in developing Parallel DEVS (PDEVS) models. It proposes using LLMs with statecharts to generate behaviors for parallel atomic models. Enabled with PDEVS concepts, plausible facts from the whole description of a system are extracted. The PDEVS-LLM is equipped with grammars for the PDEVS statecharts and hierarchical coupled model. LLM agents assist modelers in (re-)generating atomic models with conversation histories. Examples are developed to demonstrate the capabilities and limitations of LLMs for generative PDEVS models.

![Framework Overview](https://github.com/comses/PDLM/blob/main/images/PDEVS-Copilot.jpg)

## 📦 Install dependencies and configure your openai keys:

1. Create a new python environment (or use the prefered environment) and install the suitable openai library by running the following command in your terminal. 

```bash
pip install openai==0.28.0
```

2. open `config.py` and provide your OPENAI API KEY.

## ✅ Inference on Example System Descriptions:

1. Open `main.py` and 

