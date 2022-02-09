import sys
from maps_api.geocoder import *

toponym_to_find = " ".join(sys.argv[1:])

ll, spn = get_ll_spn(toponym_to_find)
show_map(ll, spn, add_params={"pt": f"{ll},pm2rdm"})
