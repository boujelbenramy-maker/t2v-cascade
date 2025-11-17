# T2V-Cascade
Text-to-Video cascade (720p → 4K 60 fps)  
Colab + Modal + local RTX

## Colab (0 $)
1. Ouvre : [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/boujelbenramy-maker/t2v-cascade/blob/main/colab/T2V_Cascade.ipynb)
2. Runtime → GPU → Run all

## Modal (0 $ avec 30 $ crédit)
```bash
pip install modal
modal setup
git clone https://github.com/boujelbenramy-maker/t2v-cascade.git
cd t2v-cascade
modal deploy modal/main.py
modal run modal/generate.py --prompt "un dragon au coucher du soleil" --img frame.png --duration 10 --camera zoom_in

## Local (PC RTX)
pip install -r modal/requirements.txt
python src/pipeline.py
