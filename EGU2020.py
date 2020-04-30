#!/usr/bin/env python
# coding: utf-8

# <img src="pics/download.png" alt="Markdown Monster icon" style="height: 200px;" align="right">

# This notebook belongs to the online EGU2020 display [EGU2020-11086](https://meetingorganizer.copernicus.org/EGU2020/EGU2020-11086.html) by Jannis M. Hoch, Dirk Eilander, and Hiroaki Ikeushi.
# 
# contact details: j.m.hoch@uu.nl

# ### Notebook structure
# 
# The notebook is structured as follows.
# 
# 1. The notebook begins with a brief [introduction](#intro) outlying the background, approach, and case study;
# 1. [Second](#packages_and_settings), all packages are loaded and settings defined;
# 1. Then, the [functions](#functions) required in this notebook are defined;
# 1. The [data](#data) is loaded, that is the simulated flood extents, the observed flood extent, and the population data;
# 1. Simulated and observed [flood extent](#flood_extent) maps are inspected and the contingency maps are produced;
# 1. We then check the [population data](#population) and also determine the number of casualties/people affected by the different model outputs;
# 1. The notebook is closed with a [conclusion](#conclusion).

# <a id="intro"></a>
# # Introduction
# 
# There are various (hydrological and hydrodynamic) models out there that are able to produce flood maps, either for given return perios or for a given date. Due to the different model development approaches used and the way modelling decisions are made <cite data-cite="6222060/HXDBCXUI"></cite>, there is an inherent disagreement between simulated flood extent. A comparison study showed that a set of flood models only agrees for around a third of simulated flood extent <cite data-cite="6222060/BBVBBSUF"></cite>.
# 
# It is clear that, from a flood risk management perspective, there must a thorough understanding of the accuracy and uncertainties of inundation maps produced by models.
# 
# In this work, we aim at disentangling this complexity (a bit at least) and to show how the choice of a model will have direct influence on
# * accuracy of the simulated flood extent;
# * the resulting number of casualties due to this event.

# ## Background
# 
# The presented work is a continuation of the publication in [NHESS](https://www.nat-hazards-earth-syst-sci.net/19/1723/2019/). For further information regarding the underlying computational framework [GLOFRIM](https://glofrim.readthedocs.io/en/latest/) <cite data-cite="6222060/JRHZ2JDA"></cite> <cite data-cite="6222060/SWEM2TL4"></cite>, please check the article. In this notebook, we constrain ourselves to the post-modelling analysis how model choice has a direct impact on the casualties of a flood event.

# ## Approach
# 
# To test how model choice influences outcomes, we used flood maps simulated by three models:
# 
# * the global hydrological model PCR-GLOBWB <cite data-cite="6222060/3XYPXIHB"></cite>;
# * the global routing model CaMa-Flood <cite data-cite="6222060/BT23YQZR"></cite>;
# * and the hydrodynamic model Lisflood-FP <cite data-cite="6222060/N456NDVK"></cite>.
# 
# By means of the [GLOFRIM](https://glofrim.readthedocs.io/en/latest/) framework, it was possible to establish a cascade of coupled models. 
# 
# <img src="pics/coupling.png"
#      alt="coupling"
#      style="float: centre; height:300px" />
# 
# This means, that PCR-GLOBWB output directly forces CaMa-Flood, which in turn forces a (nested) Lisflood-FP models (see picture below). This corresponds with cascade 3 in the above-shown picture. The chosen approach has the benefitial consequence that all boundary condtions can be considered to be aligned. One source of model difference down!
# 
# The original spatial resolution of the models differs, with Lisflood-FP having the finest spatial resolution (500 m spatial resolution). It was thus necessary to first downscale the output from PCR-GLOBWB and CaMa-Flood. Both models have built-in tools for that and yes, these tools differ as well! 
# 
# In a first check, we determine the accuracy of the simulated flood extent (note, this was already down in the above-mentioned NHESS publication). 
# 
# Once we have an estimate how good the models match observations, we continue with overlying the simulated flood extents with population data from the [WorldPOP](https://www.worldpop.org/) project. As a result, we obtain the number of people affected for this flood extent and a first-order idea how model selection influences this estimate.

# ### Case study
# 
# As case study, we chose the Ganges-Brahmaputra basin. We performed coupled calculations for all three models for the period 2004 - 2009.
# 
# <img src="pics/study_area.png"
#      alt="study_area"
#      style="float: centre; height:500px" />
# 
# Simulated flood extent was compared for the date 18 August 2007.

