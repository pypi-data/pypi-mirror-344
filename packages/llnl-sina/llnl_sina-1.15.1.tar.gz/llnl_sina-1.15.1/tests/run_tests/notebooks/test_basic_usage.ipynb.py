#!/usr/bin/env python
# coding: utf-8

import json
import random

import sina
from sina.model import Record, generate_record_from_json
from sina.utils import DataRange, has_all, has_any, any_in, all_in

simple_record_structure = {
    # The id uniquely identifies the run. It's often something like timestamp+UUID
    "id": "my_example_breakfast_simulation",

    # The type helps us categorize runs, in case there's several types of "thing" in the datastore.
    # For example, you might have runs plus information from the msubs that submitted them ("type": "msub")
    "type": "breakfast_sim_run",

    # Data is the meat and potatoes of the run. These are your inputs, outputs, metadata etc. that allow you to
    # select a run from the pile. For example, thanks to this data block, we'd be able to pull this record back if
    # we asked for all runs with an omelette_count > 1.
    "data": {"egg_count": {"value": 10},
             "omelette_count": {"value": 3},
             # In addition to a value, entries can have units and tags...we'll hold off for now
             "flavor": {"value": "tasty!"}}
    # There's other sections we can have in a record (ex: curve_sets), but we'll keep it simple for now!
}

simple_record = generate_record_from_json(simple_record_structure)

print("Created a basic record!")


possible_maintainers = ["John Doe", "Jane Doe", "Gary Stu", "Ann Bob"]


def generate_run(idx):
    # Our sample "code runs" are mostly random data. We'll generate some inputs...
    record = Record(id="rec_{}".format(idx), type="foo_prod_run")
    record.add_data('initial_density', random.randint(10, 1000) / 10.0, units='g/cm^3')
    record.add_data('num_procs', random.randint(1, 4))
    record.add_data('maintainer', random.choice(possible_maintainers), tags=["personnel"])
    # Pretend we ran a simulation in here...and add the outputs and artifacts.
    if random.randint(1, 6) == 6:
        record.add_file("{}_log.txt".format(idx))
    record.add_data('final_volume', random.random() * 100)
    return record


print("Defined a function for generating more records!")

test_rec = generate_run(0)
print("Accessing randomly-generated test record {}. Its initial_density is: {}.\nRe-running this cell will reroll this value."
      .format(test_rec.id,
              test_rec.data["initial_density"]["value"]))


# The default (read: without an argument) behavior of sina.connect() is to connect to an in-memory SQLite database.
# These are temporary, wiped from memory once they're closed. Good for tutorials, not so good for data storage!
# If you'd like to create a proper file, just provide the filename as an arg: sina.connect("my_db.sqlite")
# You can also pass the URL to a database such as MySQL or MariaDB.
ds = sina.connect()
print("Connection is ready!")


ds.records.insert(simple_record)
print("The simple Record has been inserted into the datastore")

num_to_generate = 500

for record_idx in range(0, num_to_generate):
    ds.records.insert(generate_run(record_idx))

print("{} randomly-generated Records have been inserted into the datastore.".format(num_to_generate))


maintainer_to_query = "John Doe"

print("Found {} runs with {} listed as their maintainer".format(
    len(list(ds.records.find_with_data(maintainer=maintainer_to_query))),
    maintainer_to_query))


# Let's throw an extra record in there to be sure we have at least one match!
template_rec = Record(id="john_latest", type="foo_prod_run")
template_rec.add_data("final_volume", 6)
template_rec.add_data("initial_density", 6, units="cm^3")
template_rec.add_data("maintainer", "John Doe")

ds.records.insert(template_rec)

# John's diagnostic run! "Coincidentally" looks very similar to the above. We don't want this one, though!
# Since we're changing the id, the datastore will see this as an entirely new run.
template_rec.id = "dont_fetch_me"
template_rec.type = "foo_diagnostic"
ds.records.insert(template_rec)

# Now we prepare a dictionary of criteria. This is equivalent to:
# find_with_data(maintainer="John Doe", final_volume=DataRange(max=6, max_inclusive=True))
# However, find() is more flexible than find_with_data()--we pass data criteria as a dict so we can combine them
# with other things (here, record types). Combined queries tend to be more efficient!
target_data = {"maintainer": "John Doe",
               "final_volume": DataRange(max=6, max_inclusive=True)}

john_low_volume = ds.records.find(data=target_data, types="foo_prod_run", ids_only=True)

print("John Doe's low-volume production runs: {}".format(', '.join(john_low_volume)))


ds.records.delete("dont_fetch_me")


# John wants the 3 Records with the lowest volumes.
runs_with_lowest_volumes = ds.records.find_with_min("final_volume", 3)
print("The runs with the lowest volume:")
for run in runs_with_lowest_volumes:
    print("{}: {} (maintainer: {})".format(run.id,
                                           run.data["final_volume"]["value"],
                                           run.data["maintainer"]["value"]))


# First we get the data we'll need
record_data = ds.records.get_data(["final_volume", "initial_density"])
low_mass_records = set()

