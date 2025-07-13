
from addict import Dict
star = Dict(
{
	"m": {
		"Xylos": {
			"mass": 0.148, # in solar mass
			"radius": 0.189, # in solar mass
			"age": 2685 # in billion years
		}
	},
	"k": None,
	"g": None,
	"f": {
		"Fertumi": {
			"mass": 1.48, # in solar mass
			"radius": 1.29, # in solar mass
			"age": 2.71 # in billion years
		},
		"Greggab": {
			"mass": 1.26,
			"radius": 1.05,
			"age": 3.32
		}
	},
	"a": None,
	"b": None,
	"o": {
		None:{
			"mass": 20.34, # in solar mass
			"radius": 9.86, # in solar mass
			"age": 0.00967 # in billion years
		}
	},
}
)
regular_star_type = list(['o', 'b', 'a', 'f', 'g', 'k', 'm'])
brown_dwarf = list(["l", 't', "y"])

def check_star(sel_type):
	if sel_type in (regular_star_type + brown_dwarf):
		# Directly get the dictionary for the selected type
		star_names = star.get(sel_type)
		print(f"Select a Star ({sel_type.capitalize()}-Type)")
		if star_names:
			for name, info in star_names.items():
				print(f"Star Button")
				print(f"Star Info")
				print('unnamed' if name is None else name)
				for key, value in info.items():
					if key == "mass":
						print(f"{key}: {value} M☉")
					elif key == "radius":
						print(f"{key}: {value} R☉")
					elif key == "age":
						print(f"{key}: {value} By")
		else:
			print('No Star Available')
	else:
		raise Exception("Invalid star type")

check_star("f")