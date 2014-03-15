# Module for extracting environmental data values for biological sites
# setwd("~/Dropbox/Research/SNEB")
library(dismo)

bbs_locs = read.csv("./data/bbs_locations.csv")
coordinates(bbs_locs) = c("long", "lat")

bbs_env = data.frame(bbs_locs)

bioclim_data = getData("worldclim", var = "bio", res = 2.5, path="./data/")
bioclim_bbs_vals = extract(bioclim_data, bbs_locs)
bbs_env = cbind(bbs_env, data.frame(bioclim_bbs_vals))
write.csv(bbs_env, file="./data/bbs_env_data.csv" )
