#!/usr/bin/env python
# coding: utf-8

import sina
import sina.utils
from sina.model import Record, Relationship

msub_rec = Record(id="msub_1", type="msub")
msub_rec.add_data("machine", "quartz")
msub_rec.add_data("node", 49)

run_1_rec = Record(id="run_1", type="foo_sim_run")
run_1_rec.add_data("etot", 1983.23)

run_2_rec = Record(id="run_2", type="foo_sim_run")
run_2_rec.add_data("etot", 2092.45)

recs_to_insert = [msub_rec, run_1_rec, run_2_rec]
ds = sina.connect()
ds.records.insert(recs_to_insert)

print("Inserted: {}".format(", ".join(x.id for x in recs_to_insert)))


predicate = "submits"

# Note how we specify subject_id=... !
# This is an unfortunate holdover from Sina's early days, as object_id was written as the first arg.
# While easy to correct, swapping the order to the "proper" one (subject_id first) would
# constitute an API break, and is thus being saved for a major update.
msub_rec_1_rel = Relationship(subject_id=msub_rec.id, predicate=predicate, object_id=run_1_rec.id)
msub_rec_2_rel = Relationship(subject_id=msub_rec.id, predicate=predicate, object_id=run_2_rec.id)

rels_to_insert = [msub_rec_1_rel, msub_rec_2_rel]
# ds.relationships, not ds.records!
ds.relationships.insert(rels_to_insert)
print("Inserted: {}".format(", ".join("relationship between {} & {}"
                                      .format(x.subject_id, x.object_id) for x in rels_to_insert)))


print("Relationships with {} as the subject_id:\n{}"
      .format(msub_rec.id,
              "\n".join(str(x) for x in ds.relationships.find(subject_id=msub_rec.id))))
print("\nRelationships where {} is the subject and {} is the object:\n{}"
      .format(msub_rec.id, run_1_rec.id,
              "\n".join(str(x) for x in ds.relationships.find(subject_id=msub_rec.id, object_id=run_1_rec.id))))
print("\nRelationships with a predicate of \"{}\":\n{}"
      .format(predicate,
              "\n".join(str(x) for x in ds.relationships.find(predicate=predicate))))


run_2_msub = ds.relationships.find(predicate="submits", object_id=run_2_rec.id)[0].subject_id

print("Record {} was run on node {}"
      .format(run_2_rec.id,
              ds.records.get(run_2_msub).data_values["node"]))