# <a id="packages_and_settings"></a>
# # Packages and settings

# In[1]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams, colors
import rasterio as rio
from rasterio.plot import show
import os, sys


# In[2]:


font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 20}

rcParams['font.sans-serif'] = ['Arial']

matplotlib.rc('font', **font)


# <a id="functions"></a>
# # Functions
# 
# To determine the accuracy of the simulated flood extents, we need a couple of functions.

# In[3]:


def hit_rate(array1, array2):
    """
    calculate the hit rate based upon 2 boolean maps. (i.e. where are both 1)
    """
    # count the number of cells that are flooded in both array1 and 2
    idx_both = np.sum(np.logical_and(array1, array2))
    idx_1 = np.sum(array1)
    return float(idx_both)/float(idx_1)


# In[4]:


def false_alarm_rate(array1, array2):
    """
    calculate the false alarm rate based upon 2 boolean maps. (i.e. amount of cells where array2 is True but array1 False)
    """
    # count the number of cells that are flooded in both array1 and 2
    idx_2_only = np.sum(np.logical_and(array2, array1!=1))
    idx_2_total = np.sum(array2)
    
    return float(idx_2_only)/float(idx_2_total)


# In[5]:


def critical_success(array1, array2):
    """
    calculate the critical success rate based upon 2 boolean maps. 
    """
    idx_both = np.sum(np.logical_and(array1, array2))
    idx_either = np.sum(np.logical_or(array1, array2))
    return float(idx_both)/float(idx_either)


# In[6]:


def contingency_map(array1, array2, threshold1=0., threshold2=0.):
    """
    Establish the contingency between array1 and array2.
    Returns an array where 
    1 means only array2 gives a value > threshold1, 
    2 means only array1 gives a values > threshold2,
    3 means array1 gives a value > threshold1, and array2 a value > threshold2
    0 means both arrays do not give a value > threshold1, 2 respectively
    
    function returns the threshold exceedance (0-1) of array 1 and 2, as well as the contingency map
    """
    array1_thres = array1 > threshold1
    array2_thres = array2 > threshold2
    contingency = np.zeros(array1.shape)
    contingency += np.int16(array2_thres)
    contingency += np.int16(array1_thres)*2
    return array1_thres, array2_thres, contingency


# In[7]:


def contingency(bench_d, model_d, bench_thres, model_thres):
    """
    determines hit rate, false alarm ratio, critical success index, and contingency map for a given combination of simulated and observed flood extent.
    """
    
    x_bench = bench_d.width
    y_bench = bench_d.height
    bench_data = bench_d.read(1)
    fill_bench = bench_d.nodata
    extent_bench = bench_d.bounds
    
    x_model = model_d.width
    y_model = model_d.height
    model_data = model_d.read(1)
    fill_model = model_d.nodata
    
    bench_data[bench_data==fill_bench] = 0.
    model_data[model_data==fill_model] = 0.
        
    flood1, flood2, cont_arr = contingency_map(bench_data, model_data, threshold1=bench_thres, threshold2=model_thres)
    
    hr = hit_rate(flood1, flood2)
    far = false_alarm_rate(flood1, flood2)
    csi = critical_success(flood1, flood2)
    return hr, far, csi, cont_arr


# <a id="data"></a>
# # Data
# 
# ## Simulated extent
# 
# Now get the files with boolean maps of simulated flood extent, i.e. 1 is flooded and 0 is not flooded, and open them with rasterio.

# In[8]:


PCR_fo = 'data/PCR_clipped_reprojected_boolean.tiff'


# In[9]:


PCR_d = rio.open(PCR_fo)


# In[10]:


LFP_fo = 'data/LFP_reprojected_boolean.tiff'


# In[11]:


LFP_d = rio.open(LFP_fo)


# In[12]:


CMF_fo = 'data/CMF_clipped_reprojected_boolean.tiff'


# In[13]:


CMF_d = rio.open(CMF_fo)


# In[14]:


flood_maps = {'PCR-GLOBWB':PCR_d, 
              'Lisflood-FP':LFP_d, 
              'CaMa-Flood':CMF_d}


# ## Observed extent
# 
# We now load and open the observed flood extent. We use here an 8 day composite MODIS image.

# In[15]:


OBS_fo = 'data/MODIS_clipped_boolean.tiff'


