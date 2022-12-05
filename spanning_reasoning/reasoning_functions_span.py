from owlready2 import *
import pandas as pd
import sys
from os import listdir
import time

# python3 reasoning.py 10 -- instruction to run; test.py right?


num_instances = 10  # hard-coded for now

path = "/home/kautuk/Desktop/Reasoning-work/spanning_reasoning/"
datafiles_path = path + "datafiles/" + str(num_instances) + "_instances/"

tbox = get_ontology(path + "extended_tbox.owl").load()  # loading the tbox

default_world.full_text_search_properties.append(comment)
ttp = 3
current_window_ontologies = []  # list of pair-RDDs to store the events


def get_spanning_events(owl_file, onto_fileobj):
    temp_world = World()
    temp_world.full_text_search_properties.append(comment)
    onto = temp_world.get_ontology("").load(fileobj=onto_fileobj)
    spanning_events = temp_world.search(comment=FTS("spanning*"))
    print(spanning_events)
    return spanning_events


def shift_window(infered, owl_file, onto_fileobj):
    # remove last onto, reason on it
    # add current spanning event to remaining in window
    # add onto to window

    while len(current_window_ontologies) >= ttp:
        onto_name, out_of_window_onto = current_window_ontologies.pop(0)  # remove the first event
        with infered:
            sync_reasoner([out_of_window_onto])
        x = infered.get_instances_of(tbox.ElevatorAbnormalTemperatureEvent)
        y = infered.get_instances_of(tbox.ServerRoomTemperatureEvent)
        z = out_of_window_onto.get_instances_of(tbox.Smoke)
        # len(z)!=0 will tell that smoke event has been added to onto and further reasoning can be done on that
        print('\n' + onto_name + " --> " + str([len(x), len(y), len(z), len(tbox.Fire.instances()) != 0]) + '\n')

    for event in get_spanning_events(owl_file):
        spanning_annotation = event.comment.first()
        spanning_range = int(spanning_annotation[spanning_annotation.index("-") + 1:])
        print("------------------", spanning_range)
        spanning_range -= 1  # it is there in current onto
        for onto in current_window_ontologies:
            if spanning_range > 0:
                # onto.s = event
                # print(event.)
                # with onto: # commented this, suggested by Rachna
                #     s = tbox.Smoke(event) # commented this, suggested by Rachna
                spanning_range -= 1

    onto = get_ontology("").load(fileobj=onto_fileobj)
    current_window_ontologies.append((owl_file, onto, onto_fileobj))


def reasoning_on_file(infered, owl_file, onto_fileobj):
    onto = get_ontology("").load(fileobj=onto_fileobj)
    with infered:
        sync_reasoner([onto])
    x = infered.get_instances_of(tbox.ElevatorAbnormalTemperatureEvent)
    y = infered.get_instances_of(tbox.ServerRoomTemperatureEvent)
    z = onto.get_instances_of(tbox.Smoke)
    # len(z)!=0 will tell that smoke event has been added to onto and further resoning can be done on that

    if len(current_window_ontologies) >= ttp:
        current_window_ontologies.pop(0)
        current_window_ontologies.push(onto)

    print('\n' + owl_file + " --> " + str([len(x), len(y), len(z), len(tbox.Fire.instances()) != 0]) + '\n')
    return len(x), len(y), len(z), len(tbox.Fire.instances()) != 0


# df = pd.read_csv('info.csv')
start = time.time()

for owl_file in listdir(datafiles_path):
    print("Got file ---------------", owl_file)
    infered = get_ontology(path + "output" + owl_file + ".owl")
    shift_window(infered, owl_file)

    # file_name = owl_file[:owl_file.index(".owl")]

    # df.loc[df['Sl.No.'] == int(file_name), 'Inferred_e'] = str(e)
    # df.loc[df['Sl.No.'] == int(file_name), 'Inferred_s'] = str(s)
    # df.loc[df['Sl.No.'] == int(file_name), 'Fire'] = fire

end = time.time()
print("Time taken: " + str(end - start) + " seconds")
# df.to_csv("info.csv", index=False)

