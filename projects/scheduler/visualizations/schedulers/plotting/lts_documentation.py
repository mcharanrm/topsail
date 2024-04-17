from collections import defaultdict
import re
import logging
import datetime
import math
import copy

import statistics as stats

import plotly.subplots
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from dash import html

import matrix_benchmarking.plotting.table_stats as table_stats
import matrix_benchmarking.common as common

from . import error_report, report

def register():
    LtsDocumentationReport()


class LtsDocumentationReport():
    def __init__(self):
        self.name = "report: LTS Documentation"
        self.id_name = self.name
        self.no_graph = True
        self.is_report = True

        table_stats.TableStats._register_stat(self)

    def do_hover(self, meta_value, variables, figure, data, click_info):
        return "nothing"

    def do_plot(self, *args):
        header = []
        ordered_vars, settings, setting_lists, variables, cfg = args

        for entry in common.Matrix.all_records(settings, setting_lists):
            header += [html.H1(entry.get_name(variables or [s for s in settings.keys() if s != "stats"]))]
            header += generateOneLtsDocumentationReport(entry)
            header += [html.Hr()]
        return None, header


def generateOneLtsDocumentationReport(entry):
    lts = entry.results.lts

    header = []
    header += [html.H2("metadata")]
    metadata = []

    metadata += [html.Li([html.B("settings:"), html.Ul(
        [html.Li(html.Code([html.B(k), f": {v}"])) for k, v in lts.metadata.settings.__dict__.items()]
    )])]
    metadata += [html.Li([html.B("start:"), html.Code(lts.metadata.start)])]
    metadata += [html.Li([html.B("presets:"), html.Code(", ".join(lts.metadata.presets))])]
    metadata += [html.Li([html.B("config:"), html.Code("(not shown for clarity)")])]

    header += [html.Ul(metadata)]

    header += [html.H2("kpis")]
    kpis = []
    for name, kpi in lts.kpis.items():
        labels = {k:v for k, v in kpi.__dict__.items() if k not in ("unit", "help", "timestamp", "value")}
        labels_str = ", ".join(f"{k}=\"{v}\"" for k, v in labels.items())
        kpis += [html.Li([html.P([html.Code(f"# HELP {name} {kpi.help}"), html.Br(),
                                  html.Code(f"# UNIT {name} {kpi.unit}"), html.Br(),
                                  html.Code(f"{name}{{{labels_str}}} {kpi.value}")])])]

    header += [html.Ul(kpis)]

    return header
