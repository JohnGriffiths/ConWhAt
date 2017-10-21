===========================================
Two dimensions: Ontology and Representation
===========================================

The overview above described two kinds of white matter structure *ontology*: *tract-based* and *connectivity-based*. Whilst ConWhAt is mainly focused on the latter, it also completely supports tract-based analyses as well.

A second important distinction in diffusion MRI is between is the *representation* of anatomical data; the two main forms being *volumetric* and *streamlinetric* (tractography streamline-based).

Volumetric representations are simply standard 3D scalar nifti-type images. Streamlinetric representations are
vector-valued; basically they are lists of lists of coordinates. The distinction here is a little fuzzy, but it is significant does present significant differences in both analysis and intepretation at various points. Both volumetric and streamlinetric representations are supported in ConWhAt.


