import base64
import datetime
import io
import os
import dash_html_components as html
import dash_table
import pandas as pd

from preprossor import Preporcessor, filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations

AICore = Preporcessor([filter_exclam, filter_bad_signs, filter_roman, filter_bad_signs, filter_abb, filter_stations])



