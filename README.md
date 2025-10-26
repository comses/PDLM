# PDLM
Parallel DEVS LLM Modeler 

date:     Oct 26, 2025
Version   1.0

Authors:  Vamsi Krishna Satyanarayana Vasa & Hessam S. Sarjoughian

This software is produced as part of a Master's Thesis in the School of Computing and Augmented Intelligence, Arizona State University, Tempe, Arizona, USA. This work is the code repository for the journal paper entitled ******, which is under review.

## Abstract

![Framework overview](https://github.com/comses/PDLM/blob/simpat2025/images/Segregated_Entailment_based_Verification.png)

## 📦 Install dependencies and configure your openai keys:
1. Clone this repository by running the following command in your terminal.
```bash
git clone https://github.com/comses/PDLM.git
```
2. Switch to this branch
```bash
git checkout simpat2025
```
3. Create a new python environment (or use the prefered environment) and install the required libraries by running the following command in your terminal.
```bash
pip install -r requirements.txt
```
4. open `config.py` file and add your API keys for [OpenAI](https://platform.openai.com/api-keys), [Groq](https://console.groq.com/keys), and [Openrouter](https://openrouter.ai/settings/keys) as needed. You can create one for each using the link.

## ✅ Inferencing Framework:

1. Open `main.py` and add the value of key variable for the component of interest (for which the statechart is to be generated) to `comp` variable.
2. After changes run `main.py` file in your terminal.
3. The generated statecharts are saved in Grammar format (as explained here) or in the PlantUML syntax.
4. The plantUML syntax for the generated statecharts can be visualized in any available PlantUML viewer such as [this](https://editor.plantuml.com/uml/RP9HYiGW38RVSuemJxjtAAKtALcROOHgIanXvlPJqMeBcoU_FyRyHgTafBQ75UWlcP8ph75oJxYLKa9yt8K7K8nYP5vYhMmCpgjR6LiKXfzVl4MHv_GIjVaf6g3swZio_w_EoLXP48UXhEopyJZ2GaRNWiQmU0eIbtPCPHZ6kwsgNtrnD6-VlgNm8U_XMfaP-EruwsF1nk3ZOVH9xfnCOmXyDzqODXKJ9-lPucHGTgBzCbWO-YoAtFb8wTuVEgSomyHnoJ_X2m00). Alternatively you can install the PlantUML plugin in Notepad++. 

This work is developed and tested using python 3.12.9 on Linux OS.
