from owlready2 import get_ontology, sync_reasoner

path = "/home/kautuk/Desktop/Reasoning-work/streaming_reasoning/" # this is the path on the local system
# path = "/tmp/pycharm_project_459/streaming_reasoning/" # this is the path on the server
tbox = get_ontology(path + "tbox.owl").load()


def initiate_reasoning(owl_file, onto_fileobj):
    infered = get_ontology(path + "output" + owl_file + ".owl")
    reasoning_on_file(infered, owl_file, onto_fileobj)


def reasoning_on_file(infered, owl_file, onto_fileobj):
    print("Reasoning on " + owl_file)
    onto = get_ontology("").load(fileobj=onto_fileobj)
    with infered:
        sync_reasoner([onto])
    x = infered.get_instances_of(tbox.ElevatorAbnormalTemperatureEvent)
    y = infered.get_instances_of(tbox.ServerRoomTemperatureEvent)

    print('\n' + owl_file + " --> " + str((len(x), len(y))) + '\n')
    return x, y


''' owl_file = "100_instances.owl"
f = open(datafiles_path + owl_file, "r")
onto_string = f.read()
onto_fileobj = BytesIO(str.encode(onto_string))
print("Type of str.encode(onto_RDD_value) = ", type(str.encode(onto_string)))
print("Type of onto_fileobj = ", type(onto_fileobj))

initiate_reasoning(owl_file, onto_fileobj) '''
