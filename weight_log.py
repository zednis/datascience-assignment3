from datetime import datetime
import netCDF4 as nc
import pandas

df = pandas.read_csv("data/weight_log_fitbit.csv")

dataset = nc.Dataset("daily_weight_log.nc", "w", format="NETCDF4")

time = dataset.createDimension("time")

dt_format = "%B %d, %Y at %I:%M%p"
timestamps = [datetime.strptime(x, dt_format).isoformat() for x in df["Timestamp"].values]

timestamp = dataset.createVariable("timestamp", str, "time")
body_weight = dataset.createVariable("body_weight", 'f4', "time")
body_fat = dataset.createVariable("body_fat", 'f4', "time")
lean_mass = dataset.createVariable("lean_mass", 'f4', "time")
bmi = dataset.createVariable("body_mass_index", 'f4', "time")

timestamp.format = "YYYY-MM-DDThh:mm:ss"
timestamp.calendar = "gregorian"
timestamp.short_name = "timestamp"

body_weight.units = "lb"
body_weight.sensor = "Fitbit Aria"
body_weight.short_name = "body weight"

body_fat.sensor = "Fitbit Aria"
body_fat.units = "percentage"
body_fat.sensing_process = "bioimpedance analysis"
body_fat.short_name = "body fat %"

lean_mass.units = "lb"
lean_mass.derived_from = "body weight, body fat"
lean_mass.short_name = "lean mass"

bmi.sensor = "Fitbit Aria"
bmi.units = "kg/m^2"
bmi.derived_from = "body weight, height"
bmi.short_name = "BMI"
bmi.long_name = "body mass index"

# use loop to individually set variable length timestamp strings
for i, t in enumerate(timestamps):
    timestamp[i] = t

body_weight[:] = df["Body Weight"].values
body_fat[:] = df["Body Fat %"].values
lean_mass[:] = df["Lean Mass"].values
bmi[:] = df["BMI"].values

dataset.created = datetime.now().isoformat()
dataset.title = "Weight and Body Composition Measurements"
dataset.description = "Weight and body fat measurements obtained by the subject daily"
dataset.procedure = "For consistency all measurements were made immediately after waking and using the restroom and prior to consuming any food or drink.  No clothing was worn while taking measurements."
dataset.creator = "Stephan Zednik <zednis@rpi.edu>"
dataset.source = "Stephan Zednik <zednis@rpi.edu>"
dataset.subject = "Stephan Zednik"
dataset.script = "https://github.com/zednis/datascience-assignment3/blob/master/weight_log.py"
dataset.urn = "urn:zednik:dataset:C400FD7D-2FFF-43A5-8606-AEB63DE64169"
dataset.keywords = "body weight,body fat,body mass index"

dataset.close()