# Then we go entry-by-entry, calculating the mass associated with each record id
# We'll use this to assemble a set of runs with mass < 45
for rec_id, data_dict in record_data.items():
    mass = data_dict["initial_density"]["value"] * data_dict["final_volume"]["value"]
    if mass < 45:
        low_mass_records.add(rec_id)
print("Low-mass runs: {}".format(low_mass_records))

# Now that we have our set of low mass runs, we'll intersect it with the set of John's runs
john_runs = list(ds.records.find_with_data(maintainer="John Doe"))
print("John's low-mass runs: {}".format(low_mass_records.intersection(john_runs)))


target_num_procs = 1

ann_runs = ds.records.find(data={"num_procs": target_num_procs},
                           types=["foo_prod_run"],
                           file_uri="%_log.txt",
                           ids_only=True)

print("Ann's target runs: {}".format(list(ann_runs)))


# Records expressed as JSON strings. We expect records 1 and 3 to match our query.
record_1 = """{"id": "list_rec_1",
               "type": "list_rec",
               "data": {"options_active": {"value": ["quickrun", "verification", "code_test"]},
                        "velocity": {"value": [0.0, 0.0, 0.0, 0.0, 0.0]}},
               "user_defined": {"mixed": [1, 2, "upper"]}}"""
record_2 = """{"id": "list_rec_2",
               "type": "list_rec",
               "data": {"options_active": {"value": ["quickrun", "distributed"]},
                        "velocity": {"value": [0.0, -0.2, -3.1, -12.8, -22.5]}},
               "user_defined": {"mixed": [1, 2, "upper"],
                                "nested": ["spam", ["egg"]]}}"""
record_3 = """{"id": "list_rec_3",
               "type": "list_rec",
               "data": {"options_active": {"value": ["code_test", "quickrun"]},
                        "velocity": {"value": [0.0, 1.0, 2.0, 3.0, 4.1]}},
               "user_defined": {"nested": ["spam", ["egg"]],
                                "bool_dict": {"my_key": [true, false]}}}"""

for record in (record_1, record_2, record_3):
    ds.records.insert(generate_record_from_json(json.loads(record)))
print("3 list-containing Records have been inserted into the database.\n")

# Find all the Records that have both "quickrun" and "code_test" in their options_active
quicktest = ds.records.find_with_data(options_active=has_all("quickrun", "code_test"))

# Get those Records and print their id, value for options_active, and the contents of their user_defined.\n",
print("Records whose traits include 'quickrun' and 'code_test':\n")
for id in quicktest:
    record = ds.records.get(id)
    print("{} traits: {} | user_defined: {}".format(id,
                                                    ', '.join(record['data']['options_active']['value']),
                                                    str(record['user_defined'])))


match_has_any = list(ds.records.find_with_data(options_active=has_any("quickrun", "code_test")))
print("Records whose traits include 'quickrun' and/or 'code_test': {}".format(', '.join(match_has_any)))


match_all_in = list(ds.records.find_with_data(velocity=all_in(DataRange(min=0, max=0, max_inclusive=True))))
print("Records where velocity never changed from zero: {}"
      .format(', '.join(match_all_in)))


match_any_in = list(ds.records.find_with_data(velocity=any_in(DataRange(min=0, min_inclusive=False))))
print("Records that had a velocity greater than zero at some point: {}"
      .format(', '.join(match_any_in)))


curve_rec = Record("curve_rec", "curve_rec")
# Note that similar methods (ex: add_file()) exist for other
# types of record info. Raw JSON is used in this notebook
# for at-a-glance readability, but the utility methods
# are generally recommended for "real" code.
sample_curve_set = curve_rec.add_curve_set("sample_curves")
sample_curve_set.add_independent("time", [0, 1, 2])
sample_curve_set.add_dependent("amount", [12, 14, 7])

ds.records.insert(curve_rec)
rec_with_curve_id = ds.records.find_with_data(amount=any_in(DataRange(min=12)))
print('Records with an "amount" >= 12 at some point: {}'
      .format(list(rec_with_curve_id)))


library_data_rec = """{"id": "library_rec",
                       "type": "library_rec",
                       "data": {"runtime": {"value": 12}},
                       "library_data": {
                           "outer_lib": {
                               "data": {"runtime": {"value": 10}},
                               "library_data": {
                                   "inner_lib": {
                                       "data": {"runtime": {"value": 4}}}}}}}"""
ds.records.insert(generate_record_from_json(json.loads(library_data_rec)))

runtimes = ds.records.get_data(["runtime", "outer_lib/inner_lib/runtime"])
print('Runtimes of the record itself, plus that of "inner_lib":')
for key in runtimes["library_rec"].keys():
    print(key, runtimes["library_rec"][key]["value"])


ds.close()


with sina.connect() as ds:
    # Since we closed the connection above, sqlite dropped the database and we created a new one.
    # We need to re-populate it.
    # This only happens with in-memory databases, of course! You're probably not using one.
    for record in (record_1, record_2, record_3):
        # We'll re-insert the records from List Data and Querying Them
        ds.records.insert(generate_record_from_json(json.loads(record)))
    print(list(ds.records.find_with_data(velocity=any_in(DataRange(min=-10, max=-5)))))
# Once we exit the context, since it's an in-memory db, it's once again dropped.

