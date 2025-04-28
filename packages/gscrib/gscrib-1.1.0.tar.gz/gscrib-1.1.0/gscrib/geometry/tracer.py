# -*- coding: utf-8 -*-

# Gscrib. Supercharge G-code with Python.
# Copyright (C) 2025 Joan Sala <contact@joansala.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Sequence

import numpy as np
from scipy.interpolate import CubicSpline
from typeguard import typechecked

from gscrib.enums import Direction
from gscrib.types import PathFn, PointLike

from .point import Point


class PathTracer:
    """Generating G-code with interpolated motion paths.

    This class provides methods to generate G-code commands for complex
    motion paths by approximating them with small linear segments. The
    path approximation resolution can be configured to balance between
    motion smoothness and G-code file size. Smaller resolution values
    result in smoother paths but generate more G-code commands.

    Unlike standard G-code where arc movements are affected by the
    selected plane (G17/G18/G19), this class always traces paths on the
    XY plane by default. To transform paths to other planes or orientations,
    use the transformation methods provided by the builder (translate,
    rotate, scale, etc).

    For complex transformations, the ``GCodeCore.transform`` property can
    be used as a context manager to ensure proper matrix stack handling.
    Transformations can be combined and will affect all subsequent path
    operations until the context is exited.

    Example:
        >>> g.move(x=10, y=0)      # Move to start position
        >>> g.set_resolution(0.1)  # Set 0.1mm resolution
        >>> g.set_direction("cw")  # Set clockwise direction
        >>>
        >>> # Draw a quarter circle in XY plane
        >>> g.trace.arc(target=(0, 10), center=(-10, 0))
        >>>
        >>> # Draw an arc rotated 45° around the X axis
        >>> with g.current_transform():  # Save current transform
        ...     g.move(x=0, y=0)
        ...     g.transform.rotate(45, 'x')  # Rotate 45° around X axis
        ...     g.trace.circle(center=(0, 10))
        ... # Applied transforms are restored here
    """

    def __init__(self, builder):
        self._g = builder

    @typechecked
    def arc(self, target: PointLike, center: PointLike, **kwargs) -> None:
        """Trace an arc from the current position to a target point.

        This method generates a series of linear segments that
        approximate a circular arc. The arc is traced around a center
        point, maintaining a constant radius throughout the motion.

        The direction of the arc is determined by the last call to
        set_direction(). If Z is provided for the target point, the
        arc will perform helical interpolation.

        Args:
            target (Point): Absolute or relative destination point (x, y, [z])
            center (Point): Center point (x, y) relative to the current position
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If start and end points are not equidistant

        Example:
            >>> # Draw a quarter circle (90 degrees) clockwise
            >>> g.move(x=0, y=10)
            >>> g.set_direction("cw")  # clockwise
            >>> g.trace.arc(target=(10, 0), center=(0, -10))
        """

        # Convert all coordinates to absolute positions. Coordinates
        # will be converted back to relative if needed during tracing.

        o = self._g.position.resolve()
        t = self._g.to_absolute(target)
        c = o + Point(*center).resolve()

        # Validate that both points lie on the same circle

        do = o - c; dt = t - c
        radius = np.hypot(do.x, do.y)
        target_radius = np.hypot(dt.x, dt.y)

        if not np.isclose(radius, target_radius, rtol=1e-10):
            raise ValueError(
                "Cannot trace arc: start and end points must be at "
                "an equal distance from the center point"
            )

        # Compute the angular displacement between start and end points.
        # Total angle is negative for clockwise arcs, positive otherwise

        direction = self._g.state.direction
        end_angle = np.arctan2(dt.y, dt.x)
        start_angle = np.arctan2(do.y, do.x)
        total_angle = direction.enforce(end_angle - start_angle)

        # Vertical displacement for helical motion if Z is provided

        height = t.z - o.z if len(target) > 2 else 0

        def arc_function(thetas: np.ndarray) -> np.ndarray:
            angles = start_angle + total_angle * thetas
            x = c.x + radius * np.cos(angles)
            y = c.y + radius * np.sin(angles)
            z = o.z + thetas * height
            return np.column_stack((x, y, z))

        total_length = np.hypot(radius * total_angle, height)
        self.parametric(arc_function, total_length, **kwargs)

    @typechecked
    def arc_radius(self, target: PointLike, radius: float, **kwargs) -> None:
        """Trace an arc to target point with specified radius.

        Creates an arc from the current position to the target point with
        the specified radius. Similar to G2/G3 commands, if the radius
        is positive, the shorter arc will be traced. When negative, the
        longer arc will be traced.

        The direction of the arc is determined by the last call to
        set_direction(). If Z is provided for the target point, the
        arc will perform helical interpolation.

        Args:
            target (Point): Absolute or relative destination point (x, y, [z])
            radius (float): Radius (positive for shorter arc, negative for longer)
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If radius is too small for the given points

        Example:
            >>> # Draw a quarter circle with 10mm radius (shorter arc)
            >>> g.move(x=0, y=0)
            >>> g.trace.arc_radius(target=(10, 10), radius=10)
            >>>
            >>> # Draw the longer arc between the same points
            >>> g.move(x=0, y=0)
            >>> g.trace.arc_radius(target=(10, 10), radius=-10)
        """

        o = self._g.position.resolve()
        t = self._g.to_absolute(target)

        dt = t - o; a = t + o
        distance = np.hypot(dt.x, dt.y)

        # Validate that the two points can lie on the same circle

        if radius == 0 or abs(radius) < distance / 2:
            if abs(abs(radius) - distance / 2) <= 0.01:
                radius = np.copysign(distance / 2, radius)
            else:
                raise ValueError(
                    "Radius too small for the given points")

        # Direction depends on radius sign and selected direction

        direction = self._g.state.direction
        height = np.sqrt(abs(radius) ** 2 - (distance / 2) ** 2)
        is_clockwise = (direction == Direction.CLOCKWISE)

        if is_clockwise == (radius > 0):
            cx = a.x / 2 + height * dt.y / distance
            cy = a.y / 2 - height * dt.x / distance
        else:
            cx = a.x / 2 - height * dt.y / distance
            cy = a.y / 2 + height * dt.x / distance

        center = (cx - o.x, cy - o.y)
        self.arc(target, center, **kwargs)

    @typechecked
    def circle(self, center: PointLike, **kwargs) -> None:
        """Trace a complete circle around a center point.

        Creates a full 360-degree circular path around the specified
        center point, starting and ending at the current position. The
        direction of rotation is determined by the last call to
        set_direction().

        Args:
            center (Point): Center point (x, y) relative to the current position
            **kwargs: Additional G-code parameters (added to each move)

        Example:
            >>> # Draw a circle with 10mm radius
            >>> g.move(x=10, y=0)
            >>> g.set_direction("ccw")  # counter-clockwise
            >>> g.trace.circle(center=(-10, 0))
        """

        self.arc(self._g.position, center, **kwargs)

    @typechecked
    def spline(self, targets: Sequence[PointLike], **kwargs) -> None:
        """Trace a cubic spline through the given control points.

        Creates a smooth curve that passes through all the specified
        control points, starting from the current position. The spline
        is approximated using linear segments based on the current
        resolution setting.

        Args:
            targets (Sequence[Point]): Sequence of control points (x, y, [z])
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If not enought points are provided

        Example:
            >>> # Draw a smooth curve through three points
            >>> g.trace.spline([(5, 5), (10, -5), (15, 0)])
        """

        # Convert all coordinates to absolute positions

        origin = self._g.position.resolve()
        points = self._g.to_absolute_list(targets)

        # Include current position as first control point and then
        # remove consecutive duplicate points if any

        controls = [origin]

        for point in points:
            if point != controls[-1]:
                controls.append(point)

        # Need at least 2 distinct points to create a spline

        if len(controls) < 2:
            raise ValueError(
                "Spline requires at least 2 distinct points")

        # Create a spline for each coordinate of the control points.

        thetas = np.linspace(0, 1, len(controls))
        sx = CubicSpline(thetas, [c.x for c in controls])
        sy = CubicSpline(thetas, [c.y for c in controls])
        sz = CubicSpline(thetas, [c.z for c in controls])

        def spline_function(thetas: np.ndarray) -> np.ndarray:
            return np.column_stack((
                sx(thetas),
                sy(thetas),
                sz(thetas)
            ))

        total_length = self.estimate_length(500, spline_function)
        self.parametric(spline_function, total_length, **kwargs)

    @typechecked
    def helix(self,
        target: PointLike, center: PointLike, turns: int = 1, **kwargs) -> None:
        """Trace a helical path to target point with varying radius.

        Creates a helical motion that can change radius as it moves from
        the current position to the target point. The motion is defined
        by a center point and the number of complete revolutions.

        Args:
            target (Point): Absolute or relative destination point (x, y, [z])
            center (Point): Center point (x, y) relative to the current position
            turns (int): Number of complete revolutions to make (default: 1)
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If turns is not positive

        Example:
            >>> # Create a spiral with 3 turns
            >>> g.move(x=10, y=0)
            >>> g.trace.helix(target=(5, 0), center=(-10, 0), turns=3)
            >>>
            >>> # Create a helix up 10mm with 2 turns
            >>> g.move(x=10, y=0)
            >>> g.trace.helix(target=(10, 0, 10), center=(-10, 0), turns=2)
        """

        if turns <= 0:
            raise ValueError("Turns must be positive")

        o = self._g.position.resolve()
        t = self._g.to_absolute(target)
        c = o + Point(*center).resolve()

        do = o - c; dt = t - c
        start_radius = np.hypot(do.x, do.y)
        end_radius = np.hypot(dt.x, dt.y)
        total_radius = end_radius - start_radius

        end_angle = np.arctan2(dt.y, dt.x)
        start_angle = np.arctan2(do.y, do.x)

        direction = self._g.state.direction
        turn_angle = direction.full_turn()
        base_angle = direction.enforce(end_angle - start_angle)
        total_angle = base_angle + turn_angle * (turns - 1)

        height = t.z - o.z if len(target) > 2 else 0

        def helix_function(thetas: np.ndarray) -> np.ndarray:
            angles = start_angle + total_angle * thetas
            radii = start_radius + total_radius * thetas
            x = c.x + radii * np.cos(angles)
            y = c.y + radii * np.sin(angles)
            z = o.z + thetas * height
            return np.column_stack((x, y, z))

        total_length = self.estimate_length(500, helix_function)
        self.parametric(helix_function, total_length, **kwargs)

    @typechecked
    def thread(self, target: PointLike, pitch: float = 1, **kwargs) -> None:
        """Trace a thread-like helical path to target point.

        Creates a helical motion with constant radius from the current
        position to the target point. The motion is defined by the distance
        from the current position to the target Z height and the pitch.

        Args:
            target (Point): Absolute or relative destination point (x, y, [z])
            pitch (float): Distance between turns in Z axis
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If radius or pitch is not positive
        """

        if pitch <= 0:
            raise ValueError("Pitch must be positive")

        o = self._g.position.resolve()
        t = self._g.to_absolute(target)
        center = Point((t.x - o.x) / 2 - o.x, (t.y - o.y) / 2 - o.y)
        turns = max(1, int(abs(t.z - o.z) / pitch))

        self.helix(target, center, turns, **kwargs)

    @typechecked
    def spiral(self, target: PointLike, turns: int = 1, **kwargs) -> None:
        """Trace a spiral path from current position to target point.

        Creates a spiral motion that changes radius as it moves from the
        current position to the target point. If Z is provided for the
        target point, the spiral will perform helical interpolation.

        Args:
            target (Point): Absolute or relative destination point (x, y, [z])
            turns (int): Number of complete revolutions to make (default: 1)
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If turns is not positive
        """

        self.helix(target, Point(0, 0), turns, **kwargs)

    @typechecked
    def polyline(self, targets: Sequence[PointLike], **kwargs) -> None:
        """Trace straight lines through the given points.

        Creates a series of straight lines connecting all the specified
        points, starting from the current position.

        Args:
            targets (Sequence[Point]): Sequence of control points (x, y, [z])
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If not enought points are provided
        """

        for point in self._g.to_absolute_list(targets):
            point = self._g.to_distance_mode(point)
            self._g.move(point, **kwargs)

    @typechecked
    def parametric(self, function: PathFn, length: float, **kwargs) -> None:
        """Approximate a parametric curve with linear segments.

        Divides a parametric curve into small linear segments based on the
        current resolution setting. The curve is traced using G1(linear)
        movements to create a linear approximation of the desired path.

        The curve is defined by a parametric function that maps an array
        of theta parameters in the range [0, 1] to points in space. The
        number of segments is calculated from the provided curve length
        and current resolution setting.

        Args:
            function (PathFn): Parametric function f(theta)
            length (float): Total curve length in current work units
            **kwargs: Additional G-code parameters (added to each move)

        Raises:
            ValueError: If the length parameter is not positive.

        Example:
            >>> def circle(thetas: ndarray) -> ndarray:
            ...     x = 10 * cos(2 * pi * thetas)
            ...     y = 10 * sin(2 * pi * thetas)
            ...     z = zeros(thetas.shape)
            ...     return column_stack((x, y, z))
            >>>
            >>> length = g.trace.estimate_length(100, circle)
            >>> g.trace.parametric(circle, length)
        """

        if length <= 0:
            raise ValueError("Length must be positive")

        # To fit better the curve, generate more points than needed
        # then keep only segments longer than or equal to resolution

        resolution = self._g.state.resolution
        num_segments = max(2, int(10 * length / resolution))
        thetas = np.linspace(0, 1, num_segments + 1)[1:]
        points = self._filter_segments(function(thetas))

        # Generate absolute or relative G-code moves for each point

        for point in (Point(*t) for t in points):
            point = self._g.to_distance_mode(point)
            self._g.move(point, **kwargs)

    @typechecked
    def estimate_length(self, samples: int, function: PathFn) -> float:
        """Estimate the total length of a parametric curve.

        Calculates an approximation of the curve length by sampling
        points along the curve and summing the distances between
        consecutive points. The accuracy of the estimation improves with
        a higher number of samples, but requires more computation time.

        Args:
            samples (int): Number of points to sample along the curve
            function (PathFn): Parametric function f(theta)

        Returns:
            float: Estimated length of the curve in current work units.
        """

        thetas = np.linspace(0, 1, samples)
        vectors = np.diff(function(thetas), axis=0)
        length = np.linalg.norm(vectors, axis=1).sum()

        return length

    def _filter_segments(self, points: np.ndarray) -> np.ndarray:
        """Filter segments shorter than the current resolution.

        Args:
            points (ndarray): Array of points along a curve

        Returns:
            ndarray: Filtered array of points
        """

        if points.size < 3:
            return points

        diffs = np.diff(points, axis=0)
        distances = np.linalg.norm(diffs, axis=1)
        keep_mask = np.ones(len(distances), dtype=bool)

        resolution = self._g.state.resolution
        tolerance = resolution / 10
        remaining = resolution

        for i, distance in enumerate(distances[:-1]):
            remaining -= distance

            if remaining < tolerance:
                remaining = resolution
                continue

            keep_mask[i] = False

        return np.vstack([points[0], points[1:][keep_mask]])
