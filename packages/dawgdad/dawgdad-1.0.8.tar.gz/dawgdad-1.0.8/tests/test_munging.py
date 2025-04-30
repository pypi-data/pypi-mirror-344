import warnings

from pathlib import Path, PosixPath

import dawgdad as dd
import pandas as pd
import numpy as np


pd.set_option('future.no_silent_downcasting', True)
df = pd.DataFrame(
    data=dict(
        floats=[1.0, np.nan, 3.0, np.nan, 5.0, 6.0, np.nan],
        text=["A", "B", "C", "D", "E", "F", np.nan],
        dates=[
            "1956-06-08", "1956-06-08",
            "1956-06-08", "1956-06-08",
            "1956-06-08", "1956-06-08",
            pd.NaT
        ],
        all_nan=[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
        all_none=[None, None, None, None, None, None, None],
        all_space=["", " ", "", " ", "", "", ""],
        nan_space=[np.nan, "", " ", np.nan, np.nan, np.nan, np.nan],
        nan_none=[np.nan, None, np.nan, np.nan, None, np.nan, None],
        mixed=[None, np.nan, pd.NaT, pd.NaT, None, np.nan, pd.NaT],
        integers=[1, 2, np.nan, 4, 5, 6, np.nan],
    )
).replace(
    r"^\s+$",
    np.nan,
    regex=True
).replace(
    "",
    np.nan,
    regex=True
).astype(
    dtype={
        "integers": "Int64",
        "floats": "float64",
        "text": "object",
        "dates": "datetime64[ns]",
        "all_nan": "float64",
        "all_nat": "datetime64[ns]",
        "all_none": "float64",
        "all_space": "float64",
        "nan_space": "float64",
        "nan_none": "float64",
        "mixed": "datetime64[ns]"
    }
)


def test_listone_contains_all_listtwo_substrings():
    pass


def test_number_empty_cells_in_columns():
    pass


def test_convert_seconds_to_hh_mm_ss():
    """
    Convert seconds.to hours, minutes and seconds.
    """
    result = dd.convert_seconds_to_hh_mm_ss(seconds=1)
    expected = (0, 0, 1)
    assert result == expected
    result = dd.convert_seconds_to_hh_mm_ss(seconds=61)
    expected = (0, 1, 1)
    assert result == expected
    result = dd.convert_seconds_to_hh_mm_ss(seconds=3601)
    expected = (1, 0, 1)
    assert result == expected
    result = dd.convert_seconds_to_hh_mm_ss(seconds=3661)
    expected = (1, 1, 1)
    result = dd.convert_seconds_to_hh_mm_ss(seconds=251)
    expected = (0, 4, 11)
    assert result == expected


def test_parameters_dict_replacement():
    pass


def test_parameters_text_replacement():
    pass


def test_ask_save_as_file_name_path():
    pass


def test_optimize_datetime_columns():
    pass


def test_optimize_integer_columns():
    pass


def test_print_dictionary_by_key():
    pass


def test_optimize_object_columns():
    pass


def test_ask_open_file_name_path():
    pass


def test_convert_csv_to_feather():
    pass


def test_find_int_float_columns():
    pass


def test_find_timedelta_columns():
    pass


def test_optimize_float_columns():
    pass


def test_create_dataframe_norm():
    pass


def test_replace_column_values():
    pass


def test_feature_percent_empty():
    pass


def test_find_category_columns():
    pass


def test_find_datetime_columns():
    pass


def test_list_one_list_two_ops():
    """
    Create a list of items comparing two lists:
    - Items unique to list_one
    - Items unique to list_two
    - Items common to both lists (intersection)
    Duplicate items are not removed.
    """
    list_one = [1, 2, 3, 4, 5, 6]
    list_two = [4, 5, 6, 7, 8, 9]
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_one"
    )
    expected = [1, 2, 3]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_two"
    )
    expected = [7, 8, 9]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="intersection"
    )
    expected = [4, 5, 6]
    assert result == expected
    list_one = ["mo", "larry", "curly", "curly-joe", "shemp"]
    list_two = ["curly-joe", "shemp", "tom", "dick", "harry"]
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_one"
    )
    expected = ["mo", "larry", "curly"]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_two"
    )
    expected = ["tom", "dick", "harry"]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="intersection"
    )
    expected = ["curly-joe", "shemp"]
    assert result == expected
    list_one = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    list_two = [4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_one"
    )
    expected = [1.0, 2.0, 3.0]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_two"
    )
    expected = [7.0, 8.0, 9.0]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="intersection"
    )
    expected = [4.0, 5.0, 6.0]
    assert result == expected
    list_one = [1, 2, 3.0, 4.0, 5, "mo", "larry", "curly-joe"]
    list_two = [2, 3, 4.0, 5.0, 6.0, "mo", "larry", "shemp"]
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_one"
    )
    expected = [1, 5, 3.0, "curly-joe"]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="list_two"
    )
    expected = [3, 5.0, 6.0, "shemp"]
    assert result == expected
    result = dd.list_one_list_two_ops(
        list_one=list_one,
        list_two=list_two,
        action="intersection"
    )
    expected = [2, 4.0, "mo", "larry"]
    assert result == expected


