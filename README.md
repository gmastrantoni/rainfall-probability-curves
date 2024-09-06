# rainfall probability curves
 Hydrological analysis of maximum rainfall intensity data to evaluate the return period of heavy rainfalls for different durations. 

## Project Overview
 
 A statistical analysis of maximum rainfall intensity data was performed on daily and hourly data, to evaluate the return period of heavy rainfalls for different durations. The hydrological–statistical analysis of the maximum values requires the cumulative rainfall at different time intervals to calculate the rainfall probability curves. Daily and hourly rainfall data were used to calculate cumulative rainfalls over the territory of the municipality of Rome for time stages of 1, 2, 5, 10, 20, 30, 60, 90,120 and 180 days and 1, 3, 6, 12 and 24-h, respectively. The generalised extreme value (GEV) distribution (Jenkinson 1955), widely used in extreme event frequency analysis (Fowler et al. 2003), was adopted, which follows the following function:

 $$F(x)=\exp\{-(1+\xi\frac{x-\mu}{\sigma})^{-1/\xi}\}$$
 
 where μ, σ and ξ are referred to as the location, scale and shape parameters, respectively. These parameters have been defined by applying the probability-weighted moments (PWM) method (Hosking et al. 1985) based on the maximum values of the above-mentioned rainfall time periods available from the dataset. First, the RPs of each considered variable were obtained by inverting the probability function. Then, the obtained cumulative rainfall value was fitted by a power law distribution to build the rainfall probability curves.
 The code provided in this repository was used to derive rainfall probability curve for several rain gauge within the Municipality of Rome, Italy, which were then associated with landslide occurrence.
 The published work can be found here: [https://doi.org/10.1007/s10346-023-02095-7](https://doi.org/10.1007/s10346-023-02095-7)

 Please cite our work in case you decide to use our codes: *Esposito, C., Mastrantoni, G., Marmoni, G.M. et al. From theory to practice: optimisation of available information for landslide hazard assessment in Rome relying on official, fragmented data sources. Landslides 20, 2055–2073 (2023). https://doi.org/10.1007/s10346-023-02095-7*


## License
 This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
 
 Please cite the published work when using this repository [https://doi.org/10.1007/s10346-023-02095-7](https://doi.org/10.1007/s10346-023-02095-7)

## Contact

 Giandomenico Mastrantoni - giandomenico.mastrantoni@uniroma1.it

 Project Link: []