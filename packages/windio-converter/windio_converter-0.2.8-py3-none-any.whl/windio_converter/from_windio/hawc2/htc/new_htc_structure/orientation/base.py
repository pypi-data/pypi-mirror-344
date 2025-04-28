import aesoptparam as apm
import jmespath
from numpy import arccos, cross, dot, isclose, rad2deg

from ....common import base_inipos, floater_members_c2def, mbdy_names
from ..common import new_htc_structure_base


class base(new_htc_structure_base):
    base_inipos = apm.copy_param_ref(base_inipos, "........base_inipos")
    tower_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.tower, "........mbdy_names.tower"
    )
    monopile_mbdy_name = apm.copy_param_ref(
        mbdy_names.param.monopile, "........mbdy_names.monopile"
    )
    floater_members_c2def = apm.copy_param_ref(
        floater_members_c2def, "........floater_members_c2def"
    )

    def convert(self):

        baseBodies = []

        if self.has_monopile():
            def_name = self.monopile_mbdy_name

            baseBodies.append(
                dict(
                    mbdy=def_name,
                    inipos=self.base_inipos,
                    mbdy_eulerang=[0.0, 0.0, 0.0],
                )
            )

        elif self.has_floater():
            # The base is the member with the transition piece.
            def_name, _ = self.get_floating_platform_member_with_transition()

            member_ = jmespath.search(
                f"components.floating_platform.members[?contains(name, '{def_name}')]|[0]",
                self.windio_dict,
            )

            if self.floater_members_c2def == "final":
                # FIXME:
                # In this approach, the base member is defined in its final position.
                # This is a legacy approach and needs to be removed as soon as the
                # weis-hawc2 coupling moves to the z_down formulation.

                baseBodies.append(
                    dict(
                        mbdy=def_name,
                        inipos=self.base_inipos,
                        mbdy_eulerang=[0.0, 0.0, 0.0],
                    )
                )
            elif self.floater_members_c2def == "z_down":

                # Step 1.
                # Calculate the body joint 1 and orientatio vecotr
                x0 = member_["jointObjRef"][0]["xyz"]
                axial_vector = member_["unit_axial_vector"]
                z_wise_vector = [0.0, 0.0, -1.0]

                # Step 2. calculate mbdy_axisangle
                axis_of_rotation = cross(z_wise_vector, axial_vector)
                angle = rad2deg(
                    arccos(dot(z_wise_vector, axial_vector))
                )  # both vectors are already normalized to 1 length

                # Step 3. add to the dict
                if isclose(axis_of_rotation, 0.0).all():
                    # vectors are parallel.
                    # we can get away with a euler angle
                    def_name = member_["name"]
                    baseBodies.append(
                        dict(
                            mbdy=def_name,
                            inipos=x0,
                            mbdy_eulerang=[angle, 0.0, 0.0],
                        )
                    )
                else:
                    def_name = member_["name"]
                    baseBodies.append(
                        dict(
                            mbdy=def_name,
                            inipos=x0,
                            mbdy_axisangle=[*axis_of_rotation, angle],
                        )
                    )

        else:
            def_name = self.tower_mbdy_name
            baseBodies.append(
                dict(
                    mbdy=def_name,
                    inipos=self.base_inipos,
                    mbdy_eulerang=[0.0, 0.0, 0.0],
                )
            )

        return baseBodies
