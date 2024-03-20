"""Physics object candidate mixin

This provides just a Lorentz vector with charge, but maybe
in the future it will provide some sort of composite candidate building tool
that automatically resolves duplicates in the chain.
"""

import awkward
import numpy

from coffea.nanoevents.methods import vector


@awkward.mixin_class(vector.behavior)
class Candidate(vector.LorentzVector):
    """A Lorentz vector with charge

    This mixin class requires the parent class to provide items `x`, `y`, `z`, `t`, and `charge`.
    """

    @awkward.mixin_class_method(numpy.add, {"Candidate"})
    def add(self, other):
        """Add two candidates together elementwise using `x`, `y`, `z`, `t`, and `charge` components"""
        return awkward.zip(
            {
                "x": self.x + other.x,
                "y": self.y + other.y,
                "z": self.z + other.z,
                "t": self.t + other.t,
                "charge": self.charge + other.charge,
            },
            with_name="Candidate",
            behavior=self.behavior,
        )

    def sum(self, axis=-1):
        """Sum an array of vectors elementwise using `x`, `y`, `z`, `t`, and `charge` components"""
        return awkward.zip(
            {
                "x": awkward.sum(self.x, axis=axis),
                "y": awkward.sum(self.y, axis=axis),
                "z": awkward.sum(self.z, axis=axis),
                "t": awkward.sum(self.t, axis=axis),
                "charge": awkward.sum(self.charge, axis=axis),
            },
            with_name="Candidate",
            behavior=self.behavior,
        )


@awkward.mixin_class(vector.behavior)
class PtEtaPhiMCandidate(Candidate, vector.PtEtaPhiMCandidate):
    """A Lorentz vector in eta, mass coordinates with charge

    This mixin class requires the parent class to provide items `pt`, `eta`, `phi`, `mass`, and `charge`.
    """

    pass


@awkward.mixin_class(vector.behavior)
class PtEtaPhiECandidate(Candidate, vector.PtEtaPhiELorentzVector):
    """A Lorentz vector in eta, energy coordinates with charge

    This mixin class requires the parent class to provide items `pt`, `eta`, `phi`, `energy`, and `charge`.
    """

    pass


vector._binary_dispatch_cls.update(
    {
        "Candidate": Candidate,
    }
)
vector._rank += [Candidate]

for lhs, lhs_to in vector._binary_dispatch_cls.items():
    for rhs, rhs_to in vector._binary_dispatch_cls.items():
        if lhs == "Candidate" or rhs == "Candidate":
            out_to = min(lhs_to, rhs_to, key=vector._rank.index)
            vector.behavior[(numpy.add, lhs, rhs)] = out_to.add
            vector.behavior[(numpy.subtract, lhs, rhs)] = out_to.subtract

CandidateArray.ProjectionClass2D = vector.TwoVectorArray  # noqa: F821
CandidateArray.ProjectionClass3D = vector.ThreeVectorArray  # noqa: F821
CandidateArray.ProjectionClass4D = vector.LorentzVectorArray  # noqa: F821
CandidateArray.MomentumClass = CandidateArray  # noqa: F821

PtEtaPhiMCandidateArray.ProjectionClass2D = vector.TwoVectorArray  # noqa: F821
PtEtaPhiMCandidateArray.ProjectionClass3D = vector.ThreeVectorArray  # noqa: F821
PtEtaPhiMCandidateArray.ProjectionClass4D = vector.LorentzVectorArray  # noqa: F821
PtEtaPhiMCandidateArray.MomentumClass = PtEtaPhiMCandidateArray  # noqa: F821

PtEtaPhiECandidateArray.ProjectionClass2D = vector.TwoVectorArray  # noqa: F821
PtEtaPhiECandidateArray.ProjectionClass3D = vector.ThreeVectorArray  # noqa: F821
PtEtaPhiECandidateArray.ProjectionClass4D = vector.LorentzVectorArray  # noqa: F821
PtEtaPhiECandidate.MomentumClass = PtEtaPhiECandidateArray  # noqa: F821

__all__ = ["Candidate", "PtEtaPhiMCandidate", "PtEtaPhiECandidate"]
