import aesoptparam as apm
import jmespath
from numpy import arccos, array, cross, dot, isclose, rad2deg

from ......utils import rad2deg
from ....common import floater_members_c2def, init_blade_pitch, init_rotor_speed
from ....common import mbdy_names as _mbdy_names
from ..common import new_htc_structure_base


class mbdy_names(apm.AESOptParameterized):
    tower = apm.copy_param_ref(_mbdy_names.param.tower, "...........mbdy_names.tower")
    towertop = apm.copy_param_ref(
        _mbdy_names.param.towertop, "...........mbdy_names.towertop"
    )
    connector = apm.copy_param_ref(
        _mbdy_names.param.connector, "...........mbdy_names.connector"
    )
    shaft = apm.copy_param_ref(_mbdy_names.param.shaft, "...........mbdy_names.shaft")
    hub = apm.copy_param_ref(_mbdy_names.param.hub, "...........mbdy_names.hub")
    blade = apm.copy_param_ref(_mbdy_names.param.blade, "...........mbdy_names.blade")
    monopile = apm.copy_param_ref(
        _mbdy_names.param.monopile, "...........mbdy_names.monopile"
    )


class relative(new_htc_structure_base):
    init_blade_pitch = apm.copy_param_ref(init_blade_pitch, "........init_blade_pitch")
    init_rotor_speed = apm.copy_param_ref(init_rotor_speed, "........init_rotor_speed")
    floater_members_c2def = apm.copy_param_ref(
        floater_members_c2def, "........floater_members_c2def"
    )
    mbdy_names = apm.SubParameterized(mbdy_names)

    def convert(self):
        rel = []
        # Monopile
        if self.has_monopile():
            rel += [
                self.get_base_relative_straight(
                    self.mbdy_names.monopile, self.mbdy_names.tower
                )
            ]

        elif self.has_floater():
            base_name, transition_node_nr = (
                self.get_floating_platform_member_with_transition()
            )
            baseMember = jmespath.search(
                f"components.floating_platform.members[?contains(name, '{base_name}')]|[0]",
                self.windio_dict,
            )

            # Position the tower relative to the main body position
            # Easy solution:
            # I have redefined the tower body with z downwards.

            # With the z_down convention for floater => we know the floater
            # members are defined in vertical positive down.
            # With the absolute => we know the orientation from the windio dict.
            # This is enough info.

            towerMember = self.windio_dict["components"]["tower"]
            towerMember["name"] = self.mbdy_names.tower
            towerMember["unit_axial_vector"] = array([0, 0, -1])  # z positive down.
            XOff = array([0.0, 0.0, 0.0])  # tower directly in transition piece

            # Step 2. calculate mbdy_axisangle for rotation tower relative to base member
            baseMemberc2DefPosition = baseMember.copy()
            if self.floater_members_c2def == "final":
                pass  # it's been already defined in the floater preprocessing
            elif self.floater_members_c2def == "z_down":
                baseMemberc2DefPosition["unit_axial_vector"] = [0, 0, -1]
            axis_of_rotation, angle = self.calculate_axisangle_rotation(
                baseMemberc2DefPosition, towerMember
            )

            # Step 3. add to the dict
            rel.append(
                self.return_relative_block(
                    baseMember,
                    towerMember,
                    transition_node_nr,
                    1,
                    XOff,
                    axis_of_rotation,
                    angle,
                )
            )

            # Now onto the floater members
            expression = "components.floating_platform.members[*]"
            allFloaterMembers = jmespath.search(expression, self.windio_dict)

            # Remove the base item
            i_ = allFloaterMembers.index(baseMember)
            allFloaterMembers.pop(i_)

            for other_member_ in allFloaterMembers:

                if self.floater_members_c2def == "final":
                    # FIXME:
                    # In this approach, the base member is defined in its final position.
                    # This is a legacy approach and needs to be removed as soon as the
                    # weis-hawc2 coupling moves to the z_down formulation.

                    current_member_name = other_member_["name"]
                    node1_xyz_this_member = other_member_["jointObjRef"][0]["xyz"]
                    rel += [
                        self.get_base_relative_straight(
                            base_name,
                            current_member_name,
                            0,
                            0,
                            relpos=[0.0, 0.0, 0.0],
                        )
                    ]

                elif self.floater_members_c2def == "z_down":

                    # 1. Calculate offset between the body and base body
                    x0_om = other_member_["jointObjRef"][0]["xyz"]
                    x0_base = baseMember["jointObjRef"][0]["xyz"]

                    XOff = x0_om - x0_base

                    # Step 2. calculate mbdy_axisangle for rotation
                    axis_of_rotation, angle = self.calculate_axisangle_rotation(
                        baseMember, other_member_
                    )

                    # Step 3. add to the dict
                    rel.append(
                        self.return_relative_block(
                            baseMember,
                            other_member_,
                            1,
                            1,
                            XOff,
                            axis_of_rotation,
                            angle,
                        )
                    )

        # Tower->Towertop
        rel += [
            self.get_base_relative_straight(
                self.mbdy_names.tower, self.mbdy_names.towertop
            )
        ]

        # Towertop->connector
        rel += [self.get_towertop_connector()]

        # Connector->Shaft
        rel += [
            self.get_base_relative_straight(
                self.mbdy_names.connector, self.mbdy_names.shaft
            )
        ]
        if self.init_rotor_speed is None:
            raise ValueError("`init_rotor_speed` need to be set")
        rel[-1]["mbdy2_ini_rotvec_d1"] = [0.0, 0.0, -1.0, self.init_rotor_speed]

        # Shaft->hubs
        for i in range(self.windio_dict["assembly"]["number_of_blades"]):
            rel += [self.get_shaft_hub(i)]

        # hubs->blade
        for i in range(self.windio_dict["assembly"]["number_of_blades"]):
            rel += [
                self.get_base_relative_straight(
                    self.get_full_mbdy_name(self.mbdy_names.hub, i + 1),
                    self.get_full_mbdy_name(self.mbdy_names.blade, i + 1),
                    angle=self.init_blade_pitch,
                )
            ]
        return rel

    def get_base_relative_straight(
        self,
        mbdy1,
        mbdy2,
        inode1="last",
        inode2=1,
        relpos=None,
        angle=0.0,
    ):

        out = dict(
            mbdy1=[mbdy1, inode1],
            mbdy2=[mbdy2, inode2],
            mbdy2_eulerang=[[0.0, 0.0, -angle]],
        )
        if relpos is not None:
            out["relpos"] = [relpos]
        return out

    def get_towertop_connector(self):
        tt_s = self.get_base_relative_straight(
            self.mbdy_names.towertop, self.mbdy_names.connector
        )
        tilt_deg = rad2deg(
            self.windio_dict["components"]["nacelle"]["drivetrain"]["uptilt"]
        )
        tt_s["mbdy2_eulerang"] = [
            [90.0, 0.0, 0.0],
            [tilt_deg, 0.0, 0.0],
        ]
        return tt_s

    def get_shaft_hub(self, i):
        cone = rad2deg(self.windio_dict["components"]["hub"]["cone_angle"])
        nb = self.windio_dict["assembly"]["number_of_blades"]
        ang = 180 - i * 360 / nb
        s_hub = self.get_base_relative_straight(
            self.mbdy_names.shaft, self.get_full_mbdy_name(self.mbdy_names.hub, i + 1)
        )
        s_hub["mbdy2_eulerang"] = [
            [-90.0, 0.0, 0.0],
            [0.0, ang, 0.0],
            [cone, 0.0, 0.0],
        ]
        return s_hub

    def calculate_axisangle_rotation(self, member1, member2):

        # Step 2. calculate mbdy_axisangle for rotation
        av_b1, av_b2 = member1["unit_axial_vector"], member2["unit_axial_vector"]
        axis_of_rotation = cross(av_b1, av_b2)
        angle_of_rotation = rad2deg(
            arccos(dot(av_b1, av_b2))
        )  # both vectors are already normalized to 1 length

        return axis_of_rotation, angle_of_rotation

    def return_relative_block(
        self, member1, member2, node1, node2, offset, axis, angle
    ):
        if isclose(axis, 0.0).all():
            # vectors are parallel.
            # we can get away with a euler angle
            return dict(
                mbdy1=[member1["name"], node1],  # always first node here
                mbdy2=[member2["name"], node2],
                relpos=offset,
                mbdy2_eulerang=[angle, 0.0, 0.0],
            )

        else:
            return dict(
                mbdy1=[member1["name"], node1],  # always first node here
                mbdy2=[member2["name"], node2],
                relpos=offset,
                mbdy2_axisangle=[*axis, angle],
            )
