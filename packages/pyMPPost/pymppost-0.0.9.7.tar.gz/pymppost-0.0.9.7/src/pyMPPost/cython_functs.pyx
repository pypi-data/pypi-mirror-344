import numpy as np
cimport cython
cimport numpy as cnp
from libc.stdint cimport int64_t

# Importing NumPy arrays for Cython compatibility
cnp.import_array()

# Disable bounds-checking, negative index wrapping, and initialized checks to optimize performance
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)   # turn off negative index wrapping for entire function
@cython.initializedcheck(False)
cpdef calc_pulses(int64_t[:] history, int64_t[:] cell, double[:] time, int64_t[:] detector_mat, double[:] pgt_arr, double[:] dt_arr, double tol):
    """ 
    Groups events into pulses based on their history, detector cell, time, and material properties.
    
    Args:
        history (int64_t[:] )          : Event history identifiers.
        cell (int64_t[:] )             : Detector cell IDs for each event.
        time (double[:] )           : Time of each event.
        detector_mat (int64_t[:] )     : Material IDs associated with each detector.
        pgt_arr (double[:] )        : Pulse generation time (pgt) values for each material.
        dt_arr (double[:] )         : Time window duration (dt) for pulse splitting for each material.
        tol (double)                : Tolerance value for time comparison.

    Returns:
        np.ndarray: Array of pulse IDs corresponding to each event.
    """
    cdef Py_ssize_t N = len(history)  # Number of events
    cdef double begin  # Start time for the current pulse
    cdef int64_t curr_pulse = 0  # Current pulse ID
    cdef int64_t curr_detect = -1  # Current detector ID
    cdef int64_t curr_hist = -1  # Current event history ID

    cdef Py_ssize_t k
    pulses = np.zeros(N, dtype=np.int64)  # Array to store pulse IDs for each event
    cdef int64_t[::1] pulses_view = pulses  # Cython view for efficient memory access
    
    for k in range(N):  # Loop over all events
        # Check if the history or detector cell has changed, implying a new pulse
        if curr_hist != history[k] or curr_detect != cell[k]:
            curr_hist = history[k]
            curr_detect = cell[k]
            curr_pulse = 0  # Reset pulse ID when a new history or detector is encountered
            begin = time[k]  # Set the start time for the new pulse
            mat_num = detector_mat[k]  # Get the material number for this event
            pgt = pgt_arr[mat_num]  # Get the pulse generation time for this material
            dt = dt_arr[mat_num]  # Get the time window duration for this material

        # Assign a pulse ID if the event's time is within the pulse window (within tolerance)
        if (time[k] - begin) - pgt <= tol:
            pulses_view[k] = curr_pulse
        # If the event is outside the pulse window (after the time window ends), start a new pulse
        elif (time[k] - begin) - (pgt + dt) > tol:
            begin = time[k]  # Reset the start time for the new pulse
            curr_pulse += 1  # Increment the pulse ID
            pulses_view[k] = curr_pulse
        # If the event is in-between the pulse windows, mark it as part of the ongoing pulse
        else:
            pulses_view[k] = -1  # Mark events that don't belong to a pulse window
    return pulses  # Return the pulse ID array


# Disable bounds-checking, negative index wrapping, and initialized checks to optimize performance
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)   # turn off negative index wrapping for entire function
@cython.initializedcheck(False)
cpdef shift_register_counting(int64_t[:] history, double[:] time, double window_width, double tol):
    """ 
    Implements shift register counting for multiplicity calculation. This is used to determine 
    the number of events within a given time window.

    Args:
        history (int64_t[:] )         : Event history identifiers.
        time (double[:] )          : Time of each event.
        window_width (double)      : Time window width for counting multiplicities.
        tol (double)               : Tolerance value for time comparison.

    Returns:
        np.ndarray: Array of window IDs for each event.
    """
    cdef Py_ssize_t N = len(history)  # Number of events
    cdef double begin  # Start time for the current time window
    cdef int64_t curr_hist = -1  # Current event history ID
    cdef int64_t curr_pulse = -1  # Current pulse ID (not used in this function)
    cdef int64_t curr_window = -1  # Current window ID

    cdef Py_ssize_t k
    windows = np.zeros(N, dtype=np.int64)  # Array to store window IDs for each event
    cdef int64_t[::1] window_view = windows  # Cython view for efficient memory access

    for k in range(N):  # Loop through all events
        # If the event belongs to a new history, start a new window
        if curr_hist != history[k]:
            curr_hist = history[k]
            curr_window += 1  # Increment the window ID for a new history
            begin = time[k]  # Set the start time for the new window
        
        # If the event is within the current window, assign it the current window ID
        if (time[k] - begin) - window_width <= tol:
            window_view[k] = curr_window
        # If the event is outside the current window, start a new window
        else:
            begin = time[k]  # Reset the start time for the new window
            curr_window += 1  # Increment the window ID for a new window
            window_view[k] = curr_window

    return windows  # Return the window ID array
