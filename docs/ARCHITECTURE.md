# Architecture Overview

## System Visual Flow

```
[ User / Presenter ]
         ?
         ?
[ Streamlit Web UI ] ??? (Select Scenario / 1-Click Demo)
         ?
         ?
[ Security Module: signature.py ]
   ??? Computes SHA-256 Digest
   ??? Prepares Quantum State Sequence (|0>, |+>, |+i>)
         ?
         ?
[ Quantum Engine: teleportation.py & bell.py ]
   ??? Prepares Bell Pair |Phi+>
   ??? Executes Bell State Measurement (BSM)
   ??? Applies Pauli Corrections (I, X, Z, ZX)
         ?
         ?
[ Measurement Engine: measurement.py & statistics.py ]
   ??? Performs Projective Measurements (X, Y, Z bases)
   ??? Calculates Empirical Error Rate & Forgery Probability
         ?
         ?
[ Threat Detector: detector.py & authorization.py ]
   ??? Checks Verifier Authorization List
   ??? Inspects In-Memory Replay Ledger
   ??? Evaluates Error Rate vs Acceptance Threshold
         ?
         ?
[ Threat Dashboard & Report Export (JSON/CSV) ]
```