def test_series_replace_string():
    pass


def test_delete_empty_columns():
    """
    Test that all elements of a column:
    - are empty for all columns
    - are empty for specific columns
    """
    result1 = dd.delete_empty_columns(df=df)
    expected1 = pd.DataFrame(
        data=dict(
            floats=[1.0, np.nan, 3.0, np.nan, 5.0, 6.0, np.nan],
            text=["A", "B", "C", "D", "E", "F", np.nan],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                pd.NaT
            ],
            integers=[1, 2, np.nan, 4, 5, 6, np.nan],
        )
    ).replace(
        r"^\s+$",
        np.nan,
        regex=True
    ).replace(
        "",
        np.nan,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
        }
    )
    assert result1.equals(other=expected1)
    list_empty_columns = ["mixed", "nan_none"]
    # Delete columns using list_empty_columns
    result2 = dd.delete_empty_columns(
        df=df,
        list_empty_columns=list_empty_columns
    )
    expected2 = pd.DataFrame(
        data=dict(
            floats=[1.0, np.nan, 3.0, np.nan, 5.0, 6.0, np.nan],
            text=["A", "B", "C", "D", "E", "F", np.nan],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                pd.NaT
            ],
            all_nan=[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            all_none=[None, None, None, None, None, None, None],
            all_space=["", " ", "", " ", "", "", ""],
            nan_space=[np.nan, "", " ", np.nan, np.nan, np.nan, np.nan],
            integers=[1, 2, np.nan, 4, 5, 6, np.nan],
        )
    ).replace(
        r"^\s+$",
        np.nan,
        regex=True
    ).replace(
        "",
        np.nan,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
            "all_nan": "float64",
            "all_nat": "datetime64[ns]",
            "all_none": "float64",
            "all_space": "float64",
            "nan_space": "float64"
        }
    )
    assert result2.equals(other=expected2)
    # No not delete columns using list_empty_columns because
    # not all columns in list are empty
    list_empty_columns = ["mixed", "nan_none", "integers"]
    result3 = dd.delete_empty_columns(
        df=df,
        list_empty_columns=list_empty_columns
    )
    expected3 = pd.DataFrame(
        data=dict(
            floats=[1.0, np.nan, 3.0, np.nan, 5.0, 6.0, np.nan],
            text=["A", "B", "C", "D", "E", "F", np.nan],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                pd.NaT
            ],
            all_nan=[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            all_none=[None, None, None, None, None, None, None],
            all_space=["", " ", "", " ", "", "", ""],
            nan_space=[np.nan, "", " ", np.nan, np.nan, np.nan, np.nan],
            nan_none=[np.nan, None, np.nan, np.nan, None, np.nan, None],
            mixed=[None, np.nan, pd.NaT, pd.NaT, None, np.nan, pd.NaT],
            integers=[1, 2, np.nan, 4, 5, 6, np.nan],
        )
    ).replace(
        r"^\s+$",
        np.nan,
        regex=True
    ).replace(
        "",
        np.nan,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
            "all_nan": "float64",
            "all_nat": "datetime64[ns]",
            "all_none": "float64",
            "all_space": "float64",
            "nan_space": "float64",
            "nan_none": "float64",
            "mixed": "datetime64[ns]"
        }
    )
    assert result3.equals(other=expected3)


