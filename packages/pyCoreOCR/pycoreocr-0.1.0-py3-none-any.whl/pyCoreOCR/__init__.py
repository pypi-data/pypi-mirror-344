import ctypes
import os
import platform
import sys
from typing import List, Optional

__version__ = "0.1.0"

# --- Constants matching Swift C interface ---
class CErrorCode(ctypes.c_int32):
    SUCCESS = 0
    ERROR_FILE_NOT_FOUND = 1
    ERROR_IMAGE_LOAD_FAILED = 2
    ERROR_PDF_LOAD_FAILED = 3
    ERROR_VISION_REQUEST_FAILED = 4
    ERROR_INVALID_PARAMETER = 5
    ERROR_OTHER = 6

class CRecognitionLevel(ctypes.c_int32):
    ACCURATE = 0
    FAST = 1

# Error mapping for Python exceptions
ERROR_CODE_MAP = {
    CErrorCode.ERROR_FILE_NOT_FOUND: FileNotFoundError,
    CErrorCode.ERROR_IMAGE_LOAD_FAILED: ValueError, # Or a custom error
    CErrorCode.ERROR_PDF_LOAD_FAILED: ValueError,   # Or a custom error
    CErrorCode.ERROR_VISION_REQUEST_FAILED: RuntimeError,
    CErrorCode.ERROR_INVALID_PARAMETER: ValueError,
    CErrorCode.ERROR_OTHER: RuntimeError,
}

# Custom Exception
class CoreOCRError(Exception):
    """Custom exception for errors during CoreOCR operations."""
    pass

# --- Load Swift Library ---

_lib = None
_lib_path = None

def _load_library():
    global _lib, _lib_path
    if _lib:
        return _lib

    if platform.system() != "Darwin":
        raise CoreOCRError("pyCoreOCR currently only supports macOS.")

    # Find the library within the package
    lib_name = "libCoreOCRLib.dylib"
    # __file__ is the path to this __init__.py file
    _lib_path = os.path.join(os.path.dirname(__file__), lib_name)

    if not os.path.exists(_lib_path):
        # Provide helpful message if running from source without building
        setup_py_path = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
        if os.path.exists(setup_py_path):
             raise CoreOCRError(
                 f"Swift library not found at {_lib_path}. "
                 f"Did you install the package or run \`python setup.py build\`?"
             )
        else:
            raise CoreOCRError(f"Swift library not found at {_lib_path}.")

    try:
        _lib = ctypes.CDLL(_lib_path)
    except OSError as e:
        raise CoreOCRError(f"Failed to load Swift library at {_lib_path}: {e}") from e

    # --- Define C Function Signatures ---
    try:
        # recognize_text_c
        _lib.recognize_text_c.argtypes = [
            ctypes.c_char_p,                             # filePath
            ctypes.POINTER(ctypes.c_char_p),             # languages (array of char*)
            ctypes.c_int32,                             # languageCount
            ctypes.c_int32,                             # level
            ctypes.c_int32,                             # preserveOrder
            ctypes.POINTER(ctypes.c_char_p),             # outputResult (pointer to char*)
            ctypes.POINTER(ctypes.c_char_p)              # outputError (pointer to char*)
        ]
        _lib.recognize_text_c.restype = ctypes.c_int32 # CErrorCode

        # free_swift_string
        _lib.free_swift_string.argtypes = [ctypes.c_char_p] # ptr
        _lib.free_swift_string.restype = None

    except AttributeError as e:
         raise CoreOCRError(
             f"Failed to find expected C functions in the Swift library at {_lib_path}. "
             f"Ensure the Swift code was built correctly. Missing function: {e}"
         )

    return _lib

# --- Python Wrapper Function ---

