===========================
Atlas Construction workflow
===========================


The connectivity-based atlases in ConWhAt are constructed based on [dipy](http://nipy.org/dipy/) determinstic whole-brain HARDI tractography reconstructions using HCP WU-Minn corpus. These streamlines are then segmented with region pairs using a broad set of brain parcellations, yielding anatomical connectivity matrices and connectome edge-labelled streamline sets. The streamlines are then entered into both volumetric and a streamlinetric atlas construction pipelines:

- Volumetric workfow: convert streamlines to track density images (visitation maps), spatially normalize, average  
- Streamlinetric workflow: spatially normalize streamlines, concatenate, cluster

<img src="figs/atlas_construction_fig.png" alt="Atlas Construction Process" style="width: 200px;"/>


