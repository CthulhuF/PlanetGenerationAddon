bl_info = {
    "name": "Planet Generation Panel",
    "author": "Voznyuk Anton",
    "version": (0, 0, 2),
    "blender": (3, 2, 0),
    "location": "Properties > Scene Properties",
    "description": "Another Noise Tool: Textured Version",
    "warning": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty

# Define global variables for using it in props
obj_name = ''
t_name = ''
atmo_name = ''
water_name = ''


def add_planet_surface(context):
    bpy.ops.mesh.primitive_round_cube_add(radius=1, arc_div=128)
    global obj_name
    obj_name = bpy.data.objects.keys()[-1]
    base_geometry = bpy.data.objects[obj_name]

    bpy.ops.texture.new()
    global t_name
    t_name = bpy.data.textures.keys()[-1]
    bpy.data.textures[t_name].type = 'DISTORTED_NOISE'
    bpy.data.textures[t_name].noise_basis = 'IMPROVED_PERLIN'
    bpy.data.textures[t_name].noise_distortion = 'VORONOI_F4'

    modifier = base_geometry.modifiers.new(name="Displace", type='DISPLACE')
    modifier.texture = bpy.data.textures[t_name]
    modifier.strength = 0.1
    bpy.ops.object.shade_smooth()


class AddOperator(bpy.types.Operator):
    """Executes the function which creates a planet geometry"""
    bl_idname = "object.add_operator"
    bl_label = "Add Planet Surface"

    def execute(self, context):
        add_planet_surface(context)

        return {'FINISHED'}


def add_planet_water(context):
    bpy.ops.mesh.primitive_round_cube_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False,
                                          radius=0.96, size=(0.01, 0.01, 0.01), arc_div=40)
    bpy.ops.object.shade_smooth()
    global water_name
    water_name = bpy.data.objects.keys()[-1]


class AddWater(bpy.types.Operator):
    """Executes the function which creates a planet water"""
    bl_idname = "object.add_water_operator"
    bl_label = "Add Planet Water"

    def execute(self, context):
        add_planet_water(context)

        return {'FINISHED'}


def add_planet_atmoshpere(context):
    bpy.ops.mesh.primitive_round_cube_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False,
                                          radius=1.1, size=(0.01, 0.01, 0.01), arc_div=40)
    global atmo_name
    atmo_name = bpy.data.objects.keys()[-1]


class AddAtmosphere(bpy.types.Operator):
    """Executes the function which creates a planet atmoshpere"""
    bl_idname = "object.add_atmosphere_operator"
    bl_label = "Add Planet Atmosphere"

    def execute(self, context):
        add_planet_atmoshpere(context)

        return {'FINISHED'}


def apply_planet_surface(context):
    bpy.ops.object.modifier_apply(modifier='Displace')


class ApplyOperator(bpy.types.Operator):
    """Executes the function which applies distortion modifier"""
    bl_idname = "object.apply_operator"
    bl_label = "Apply Planet Surface"

    def execute(self, context):
        apply_planet_surface(context)

        return {'FINISHED'}


class PlanetPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Planet Generation Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        row = layout.row()
        row.label(text="Planet Settings", icon='MESH_UVSPHERE')
        col = layout.column

        try:
            texture = bpy.data.textures[t_name]
            object = bpy.data.objects[obj_name]

            row.operator("object.apply_operator", icon='ERROR')
            split = layout.split()
            col = split.column(align=True)
            col.label(text="Surface Settings:")
            col.prop(texture, "distortion", text='Shape')
            col.prop(texture, "noise_scale", text='Noise Scale')
            col.prop(texture, "intensity", text='Altitude')
            col.prop(texture, "contrast", text='Altitude Difference')
            split = layout.split()
            col = split.column()
            col.prop(object, "scale", text='Planet Size')
        except KeyError:
            split = layout.split()
            row = layout.row()

            row.operator("object.add_operator", icon='RNDCURVE')

        try:
            water = bpy.data.objects[water_name]
            split = layout.split()
            col.prop(water, "scale", text='Water Level')
        except KeyError:
            split = layout.split()
            row = layout.row()
            row.operator("object.add_water_operator", icon='MOD_FLUIDSIM')

        try:
            atmosphere = bpy.data.objects[atmo_name]
            split = layout.split()
            col.prop(atmosphere, "scale", text='Atmosphere Level')
        except KeyError:
            split = layout.split()
            row = layout.row()
            row.operator("object.add_atmosphere_operator", icon='PROP_CON')


CLASSES = [
    AddOperator,
    ApplyOperator,
    PlanetPanel,
    AddWater,
    AddAtmosphere,
]


def register():
    for another_class in CLASSES:
        bpy.utils.register_class(another_class)


def unregister():
    for another_class in reverse(CLASSES):
        bpy.utils.unregister_class(another_class)


if __name__ == "__main__":
    register()