def test_directory_file_print():
    pass


def test_replace_text_numbers():
    pass


def test_find_integer_columns():
    pass


def test_find_object_columns():
    pass


def test_rename_some_columns():
    pass


def test_series_memory_usage():
    pass


def test_ask_directory_path():
    pass


def test_rename_all_columns():
    pass


def test_find_float_columns():
    pass


def test_remove_punctuation():
    pass


def test_print_list_by_item():
    pass


def test_delete_empty_rows():
    """
    Test delete empty rows:
    - all elements for a row for all columns
    - all elements for a row for specific columns
    """
    # Delete columns where all elements of a column are empty
    result = dd.delete_empty_rows(df=df)
    expected = pd.DataFrame(
        data=dict(
            floats=[1.0, np.nan, 3.0, np.nan, 5.0, 6.0],
            text=["A", "B", "C", "D", "E", "F"],
            dates=[
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08",
                "1956-06-08", "1956-06-08"
            ],
            all_nan=[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            all_nat=[pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT],
            all_none=[None, None, None, None, None, None],
            all_space=["", " ", "", " ", "", ""],
            nan_space=[np.nan, "", " ", np.nan, np.nan, np.nan],
            nan_none=[np.nan, None, np.nan, np.nan, None, np.nan],
            mixed=[None, np.nan, pd.NaT, pd.NaT, None, np.nan],
            integers=[1, 2, np.nan, 4, 5, 6],
        )
    ).replace(
        r"^\s+$",
        np.nan,
        regex=True
    ).replace(
        "",
        np.nan,
        regex=True
    ).astype(
        dtype={
            "integers": "Int64",
            "floats": "float64",
            "text": "object",
            "dates": "datetime64[ns]",
            "all_nan": "float64",
            "all_nat": "datetime64[ns]",
            "all_none": "float64",
            "all_space": "float64",
            "nan_space": "float64",
            "nan_none": "float64",
            "mixed": "datetime64[ns]"
        }
    )
    assert result.equals(other=expected)


def test_delete_list_files():
    pattern_startswith = ["job_aids"]
    path = "dir_directories"
    result1 = dd.list_directories(path=path)
    expected1 = [
        "cheatsheet_directory", "another_directory", "job_aids_directory"
    ]
    assert set(result1) == set(expected1)
    result2 = dd.list_directories(
        path=path,
        pattern_startswith=pattern_startswith
    )
    expected2 = ["job_aids_directory"]
    assert set(result2) == set(expected2)
    pattern_startswith = ["job_aids", "cheatsheet"]
    result3 = dd.list_directories(
        path=path,
        pattern_startswith=pattern_startswith
    )
    expected3 = ["cheatsheet_directory", "job_aids_directory"]
    assert set(result3) == set(expected3)


def test_find_bool_columns():
    pass


def test_create_dataframe():
    pass


def test_create_directory():
    pass


def test_delete_directory():
    pass


def test_list_change_case():
    pass


def test_list_directories():
    pattern_startswith = ["job_aids"]
    path = "dir_directories"
    result1 = dd.list_directories(path=path)
    expected1 = [
        'cheatsheet_directory', 'another_directory', 'job_aids_directory'
    ]
    assert set(result1) == set(expected1)
    result2 = dd.list_directories(
        path=path,
        pattern_startswith=pattern_startswith
    )
    expected2 = ['job_aids_directory']
    assert set(result2) == set(expected2)
    pattern_startswith = ["job_aids", "cheatsheet"]
    result3 = dd.list_directories(
        path=path,
        pattern_startswith=pattern_startswith
    )
    expected3 = ['cheatsheet_directory', 'job_aids_directory']
    assert set(result3) == set(expected3)


def test_optimize_columns():
    pass


def test_rename_directory():
    pass


def test_process_columns():
    pass


def test_copy_directory():
    pass


def test_dataframe_info():
    pass


def test_delete_columns():
    pass


def test_quit_sap_excel():
    pass


def test_mask_outliers():
    pass


def test_process_rows():
    pass


def test_delete_rows():
    pass


def test_list_files():
    pattern_extension = [".html", ".HTML", ".mkd", ".MKD"]
    pattern_startswith = ["file_", "job_aid_"]
    directory = "dir_files"
    result1 = sorted(dd.list_files(directory=directory))
    expected1 = sorted([
        PosixPath("dir_files/job_aid_file_one.html"),
        PosixPath("dir_files/job_aid_file_two.HTML"),
        PosixPath("dir_files/job_aid_file_one.mkd"),
        PosixPath("dir_files/job_aid_file_two.MKD"),
        PosixPath("dir_files/file_one.html"),
        PosixPath("dir_files/file_two.HTML"),
        PosixPath("dir_files/file_one.mkd"),
        PosixPath("dir_files/file_two.MKD")
    ])
    assert result1 == expected1
    result2 = sorted(dd.list_files(
        directory=directory,
        pattern_startswith=pattern_startswith
    ))
    expected2 = sorted([
        PosixPath("dir_files/job_aid_file_one.html"),
        PosixPath("dir_files/job_aid_file_two.HTML"),
        PosixPath("dir_files/job_aid_file_one.mkd"),
        PosixPath("dir_files/job_aid_file_two.MKD"),
        PosixPath("dir_files/file_one.html"),
        PosixPath("dir_files/file_two.HTML"),
        PosixPath("dir_files/file_one.mkd"),
        PosixPath("dir_files/file_two.MKD")
    ])
    assert result2 == expected2
    result3 = sorted(dd.list_files(
        directory=directory,
        pattern_extension=pattern_extension,
    ))
    expected3 = sorted([
        PosixPath("dir_files/job_aid_file_one.html"),
        PosixPath("dir_files/job_aid_file_two.HTML"),
        PosixPath("dir_files/job_aid_file_one.mkd"),
        PosixPath("dir_files/job_aid_file_two.MKD"),
        PosixPath("dir_files/file_one.html"),
        PosixPath("dir_files/file_two.HTML"),
        PosixPath("dir_files/file_one.mkd"),
        PosixPath("dir_files/file_two.MKD")
    ])
    assert result3 == expected3
    result4 = sorted(dd.list_files(
        directory=directory,
        pattern_startswith=pattern_startswith,
        pattern_extension=pattern_extension
    ))
    expected4 = sorted([
        PosixPath("dir_files/job_aid_file_one.html"),
        PosixPath("dir_files/job_aid_file_two.HTML"),
        PosixPath("dir_files/job_aid_file_one.mkd"),
        PosixPath("dir_files/job_aid_file_two.MKD"),
        PosixPath("dir_files/file_one.html"),
        PosixPath("dir_files/file_two.HTML"),
        PosixPath("dir_files/file_one.mkd"),
        PosixPath("dir_files/file_two.MKD")
    ])
    assert result4 == expected4


def test_byte_size():
    pass


def test_get_mtime():
    pass


def test_file_size():
    pass


def test_read_file():
    pass


def test_save_file():
    pass


def test_sort_rows():
    pass


def test_datetime():
    """Tests if specific columns are of datetime64[ns] type."""
    assert pd.api.types.is_datetime64_any_dtype(df["dates"])
    assert pd.api.types.is_datetime64_any_dtype(df["all_nat"])
    assert pd.api.types.is_datetime64_any_dtype(df["mixed"])


def test_integer_types():
    """Tests if integer-related columns are of the expected types."""
    assert pd.api.types.is_integer_dtype(df["integers"])
#     assert pd.api.types.is_integer_dtype(df["integers_int64"])
#     assert pd.api.types.is_integer_dtype(df["integers_uint8"])
#     assert pd.api.types.is_float_dtype(df["integers_float64"])
#     assert pd.api.types.is_float_dtype(df["floats"])


def test_float_types():
    """Tests if float columns are of the expected types."""
    assert pd.api.types.is_float_dtype(df["floats"])
    # assert pd.api.types.is_float_dtype(df["floats_float64"])
    # assert pd.api.types.is_float_dtype(df["floats_float32"])


def test_text_types():
    """Tests if text columns are of the expected types."""
    assert pd.api.types.is_object_dtype(df["text"])
    # assert pd.api.types.is_object_dtype(df["text_object"])
    # assert pd.api.types.is_string_dtype(df["text_string"])
