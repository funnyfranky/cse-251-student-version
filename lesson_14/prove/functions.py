"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family_id = 6128784944
request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
person_id = 2373686152
request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def dfs_helper(family_id, tree, visited_families):
    if family_id in visited_families:
        return
    visited_families.add(family_id)
    # Fetch family data
    fam_req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    fam_req.start()
    fam_req.join()
    family_data = fam_req.get_response()
    if not family_data:
        return
    family = Family(family_data)
    tree.add_family(family)
    # Fetch and add husband
    husband_id = family.get_husband()
    if husband_id and not tree.does_person_exist(husband_id):
        husb_req = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
        husb_req.start()
        husb_req.join()
        husb_data = husb_req.get_response()
        if husb_data:
            husband = Person(husb_data)
            tree.add_person(husband)
            if husband.get_parentid():
                dfs_helper(husband.get_parentid(), tree, visited_families)
    # Fetch and add wife
    wife_id = family.get_wife()
    if wife_id and not tree.does_person_exist(wife_id):
        wife_req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
        wife_req.start()
        wife_req.join()
        wife_data = wife_req.get_response()
        if wife_data:
            wife = Person(wife_data)
            tree.add_person(wife)
            if wife.get_parentid():
                dfs_helper(wife.get_parentid(), tree, visited_families)
    # Fetch and add children
    for child_id in family.get_children():
        if not tree.does_person_exist(child_id):
            child_req = Request_thread(f'{TOP_API_URL}/person/{child_id}')
            child_req.start()
            child_req.join()
            child_data = child_req.get_response()
            if child_data:
                child = Person(child_data)
                tree.add_person(child)
def depth_fs_pedigree(family_id, tree):

    # Start the recursive helper
    dfs_helper(family_id, tree, set())

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    # que = queue.Queue()
    # que.put(family_id)

    # while not que.empty():
    #     id = que.get()
    #     # HINTED WE NEED ANOTHER WHILE LOOP
    #     # get family details
    #     # add parents to queue

    q = queue.Queue()
    q.put(family_id)
    visited_families = set()

    while not q.empty():
        current_family_id = q.get()

        if current_family_id in visited_families:
            continue
        visited_families.add(current_family_id)

        # Get family data
        fam_req = Request_thread(f'{TOP_API_URL}/family/{current_family_id}')
        fam_req.start()
        fam_req.join()
        family_data = fam_req.get_response()

        if not family_data:
            continue

        family = Family(family_data)
        tree.add_family(family)

        # Process husband
        husband_id = family.get_husband()
        if husband_id and not tree.does_person_exist(husband_id):
            husb_req = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
            husb_req.start()
            husb_req.join()
            husb_data = husb_req.get_response()
            if husb_data:
                person = Person(husb_data)
                tree.add_person(person)
                # Add husband's parents' family to the queue
                if person.get_parentid():
                    q.put(person.get_parentid())

        # Process wife
        wife_id = family.get_wife()
        if wife_id and not tree.does_person_exist(wife_id):
            wife_req = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
            wife_req.start()
            wife_req.join()
            wife_data = wife_req.get_response()
            if wife_data:
                person = Person(wife_data)
                tree.add_person(person)
                # Add wife's parents' family to the queue
                if person.get_parentid():
                    q.put(person.get_parentid())

        # Process children
        for child_id in family.get_children():
            if not tree.does_person_exist(child_id):
                child_req = Request_thread(f'{TOP_API_URL}/person/{child_id}')
                child_req.start()
                child_req.join()
                child_data = child_req.get_response()
                if child_data:
                    person = Person(child_data)
                    tree.add_person(person)
                    # Child might be part of their own family
                    if person.get_familyid():
                        q.put(person.get_familyid())

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass