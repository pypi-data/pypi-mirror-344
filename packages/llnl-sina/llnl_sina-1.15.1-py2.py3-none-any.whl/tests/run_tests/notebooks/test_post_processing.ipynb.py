#!/usr/bin/env python
# coding: utf-8

import sina
import sina.utils
import sina.model
import random
import sina.postprocessing

# We'll dump sample data here to create our input file. This json is our "simulation run".
source_path = "my_sample_simulation.json"
# This is the stringified form of what we'll be dumping, a mockup of some minimal
# simulation data. Don't worry about reading it--we'll have it in a clearer form shortly
data_to_dump = """{"records": [{"id": "sample_rec", "type": "sample", "data": {"runtime": {"value": 10.5, "units": "s"}, "user": {"value": "Anna Bob"}, "volume": {"value": [5, 6, 7, 12]}, "mass": {"value": [0.5, 0.5, 0.5, 0.5]}}}], "relationships": []}"""
with open(source_path, 'w') as f:
    f.write(data_to_dump)

# We'll write our data to here. In a real workflow, we may want to write back to the
# source path, or we may want to keep things "versioned", especially if we're still
# developing a workflow. We do the latter here. Use whatever works best for you!
dest_path = "my_sample_simulation_post.json"


# We first load up our "simulation" output json
rec = sina.utils.load_sole_record(source_path)


#################################
#          Adding Data          #
#################################

# Now our simulation data is available as a Python object!
# Let's add that we're post-processing it, just in case
rec.add_data("was_post_processed", True)

# Derived quantities are a common case for post-processing.
# Let's calculate density and add it to our record.
rec.add_data("density", [x / y for x, y in zip(rec.data_values["mass"],
                                               rec.data_values["volume"])])


#################################
#         Updating Data         #
#################################

# We can update existing data too. Let's add a tag.
rec.set_data("user", rec.data_values["user"], tags=["metadata"])

# Or how about a unit conversion? Our code output seconds, but we want milliseconds
rec.set_data("runtime", rec.data_values["runtime"] * 1000, units="ms")


#################################
#          Saving Data          #
#################################

# We're not quite sure about the changes we're making, so we'll save this as
# a different record entirely. You don't always want to do this (ex: if you
# have both of these in a datastore and make a scatterplot on, say, mass,
# it'll find 2x the records to plot), but it's useful in dev.
original_rec_id = rec.id
rec.id = original_rec_id + ("_post")

# Now let's dump this back to the filesystem!
rec.to_file(dest_path)


#################################
#           Verifying           #
#################################

# So, how did we measure up? Let's put both of those in a temporary datastore.
ds = sina.connect()
ds.records.insert([sina.utils.load_sole_record(source_path),
                   sina.utils.load_sole_record(dest_path)])

# Queries only return runs that contain the data we want, so we'll only get the edited one
print("Post-processed record: {}".format(next(ds.records.find_with_data(was_post_processed=True))))

# And of course, our old record still has its pre-edit units
print("Units for {}'s runtime: {}"
      .format(original_rec_id,
              ds.records.get(original_rec_id).data["runtime"]["units"]))
print("Units for {}'s runtime: {}"
      .format(original_rec_id + "_post",
              ds.records.get(original_rec_id + "_post").data["runtime"]["units"]))


# We'll create a brand new Record now, but let's pretend we've just grabbed it from a sina.json output by a code
# It has a number of quantities we're not interested in and don't mind discarding "for good."
# We won't write anything "back" to file, so those quantities are still there if we REALLY need them...
# assuming nothing happens to the file!

# Note that the actual count of data keys isn't meant to indicate "largeness", it's just that we won't need these
# in our imaginary workflow, and have (for whatever reason) decided we want them gone.
junk_terms = ["space", "plant", "floral", "wibbly", "lemon", "core", "tomorrow", "cruft", "analog", "tremendous"]


def make_wasteful_record(idx):
    rec = sina.model.Record(id=f"rec_{idx}", type="wasteful")
    cartesian_data_names = [(x, y) for x in junk_terms for y in junk_terms]
    for datum_name_chunks in cartesian_data_names:
        rec.add_data("_".join(datum_name_chunks), random.random() * 1000)
    return rec


# This record represents what we "really" want.
reduced_rec = sina.model.Record(id="reduced_rec", type="reduced")
reduced_rec.add_data("space_plant", 22)
reduced_rec.add_data("tremendous_cruft", 500)
reduced_rec.add_data("floral_core", 5)
reduced_rec.add_data("not_originally_present", "me!")  # This isn't in our "output" run...we'll come back to it


# And here's our test for the contents in our records. You'll see above that we want floral_core, but don't want lemon_cruft
# We also want to be sure our filter isn't ADDING values (there's a different function if you want to do that)
# Finally, derived_quantity will be relevant in a little bit...
def print_summary(rec):
    print(f"Number of data in {rec.id}: {len(rec.data.keys())}")
    print(f"Value of floral_core: {rec.data.get('floral_core', {'value': 'N/A'})['value']}")
    print(f"Value of lemon_cruft: {rec.data.get('lemon_cruft', {'value': 'N/A'})['value']}")
    print(f"Value of not_present: {rec.data.get('not_originally_present', {'value': 'N/A'})['value']}")
    print(f"Value of derived_quantity: {rec.data.get('derived_quantity', {'value': 'N/A'})['value']}")


wasteful_rec = make_wasteful_record(0)
print("=== PRE-FILTER ===")
print_summary(wasteful_rec)
print("\n=== THE FILTER ===")
print_summary(reduced_rec)

# We'll use Sina's postprocessing library to create a function that'll apply a filter to any record we feed it
# By using reduced_rec as a filter, we can remove all values in wasteful_rec that aren't present in reduced_rec
filter_using_reduced_rec = sina.postprocessing.filter_keep(reduced_rec)
wasteful_rec = filter_using_reduced_rec(wasteful_rec)
print("\n=== POST-FILTER ===")
print_summary(wasteful_rec)


# Let's pretend we ran our code a few more times
waste_recs = [make_wasteful_record(x) for x in range(1, 21)]


# This time, we want to do something like we did in the first cell.
# We just need to make a function that takes a record and returns the edited record.
def add_derived_quantity(rec):
    rec.add_data("derived_quantity", rec.data_values["space_plant"] * rec.data_values["tremendous_cruft"])
    return rec


# Let's also update the type, since we've post-processed them
def update_type(rec):
    rec.type = "reduced"
    return rec


# All that's left to do is ingest them! Our functions will be applied in order. And order does matter here--
# our filtration record doesn't have derived_quantity, but we don't want to edit it out, so we filter THEN add it.
# NOTE: We "remake" our filter function only to provide an example of how it'll look in normal usage

# This isn't an exhaustive tutorial; check out filter_remove (to excise features you don't want), resample_scalar_lists
# (to perform manipulations like downsampling overly-long timeseries to minify records) and more!
ds = sina.connect()
ds.records.insert(waste_recs, [sina.postprocessing.filter_keep(reduced_rec), add_derived_quantity, update_type],
                  # Here's where we allow the Record itself to be edited. Without passing this, only the queryable data in the
                  # database would be altered. Try changing this to True and see the get() at the end!
                  ingest_funcs_preserve_raw=False)

print(f"#recs with a derived_quantity: {len(list(ds.records.find_with_data(derived_quantity=sina.utils.exists())))} (expect 20)")

returned_rec = ds.records.get(f"rec_{random.randint(1, 21)}")
print("\n=== POST-INGEST ===")
print_summary(returned_rec)