# In[16]:


OBS_d = rio.open(OBS_fo)


# ## WorldPOP data
# 
# WorldPOP data for Bangladesh was downloaded and resampled and clipped to the area under consideration.

# In[17]:


POP_fo = 'data/bgd_ppp_2020_resampled.tiff'


# In[18]:


POP_d = rio.open(POP_fo)


# <a id="flood_extent"></a>
# # Flood extent
# 
# In a first exploratory step, we have a look at the observed and simulated flood extents.

# In[19]:


fig, axes = plt.subplots(2, 2, figsize=(20,10), sharey=True, sharex=True)
show(OBS_d, ax=axes[0,0], cmap='Oranges')
axes[0,0].set_title('Observed extent')
show(PCR_d, ax=axes[0,1], cmap='Blues')
axes[0,1].set_title('PCR-GLOBWB')
show(LFP_d, ax=axes[1,0], cmap='Blues')
axes[1,0].set_title('Lisflood-FP')
show(CMF_d, ax=axes[1,1], cmap='Blues')
axes[1,1].set_title('CaMa-Flood')
plt.tight_layout()

plt.savefig('out/flood_extents.png', dpi=300)


# What we see here is that the simulated flood extents differ greatly. 
# 
# While PCR-GLOBWB has a somewhat intermediate extent, Lisflood-FP shows the biggest extent. This is most likely due to the fact that the model can simulated 2D floodplain flow and more complex channel-floodplain interactions, also via smaller channels. As outlined above, the flood extent from CaMa-Flood is obtained by static post-processing. What can be seen is that this can lead to problems when for some parts of a river reach the simulated water volume just remains within the river bed while for others not - a very sudden transition between flooded and not-flooded areas.

# ## Contingency analysis
# 
# But how well do the simulated extents match the observations? To understand this, we plot the Contingency maps and determine the values for the hit rate (HR), false alarm ratio (FAR), and critical success index (CSI). We refer to the NHESS publication for an explanation of those concepts.
# 
# In these plots, the color-coding is as follows:
# 
# * blue: simulated extent only
# * red: observed extent only
# * green: both

# In[20]:


