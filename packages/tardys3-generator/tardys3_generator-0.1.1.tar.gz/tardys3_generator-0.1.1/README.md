# TardyS3 file generator

A simple TardyS3 reservation file generator. The TARDyS3 (Telecommunications Advanced Research and Dynamic Spectrum Sharing System) is an automated scheduling system developed by the U.S. Department of Defense (DoD) to manage spectrum use in the 3.5 GHz band. It replaces the previous manual scheduling portal used to activate Portal-Activated Dynamic Protection Areas (P-DPAs), which protect certain federal operations from interference by Citizens Broadband Radio Service (CBRS) users.

Why is TARDyS3 Important?
Automation & Efficiency – It allows federal spectrum managers to schedule protected spectrum use autonomously, reducing delays and improving coordination.
Compatibility – The system is designed to work seamlessly with Spectrum Access Systems (SAS) that manage CBRS spectrum allocations.
Protection of Military Operations – It ensures military testing and operations in the 3.5 GHz band remain protected from commercial interference.
Regulatory Compliance – The FCC has mandated that all SAS administrators must transition from the manual system to TARDyS3.
This system is critical for dynamic spectrum sharing, balancing federal and commercial use of the mid-band spectrum, which is essential for 5G and other wireless services.

## Installation
```
pip install tardys3-generator
```

To run from source
```python
python3 tardys3_generator.py
```