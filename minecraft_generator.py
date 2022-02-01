# Generate a map with Perlin noise for altitude


import bpy
import bmesh
import math
import random


world_width = 20
world_length = 10

scene = bpy.context.scene
original_cube = scene.objects['Cube.000']
random.seed()


original_collection = scene.collection.children.get("Original_cubes")

clones_collection = scene.collection.children.get("Clones")

def remove_clones():
    unselect_everything()
    for object in bpy.data.collections["Clones"].objects:
        bpy.data.objects[object.name].select_set(True)
    bpy.ops.object.delete()
    print("Deletion done.")
     

def unselect_everything():
    bpy.ops.object.select_all(action='DESELECT')
    

def get_vertices_avg_x(object):
    sumX = 0
    nb_vertices = 0
    for vertex in object.data.vertices:
        sumX = sumX + vertex.co.x
        nb_vertices = nb_vertices + 1
    return sumX / nb_vertices

def get_vertices_avg_y(object):
    sumY = 0
    nb_vertices = 0
    for vertex in object.data.vertices:
        sumY = sumY + vertex.co.y
        nb_vertices = nb_vertices + 1
    return sumY / nb_vertices

def create_clones_batch():
    bpy.context.view_layer.objects.active = original_cube
    bpy.data.objects[original_cube.name].select_set(True)
    
    print("First modifier")
    # First modifier: array along X
    bpy.ops.object.modifier_add(type='ARRAY')
    original_cube.modifiers["Array"].count = world_width
    bpy.ops.object.modifier_apply(modifier="Array")
    
    print("Second modifier")
    # Second modifier: array along Y
    bpy.ops.object.modifier_add(type='ARRAY')
    original_cube.modifiers["Array"].count = world_length
    original_cube.modifiers["Array"].relative_offset_displace[0] = 0
    original_cube.modifiers["Array"].relative_offset_displace[1] = 1
    bpy.ops.object.modifier_apply(modifier="Array")

    # Place the clones in the Clones collection
    clones_collection.objects.link(original_cube)
    original_collection.objects.unlink(original_cube)
    # Separate individual clones
    original_cube.select_set(True)
    bpy.ops.mesh.separate(type='LOOSE')
    # Move original cube back to Original_cubes collection
    original_collection.objects.link(original_cube)    
    clones_collection.objects.unlink(original_cube)    

    print("Cubes for altitude")        
    # Creating cube stacks to match the altitude
    for object in bpy.data.collections["Clones"].objects:
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.modifier_add(type='ARRAY')
        
        # Extract coordinates from vertices
        x = get_vertices_avg_x(object)
        y = get_vertices_avg_y(object)
        object.modifiers["Array"].count = perlin_generator.get_value(x, y)
        object.modifiers["Array"].relative_offset_displace[0] = 0
        object.modifiers["Array"].relative_offset_displace[2] = 1
    print("Done.")

class PerlinGenerator:
    grid_size = 10
    
    def get_value(self, x, y):
        # default value for testing purposes:
        return (int(x)%4) + (int(y)%3)
        

perlin_generator = PerlinGenerator()

remove_clones()
create_clones_batch()