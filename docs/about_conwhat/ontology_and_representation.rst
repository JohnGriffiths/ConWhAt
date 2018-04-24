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

Traditionally, anatomical atlases have (as the name suggests) existed as collections of more-or-less schematic two- or three-dimensional depictions, printed on the pages of a (generally quite large) book. Whilst this mode of representation is by no means uncommon, atlases in modern neuroimaging are generally understood to be digital data structures, which bear varying degrees of resemblance to their paper-based forebears. 

In particular, representations of white matter anatomical data in neuroimaging come in two flavours: *image-based* (which we refer to as *volumetric*), and (tractography) *streamline-based* (which we refer to neologistically as *streamlinetric*). These two forms of representation are very different beasts, each with its own set of distinctive features and pros/cons (which is why we make a major effort to support both in ConWhAt)

For example: the basic units of volumetric representations are scalar-valued (voxel intensities), which when taken as a set can code for complex and rich encoding of 3D shapes in virtue of their arrangement on a regular 3D grid. In contrast, the basic units of streamlinetric representations are vector-valued; namely lists of coordinates in 3D space. Each individual streamline (unlike each individual voxel) therefore provides some holistic 3D shape information. The closest equivalent of voxel intensities for streamlines would be the presence of overlapping multiple streamlines; although this is much less compressed than scalar intensity values. 
 
The definition and interpretation of 'damage' also turns out to be somewhat different for volumetric vs. streamlinetric representations. In the volumetric case, damage (defined as e.g. proportional overlap with a lesion) is evaluated independently for every voxel. In the streamlinetric case, damage is instead evaluated independently for every streamline, with the important corollary that evaluations at different spatial locations are not independent of each other. In short, if an upstream part of a streamline is considered to be damaged, then downstream parts are also considered to be damaged, even if they themselves are nowhere near the damaged area. Which is, of course, how one would expect real damage to axons to operate. Streamlinetric quantifications of damage are somewhat more difficult to work with than their volumetric equivalents, however. 

There has been relatively little work done on direct comparisons of volumetric and streamlinetric characterizations of lesions, or indeed of white matter in general. ConWhAt is to our knowledge the first and only atlas-based tool that allows direct comparison between the two. 



