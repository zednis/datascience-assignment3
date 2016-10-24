from datetime import datetime
import netCDF4 as nc
import pandas

df = pandas.read_csv("data/img040_profile.txt", delimiter='\t', names=['parallel distance', 'diffraction intensity'])

dataset = nc.Dataset("rheed.nc", "w", format="NETCDF4")
i = dataset.createDimension("i")

parallel_distance = dataset.createVariable("parallel_distance", 'f4', "i")
parallel_distance.short_name = "parallel distance"

diffraction_intensity = dataset.createVariable("diffraction_intensity", 'f4', "i")
diffraction_intensity.short_name = "diffraction intensity"

parallel_distance[:] = df["parallel distance"].values
diffraction_intensity[:] = df["diffraction intensity"].values

dataset.created = datetime.now().isoformat()
dataset.title = "Reflection High-Energy Electron Diffraction data on graphene sample"
dataset.description = "This data is obtained from Reflection high-energy electron diffraction (RHEED) experiment on graphene sample."
dataset.creator = "Stephan Zednik <zednis@rpi.edu>"
dataset.source = "Jie Cheng <chengj5@rpi.edu>"
dataset.subject = "graphene sample"
dataset.script = "https://github.com/zednis/datascience-assignment3/blob/master/rheed.py"

dataset.close()
