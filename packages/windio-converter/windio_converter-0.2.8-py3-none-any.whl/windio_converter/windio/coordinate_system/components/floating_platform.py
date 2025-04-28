from copy import deepcopy

import aesoptparam as apm
from numpy import cos, sin

from ..common import cs_base


class joints(cs_base):

    def convert(self):
        listOfJointsOriginalCoordinates = deepcopy(self.windio_dict)
        coord_trans = self.get_cs_transform()

        listOfJointsTransformedCoordinates = []
        for thisJoint_ in listOfJointsOriginalCoordinates:
            # thisJoint_ is a dict which is an element of a list
            # of joints. It contains: name, location (x,y,z)

            # We make a dictionary with the input location
            # check if it's specified in cylindrical coodinates
            if not thisJoint_.get("cylindrical", False):
                inputLocation_ = {
                    "x": thisJoint_["location"][0],
                    "y": thisJoint_["location"][1],
                    "z": thisJoint_["location"][2],
                }
            else:
                inputLocation_ = {
                    "x": thisJoint_["location"][0] * cos(thisJoint_["location"][1]),
                    "y": thisJoint_["location"][0] * sin(thisJoint_["location"][1]),
                    "z": thisJoint_["location"][2],
                }
                # FIXME: Do not convert back to cylindrical
                thisJoint_["cylindrical"] = False

            # This is after the coordinate transformation
            outputLocation = dict()
            for i_, _name in enumerate(["x", "y", "z"]):
                sign = -1 if coord_trans[_name][0] == "-" else 1
                name = coord_trans[_name].replace("-", "")
                outputLocation[_name] = sign * inputLocation_[name]

            thisJoint_["location"] = [outputLocation[c_] for c_ in ["x", "y", "z"]]

            thisJoint_ = self.add_coordinate_system_description(thisJoint_, coord_trans)

            listOfJointsTransformedCoordinates.append(thisJoint_)

        return listOfJointsTransformedCoordinates


class floating_platform(cs_base):

    joints = apm.SubParameterized(joints)

    def convert(self):
        comp = deepcopy(self.windio_dict)
        comp["joints"] = self.joints.convert()

        return comp