cmap = colors.ListedColormap(['blue', 'red', 'green'])
bounds=[0.5, 1.5, 2.5, 3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, axes = plt.subplots(1, 3, figsize=(20,10), sharey=True)

i=0

for key in flood_maps.keys():

    hr, far, csi, cont_arr = contingency(OBS_d, flood_maps[key], 0.5, 0.)

    plot_image = np.ma.masked_where(cont_arr==0, cont_arr)

    img = axes[i].imshow(plot_image, cmap=cmap, vmin=1., vmax=3., extent=(OBS_d.bounds[0], OBS_d.bounds[2], OBS_d.bounds[1], OBS_d.bounds[3]))

    axes[i].set_title('Contingency map {:s}'.format(key))

#     cbar = plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[1, 2, 3], orientation='vertical')
    
    i += 1
    
    print('Model: {:s}'.format(key))
    print('Hit rate: {:f}'.format(hr))
    print('False Alarm rate: {:f}'.format(far))
    print('Critical success index: {:f}'.format(csi))
    print('')

plt.savefig('out/contingency_maps.png', dpi=300)
    
plt.tight_layout()


# It shows that simulating inundation maps can benefit greatly from adding 2D hydrodynamic floodplain flow computations. Validating the downscaled inundation maps from PCR-GLOBWB and CaMa-Flood with the modelled results of Lisflood-FP shows significant deviations. In fact, results insinuate that acceptable representation of inundation patterns as expressed by the CSI can only be achieved by also accounting for floodplain flow and discharge through side channels.
# 
# The differences in HR largely result from simulated inundations along smaller water bodies, especially compared to CaMa-Flood, and from simulating the extent across the entire river floodplain, which is particularly not the case for PCR-GLOBWB. It is for those areas, which may not necessarily be directly adjacent to the main river stem, that downscaling procedures based on volume or water depth distribution curves may not suffice to represent the actual locally relevant flood-triggering processes, leading to a low HR.

# <a id="population"></a>
# # Population
# 
# Let's check out the WorldPOP data in our study area. Seems there is only little population for the biggest part of the area and one bigger settlement in the N-E (guess this bigger settlment is Dhaka).

# In[21]:


plot_image = np.ma.masked_where(POP_d.read(1)<=0, POP_d.read(1))

plt.subplots(1, 1, figsize=(20,10))
img = plt.imshow(plot_image, cmap='Paired', vmin=1., vmax=1200., extent=(POP_d.bounds[0], POP_d.bounds[2], POP_d.bounds[1], POP_d.bounds[3]))
plt.colorbar()
plt.title('WorldPOP population data');

plt.savefig('out/population_data.png', dpi=300)


# ## Casualties
# 
# To assess the impact how the differences in simulated flood extent impact the number of casulaties in this flood event. This is done in a very simple first-order approach, where we overlay inundation maps with population data.
# 
# Note here that this of couse not a realistic value and does not say anyting about actual flood risk in the region!!!
# 
# First, we mask all cells with negative values (often the nodata values) with zeros to obtain sensible results from the multiplications.

# In[22]:


POP_mask = POP_d.read(1) * np.greater(POP_d.read(1), 0.0)


# We can now compute the number of people affected by the inundation event by multiplying the boolean map of the observations with the number of people per cell. This would give us a benchmark value to compare the other values with.

# In[23]:


casualties_arr = OBS_d.read(1) * np.greater(OBS_d.read(1), 0.0) * POP_mask
casualties_sum = np.sum(casualties_arr)

print('Casualties inflicted with observed extent: {:f}'.format(casualties_sum))
print('')


# Let's now do the same with the simulated extents and see how many people would be affected with which model

# In[24]:


print('Casualties inflicted with extent per model')
print('')

fig, axes = plt.subplots(1, 3, figsize=(20,10), sharey=True)

i=0

for key in flood_maps.keys():

    casualties_arr = flood_maps[key].read(1) * np.greater(flood_maps[key].read(1), 0.0) * POP_mask
    casualties_sum = np.sum(casualties_arr)
    
    plot_image = np.ma.masked_where(casualties_arr<=0, casualties_arr)
    
    img = axes[i].imshow(plot_image, cmap='Paired', vmin=1., extent=(OBS_d.bounds[0], OBS_d.bounds[2], OBS_d.bounds[1], OBS_d.bounds[3]))

    axes[i].set_title(format(key))
    
    print('Model: {:s}'.format(key))
    print('People affected: {:f}'.format(casualties_sum))
    print('')
    
    i += 1

plt.savefig('out/people_affected.png', dpi=300)
    
plt.tight_layout()


# We see that the results obtained with the downscaled PCR-GLOBWB model come closest to our benchmark value. This is interesting, because it is not the model performing best in the contingency analysis in terms of CSI!
# 
# Also if the FAR and HR of PCR-GLOBWB is compared with those of the other models, we cannot find a clear connection between the contingency analysis and the number of people affected. This may be because those funtions are determined for the entire study area, whereas the number of people affected is very much defined by model accuracy for a limited region.

# <a id="conclusion"></a>
# # Conclusion
# 
# This small analysis shows us that the model choice has a great influence on not only flood extent accuracy, but also on the number of people affected.
# 
# Such a finding is particularly relevant for flood management plans and flood risk assessments, which often rely heavily on model output. It is clear that there is not this one model outperforming all others, but that some model properties may be more relevant is certain regions than in others. 
# 
# With a large ensemble of flood models available, this work highlights the need for more structured flood model inter-comparison frameworks <cite data-cite="6222060/WE46DM4F"></cite>.
# 
# The results obtaind may lead to questions on how to actually validate flood models. Modelled flood extent is commonly used for validating and calibrating models. But in this case, if we had chosen the model with the most accurate output (expressed as highest CSI), we would have stongly overpredicted the number of people affected compared to the benchmark value.
# 
# And while it remains very important to validate and calibrate flood models over large areas and entire flood events, there may also be the case for additional procedures focussing more on correctly representing flood losses - even if the overall accuracy may be reduced.
# 
# What do you think?

# ## Code
# 
# The GLOFRIM code used for producing the inundation maps can be found [here](https://doi.org/10.5281/zenodo.3364388).
# 
# This notebook and all underlying data is hosted on [GitHub](https://github.com/JannisHoch/shareEGU20) and ready to be forked!

# ## Acknowledgments
# 
# Part of the code for calculating the contingency maps is borrowed from Hessel Winsemius. Many thanks!

# # References
# 
# <div class="cite2c-biblio"></div>

# <div class="cite2c-biblio"></div><img src="pics/license.png" alt="Markdown Monster icon" style="height: 50px;" align="right">
