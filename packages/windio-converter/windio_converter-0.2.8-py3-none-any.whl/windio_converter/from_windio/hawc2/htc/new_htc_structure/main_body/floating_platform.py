import os

import aesoptparam as apm
import numpy as np

from ......utils import interp
from ....common import filenames, floater_members_c2def, floater_mooring_base
from .common import main_body_base


class floating_platform(main_body_base, floater_mooring_base):
    filename = apm.copy_param_ref(filenames.param.floater, "........filenames.floater")
    floater_members_c2def = apm.copy_param_ref(
        floater_members_c2def, "........floater_members_c2def"
    )

    def convert(self):
        floaterMultibodies = []

        # Checks what member name hosts a transition piece
        nameTrans, nsecTrans = self.get_floating_platform_member_with_transition()

        # Cycle through the members and make the htc dictionary
        for member_ in self.windio_dict["components"]["floating_platform"]["members"]:
            mono_axis = member_["reference_axis"]
            grid = mono_axis["grid"]

            # Coordinate in local coordinate system
            z_val = mono_axis["values"]
            z_val = [z - z_val[0] for z in z_val]
            z_loc = interp(grid, mono_axis["grid"], z_val)

            nsec = len(grid)
            memberBase = self.get_mbdy_base(member_["name"], nbodies=1)

            # Let's initialize a concentrated mass list
            concentrated_masses = []

            # The transition piece is treated as a concentrated mass
            if member_["name"] == nameTrans:
                concentrated_masses.append(
                    [
                        nsecTrans,
                        0.0,
                        0.0,
                        0.0,
                        self.windio_dict["components"]["floating_platform"][
                            "transition_piece_mass"
                        ],
                        0.0,
                        0.0,
                        0.0,
                    ]
                )

            # Check if the body contains a ballast
            if self.has_fixed_ballasts(member_["name"]):
                # The array member_["nodeBallastWeight"] contains the concentrated masses
                # Through the index i_, we can reconstruct in which node the concentrated mass
                # is to be applied
                for i_, cm_ in enumerate(member_["nodeBallastWeight"]):
                    if np.greater(cm_, 0.0):
                        nSec = i_ + 1  # sections are 1 based
                        concentrated_masses.append(
                            [
                                nSec,
                                0.0,
                                0.0,
                                0.0,
                                cm_,
                                0.0,
                                0.0,
                                0.0,
                            ]
                        )

            if concentrated_masses:  # if this list is not empty, then save it
                memberBase["concentrated_mass"] = concentrated_masses

            # Add sec and nsec
            sec = [None] * nsec
            if self.floater_members_c2def == "final":
                # FIXME:
                # In this approach, the base member is defined in its final position.
                # This is a legacy approach and needs to be removed as soon as the
                # weis-hawc2 coupling moves to the z_down formulation.

                # Initial offset
                x0 = member_["jointObjRef"][0]["xyz"]

                # Coordinates in global system
                coord_abs = x0 + np.outer(z_loc, member_["unit_axial_vector"])

                for i, (x, y, z) in enumerate(coord_abs):
                    sec[i] = [i + 1, x, y, z, 0.0]

            if self.floater_members_c2def == "z_down":

                for i, z in enumerate(z_loc):
                    sec[i] = [i + 1, 0.0, 0.0, -z, 0.0]

            memberBase["c2_def"]["nsec"] = nsec
            memberBase["c2_def"]["sec"] = sec
            memberBase["timoschenko_input"]["mass_scale_method"] = 0

            floaterMultibodies.append(memberBase)

        if self.has_mooring():
            self.preprocessMooringMembers()

        return floaterMultibodies

    def get_mbdy_base(self, mbdy_name, imbdy=None, nbodies=1):
        name = self.get_full_mbdy_name(mbdy_name, imbdy)
        filename = self.filename.replace("_st.dat", f"_{mbdy_name}_st.dat")
        return dict(
            name=name,
            type="timoschenko",
            nbodies=nbodies,
            node_distribution="c2_def",
            timoschenko_input=dict(filename=filename, set=[1, 1]),
            c2_def=dict(),
        )
