# This code generates a complex 3D surface and a moving tangent plane.

from manim import *
import numpy as np

class MovingTangentPlane(ThreeDScene):
    def construct(self):
        # Define the surface function
        def surface_function(u, v):
            return np.array([
                u,
                v,
                np.sin(u) + np.cos(v)
            ])

        # Define the partial derivatives
        def partial_u(u, v):
            return np.array([
                1,
                0,
                np.cos(u)
            ])

        def partial_v(u, v):
            return np.array([
                0,
                1,
                -np.sin(v)
            ])

        # Define the cross product for the normal vector
        def normal_vector(u, v):
            return np.cross(partial_u(u, v), partial_v(u, v))

        # Surface parameters
        u_range = [-3, 3]
        v_range = [-3, 3]

        # Create the surface
        surface = Surface(
            surface_function,
            u_range=u_range,
            v_range=v_range,
            checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 15),
        )

        # Initial point for the tangent plane
        u_val = -2
        v_val = -2

        # Function to create the tangent plane
        def create_tangent_plane(u, v):
            point = surface_function(u, v)
            normal = normalize(normal_vector(u, v))  # Normalize the normal vector

            # Create two vectors orthogonal to the normal to span the plane
            vector1 = partial_u(u, v)
            vector2 = partial_v(u, v)

            # Define the tangent plane function
            def tangent_plane_function(x, y):
                return point + x * vector1 + y * vector2

            tangent_plane = Surface(
                tangent_plane_function,
                u_range=[-1, 1],
                v_range=[-1, 1],
                resolution=(5, 5),
                fill_opacity=0.5,
                stroke_width=0.5,
                fill_color=GREEN,
                stroke_color=GREEN
            )
            return tangent_plane

        # Create initial tangent plane
        tangent_plane = create_tangent_plane(u_val, v_val)

        # Create a dot to mark the point of tangency
        tangent_point = Dot3D(surface_function(u_val, v_val), color=YELLOW)

        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(surface, tangent_plane, tangent_point)
        self.begin_ambient_camera_rotation(rate=0.2)  # Add subtle camera rotation

        # Animation: Move the tangent plane
        def update_tangent_plane(mob, alpha):
            u = interpolate(u_range[0], u_range[1], alpha)
            v = interpolate(v_range[0], v_range[1], alpha)
            new_plane = create_tangent_plane(u, v)
            mob.become(new_plane)
            return mob

        def update_tangent_point(mob, alpha):
             u = interpolate(u_range[0], u_range[1], alpha)
             v = interpolate(v_range[0], v_range[1], alpha)
             mob.move_to(surface_function(u,v))
             return mob

        self.play(
            UpdateFromAlphaFunc(tangent_plane, update_tangent_plane),
            UpdateFromAlphaFunc(tangent_point, update_tangent_point),
            )

        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.interactive_embed()