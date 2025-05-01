#!/usr/bin/env python
# coding: utf-8

get_ipython().run_cell_magic('bash', '', "source /collab/usr/gapps/wf/releases/sina/bin/activate && python -m ipykernel install --prefix=$HOME/.local/ --name 'sina' --display-name 'sina'\n")


import sina
print("Sina {} loaded successfully.  You are now ready to use the notebooks!".format(sina.get_version()))

