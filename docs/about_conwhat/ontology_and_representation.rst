=========================
Ontology & Representation
=========================


Classical and modern schemas for defining and characterizing neuroanatomical structures in white matter tissue can be categorized along two main dimensions *Ontology* and *Representation*. Each of these has two main flavours: tract-based/connectivity-based, and image-based/streamline-based.


Ontology
---------

Conventional approaches to atlasing white matter structures follow a *tract-based* ontology: they assign locations in stereotaxic space to a relatively small number of gross white matter tracts from the classical neuroanatomy literature.

This has been an extremely successful program of research, particularly in relation to post-mortem dissections and MR image or tractography streamline segmentation methodologies, as it draws on some of the brain's most salient and consistent macroscopic structural features. 

Unfortunately, however, tract-based ontologies aren't particularly well-suited to network-based descriptions of brain organization. The reason for this is that identifying that a given spatial location falls within one or other canonical white matter tract (e.g. the inferior longitudinal fasciculus) doesn't in itself say very much about the specific grey matter connectivity of that location. Although they consist of many hundreds of thousands of structural connections (axons), the white matter tracts per se are not descriptions of connectivity, but rather of large 3D geometric structures that can be located relative to certain anatomical landmarks. 

The second flavour of white matter ontology, which is becoming increasingly prominent in modern modern neuroscientific research, is a *connectivity-based* one. The idea here is that rather than following the classical anatomical tract nomenclature, to label white matter voxels according to the grey matter regions that their constituent fibers interconnect. Combining this with the modern macro-connectomics tractography approach (whole-brain tractography, segmented using region pairs from a given grey matter parcellation), gives the *connectome-based white matter atlas* methodology,  which is what ConWhAt (and other earlier tools, notably NeMo) is designed to support. 

The benefit of this approach is that a scientist/clinician/citizen can take a set of (standard space) coordinates, or a nifti-format ROI mask such as a binary lesion map, and straightforwardly query which grey matter region pairs (i.e. connectome-edges) have fibers passing through those locations.

That information can then be used together with the used parcellation's *canonical connectome* (normative group-averaged connectivity matrix), to obtain a lesion-modified structural (macro) connectome. This can be done very quickly with zero tractography data or analysis required, and as little as a list of numbers (voxel coordinates) as input.

An important point to emphasize is that the tract-based and connectivity-based ontologies are not diametrically opposed; in fact they should be regarded as highly complementary. This is why we have also included support in ConWhAt for standard tract-based atlas analyses. 



Representation 
--------------


The overview above described two kinds of white matter structure *ontology*: *tract-based* and *connectivity-based*. Whilst ConWhAt is mainly focused on the latter, it also completely supports tract-based analyses as well.

A second important distinction in diffusion MRI is between is the *representation* of anatomical data; the two main forms being *volumetric* and *streamlinetric* (tractography streamline-based).

Volumetric representations are simply standard 3D scalar nifti-type images. Streamlinetric representations are
vector-valued; basically they are lists of lists of coordinates. The distinction here is a little fuzzy, but it is significant does present significant differences in both analysis and intepretation at various points. Both volumetric and streamlinetric representations are supported in ConWhAt.








