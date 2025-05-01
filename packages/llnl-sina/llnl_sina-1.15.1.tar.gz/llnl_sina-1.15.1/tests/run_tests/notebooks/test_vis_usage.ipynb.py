#!/usr/bin/env python
# coding: utf-8

import random
import warnings

import sina
from sina.visualization import Visualizer
from sina.model import CurveSet

import matplotlib.pyplot as plt
plt.style.use('dark_background')

#########################
# %matplotlib notebook
#########################

# Using interactive visualizations without setting the notebook mode would usually print warnings.
# We silence them here to keep things friendly to web readers.
warnings.filterwarnings("ignore")

ds = sina.connect()
record_handler = ds.records

print("Connection is ready!")


possible_mode = ["quick", "standard", "test", "high-def"]
possible_machine = ["Quartz", "Catalyst", "local", "Sierra", "Lassen", "Ruby"]

num_data_records = 100

for val in range(0, num_data_records):
    # Our sample "code runs" are mostly random data
    record = sina.model.Record(id="rec_{}".format(val), type="foo_type")
    record.add_data('total_energy', random.randint(0, 1000) / 10.0)
    record.add_data('start_time', 0)
    record.add_data('elapsed_time', random.randint(1, 200))
    record.add_data('initial_volume', val)
    record.add_data('final_volume', val * random.randint(1, int(num_data_records / 5)))
    record.add_data('num_procs', random.randint(1, 4))
    record.add_data('mode', random.choice(possible_mode))
    record.add_data('machine', random.choice(possible_machine))
    record.add_data('fibonacci_scramble', random.sample([1, 1, 2, 3, 5, 8, 13], 7))
    cs1 = CurveSet("quick_sample")
    cs1.add_independent("time", [1, 2, 3, 4])
    cs1.add_dependent("local_density", random.sample(range(1, 10), 4))
    cs1.add_dependent("est_overall_density", random.sample(range(1, 10), 4))
    record.add_curve_set(cs1)
    cs2 = CurveSet("slow_sample")
    cs2.add_independent("longer_timestep", [2, 4])
    cs2.add_dependent("overall_density", random.sample(range(1, 10), 2))
    record.add_curve_set(cs2)
    if random.randint(1, 6) == 6:
        record.add_file("{}_log.txt".format(val))
    record_handler.insert(record)

print("{} Records have been inserted into the database.".format(num_data_records + 1))


vis = Visualizer(ds)

# A histogram of string data
# The final .display() forces a redraw, and is included only for the sake of the online documentation, to ensure
# it displays. The visualizer automatically shows graphs you make; you usually won't need display()!
vis.create_histogram(x="machine").display()

# A 2d histogram with both scalar and string data
vis.create_histogram(x="machine", y="final_volume").display()


# Enabling interactive mode
interactive_hist = vis.create_histogram(x="machine", y="final_volume", interactive=True)
# The additional "show" calls are also for the sake of the online documentation. You can leave them off if you're
# doing things locally; it's essentially half of a display() call.
interactive_hist.fig.show()


interactive_scatter = vis.create_scatter_plot(x="initial_volume", y="final_volume", z="elapsed_time", color_val="total_energy", interactive=True)
interactive_scatter.fig.show()


fig, ax = plt.subplots(1, 1, figsize=(8, 4))
settings = {"cmap": "magma", "alpha": 0.25}
vis.create_scatter_plot(fig=fig, ax=ax,
                        title="My Cool Graph of Initial vs. Final Volume",
                        x="initial_volume", y="final_volume",
                        color_val="total_energy",
                        matplotlib_options=settings).display()
ax.set_xlabel("Final Volume (m^3)")
_ = ax.set_ylabel("Initial Volume (m^3)")  # The _ = silences some Jupyter text output


config_hist = vis.create_histogram("machine", selectable_data=["final_volume", "machine"], interactive=True,
                                   matplotlib_options={"color": "darkgreen"})
config_hist.fig.show()


non_constant_data = vis.get_contained_data_names(filter_constants=True)

var_hist = vis.create_histogram("final_volume", "total_energy", selectable_data=non_constant_data["scalar"], interactive=True)
var_hist.fig.show()


# You can pass id_pool at the Visualizer level, or per visualization.
# curve_vis = Visualizer(ds, id_pool=["rec_1", "rec_2", "rec_3"])

curve_plot = vis.create_line_plot(x="time", y="local_density", curve_set="quick_sample", interactive=True,
                                  id_pool=["rec_1", "rec_2", "rec_3"], label="Total energy {total_energy} on machine {machine}",
                                  include_rec_id_in_label=False)
curve_plot.fig.show()


surface_plot = vis.create_surface_plot(x="initial_volume", y="elapsed_time", z="final_volume", interactive=True)
surface_plot.fig.show()


get_ipython().run_line_magic('matplotlib', 'notebook')
violin_box_plot = vis.create_violin_box_plot(x="final_volume", interactive=True)
violin_box_plot.fig.show()


get_ipython().run_line_magic('matplotlib', 'notebook')
pdf_cdf_plot = vis.create_pdf_cdf_plot(x="final_volume", interactive=True)
pdf_cdf_plot.fig.show()




