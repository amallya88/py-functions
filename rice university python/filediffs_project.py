"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1  # const


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    count = 0

    for l1_ch, l2_ch in zip(line1, line2):
        if l1_ch != l2_ch:
            return count
        count += 1

    if len(line1) == len(line2) == count:
        return IDENTICAL
    else:
        return count


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    # return "" if either arg has \n or \r
    if sum([1 for chr in line1 if chr in ("\r", "\n")]
           + [1 for chr in line2 if chr in ("\r", "\n")]) > 0:
        return ""
    # index of diff cannot be greater than length of either string
    if idx > len(line1) or idx > len(line2) or idx < 0:
        return ""
    else:
        # Output a string that is formatted as follows:
        # abcd
        # == ^
        # abef
        ret_diff_string = "{}\n{}{}\n{}\n".format(line1, "=" * idx, "^", line2)
    return ret_diff_string


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    lin_count = 0
    lin_compare = 0
    for lin1, lin2 in zip(lines1, lines2):
        lin_compare = singleline_diff(lin1, lin2)
        if lin_compare != IDENTICAL:
            return lin_count, lin_compare
        lin_count += 1

    if len(lines1) == len(lines2) == lin_count:
        return IDENTICAL, IDENTICAL
    else:
        # if one list had fewer items than the other, the first diff
        # is at index 0 of the first line that that does not exist in the other list
        if len(lines1) < len(lines2):
            return len(lines1), 0
        else:
            return len(lines2), 0


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lst_contents = []
    with open(filename, 'r') as file:
        for line in file:
            lst_contents.append(line.strip("\r\n"))
        return lst_contents


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file1_lines = get_file_lines(filename1)
    file2_lines = get_file_lines(filename2)
    file_diff = multiline_diff(file1_lines, file2_lines)
    if file_diff == (IDENTICAL, IDENTICAL):
        return "No differences\n"
    else:
        file_diff_idx = file_diff[0]  # line number starting from 0 where diffs exist
        try:
            line1 = file1_lines[file_diff[0]]
        except IndexError:
            line1 = ""  # if line doesn't exist, return empty line
        try:
            line2 = file2_lines[file_diff[0]]
        except IndexError:
            line2 = ""  # if line doesn't exist, return empty line

        line_diff_idx = file_diff[1]  # index where two lines have diff
        diff_str = singleline_diff_format(line1, line2, line_diff_idx)
        ret_diff_result = "Line {}:\n{}".format(file_diff_idx, diff_str)
        return ret_diff_result