def recognize_text(
    file_path: str,
    languages: Optional[List[str]] = None,
    level: str = 'accurate',
    preserve_order: bool = True
) -> str:
    """Recognizes text from an image or PDF file using the CoreOCR Swift library.

    Args:
        file_path: Path to the image or PDF file.
        languages: List of language codes (e.g., ["en-US", "ja-JP"]) for recognition.
                   Defaults to None (auto-detection by Vision framework).
        level: Recognition level, either 'accurate' (default) or 'fast'.
               Note: 'fast' mode might be unstable for some PDF files.
        preserve_order: For PDF files, whether to process pages sequentially to
                        preserve text order (default: True). Setting to False
                        may be faster but text order is not guaranteed.

    Returns:
        The recognized text as a single string.

    Raises:
        FileNotFoundError: If the input file_path does not exist (checked by Swift).
        ValueError: If an invalid parameter (level, languages) is provided,
                    or if loading image/PDF fails.
        RuntimeError: If the underlying Vision request fails or another unexpected
                      error occurs in the Swift library.
        CoreOCRError: If the Swift library cannot be loaded or other setup issues occur.
    """
    lib = _load_library()

    # --- Argument Conversion ---
    c_file_path = file_path.encode('utf-8')

    c_languages_array = None
    c_language_count = 0
    lang_pointers = [] # Keep intermediate ctypes objects alive
    if languages is not None:
        if not isinstance(languages, list):
            raise ValueError("'languages' parameter must be a list of strings or None.")
        # Convert list of Python strings to array of C char pointers
        lang_pointers = [lang.encode('utf-8') for lang in languages]
        # Create the C array type: (ctypes.c_char_p * len(languages))
        CCharPArray = ctypes.c_char_p * len(lang_pointers)
        # Create an instance of the array, populating it with the Python bytes
        c_languages_array = CCharPArray(*lang_pointers)
        c_language_count = len(languages)
    # If languages is None, c_languages_array remains None (interpreted as NULL by ctypes)
    # and c_language_count remains 0. Swift code handles this as auto-detection.

    if level == 'accurate':
        c_level = CRecognitionLevel.ACCURATE
    elif level == 'fast':
        c_level = CRecognitionLevel.FAST
    else:
        raise ValueError("'level' parameter must be 'accurate' or 'fast'.")

    c_preserve_order = ctypes.c_int32(1) if preserve_order else ctypes.c_int32(0)

    # --- Prepare Output Pointers ---
    # Create empty C string pointers for the output
    result_ptr = ctypes.c_char_p()
    error_ptr = ctypes.c_char_p()

    # --- Call C Function ---
    try:
        return_code = lib.recognize_text_c(
            c_file_path,
            c_languages_array, # Pass the array instance (or None)
            c_language_count,
            c_level,
            c_preserve_order,
            ctypes.byref(result_ptr), # Pass pointers *by reference*
            ctypes.byref(error_ptr)
        )

        # --- Handle Result/Error ---
        if return_code == CErrorCode.SUCCESS:
            if result_ptr.value:
                # Decode C string (bytes) to Python string (Unicode)
                py_result = result_ptr.value.decode('utf-8')
                return py_result
            else:
                # Should not happen on success, but handle defensively
                return ""
        else:
            # An error occurred
            error_message = "Unknown error"
            if error_ptr.value:
                error_message = error_ptr.value.decode('utf-8')

            # Raise specific Python exception based on error code
            ExceptionType = ERROR_CODE_MAP.get(return_code, CoreOCRError)
            raise ExceptionType(f"[CoreOCR Error Code {return_code}] {error_message}")

    finally:
        # --- ALWAYS Free C Memory --- 
        # Ensure C strings allocated by Swift (via strdup) are freed
        if result_ptr.value:
            lib.free_swift_string(result_ptr)
        if error_ptr.value:
            lib.free_swift_string(error_ptr)

# Optional: Clean up library handle on exit? Generally not necessary.
# import atexit
# def _unload_library():
#    global _lib
#    if _lib and hasattr(_lib, '_handle'): # Check if CDLL has _handle (platform dependent)
#         try:
#              # This is platform specific and might not work reliably
#              ctypes.dlclose(_lib._handle)
#         except Exception:
#              pass # Ignore errors during cleanup
#    _lib = None
# atexit.register(_unload_library) 