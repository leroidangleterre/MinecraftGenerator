# Generate a map with Perlin noise for altitude


import bpy
import random


world_width = 10
world_length = 10

scene = bpy.context.scene
original_cube = scene.objects['Cube.000']
random.seed()


original_collection = scene.collection.children.get("Original_cubes")
print("coll_target: " + str(original_collection))

clones_collection = scene.collection.children.get("Clones")
print("clones_collection: " + str(clones_collection))

def remove_clones():
    print("Selecting for deletion")
    for object in bpy.data.collections["Clones"].objects:
        bpy.data.objects[object.name].select_set(True)
    print("Selecting for deletion done. Deleting...")
    bpy.ops.object.delete()
    print("Deletion done.")
     

def unselect_everything():
    bpy.ops.object.select_all(action='DESELECT')
    #    for object in scene.objects:
    #        bpy.data.objects[object.name].select_set(False)
        

def clone_cubes():
    print("Cloning cubes...")
    nb_steps = 10    
    
    for x in range(int(-world_width/2), int(world_width/2+1)):
        print("   Cloning row " + str(x))
        for y in range(int(-world_length/2), int(world_length/2+1)):
            
            unselect_everything()

            max_z = 0.5 + random.randint(1, 4)
            
            for z in range(0, int(max_z)):
                # Clone the original cube
                bpy.context.view_layer.objects.active = original_cube
                bpy.data.objects[original_cube.name].select_set(True)
                bpy.ops.object.duplicate(linked=True)
                clone = bpy.context.view_layer.objects.active
                clone.location = (x, y, z)
                # Move clone to the clones collection:
                clones_collection.objects.link(clone)
                original_collection.objects.unlink(clone)
    print("Cloning done.")

remove_clones()
clone_cubes()
